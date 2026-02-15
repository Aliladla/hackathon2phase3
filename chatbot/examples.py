"""Usage examples for Phase 3 chatbot.

This file demonstrates various ways to use the chatbot programmatically.
"""
import asyncio
from chatbot.agent import TodoAgent
from chatbot.conversation import ConversationContext, SessionStore
from chatbot.api.client import APIClient


# Example 1: Basic conversation
async def example_basic_conversation():
    """Example: Basic conversation with the chatbot."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Conversation")
    print("=" * 70 + "\n")

    # Replace with your actual JWT token
    jwt_token = "your_jwt_token_here"

    # Create conversation context and agent
    context = ConversationContext()
    agent = TodoAgent(jwt_token=jwt_token, context=context)

    # Send messages
    response1 = await agent.process_message("Add a task to buy groceries")
    print(f"User: Add a task to buy groceries")
    print(f"Bot: {response1}\n")

    response2 = await agent.process_message("Show me my tasks")
    print(f"User: Show me my tasks")
    print(f"Bot: {response2}\n")


# Example 2: Session management
async def example_session_management():
    """Example: Managing multiple conversation sessions."""
    print("\n" + "=" * 70)
    print("Example 2: Session Management")
    print("=" * 70 + "\n")

    jwt_token = "your_jwt_token_here"

    # Create session store
    store = SessionStore()

    # Create multiple sessions
    session1 = store.create_session()
    session2 = store.create_session()

    print(f"Created session 1: {session1.session_id}")
    print(f"Created session 2: {session2.session_id}")

    # Use different agents for different sessions
    agent1 = TodoAgent(jwt_token=jwt_token, context=session1)
    agent2 = TodoAgent(jwt_token=jwt_token, context=session2)

    # Each session maintains independent context
    await agent1.process_message("Add a task to buy milk")
    await agent2.process_message("Add a task to call dentist")

    print(f"\nSession 1 last task: {session1.last_task_id}")
    print(f"Session 2 last task: {session2.last_task_id}")

    # Cleanup
    store.delete_session(session1.session_id)
    store.delete_session(session2.session_id)


# Example 3: Direct API client usage
async def example_direct_api_usage():
    """Example: Using the API client directly (without chatbot)."""
    print("\n" + "=" * 70)
    print("Example 3: Direct API Client Usage")
    print("=" * 70 + "\n")

    jwt_token = "your_jwt_token_here"

    # Create API client
    client = APIClient(jwt_token=jwt_token)

    try:
        # Create a task
        task = await client.post("/api/tasks", {
            "title": "Direct API task",
            "description": "Created without chatbot"
        })
        print(f"Created task: {task}")

        # List tasks
        tasks = await client.get("/api/tasks", params={"limit": 5})
        print(f"\nTasks: {tasks}")

        # Update task
        updated = await client.patch(f"/api/tasks/{task['id']}", {
            "completed": True
        })
        print(f"\nUpdated task: {updated}")

        # Delete task
        await client.delete(f"/api/tasks/{task['id']}")
        print(f"\nDeleted task {task['id']}")

    except Exception as e:
        print(f"Error: {str(e)}")


# Example 4: Context-aware conversation
async def example_contextual_conversation():
    """Example: Using context for natural references."""
    print("\n" + "=" * 70)
    print("Example 4: Context-Aware Conversation")
    print("=" * 70 + "\n")

    jwt_token = "your_jwt_token_here"

    context = ConversationContext()
    agent = TodoAgent(jwt_token=jwt_token, context=context)

    # Create a task
    response1 = await agent.process_message("Add a task to buy milk")
    print(f"User: Add a task to buy milk")
    print(f"Bot: {response1}")
    print(f"Context: Last task ID = {context.last_task_id}\n")

    # Use contextual reference
    response2 = await agent.process_message("Mark that task as complete")
    print(f"User: Mark that task as complete")
    print(f"Bot: {response2}")
    print(f"Context: Last operation = {context.last_operation}\n")


# Example 5: Error handling
async def example_error_handling():
    """Example: Handling errors gracefully."""
    print("\n" + "=" * 70)
    print("Example 5: Error Handling")
    print("=" * 70 + "\n")

    jwt_token = "your_jwt_token_here"

    context = ConversationContext()
    agent = TodoAgent(jwt_token=jwt_token, context=context)

    # Try to get non-existent task
    response = await agent.process_message("Show me task 999999")
    print(f"User: Show me task 999999")
    print(f"Bot: {response}\n")

    # The agent handles the error gracefully and provides a helpful message


# Example 6: MCP tools usage
async def example_mcp_tools():
    """Example: Using MCP tools directly."""
    print("\n" + "=" * 70)
    print("Example 6: MCP Tools Direct Usage")
    print("=" * 70 + "\n")

    jwt_token = "your_jwt_token_here"

    from chatbot.api.client import APIClient
    from chatbot.mcp.executor import MCPToolExecutor

    # Create executor
    api_client = APIClient(jwt_token=jwt_token)
    executor = MCPToolExecutor(api_client=api_client)

    # Execute create_task tool
    result = await executor.execute("create_task", {
        "title": "MCP tool test",
        "description": "Created via MCP tool"
    })

    print(f"Tool: create_task")
    print(f"Success: {result.success}")
    print(f"Result: {result.result}")
    print(f"Execution time: {result.execution_time:.3f}s\n")

    # Execute list_tasks tool
    result = await executor.execute("list_tasks", {
        "completed": False,
        "limit": 5,
        "offset": 0
    })

    print(f"Tool: list_tasks")
    print(f"Success: {result.success}")
    print(f"Tasks found: {len(result.result.get('tasks', []))}")


# Example 7: Custom system prompt
async def example_custom_prompt():
    """Example: Using a custom system prompt."""
    print("\n" + "=" * 70)
    print("Example 7: Custom System Prompt")
    print("=" * 70 + "\n")

    jwt_token = "your_jwt_token_here"

    context = ConversationContext()
    agent = TodoAgent(jwt_token=jwt_token, context=context)

    # You can modify the system prompt in agent.prompts.py
    # or override it programmatically before processing messages

    response = await agent.process_message("Hello!")
    print(f"User: Hello!")
    print(f"Bot: {response}\n")


# Example 8: Batch operations
async def example_batch_operations():
    """Example: Performing multiple operations in sequence."""
    print("\n" + "=" * 70)
    print("Example 8: Batch Operations")
    print("=" * 70 + "\n")

    jwt_token = "your_jwt_token_here"

    context = ConversationContext()
    agent = TodoAgent(jwt_token=jwt_token, context=context)

    # Create multiple tasks
    tasks_to_create = [
        "Buy groceries",
        "Call dentist",
        "Pay electricity bill",
        "Finish report"
    ]

    print("Creating tasks...")
    for task_title in tasks_to_create:
        response = await agent.process_message(f"Add a task to {task_title}")
        print(f"  ✓ {task_title}")

    # List all tasks
    response = await agent.process_message("Show me all my tasks")
    print(f"\n{response}\n")


# Example 9: REST API client usage
async def example_rest_api_client():
    """Example: Using the chatbot via REST API."""
    print("\n" + "=" * 70)
    print("Example 9: REST API Client Usage")
    print("=" * 70 + "\n")

    import httpx

    jwt_token = "your_jwt_token_here"
    base_url = "http://localhost:8001"

    async with httpx.AsyncClient() as client:
        # Create session
        response = await client.post(f"{base_url}/sessions")
        session_data = response.json()
        session_id = session_data["session_id"]
        print(f"Created session: {session_id}")

        # Send message
        response = await client.post(
            f"{base_url}/chat",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json={
                "message": "Add a task to buy milk",
                "session_id": session_id
            }
        )
        chat_response = response.json()
        print(f"\nBot response: {chat_response['response']}")

        # Get session context
        response = await client.get(f"{base_url}/sessions/{session_id}/context")
        context_data = response.json()
        print(f"\nSession context: {context_data}")

        # Delete session
        await client.delete(f"{base_url}/sessions/{session_id}")
        print(f"\nDeleted session: {session_id}")


# Example 10: Testing with mocked OpenAI
async def example_testing_with_mocks():
    """Example: Testing chatbot with mocked OpenAI responses."""
    print("\n" + "=" * 70)
    print("Example 10: Testing with Mocks")
    print("=" * 70 + "\n")

    from unittest.mock import AsyncMock, MagicMock, patch

    jwt_token = "test_token"

    with patch("chatbot.agent.agent.AsyncOpenAI") as mock_openai:
        # Mock OpenAI response
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Mocked response"
        mock_response.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        # Create agent with mocked OpenAI
        context = ConversationContext()
        agent = TodoAgent(jwt_token=jwt_token, context=context)

        # Process message (will use mocked response)
        response = await agent.process_message("Test message")
        print(f"Mocked response: {response}")


async def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("📚 Phase 3 Chatbot - Usage Examples")
    print("=" * 70)

    print("\n⚠️  Note: These examples require:")
    print("  1. Phase 2 backend running at http://localhost:8000")
    print("  2. Valid JWT token from Phase 2")
    print("  3. OpenAI API key configured in .env")
    print("\nReplace 'your_jwt_token_here' with your actual JWT token.")
    print("\nUncomment the example you want to run in the main() function.")

    # Uncomment the example you want to run:
    # await example_basic_conversation()
    # await example_session_management()
    # await example_direct_api_usage()
    # await example_contextual_conversation()
    # await example_error_handling()
    # await example_mcp_tools()
    # await example_custom_prompt()
    # await example_batch_operations()
    # await example_rest_api_client()
    # await example_testing_with_mocks()


if __name__ == "__main__":
    asyncio.run(main())
