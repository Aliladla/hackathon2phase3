"""Integration tests for chatbot with Phase 2 backend."""
import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from chatbot.agent import TodoAgent
from chatbot.conversation import ConversationContext
from chatbot.api.client import APIClient


@pytest.fixture
def integration_jwt_token():
    """Fixture for integration test JWT token."""
    return "integration_test_token_12345"


@pytest.fixture
def integration_context():
    """Fixture for integration test conversation context."""
    return ConversationContext()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_task_flow(integration_jwt_token, integration_context):
    """Test complete flow for creating a task."""
    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        # Mock OpenAI responses
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client

        # First call: tool call to create task
        from unittest.mock import MagicMock
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_create_123"
        mock_tool_call.type = "function"
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = '{"title": "Buy groceries", "description": "Milk and eggs"}'

        mock_response_1 = MagicMock()
        mock_response_1.choices = [MagicMock()]
        mock_response_1.choices[0].message.content = ""
        mock_response_1.choices[0].message.tool_calls = [mock_tool_call]

        # Second call: final response
        mock_response_2 = MagicMock()
        mock_response_2.choices = [MagicMock()]
        mock_response_2.choices[0].message.content = "I've added 'Buy groceries' to your list. It's task #1."
        mock_response_2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_1, mock_response_2]
        )

        # Create agent
        agent = TodoAgent(jwt_token=integration_jwt_token, context=integration_context)

        # Mock API client response
        agent.api_client.post = AsyncMock(return_value={
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk and eggs",
            "completed": False,
            "user_id": str(uuid4()),
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        })

        # Process message
        response = await agent.process_message("Add a task to buy groceries with milk and eggs")

        # Verify response
        assert "buy groceries" in response.lower() or "added" in response.lower()

        # Verify context updated
        assert integration_context.last_task_id == 1
        assert integration_context.last_operation == "create"

        # Verify messages added
        assert len(integration_context.messages) == 3


@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_and_complete_task_flow(integration_jwt_token, integration_context):
    """Test flow for listing tasks and marking one complete."""
    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client

        from unittest.mock import MagicMock

        # Create agent
        agent = TodoAgent(jwt_token=integration_jwt_token, context=integration_context)

        # Step 1: List tasks
        mock_tool_call_list = MagicMock()
        mock_tool_call_list.id = "call_list_123"
        mock_tool_call_list.type = "function"
        mock_tool_call_list.function.name = "list_tasks"
        mock_tool_call_list.function.arguments = '{"completed": null, "limit": 100, "offset": 0}'

        mock_response_list_1 = MagicMock()
        mock_response_list_1.choices = [MagicMock()]
        mock_response_list_1.choices[0].message.content = ""
        mock_response_list_1.choices[0].message.tool_calls = [mock_tool_call_list]

        mock_response_list_2 = MagicMock()
        mock_response_list_2.choices = [MagicMock()]
        mock_response_list_2.choices[0].message.content = "You have 2 tasks: 1. Buy groceries, 2. Call dentist"
        mock_response_list_2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_list_1, mock_response_list_2]
        )

        agent.api_client.get = AsyncMock(return_value={
            "tasks": [
                {"id": 1, "title": "Buy groceries", "completed": False},
                {"id": 2, "title": "Call dentist", "completed": False}
            ],
            "total": 2,
            "limit": 100,
            "offset": 0
        })

        response = await agent.process_message("Show me my tasks")
        assert "tasks" in response.lower() or "buy groceries" in response.lower()

        # Step 2: Mark task complete
        mock_tool_call_complete = MagicMock()
        mock_tool_call_complete.id = "call_complete_456"
        mock_tool_call_complete.type = "function"
        mock_tool_call_complete.function.name = "toggle_complete"
        mock_tool_call_complete.function.arguments = '{"task_id": 1}'

        mock_response_complete_1 = MagicMock()
        mock_response_complete_1.choices = [MagicMock()]
        mock_response_complete_1.choices[0].message.content = ""
        mock_response_complete_1.choices[0].message.tool_calls = [mock_tool_call_complete]

        mock_response_complete_2 = MagicMock()
        mock_response_complete_2.choices = [MagicMock()]
        mock_response_complete_2.choices[0].message.content = "Done! I've marked task #1 as complete."
        mock_response_complete_2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_complete_1, mock_response_complete_2]
        )

        agent.api_client.patch = AsyncMock(return_value={
            "id": 1,
            "title": "Buy groceries",
            "completed": True
        })

        response = await agent.process_message("Mark task 1 as complete")
        assert "complete" in response.lower() or "done" in response.lower()

        # Verify context
        assert integration_context.last_task_id == 1
        assert integration_context.last_operation == "complete"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_task_flow(integration_jwt_token, integration_context):
    """Test flow for updating a task."""
    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client

        from unittest.mock import MagicMock

        agent = TodoAgent(jwt_token=integration_jwt_token, context=integration_context)

        # Mock update task tool call
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_update_789"
        mock_tool_call.type = "function"
        mock_tool_call.function.name = "update_task"
        mock_tool_call.function.arguments = '{"task_id": 3, "title": "Buy groceries and snacks"}'

        mock_response_1 = MagicMock()
        mock_response_1.choices = [MagicMock()]
        mock_response_1.choices[0].message.content = ""
        mock_response_1.choices[0].message.tool_calls = [mock_tool_call]

        mock_response_2 = MagicMock()
        mock_response_2.choices = [MagicMock()]
        mock_response_2.choices[0].message.content = "I've updated task #3 to 'Buy groceries and snacks'."
        mock_response_2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_1, mock_response_2]
        )

        agent.api_client.patch = AsyncMock(return_value={
            "id": 3,
            "title": "Buy groceries and snacks",
            "description": "",
            "completed": False
        })

        response = await agent.process_message("Change task 3 title to Buy groceries and snacks")

        assert "updated" in response.lower() or "changed" in response.lower()
        assert integration_context.last_task_id == 3
        assert integration_context.last_operation == "update"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_delete_task_flow(integration_jwt_token, integration_context):
    """Test flow for deleting a task."""
    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client

        from unittest.mock import MagicMock

        agent = TodoAgent(jwt_token=integration_jwt_token, context=integration_context)

        # Mock delete task tool call
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_delete_999"
        mock_tool_call.type = "function"
        mock_tool_call.function.name = "delete_task"
        mock_tool_call.function.arguments = '{"task_id": 7}'

        mock_response_1 = MagicMock()
        mock_response_1.choices = [MagicMock()]
        mock_response_1.choices[0].message.content = ""
        mock_response_1.choices[0].message.tool_calls = [mock_tool_call]

        mock_response_2 = MagicMock()
        mock_response_2.choices = [MagicMock()]
        mock_response_2.choices[0].message.content = "Done! I've deleted task #7 from your list."
        mock_response_2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_1, mock_response_2]
        )

        agent.api_client.delete = AsyncMock(return_value=None)

        response = await agent.process_message("Delete task 7")

        assert "deleted" in response.lower() or "removed" in response.lower()
        assert integration_context.last_operation == "delete"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_contextual_reference_flow(integration_jwt_token, integration_context):
    """Test flow using contextual references like 'that task'."""
    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client

        from unittest.mock import MagicMock

        agent = TodoAgent(jwt_token=integration_jwt_token, context=integration_context)

        # Step 1: Create a task
        integration_context.update_task_context(task_id=5, operation="create")

        # Step 2: Reference "that task" to mark it complete
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_context_123"
        mock_tool_call.type = "function"
        mock_tool_call.function.name = "toggle_complete"
        mock_tool_call.function.arguments = '{"task_id": 5}'

        mock_response_1 = MagicMock()
        mock_response_1.choices = [MagicMock()]
        mock_response_1.choices[0].message.content = ""
        mock_response_1.choices[0].message.tool_calls = [mock_tool_call]

        mock_response_2 = MagicMock()
        mock_response_2.choices = [MagicMock()]
        mock_response_2.choices[0].message.content = "Done! I've marked task #5 as complete."
        mock_response_2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_1, mock_response_2]
        )

        agent.api_client.patch = AsyncMock(return_value={
            "id": 5,
            "title": "Previous task",
            "completed": True
        })

        # The system prompt should include context about task 5
        response = await agent.process_message("Mark that task as complete")

        assert "complete" in response.lower()

        # Verify system prompt included context
        call_args = mock_client.chat.completions.create.call_args_list[0]
        messages = call_args.kwargs["messages"]
        system_message = messages[0]["content"]
        assert "Last mentioned task ID: 5" in system_message


@pytest.mark.asyncio
@pytest.mark.integration
async def test_error_recovery_flow(integration_jwt_token, integration_context):
    """Test error recovery when API calls fail."""
    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client

        from unittest.mock import MagicMock
        from chatbot.api.client import AuthenticationError

        agent = TodoAgent(jwt_token=integration_jwt_token, context=integration_context)

        # Mock tool call that will fail
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_error_123"
        mock_tool_call.type = "function"
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = '{"title": "Test task"}'

        mock_response_1 = MagicMock()
        mock_response_1.choices = [MagicMock()]
        mock_response_1.choices[0].message.content = ""
        mock_response_1.choices[0].message.tool_calls = [mock_tool_call]

        mock_response_2 = MagicMock()
        mock_response_2.choices = [MagicMock()]
        mock_response_2.choices[0].message.content = "Your session has expired. Please sign in again."
        mock_response_2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_1, mock_response_2]
        )

        # Mock API client to raise authentication error
        agent.api_client.post = AsyncMock(side_effect=AuthenticationError("Token expired"))

        response = await agent.process_message("Add a task")

        assert "session" in response.lower() or "expired" in response.lower() or "sign in" in response.lower()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_multi_turn_conversation_flow(integration_jwt_token, integration_context):
    """Test multi-turn conversation maintaining context."""
    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client

        from unittest.mock import MagicMock

        agent = TodoAgent(jwt_token=integration_jwt_token, context=integration_context)

        # Turn 1: Greeting
        mock_response_greeting = MagicMock()
        mock_response_greeting.choices = [MagicMock()]
        mock_response_greeting.choices[0].message.content = "Hello! How can I help you with your tasks today?"
        mock_response_greeting.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(return_value=mock_response_greeting)

        response1 = await agent.process_message("Hello")
        assert "hello" in response1.lower() or "help" in response1.lower()

        # Turn 2: Create task
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_multi_123"
        mock_tool_call.type = "function"
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = '{"title": "Buy milk"}'

        mock_response_create_1 = MagicMock()
        mock_response_create_1.choices = [MagicMock()]
        mock_response_create_1.choices[0].message.content = ""
        mock_response_create_1.choices[0].message.tool_calls = [mock_tool_call]

        mock_response_create_2 = MagicMock()
        mock_response_create_2.choices = [MagicMock()]
        mock_response_create_2.choices[0].message.content = "I've added 'Buy milk' to your list."
        mock_response_create_2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_create_1, mock_response_create_2]
        )

        agent.api_client.post = AsyncMock(return_value={
            "id": 1,
            "title": "Buy milk",
            "completed": False
        })

        response2 = await agent.process_message("Add a task to buy milk")
        assert "added" in response2.lower() or "buy milk" in response2.lower()

        # Verify conversation history maintained
        assert len(integration_context.messages) >= 4  # greeting pair + create task pair
