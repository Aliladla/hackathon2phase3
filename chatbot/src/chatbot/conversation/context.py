"""Conversation context management."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any


@dataclass
class ChatMessage:
    """Represents a single message in a conversation."""

    id: UUID
    session_id: UUID
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: datetime
    tool_calls: Optional[List[Dict]] = None
    tool_results: Optional[List[Dict]] = None


@dataclass
class ConversationContext:
    """Maintains state and context across messages in a conversation session."""

    session_id: UUID = field(default_factory=uuid4)
    user_id: Optional[UUID] = None
    messages: List[ChatMessage] = field(default_factory=list)
    last_task_id: Optional[int] = None
    last_operation: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=30))

    def add_message(
        self,
        role: str,
        content: str,
        tool_calls: Optional[List[Dict]] = None,
        tool_results: Optional[List[Dict]] = None
    ) -> None:
        """
        Add a message to the conversation.

        Args:
            role: Message role ("user", "assistant", "system")
            content: Message content
            tool_calls: Optional OpenAI tool calls
            tool_results: Optional tool execution results
        """
        message = ChatMessage(
            id=uuid4(),
            session_id=self.session_id,
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            tool_calls=tool_calls,
            tool_results=tool_results
        )
        self.messages.append(message)

        # Keep only last 10 messages to manage context size
        if len(self.messages) > 10:
            self.messages = self.messages[-10:]

        self.updated_at = datetime.utcnow()
        self.expires_at = datetime.utcnow() + timedelta(minutes=30)

    def get_context_summary(self) -> str:
        """
        Get a summary of current context for system prompt.

        Returns:
            Context summary string
        """
        context_parts = []

        if self.last_task_id:
            context_parts.append(f"Last mentioned task ID: {self.last_task_id}")

        if self.last_operation:
            context_parts.append(f"Last operation: {self.last_operation}")

        return "\n".join(context_parts) if context_parts else "No previous context"

    def get_messages_for_openai(self) -> List[Dict[str, str]]:
        """
        Get messages in OpenAI format.

        Returns:
            List of message dictionaries for OpenAI API
        """
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]

    def is_expired(self) -> bool:
        """
        Check if session has expired.

        Returns:
            True if expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at

    def update_task_context(self, task_id: Optional[int], operation: Optional[str]) -> None:
        """
        Update task-related context.

        Args:
            task_id: Last mentioned task ID
            operation: Last operation type
        """
        if task_id is not None:
            self.last_task_id = task_id
        if operation is not None:
            self.last_operation = operation
        self.updated_at = datetime.utcnow()


class SessionStore:
    """In-memory session storage."""

    def __init__(self):
        self._sessions: Dict[UUID, ConversationContext] = {}

    def create_session(self, user_id: Optional[UUID] = None) -> ConversationContext:
        """Create a new conversation session."""
        context = ConversationContext(user_id=user_id)
        self._sessions[context.session_id] = context
        return context

    def get_session(self, session_id: UUID) -> Optional[ConversationContext]:
        """Get an existing session."""
        context = self._sessions.get(session_id)
        if context and context.is_expired():
            del self._sessions[session_id]
            return None
        return context

    def update_session(self, context: ConversationContext) -> None:
        """Update session in storage."""
        self._sessions[context.session_id] = context

    def delete_session(self, session_id: UUID) -> None:
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def cleanup_expired(self) -> None:
        """Remove expired sessions."""
        expired = [
            sid for sid, ctx in self._sessions.items()
            if ctx.is_expired()
        ]
        for sid in expired:
            del self._sessions[sid]
