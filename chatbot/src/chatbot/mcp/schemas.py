"""MCP tool schemas and data models."""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class MCPToolDefinition:
    """Definition of an MCP tool for OpenAI function calling."""

    name: str
    description: str
    parameters: Dict[str, Any]
    required: List[str]

    def to_openai_function(self) -> Dict[str, Any]:
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


@dataclass
class MCPToolResult:
    """Result of executing an MCP tool."""

    tool_name: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "tool_name": self.tool_name,
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "execution_time": self.execution_time
        }


# MCP Tool Definitions for all task operations

CREATE_TASK_TOOL = MCPToolDefinition(
    name="create_task",
    description="Create a new task with a title and optional description. Use this when the user wants to add a new item to their todo list.",
    parameters={
        "title": {
            "type": "string",
            "description": "The task title (1-200 characters). This is what the user wants to do."
        },
        "description": {
            "type": "string",
            "description": "Optional additional details about the task (0-1000 characters)."
        }
    },
    required=["title"]
)

LIST_TASKS_TOOL = MCPToolDefinition(
    name="list_tasks",
    description="Get a list of the user's tasks. Can filter by completion status. Use this when the user wants to see their todo list.",
    parameters={
        "completed": {
            "type": "boolean",
            "description": "Filter by completion status. true = only completed, false = only incomplete, omit = all tasks"
        },
        "limit": {
            "type": "integer",
            "description": "Maximum number of tasks to return (default 100)"
        }
    },
    required=[]
)

GET_TASK_TOOL = MCPToolDefinition(
    name="get_task",
    description="Get details of a specific task by its ID. Use this when the user asks about a particular task.",
    parameters={
        "task_id": {
            "type": "integer",
            "description": "The ID of the task to retrieve"
        }
    },
    required=["task_id"]
)

UPDATE_TASK_TOOL = MCPToolDefinition(
    name="update_task",
    description="Update a task's title, description, or completion status. Use this when the user wants to modify an existing task.",
    parameters={
        "task_id": {
            "type": "integer",
            "description": "The ID of the task to update"
        },
        "title": {
            "type": "string",
            "description": "New task title (1-200 characters). Only provide if changing the title."
        },
        "description": {
            "type": "string",
            "description": "New task description. Only provide if changing the description."
        },
        "completed": {
            "type": "boolean",
            "description": "New completion status. Only provide if changing the status."
        }
    },
    required=["task_id"]
)

DELETE_TASK_TOOL = MCPToolDefinition(
    name="delete_task",
    description="Permanently delete a task. Use this when the user wants to remove a task. ALWAYS confirm with the user before calling this.",
    parameters={
        "task_id": {
            "type": "integer",
            "description": "The ID of the task to delete"
        }
    },
    required=["task_id"]
)

TOGGLE_COMPLETE_TOOL = MCPToolDefinition(
    name="toggle_complete",
    description="Toggle a task's completion status. If incomplete, mark complete. If complete, mark incomplete. Use when user wants to mark a task as done.",
    parameters={
        "task_id": {
            "type": "integer",
            "description": "The ID of the task to toggle"
        }
    },
    required=["task_id"]
)

# All available MCP tools
ALL_TOOLS = [
    CREATE_TASK_TOOL,
    LIST_TASKS_TOOL,
    GET_TASK_TOOL,
    UPDATE_TASK_TOOL,
    DELETE_TASK_TOOL,
    TOGGLE_COMPLETE_TOOL
]
