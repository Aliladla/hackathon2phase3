"""Unit tests for conversation context management."""
import pytest
from datetime import datetime, timedelta
from uuid import UUID
from chatbot.conversation import ChatMessage, ConversationContext, SessionStore


def test_chat_message_creation():
    """Test ChatMessage creation."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")

    message = ChatMessage(
        id=UUID("87654321-4321-8765-4321-876543218765"),
        session_id=session_id,
        role="user",
        content="Add a task to buy milk",
        timestamp=datetime.utcnow()
    )

    assert message.session_id == session_id
    assert message.role == "user"
    assert message.content == "Add a task to buy milk"
    assert message.tool_calls is None
    assert message.tool_results is None


def test_conversation_context_initialization():
    """Test ConversationContext initialization."""
    context = ConversationContext()

    assert isinstance(context.session_id, UUID)
    assert context.user_id is None
    assert len(context.messages) == 0
    assert context.last_task_id is None
    assert context.last_operation is None
    assert isinstance(context.created_at, datetime)
    assert isinstance(context.updated_at, datetime)
    assert isinstance(context.expires_at, datetime)


def test_add_message(conversation_context):
    """Test adding messages to conversation context."""
    conversation_context.add_message(
        role="user",
        content="Show me my tasks"
    )

    assert len(conversation_context.messages) == 1
    assert conversation_context.messages[0].role == "user"
    assert conversation_context.messages[0].content == "Show me my tasks"
    assert conversation_context.messages[0].session_id == conversation_context.session_id


def test_add_message_with_tool_calls(conversation_context):
    """Test adding message with tool calls."""
    tool_calls = [
        {
            "id": "call_123",
            "type": "function",
            "function": {"name": "list_tasks", "arguments": "{}"}
        }
    ]

    conversation_context.add_message(
        role="assistant",
        content="",
        tool_calls=tool_calls
    )

    assert len(conversation_context.messages) == 1
    assert conversation_context.messages[0].tool_calls == tool_calls


def test_message_limit(conversation_context):
    """Test that context keeps only last 10 messages."""
    # Add 15 messages
    for i in range(15):
        conversation_context.add_message(
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message {i}"
        )

    # Should only keep last 10
    assert len(conversation_context.messages) == 10
    assert conversation_context.messages[0].content == "Message 5"
    assert conversation_context.messages[-1].content == "Message 14"


def test_get_context_summary_empty(conversation_context):
    """Test context summary with no context."""
    summary = conversation_context.get_context_summary()

    assert summary == "No previous context"


def test_get_context_summary_with_task(conversation_context):
    """Test context summary with task context."""
    conversation_context.update_task_context(task_id=5, operation="create")

    summary = conversation_context.get_context_summary()

    assert "Last mentioned task ID: 5" in summary
    assert "Last operation: create" in summary


def test_get_messages_for_openai(conversation_context):
    """Test converting messages to OpenAI format."""
    conversation_context.add_message(role="user", content="Hello")
    conversation_context.add_message(role="assistant", content="Hi there!")

    messages = conversation_context.get_messages_for_openai()

    assert len(messages) == 2
    assert messages[0] == {"role": "user", "content": "Hello"}
    assert messages[1] == {"role": "assistant", "content": "Hi there!"}


def test_is_expired_not_expired(conversation_context):
    """Test that new context is not expired."""
    assert conversation_context.is_expired() is False


def test_is_expired_expired():
    """Test that old context is expired."""
    context = ConversationContext()
    # Set expiration to past
    context.expires_at = datetime.utcnow() - timedelta(minutes=1)

    assert context.is_expired() is True


def test_update_task_context(conversation_context):
    """Test updating task context."""
    conversation_context.update_task_context(task_id=10, operation="update")

    assert conversation_context.last_task_id == 10
    assert conversation_context.last_operation == "update"


def test_update_task_context_partial(conversation_context):
    """Test partial task context update."""
    conversation_context.update_task_context(task_id=5, operation="create")
    conversation_context.update_task_context(task_id=None, operation="delete")

    # task_id should remain 5 (not updated to None)
    assert conversation_context.last_task_id == 5
    assert conversation_context.last_operation == "delete"


def test_session_expiration_extends_on_message(conversation_context):
    """Test that adding messages extends session expiration."""
    initial_expires = conversation_context.expires_at

    # Wait a bit and add message
    import time
    time.sleep(0.1)

    conversation_context.add_message(role="user", content="Test")

    # Expiration should be extended
    assert conversation_context.expires_at > initial_expires


def test_session_store_create_session(session_store):
    """Test creating a new session."""
    context = session_store.create_session()

    assert isinstance(context, ConversationContext)
    assert isinstance(context.session_id, UUID)

    # Should be retrievable
    retrieved = session_store.get_session(context.session_id)
    assert retrieved is not None
    assert retrieved.session_id == context.session_id


def test_session_store_get_session(session_store):
    """Test retrieving an existing session."""
    context = session_store.create_session()
    session_id = context.session_id

    retrieved = session_store.get_session(session_id)

    assert retrieved is not None
    assert retrieved.session_id == session_id


def test_session_store_get_nonexistent_session(session_store):
    """Test retrieving a non-existent session."""
    fake_id = UUID("00000000-0000-0000-0000-000000000000")

    retrieved = session_store.get_session(fake_id)

    assert retrieved is None


def test_session_store_get_expired_session(session_store):
    """Test that expired sessions are removed on retrieval."""
    context = session_store.create_session()
    session_id = context.session_id

    # Expire the session
    context.expires_at = datetime.utcnow() - timedelta(minutes=1)
    session_store.update_session(context)

    # Should return None and remove from store
    retrieved = session_store.get_session(session_id)

    assert retrieved is None


def test_session_store_update_session(session_store):
    """Test updating a session."""
    context = session_store.create_session()
    session_id = context.session_id

    # Modify context
    context.add_message(role="user", content="Test message")
    session_store.update_session(context)

    # Retrieve and verify
    retrieved = session_store.get_session(session_id)
    assert len(retrieved.messages) == 1
    assert retrieved.messages[0].content == "Test message"


def test_session_store_delete_session(session_store):
    """Test deleting a session."""
    context = session_store.create_session()
    session_id = context.session_id

    # Delete session
    session_store.delete_session(session_id)

    # Should not be retrievable
    retrieved = session_store.get_session(session_id)
    assert retrieved is None


def test_session_store_cleanup_expired(session_store):
    """Test cleaning up expired sessions."""
    # Create multiple sessions
    context1 = session_store.create_session()
    context2 = session_store.create_session()
    context3 = session_store.create_session()

    # Expire two of them
    context1.expires_at = datetime.utcnow() - timedelta(minutes=1)
    context2.expires_at = datetime.utcnow() - timedelta(minutes=1)
    session_store.update_session(context1)
    session_store.update_session(context2)

    # Cleanup
    session_store.cleanup_expired()

    # Only context3 should remain
    assert session_store.get_session(context1.session_id) is None
    assert session_store.get_session(context2.session_id) is None
    assert session_store.get_session(context3.session_id) is not None


def test_session_store_create_with_user_id(session_store):
    """Test creating session with user ID."""
    user_id = UUID("11111111-1111-1111-1111-111111111111")

    context = session_store.create_session(user_id=user_id)

    assert context.user_id == user_id
