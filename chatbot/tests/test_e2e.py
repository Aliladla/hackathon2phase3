"""End-to-end tests with actual Phase 2 backend.

These tests require:
1. Phase 2 backend running at http://localhost:8000
2. Valid JWT token from backend
3. OpenAI API key configured

Run with: pytest -m e2e tests/test_e2e.py
"""
import pytest
import os
from chatbot.agent import TodoAgent
from chatbot.conversation import ConversationContext
from chatbot.config import settings


# Skip all e2e tests if backend URL or OpenAI key not configured
pytestmark = pytest.mark.skipif(
    not settings.OPENAI_API_KEY or settings.BACKEND_API_URL == "http://localhost:8000",
    reason="E2E tests require OpenAI API key and running backend"
)


@pytest.fixture
def e2e_jwt_token():
    """
    Fixture for E2E JWT token.

    Set JWT_TOKEN environment variable before running E2E tests.
    """
    token = os.getenv("JWT_TOKEN")
    if not token:
        pytest.skip("JWT_TOKEN environment variable not set")
    return token


@pytest.fixture
def e2e_context():
    """Fixture for E2E conversation context."""
    return ConversationContext()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_create_and_list_tasks(e2e_jwt_token, e2e_context):
    """
    E2E test: Create a task and list all tasks.

    This test makes real API calls to Phase 2 backend and OpenAI.
    """
    agent = TodoAgent(jwt_token=e2e_jwt_token, context=e2e_context)

    # Create a task
    response1 = await agent.process_message("Add a task to test E2E integration")

    assert "added" in response1.lower() or "created" in response1.lower()
    assert e2e_context.last_operation == "create"
    task_id = e2e_context.last_task_id
    assert task_id is not None

    # List tasks
    response2 = await agent.process_message("Show me my tasks")

    assert "task" in response2.lower()
    assert "e2e integration" in response2.lower() or str(task_id) in response2


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_full_task_lifecycle(e2e_jwt_token, e2e_context):
    """
    E2E test: Complete task lifecycle (create, update, complete, delete).

    This test makes real API calls to Phase 2 backend and OpenAI.
    """
    agent = TodoAgent(jwt_token=e2e_jwt_token, context=e2e_context)

    # Step 1: Create task
    response1 = await agent.process_message("Add a task to test full lifecycle")
    assert "added" in response1.lower() or "created" in response1.lower()
    task_id = e2e_context.last_task_id

    # Step 2: Update task
    response2 = await agent.process_message(
        f"Update task {task_id} title to Test full lifecycle - updated"
    )
    assert "updated" in response2.lower() or "changed" in response2.lower()

    # Step 3: Mark complete
    response3 = await agent.process_message(f"Mark task {task_id} as complete")
    assert "complete" in response3.lower() or "done" in response3.lower()

    # Step 4: Delete task
    response4 = await agent.process_message(f"Delete task {task_id}")
    assert "deleted" in response4.lower() or "removed" in response4.lower()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_contextual_references(e2e_jwt_token, e2e_context):
    """
    E2E test: Contextual references like "that task".

    This test makes real API calls to Phase 2 backend and OpenAI.
    """
    agent = TodoAgent(jwt_token=e2e_jwt_token, context=e2e_context)

    # Create a task
    response1 = await agent.process_message("Add a task to test contextual references")
    assert "added" in response1.lower()
    task_id = e2e_context.last_task_id

    # Use contextual reference
    response2 = await agent.process_message("Mark that task as complete")
    assert "complete" in response2.lower()
    assert e2e_context.last_task_id == task_id

    # Cleanup
    await agent.process_message(f"Delete task {task_id}")


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_multi_turn_conversation(e2e_jwt_token, e2e_context):
    """
    E2E test: Multi-turn conversation maintaining context.

    This test makes real API calls to Phase 2 backend and OpenAI.
    """
    agent = TodoAgent(jwt_token=e2e_jwt_token, context=e2e_context)

    # Turn 1: Greeting
    response1 = await agent.process_message("Hello")
    assert len(response1) > 0

    # Turn 2: Create task
    response2 = await agent.process_message("Add a task to buy milk")
    assert "milk" in response2.lower()

    # Turn 3: Create another task
    response3 = await agent.process_message("Also add a task to call dentist")
    assert "dentist" in response3.lower()

    # Turn 4: List tasks
    response4 = await agent.process_message("What are my tasks?")
    assert "milk" in response4.lower() or "dentist" in response4.lower()

    # Verify conversation history
    assert len(e2e_context.messages) >= 8  # 4 turns = 8 messages


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_error_handling_invalid_task_id(e2e_jwt_token, e2e_context):
    """
    E2E test: Error handling for invalid task ID.

    This test makes real API calls to Phase 2 backend and OpenAI.
    """
    agent = TodoAgent(jwt_token=e2e_jwt_token, context=e2e_context)

    # Try to get non-existent task
    response = await agent.process_message("Show me task 999999")

    assert "not found" in response.lower() or "couldn't find" in response.lower()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_natural_language_variations(e2e_jwt_token, e2e_context):
    """
    E2E test: Various natural language phrasings.

    This test makes real API calls to Phase 2 backend and OpenAI.
    """
    agent = TodoAgent(jwt_token=e2e_jwt_token, context=e2e_context)

    # Different ways to create tasks
    variations = [
        "I need to remember to buy eggs",
        "Create a task: Call mom",
        "Add buy bread to my list"
    ]

    task_ids = []

    for variation in variations:
        response = await agent.process_message(variation)
        assert len(response) > 0
        if e2e_context.last_task_id:
            task_ids.append(e2e_context.last_task_id)

    # Cleanup
    for task_id in task_ids:
        await agent.process_message(f"Delete task {task_id}")


# Note: To run E2E tests:
# 1. Start Phase 2 backend: cd backend && uv run uvicorn app.main:app
# 2. Get JWT token by signing in to backend
# 3. Set environment variables:
#    export JWT_TOKEN="your_jwt_token_here"
#    export OPENAI_API_KEY="your_openai_key_here"
# 4. Run tests: pytest -m e2e tests/test_e2e.py -v
