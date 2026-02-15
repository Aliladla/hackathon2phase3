"""MCP tools executor for calling Phase 2 backend API."""
import time
from typing import Dict, Any, Optional
from chatbot.api.client import APIClient, APIError, AuthenticationError, NotFoundError
from chatbot.mcp.schemas import MCPToolResult


class MCPToolExecutor:
    """Executes MCP tools by calling Phase 2 backend API."""

    def __init__(self, api_client: APIClient):
        """
        Initialize MCP tool executor.

        Args:
            api_client: API client for Phase 2 backend
        """
        self.api_client = api_client

    async def execute(self, tool_name: str, arguments: Dict[str, Any]) -> MCPToolResult:
        """
        Execute an MCP tool with given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            MCPToolResult with execution result
        """
        start_time = time.time()

        try:
            if tool_name == "create_task":
                result = await self._create_task(**arguments)
            elif tool_name == "list_tasks":
                result = await self._list_tasks(**arguments)
            elif tool_name == "get_task":
                result = await self._get_task(**arguments)
            elif tool_name == "update_task":
                result = await self._update_task(**arguments)
            elif tool_name == "delete_task":
                result = await self._delete_task(**arguments)
            elif tool_name == "toggle_complete":
                result = await self._toggle_complete(**arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            execution_time = time.time() - start_time
            return MCPToolResult(
                tool_name=tool_name,
                success=True,
                result=result,
                execution_time=execution_time
            )

        except AuthenticationError as e:
            execution_time = time.time() - start_time
            return MCPToolResult(
                tool_name=tool_name,
                success=False,
                error="Your session has expired. Please sign in again.",
                execution_time=execution_time
            )

        except NotFoundError as e:
            execution_time = time.time() - start_time
            return MCPToolResult(
                tool_name=tool_name,
                success=False,
                error="Task not found. It may have been deleted.",
                execution_time=execution_time
            )

        except APIError as e:
            execution_time = time.time() - start_time
            return MCPToolResult(
                tool_name=tool_name,
                success=False,
                error=str(e),
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return MCPToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Unexpected error: {str(e)}",
                execution_time=execution_time
            )

    async def _create_task(self, title: str, description: str = "") -> Dict[str, Any]:
        """Create a new task."""
        return await self.api_client.post("/api/tasks", {
            "title": title,
            "description": description
        })

    async def _list_tasks(
        self,
        completed: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List tasks with optional filtering."""
        params = {"limit": limit, "offset": offset}
        if completed is not None:
            params["completed"] = completed
        return await self.api_client.get("/api/tasks", params=params)

    async def _get_task(self, task_id: int) -> Dict[str, Any]:
        """Get a specific task by ID."""
        return await self.api_client.get(f"/api/tasks/{task_id}")

    async def _update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update a task."""
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if completed is not None:
            data["completed"] = completed

        return await self.api_client.patch(f"/api/tasks/{task_id}", data)

    async def _delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task."""
        await self.api_client.delete(f"/api/tasks/{task_id}")
        return {"success": True, "message": f"Task {task_id} deleted"}

    async def _toggle_complete(self, task_id: int) -> Dict[str, Any]:
        """Toggle task completion status."""
        return await self.api_client.patch(f"/api/tasks/{task_id}/complete")
