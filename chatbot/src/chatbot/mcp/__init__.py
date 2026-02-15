"""MCP package initialization."""
from chatbot.mcp.schemas import (
    MCPToolDefinition,
    MCPToolResult,
    ALL_TOOLS,
    CREATE_TASK_TOOL,
    LIST_TASKS_TOOL,
    GET_TASK_TOOL,
    UPDATE_TASK_TOOL,
    DELETE_TASK_TOOL,
    TOGGLE_COMPLETE_TOOL
)
from chatbot.mcp.executor import MCPToolExecutor

__all__ = [
    "MCPToolDefinition",
    "MCPToolResult",
    "MCPToolExecutor",
    "ALL_TOOLS",
    "CREATE_TASK_TOOL",
    "LIST_TASKS_TOOL",
    "GET_TASK_TOOL",
    "UPDATE_TASK_TOOL",
    "DELETE_TASK_TOOL",
    "TOGGLE_COMPLETE_TOOL"
]
