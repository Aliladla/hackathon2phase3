"""Unit tests for OpenAI agent."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from chatbot.agent import TodoAgent
from chatbot.conversation import ConversationContext


@pytest.fixture
def todo_agent(mock_jwt_token, conversation_context, mock_openai_client):
    """Fixture for TodoAgent with mocked dependencies."""
    with patch("chatbot.agent.agent.AsyncOpenAI", return_value=mock_openai_client):
        agent = TodoAgent(jwt_token=mock_jwt_token, context=conversation_context)
        return agent


@pytest.mark.asyncio
async def test_agent_initialization(mock_jwt_token, conversation_context):
    """Test agent initialization."""
    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        agent = TodoAgent(jwt_token=mock_jwt_token, context=conversation_context)

        assert agent.context == conversation_context
        assert agent.model == "gpt-4-turbo-preview"
        mock_openai.assert_called_once()


@pytest.mark.asyncio
async def test_process_message_simple_response(todo_agent, mock_openai_client):
    """Test processing a message with simple response (no tool calls)."""
    # Mock OpenAI response without tool calls
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello! How can I help you?"
    mock_response.choices[0].message.tool_calls = None

    mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)

    response = await todo_agent.process_message("Hello")

    assert response == "Hello! How can I help you?"
    assert len(todo_agent.context.messages) == 2  # user + assistant
    assert todo_agent.context.messages[0].role == "user"
    assert todo_agent.context.messages[0].content == "Hello"
    assert todo_agent.context.messages[1].role == "assistant"
    assert todo_agent.context.messages[1].content == "Hello! How can I help you?"


@pytest.mark.asyncio
async def test_process_message_with_tool_call(todo_agent, mock_openai_client, sample_task):
    """Test processing a message that triggers tool calls."""
    # Mock first response with tool call
    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_123"
    mock_tool_call.type = "function"
    mock_tool_call.function.name = "create_task"
    mock_tool_call.function.arguments = '{"title": "Buy milk", "description": ""}'

    mock_response_1 = MagicMock()
    mock_response_1.choices = [MagicMock()]
    mock_response_1.choices[0].message.content = ""
    mock_response_1.choices[0].message.tool_calls = [mock_tool_call]

    # Mock second response after tool execution
    mock_response_2 = MagicMock()
    mock_response_2.choices = [MagicMock()]
    mock_response_2.choices[0].message.content = "I've added 'Buy milk' to your list. It's task #1."
    mock_response_2.choices[0].message.tool_calls = None

    mock_openai_client.chat.completions.create = AsyncMock(
        side_effect=[mock_response_1, mock_response_2]
    )

    # Mock API client for tool execution
    todo_agent.api_client.post = AsyncMock(return_value=sample_task)

    response = await todo_agent.process_message("Add a task to buy milk")

    assert "added" in response.lower() or "buy milk" in response.lower()
    assert len(todo_agent.context.messages) == 3  # user + assistant (with tools) + assistant (final)
    assert todo_agent.context.last_task_id == 1
    assert todo_agent.context.last_operation == "create"


@pytest.mark.asyncio
async def test_process_message_list_tasks(todo_agent, mock_openai_client, sample_task_list):
    """Test processing a message to list tasks."""
    # Mock tool call for list_tasks
    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_456"
    mock_tool_call.type = "function"
    mock_tool_call.function.name = "list_tasks"
    mock_tool_call.function.arguments = '{"completed": null, "limit": 100, "offset": 0}'

    mock_response_1 = MagicMock()
    mock_response_1.choices = [MagicMock()]
    mock_response_1.choices[0].message.content = ""
    mock_response_1.choices[0].message.tool_calls = [mock_tool_call]

    mock_response_2 = MagicMock()
    mock_response_2.choices = [MagicMock()]
    mock_response_2.choices[0].message.content = "You have 2 tasks: 1. Buy groceries, 2. Call dentist (completed)"
    mock_response_2.choices[0].message.tool_calls = None

    mock_openai_client.chat.completions.create = AsyncMock(
        side_effect=[mock_response_1, mock_response_2]
    )

    # Mock API client
    todo_agent.api_client.get = AsyncMock(return_value=sample_task_list)

    response = await todo_agent.process_message("Show me my tasks")

    assert "tasks" in response.lower() or "buy groceries" in response.lower()


@pytest.mark.asyncio
async def test_process_message_error_handling(todo_agent, mock_openai_client):
    """Test error handling in message processing."""
    # Mock OpenAI to raise an exception
    mock_openai_client.chat.completions.create = AsyncMock(
        side_effect=Exception("API error")
    )

    response = await todo_agent.process_message("Test message")

    assert "error" in response.lower()
    assert len(todo_agent.context.messages) == 2  # user + error response


@pytest.mark.asyncio
async def test_execute_tool_calls_single_tool(todo_agent, sample_task):
    """Test executing a single tool call."""
    mock_tool_call = MagicMock()
    mock_tool_call.function.name = "create_task"
    mock_tool_call.function.arguments = '{"title": "Test task", "description": "Test"}'

    # Mock executor
    todo_agent.executor.execute = AsyncMock(return_value=MagicMock(
        tool_name="create_task",
        success=True,
        result=sample_task,
        error=None,
        execution_time=0.1
    ))

    results = await todo_agent._execute_tool_calls([mock_tool_call])

    assert len(results) == 1
    assert results[0]["tool_name"] == "create_task"
    assert results[0]["success"] is True
    assert results[0]["result"] == sample_task


@pytest.mark.asyncio
async def test_execute_tool_calls_multiple_tools(todo_agent, sample_task, sample_task_list):
    """Test executing multiple tool calls."""
    mock_tool_call_1 = MagicMock()
    mock_tool_call_1.function.name = "create_task"
    mock_tool_call_1.function.arguments = '{"title": "Task 1"}'

    mock_tool_call_2 = MagicMock()
    mock_tool_call_2.function.name = "list_tasks"
    mock_tool_call_2.function.arguments = '{}'

    # Mock executor responses
    todo_agent.executor.execute = AsyncMock(side_effect=[
        MagicMock(
            tool_name="create_task",
            success=True,
            result=sample_task,
            error=None,
            execution_time=0.1
        ),
        MagicMock(
            tool_name="list_tasks",
            success=True,
            result=sample_task_list,
            error=None,
            execution_time=0.05
        )
    ])

    results = await todo_agent._execute_tool_calls([mock_tool_call_1, mock_tool_call_2])

    assert len(results) == 2
    assert results[0]["tool_name"] == "create_task"
    assert results[1]["tool_name"] == "list_tasks"


@pytest.mark.asyncio
async def test_update_context_from_create_task(todo_agent):
    """Test context update after creating a task."""
    tool_results = [
        {
            "tool_name": "create_task",
            "success": True,
            "result": {"id": 5, "title": "New task"},
            "error": None,
            "execution_time": 0.1
        }
    ]

    todo_agent._update_context_from_results(tool_results)

    assert todo_agent.context.last_task_id == 5
    assert todo_agent.context.last_operation == "create"


@pytest.mark.asyncio
async def test_update_context_from_get_task(todo_agent):
    """Test context update after getting a task."""
    tool_results = [
        {
            "tool_name": "get_task",
            "success": True,
            "result": {"id": 10, "title": "Existing task"},
            "error": None,
            "execution_time": 0.05
        }
    ]

    todo_agent._update_context_from_results(tool_results)

    assert todo_agent.context.last_task_id == 10
    assert todo_agent.context.last_operation == "view"


@pytest.mark.asyncio
async def test_update_context_from_update_task(todo_agent):
    """Test context update after updating a task."""
    tool_results = [
        {
            "tool_name": "update_task",
            "success": True,
            "result": {"id": 7, "title": "Updated task"},
            "error": None,
            "execution_time": 0.08
        }
    ]

    todo_agent._update_context_from_results(tool_results)

    assert todo_agent.context.last_task_id == 7
    assert todo_agent.context.last_operation == "update"


@pytest.mark.asyncio
async def test_update_context_from_toggle_complete(todo_agent):
    """Test context update after toggling task completion."""
    tool_results = [
        {
            "tool_name": "toggle_complete",
            "success": True,
            "result": {"id": 3, "completed": True},
            "error": None,
            "execution_time": 0.06
        }
    ]

    todo_agent._update_context_from_results(tool_results)

    assert todo_agent.context.last_task_id == 3
    assert todo_agent.context.last_operation == "complete"


@pytest.mark.asyncio
async def test_update_context_from_delete_task(todo_agent):
    """Test context update after deleting a task."""
    # Set initial context
    todo_agent.context.update_task_context(task_id=5, operation="view")

    tool_results = [
        {
            "tool_name": "delete_task",
            "success": True,
            "result": {"success": True, "message": "Task deleted"},
            "error": None,
            "execution_time": 0.07
        }
    ]

    todo_agent._update_context_from_results(tool_results)

    # After delete, operation should be "delete" but task_id might be cleared
    assert todo_agent.context.last_operation == "delete"


@pytest.mark.asyncio
async def test_update_context_skips_failed_tools(todo_agent):
    """Test that context update skips failed tool executions."""
    tool_results = [
        {
            "tool_name": "create_task",
            "success": False,
            "result": None,
            "error": "Authentication failed",
            "execution_time": 0.05
        }
    ]

    initial_task_id = todo_agent.context.last_task_id
    initial_operation = todo_agent.context.last_operation

    todo_agent._update_context_from_results(tool_results)

    # Context should not change for failed operations
    assert todo_agent.context.last_task_id == initial_task_id
    assert todo_agent.context.last_operation == initial_operation


@pytest.mark.asyncio
async def test_context_includes_system_prompt(todo_agent, mock_openai_client):
    """Test that system prompt includes context summary."""
    # Set some context
    todo_agent.context.update_task_context(task_id=5, operation="create")

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Response"
    mock_response.choices[0].message.tool_calls = None

    mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)

    await todo_agent.process_message("Test")

    # Verify system prompt was included in the call
    call_args = mock_openai_client.chat.completions.create.call_args
    messages = call_args.kwargs["messages"]

    assert messages[0]["role"] == "system"
    assert "Last mentioned task ID: 5" in messages[0]["content"]
    assert "Last operation: create" in messages[0]["content"]
