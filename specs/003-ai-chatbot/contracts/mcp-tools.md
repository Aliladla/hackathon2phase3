# MCP Tools Specification: AI-Powered Todo Chatbot (Phase 3)

**Date**: 2025-02-15
**Feature**: 003-ai-chatbot
**Purpose**: Define MCP (Model Context Protocol) tools for task management operations

## Overview

This document specifies all MCP tools that the AI agent can use to interact with the Phase 2 backend API. Each tool provides a structured interface for a specific task management operation, enabling the AI to translate natural language into API calls.

## MCP Tool Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent (OpenAI)                         │
│  - Receives natural language input                           │
│  - Recognizes intent                                         │
│  - Calls appropriate MCP tool                                │
└────────────────────┬────────────────────────────────────────┘
                     │ Function Call
                     │ {"name": "create_task", "arguments": {...}}
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Tools Layer                           │
│  - Validates tool inputs                                     │
│  - Executes API calls                                        │
│  - Formats responses                                         │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP Request + JWT
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Phase 2 Backend API (FastAPI)                   │
│  - Processes request                                         │
│  - Returns JSON response                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Tool 1: create_task

Creates a new task for the authenticated user.

### Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "create_task",
    "description": "Create a new task with a title and optional description. Use this when the user wants to add a new item to their todo list.",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "The task title (1-200 characters). This is what the user wants to do.",
          "minLength": 1,
          "maxLength": 200
        },
        "description": {
          "type": "string",
          "description": "Optional additional details about the task (0-1000 characters). Use this for extra context or notes.",
          "maxLength": 1000,
          "default": ""
        }
      },
      "required": ["title"]
    }
  }
}
```

### API Mapping

- **Endpoint**: `POST /api/tasks`
- **Authentication**: JWT token required
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string"
  }
  ```

### Example Usage

**User Input**: "Add a task to buy groceries"

**Tool Call**:
```json
{
  "name": "create_task",
  "arguments": {
    "title": "Buy groceries",
    "description": ""
  }
}
```

**API Response**:
```json
{
  "id": 42,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "",
  "completed": false,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T10:30:00Z"
}
```

**Agent Response**: "I've added 'Buy groceries' to your list. It's task #42."

### Error Handling

| Error | Status Code | Agent Response |
|-------|-------------|----------------|
| Empty title | 400 | "I need a task title. What would you like to add?" |
| Title too long | 400 | "That title is too long. Can you make it shorter (under 200 characters)?" |
| Authentication failed | 401 | "Your session has expired. Please sign in again." |
| Server error | 500 | "I'm having trouble creating that task. Please try again." |

---

## Tool 2: list_tasks

Lists all tasks for the authenticated user with optional filtering.

### Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "list_tasks",
    "description": "Get a list of the user's tasks. Can filter by completion status. Use this when the user wants to see their todo list.",
    "parameters": {
      "type": "object",
      "properties": {
        "completed": {
          "type": "boolean",
          "description": "Filter by completion status. true = only completed tasks, false = only incomplete tasks, null/undefined = all tasks"
        },
        "limit": {
          "type": "integer",
          "description": "Maximum number of tasks to return (1-1000)",
          "default": 100,
          "minimum": 1,
          "maximum": 1000
        },
        "offset": {
          "type": "integer",
          "description": "Number of tasks to skip for pagination",
          "default": 0,
          "minimum": 0
        }
      },
      "required": []
    }
  }
}
```

### API Mapping

- **Endpoint**: `GET /api/tasks`
- **Authentication**: JWT token required
- **Query Parameters**: `completed`, `limit`, `offset`

### Example Usage

**User Input**: "Show me my incomplete tasks"

**Tool Call**:
```json
{
  "name": "list_tasks",
  "arguments": {
    "completed": false,
    "limit": 100,
    "offset": 0
  }
}
```

**API Response**:
```json
{
  "tasks": [
    {
      "id": 42,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "",
      "completed": false,
      "created_at": "2025-02-15T10:30:00Z",
      "updated_at": "2025-02-15T10:30:00Z"
    },
    {
      "id": 43,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Finish project report",
      "description": "Due Friday",
      "completed": false,
      "created_at": "2025-02-15T11:00:00Z",
      "updated_at": "2025-02-15T11:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

**Agent Response**: "You have 2 incomplete tasks:\n1. Task #42: Buy groceries\n2. Task #43: Finish project report (Due Friday)"

### Error Handling

| Error | Status Code | Agent Response |
|-------|-------------|----------------|
| Authentication failed | 401 | "Your session has expired. Please sign in again." |
| Server error | 500 | "I'm having trouble retrieving your tasks. Please try again." |

---

## Tool 3: get_task

Gets details of a specific task by ID.

### Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "get_task",
    "description": "Get details of a specific task by its ID. Use this when the user asks about a particular task.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The ID of the task to retrieve"
        }
      },
      "required": ["task_id"]
    }
  }
}
```

### API Mapping

- **Endpoint**: `GET /api/tasks/{task_id}`
- **Authentication**: JWT token required

### Example Usage

**User Input**: "Tell me about task 42"

**Tool Call**:
```json
{
  "name": "get_task",
  "arguments": {
    "task_id": 42
  }
}
```

**API Response**:
```json
{
  "id": 42,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T10:30:00Z"
}
```

**Agent Response**: "Task #42 is 'Buy groceries'. Details: Milk, eggs, bread. Status: Not completed."

### Error Handling

| Error | Status Code | Agent Response |
|-------|-------------|----------------|
| Task not found | 404 | "I couldn't find task #42. Would you like to see your task list?" |
| Authentication failed | 401 | "Your session has expired. Please sign in again." |
| Server error | 500 | "I'm having trouble retrieving that task. Please try again." |

---

## Tool 4: update_task

Updates a task's title, description, or completion status.

### Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "update_task",
    "description": "Update a task's title, description, or completion status. Use this when the user wants to modify an existing task.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The ID of the task to update"
        },
        "title": {
          "type": "string",
          "description": "New task title (1-200 characters). Only provide if changing the title.",
          "minLength": 1,
          "maxLength": 200
        },
        "description": {
          "type": "string",
          "description": "New task description (0-1000 characters). Only provide if changing the description.",
          "maxLength": 1000
        },
        "completed": {
          "type": "boolean",
          "description": "New completion status. Only provide if changing the status."
        }
      },
      "required": ["task_id"]
    }
  }
}
```

### API Mapping

- **Endpoint**: `PUT /api/tasks/{task_id}` or `PATCH /api/tasks/{task_id}`
- **Authentication**: JWT token required
- **Request Body**: Only fields being updated

### Example Usage

**User Input**: "Change task 42 title to 'Buy organic groceries'"

**Tool Call**:
```json
{
  "name": "update_task",
  "arguments": {
    "task_id": 42,
    "title": "Buy organic groceries"
  }
}
```

**API Response**:
```json
{
  "id": 42,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy organic groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T12:00:00Z"
}
```

**Agent Response**: "I've updated task #42. The new title is 'Buy organic groceries'."

### Error Handling

| Error | Status Code | Agent Response |
|-------|-------------|----------------|
| Task not found | 404 | "I couldn't find task #42. Would you like to see your task list?" |
| Empty title | 400 | "The task title can't be empty. What would you like to call it?" |
| Title too long | 400 | "That title is too long. Can you make it shorter (under 200 characters)?" |
| Authentication failed | 401 | "Your session has expired. Please sign in again." |
| Server error | 500 | "I'm having trouble updating that task. Please try again." |

---

## Tool 5: delete_task

Deletes a task permanently.

### Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "delete_task",
    "description": "Permanently delete a task. Use this when the user wants to remove a task from their list. ALWAYS confirm with the user before calling this function.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The ID of the task to delete"
        }
      },
      "required": ["task_id"]
    }
  }
}
```

### API Mapping

- **Endpoint**: `DELETE /api/tasks/{task_id}`
- **Authentication**: JWT token required

### Example Usage

**User Input**: "Delete task 42"

**Agent Confirmation**: "Are you sure you want to delete task #42 ('Buy groceries')? This cannot be undone. (yes/no)"

**User Confirms**: "yes"

**Tool Call**:
```json
{
  "name": "delete_task",
  "arguments": {
    "task_id": 42
  }
}
```

**API Response**: 204 No Content

**Agent Response**: "Done! I've deleted task #42 ('Buy groceries') from your list."

### Error Handling

| Error | Status Code | Agent Response |
|-------|-------------|----------------|
| Task not found | 404 | "I couldn't find task #42. It may have already been deleted." |
| Authentication failed | 401 | "Your session has expired. Please sign in again." |
| Server error | 500 | "I'm having trouble deleting that task. Please try again." |

---

## Tool 6: toggle_complete

Toggles a task's completion status (complete ↔ incomplete).

### Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "toggle_complete",
    "description": "Toggle a task's completion status. If it's incomplete, mark it complete. If it's complete, mark it incomplete. Use this when the user wants to mark a task as done or undone.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The ID of the task to toggle"
        }
      },
      "required": ["task_id"]
    }
  }
}
```

### API Mapping

- **Endpoint**: `PATCH /api/tasks/{task_id}/complete`
- **Authentication**: JWT token required

### Example Usage

**User Input**: "Mark task 42 as complete"

**Tool Call**:
```json
{
  "name": "toggle_complete",
  "arguments": {
    "task_id": 42
  }
}
```

**API Response**:
```json
{
  "id": 42,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T13:00:00Z"
}
```

**Agent Response**: "Done! I've marked task #42 ('Buy groceries') as complete. Great job!"

### Error Handling

| Error | Status Code | Agent Response |
|-------|-------------|----------------|
| Task not found | 404 | "I couldn't find task #42. Would you like to see your task list?" |
| Authentication failed | 401 | "Your session has expired. Please sign in again." |
| Server error | 500 | "I'm having trouble updating that task. Please try again." |

---

## Tool Execution Flow

### Standard Flow

1. **Agent receives user message** → Analyzes intent
2. **Agent selects appropriate tool** → Based on intent
3. **Agent extracts parameters** → From natural language
4. **Agent calls tool** → With structured parameters
5. **Tool validates inputs** → Check required fields, types, constraints
6. **Tool executes API call** → HTTP request to Phase 2 backend
7. **Tool handles response** → Success or error
8. **Tool returns result** → Formatted for agent
9. **Agent generates response** → Conversational message to user
10. **Context updated** → Last task ID, operation type

### Error Flow

1. **Tool execution fails** → API error or validation error
2. **Tool catches error** → Determines error type
3. **Tool formats error message** → User-friendly message
4. **Tool returns error result** → To agent
5. **Agent generates error response** → Helpful message to user
6. **Agent suggests next action** → If appropriate

---

## Tool Implementation Guidelines

### Input Validation

All tools must validate inputs before making API calls:

```python
def validate_title(title: str) -> None:
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title too long (max 200 characters)")

def validate_description(description: str) -> None:
    if len(description) > 1000:
        raise ValueError("Description too long (max 1000 characters)")

def validate_task_id(task_id: int) -> None:
    if task_id <= 0:
        raise ValueError("Task ID must be positive")
```

### Error Handling

All tools must handle common errors:

```python
async def execute_tool(tool_name: str, **kwargs):
    try:
        # Validate inputs
        validate_inputs(**kwargs)

        # Execute API call
        response = await api_client.call(tool_name, **kwargs)

        # Return success result
        return MCPToolResult(
            tool_name=tool_name,
            success=True,
            result=response.data
        )

    except ValidationError as e:
        return MCPToolResult(
            tool_name=tool_name,
            success=False,
            error=f"Invalid input: {str(e)}"
        )

    except AuthenticationError as e:
        return MCPToolResult(
            tool_name=tool_name,
            success=False,
            error="Authentication failed. Please sign in again."
        )

    except APIError as e:
        return MCPToolResult(
            tool_name=tool_name,
            success=False,
            error=f"API error: {str(e)}"
        )

    except Exception as e:
        return MCPToolResult(
            tool_name=tool_name,
            success=False,
            error="An unexpected error occurred. Please try again."
        )
```

### Response Formatting

Tools should format responses for natural conversation:

```python
def format_task_list(tasks: List[Dict]) -> str:
    if not tasks:
        return "You have no tasks."

    lines = [f"You have {len(tasks)} task{'s' if len(tasks) != 1 else ''}:"]
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["completed"] else "○"
        lines.append(f"{i}. {status} Task #{task['id']}: {task['title']}")
        if task["description"]:
            lines.append(f"   {task['description']}")

    return "\n".join(lines)
```

---

## Testing MCP Tools

### Unit Tests

Test each tool in isolation with mocked API responses:

```python
@pytest.mark.asyncio
async def test_create_task_success(mock_api_client):
    # Mock API response
    mock_api_client.post.return_value = APIResponse(
        status_code=201,
        data={"id": 42, "title": "Buy milk", "completed": False}
    )

    # Execute tool
    tool = CreateTaskTool(api_client=mock_api_client)
    result = await tool.execute(title="Buy milk")

    # Assert
    assert result.success
    assert result.result["id"] == 42
    assert result.result["title"] == "Buy milk"
```

### Integration Tests

Test tools with real Phase 2 backend:

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_and_list_tasks(api_client):
    # Create task
    create_tool = CreateTaskTool(api_client=api_client)
    create_result = await create_tool.execute(title="Test task")
    assert create_result.success

    # List tasks
    list_tool = ListTasksTool(api_client=api_client)
    list_result = await list_tool.execute()
    assert list_result.success
    assert len(list_result.result["tasks"]) > 0
```

---

## Conclusion

These MCP tools provide a structured interface between the AI agent and Phase 2 backend API. Each tool is designed to be:
- **Self-contained**: Clear inputs and outputs
- **Validated**: Input validation before API calls
- **Error-handled**: Graceful error handling with user-friendly messages
- **Testable**: Easy to unit test and integration test
- **Conversational**: Responses formatted for natural conversation

**Ready for Quickstart**: Proceed to quickstart.md for setup and usage instructions.
