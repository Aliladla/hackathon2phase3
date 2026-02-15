"""Task management API endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlmodel import Session
from uuid import UUID
from datetime import datetime
from backend.database import get_session
from backend.api.dependencies import get_current_user
from backend.repositories.task_repository import TaskRepository
from backend.domain.task_manager import TaskManager
from backend.domain.exceptions import InvalidTaskDataError, TaskNotFoundError

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


# Request/Response Models
class CreateTaskRequest(BaseModel):
    """Create task request body."""
    title: str = Field(min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: str = Field(default="", max_length=1000, description="Optional description (0-1000 characters)")


class UpdateTaskRequest(BaseModel):
    """Update task request body (full update)."""
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = False


class PatchTaskRequest(BaseModel):
    """Patch task request body (partial update)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Task data in responses."""
    id: int
    user_id: UUID
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """Task list response with pagination info."""
    tasks: List[TaskResponse]
    total: int
    limit: int
    offset: int


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List all tasks for the authenticated user.

    - **completed**: Optional filter by completion status (true/false)
    - **limit**: Maximum tasks to return (1-1000, default 100)
    - **offset**: Number of tasks to skip for pagination (default 0)

    Returns list of tasks with pagination info.
    """
    task_repo = TaskRepository(session)
    task_manager = TaskManager(task_repo)

    # Get tasks
    tasks = task_manager.list_tasks(user_id, completed, limit, offset)

    # Get total count
    total = task_manager.count_tasks(user_id, completed)

    return TaskListResponse(
        tasks=[
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ],
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Returns 404 if task not found or belongs to another user.
    """
    task_repo = TaskRepository(session)
    task_manager = TaskManager(task_repo)

    try:
        task = task_manager.get_task(task_id, user_id)
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    - **title**: Task title (1-200 characters, required)
    - **description**: Optional description (0-1000 characters)

    Returns created task.
    """
    task_repo = TaskRepository(session)
    task_manager = TaskManager(task_repo)

    try:
        task = task_manager.create_task(user_id, request.title, request.description)
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except InvalidTaskDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a task (full update).

    - **title**: New task title (1-200 characters, required)
    - **description**: New description (0-1000 characters)
    - **completed**: New completion status

    Returns updated task. Returns 404 if task not found or belongs to another user.
    """
    task_repo = TaskRepository(session)
    task_manager = TaskManager(task_repo)

    try:
        task = task_manager.update_task(
            task_id,
            user_id,
            title=request.title,
            description=request.description,
            completed=request.completed
        )
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    except InvalidTaskDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{task_id}", response_model=TaskResponse)
async def patch_task(
    task_id: int,
    request: PatchTaskRequest,
    user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Partially update a task (only specified fields).

    - **title**: New task title (optional, 1-200 characters if provided)
    - **description**: New description (optional, 0-1000 characters if provided)
    - **completed**: New completion status (optional)

    Returns updated task. Returns 404 if task not found or belongs to another user.
    """
    task_repo = TaskRepository(session)
    task_manager = TaskManager(task_repo)

    try:
        task = task_manager.update_task(
            task_id,
            user_id,
            title=request.title,
            description=request.description,
            completed=request.completed
        )
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    except InvalidTaskDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    task_id: int,
    user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.

    Toggles between complete (true) and incomplete (false).
    Returns updated task. Returns 404 if task not found or belongs to another user.
    """
    task_repo = TaskRepository(session)
    task_manager = TaskManager(task_repo)

    try:
        task = task_manager.toggle_complete(task_id, user_id)
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.

    Returns 204 No Content on success.
    Returns 404 if task not found or belongs to another user.
    """
    task_repo = TaskRepository(session)
    task_manager = TaskManager(task_repo)

    try:
        task_manager.delete_task(task_id, user_id)
        return None
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
