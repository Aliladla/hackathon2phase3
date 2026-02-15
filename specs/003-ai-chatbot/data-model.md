# Data Model: AI-Powered Todo Chatbot (Phase 3)

**Date**: 2025-02-15
**Feature**: 003-ai-chatbot
**Purpose**: Define entities, schemas, and data structures for chatbot service

## Overview

Phase 3 introduces conversational AI capabilities with conversation context management and MCP tool schemas. The data model focuses on maintaining conversation state and defining structured interfaces between the AI agent and Phase 2 backend.

## Entities

### ChatMessage

Represents a single message in a conversation.

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, AUTO | Unique message identifier |
| session_id | UUID | NOT NULL, INDEX | Conversation session identifier |
| role | Enum | NOT NULL | Message role: "user", "assistant", "system" |
| content | TEXT | NOT NULL | Message content (natural language) |
| timestamp | TIMESTAMP | DEFAULT NOW() | Message creation time |
| tool_calls | JSON | NULLABLE | OpenAI tool calls (if any) |
| tool_results | JSON | NULLABLE | Tool execution results (if any) |

**Validation Rules:**
- Role must be one of: "user", "assistant", "system"
- Content cannot be empty
- Tool calls must be valid JSON if present

**Python Model:**
```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict

@dataclass
class ChatMessage:
    id: UUID
    session_id: UUID
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: datetime
    tool_calls: Optional[List[Dict]] = None
    tool_results: Optional[List[Dict]] = None
```

---

### ConversationContext

Maintains state and context across messages in a conversation session.

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| session_id | UUID | PRIMARY KEY | Unique session identifier |
| user_id | UUID | NOT NULL | User who owns this session |
| messages | List[ChatMessage] | NOT NULL | Recent messages (last 10) |
| last_task_id | INT | NULLABLE | Last mentioned task ID |
| last_operation | VARCHAR(50) | NULLABLE | Last operation type |
| created_at | TIMESTAMP | DEFAULT NOW() | Session creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last activity time |
| expires_at | TIMESTAMP | NOT NULL | Session expiration time |

**Validation Rules:**
- Messages list limited to 10 most recent
- Last operation must be one of: "create", "view", "update", "delete", "complete"
- Session expires after 30 minutes of inactivity

**Python Model:**
```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from typing import Optional, List

@dataclass
class ConversationContext:
    session_id: UUID = field(default_factory=uuid4)
    user_id: UUID = None
    messages: List[ChatMessage] = field(default_factory=list)
    last_task_id: Optional[int] = None
    last_operation: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=30))

    def add_message(self, role: str, content: str, tool_calls=None, tool_results=None):
        """Add a message to the conversation."""
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

        # Keep only last 10 messages
        if len(self.messages) > 10:
            self.messages = self.messages[-10:]

        self.updated_at = datetime.utcnow()
        self.expires_at = datetime.utcnow() + timedelta(minutes=30)

    def get_context_summary(self) -> str:
        """Get a summary of current context for system prompt."""
        context_parts = []

        if self.last_task_id:
            context_parts.append(f"Last mentioned task ID: {self.last_task_id}")

        if self.last_operation:
            context_parts.append(f"Last operation: {self.last_operation}")

        return "\n".join(context_parts) if context_parts else "No previous context"

    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.utcnow() > self.expires_at
```

---

### MCPToolDefinition

Defines an MCP tool that the AI agent can call.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| name | str | Tool name (e.g., "create_task") |
| description | str | Human-readable description |
| parameters | dict | JSON Schema for tool parameters |
| required | list[str] | Required parameter names |

**Python Model:**
```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class MCPToolDefinition:
    name: str
    description: str
    parameters: Dict
    required: List[str]

    def to_openai_function(self) -> Dict:
        """Convert to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": self.required
                }
            }
        }
```

---

### MCPToolResult

Represents the result of executing an MCP tool.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| tool_name | str | Name of the tool that was executed |
| success | bool | Whether execution succeeded |
| result | dict | Tool execution result data |
| error | str | Error message (if failed) |
| execution_time | float | Time taken to execute (seconds) |

**Python Model:**
```python
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class MCPToolResult:
    tool_name: str
    success: bool
    result: Optional[Dict] = None
    error: Optional[str] = None
    execution_time: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "tool_name": self.tool_name,
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "execution_time": self.execution_time
        }
```

---

## MCP Tool Schemas

### create_task

Creates a new task for the user.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Task title (1-200 characters)",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Optional task description (0-1000 characters)",
      "maxLength": 1000,
      "default": ""
    }
  },
  "required": ["title"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "user_id": {"type": "string"},
    "title": {"type": "string"},
    "description": {"type": "string"},
    "completed": {"type": "boolean"},
    "created_at": {"type": "string", "format": "date-time"},
    "updated_at": {"type": "string", "format": "date-time"}
  }
}
```

---

### list_tasks

Lists all tasks for the user with optional filtering.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "completed": {
      "type": "boolean",
      "description": "Filter by completion status (optional)"
    },
    "limit": {
      "type": "integer",
      "description": "Maximum tasks to return",
      "default": 100,
      "minimum": 1,
      "maximum": 1000
    },
    "offset": {
      "type": "integer",
      "description": "Number of tasks to skip",
      "default": 0,
      "minimum": 0
    }
  },
  "required": []
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "title": {"type": "string"},
          "description": {"type": "string"},
          "completed": {"type": "boolean"},
          "created_at": {"type": "string"},
          "updated_at": {"type": "string"}
        }
      }
    },
    "total": {"type": "integer"},
    "limit": {"type": "integer"},
    "offset": {"type": "integer"}
  }
}
```

---

### get_task

Gets a specific task by ID.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Task ID to retrieve"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "user_id": {"type": "string"},
    "title": {"type": "string"},
    "description": {"type": "string"},
    "completed": {"type": "boolean"},
    "created_at": {"type": "string"},
    "updated_at": {"type": "string"}
  }
}
```

---

### update_task

Updates a task's title, description, or completion status.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Task ID to update"
    },
    "title": {
      "type": "string",
      "description": "New task title (optional)",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "New task description (optional)",
      "maxLength": 1000
    },
    "completed": {
      "type": "boolean",
      "description": "New completion status (optional)"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "user_id": {"type": "string"},
    "title": {"type": "string"},
    "description": {"type": "string"},
    "completed": {"type": "boolean"},
    "created_at": {"type": "string"},
    "updated_at": {"type": "string"}
  }
}
```

---

### delete_task

Deletes a task permanently.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Task ID to delete"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "message": {"type": "string"}
  }
}
```

---

### toggle_complete

Toggles a task's completion status.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Task ID to toggle"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "user_id": {"type": "string"},
    "title": {"type": "string"},
    "description": {"type": "string"},
    "completed": {"type": "boolean"},
    "created_at": {"type": "string"},
    "updated_at": {"type": "string"}
  }
}
```

---

## Session Management

### Session Storage

**In-Memory Storage (Phase 3):**
```python
from typing import Dict
from uuid import UUID

class SessionStore:
    """In-memory session storage."""

    def __init__(self):
        self._sessions: Dict[UUID, ConversationContext] = {}

    def create_session(self, user_id: UUID) -> ConversationContext:
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

    def update_session(self, context: ConversationContext):
        """Update session in storage."""
        self._sessions[context.session_id] = context

    def delete_session(self, session_id: UUID):
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def cleanup_expired(self):
        """Remove expired sessions."""
        expired = [
            sid for sid, ctx in self._sessions.items()
            if ctx.is_expired()
        ]
        for sid in expired:
            del self._sessions[sid]
```

---

## API Client Data Models

### APIRequest

Represents a request to Phase 2 backend API.

**Python Model:**
```python
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class APIRequest:
    method: str  # GET, POST, PUT, PATCH, DELETE
    endpoint: str  # /api/tasks, /api/tasks/5, etc.
    data: Optional[Dict] = None
    params: Optional[Dict] = None
    jwt_token: str = None
```

---

### APIResponse

Represents a response from Phase 2 backend API.

**Python Model:**
```python
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class APIResponse:
    status_code: int
    data: Optional[Dict] = None
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return 200 <= self.status_code < 300
```

---

## Error Models

### ChatbotError

Base exception for chatbot errors.

**Python Model:**
```python
class ChatbotError(Exception):
    """Base exception for chatbot errors."""
    pass

class IntentRecognitionError(ChatbotError):
    """Raised when intent cannot be recognized."""
    pass

class ToolExecutionError(ChatbotError):
    """Raised when MCP tool execution fails."""
    pass

class APIClientError(ChatbotError):
    """Raised when API client encounters an error."""
    pass

class AuthenticationError(ChatbotError):
    """Raised when authentication fails."""
    pass

class SessionExpiredError(ChatbotError):
    """Raised when conversation session expires."""
    pass
```

---

## Conclusion

The Phase 3 data model focuses on conversation state management and MCP tool schemas. All entities are designed to be lightweight and stateless (except for session context), enabling easy scaling and deployment in Phase 4.

**Key Features:**
- Conversation context with recent message history
- MCP tool schemas for all Basic Level operations
- Session management with expiration
- Clear error models for different failure scenarios
- Integration with Phase 2 backend via API client

**Ready for Contracts**: Proceed to contracts/mcp-tools.md for detailed MCP tool specifications.
