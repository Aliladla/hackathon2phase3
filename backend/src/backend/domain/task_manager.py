"""Task manager business logic (adapted from Phase 1 for multi-user support)."""
from uuid import UUID
from typing import List, Optional
from backend.domain.task import TaskEntity
from backend.domain.exceptions import InvalidTaskDataError, TaskNotFoundError
from backend.repositories.task_repository import TaskRepository


class TaskManager:
    """
    Business logic for task management operations (reused from Phase 1).

    All operations now require user_id for multi-user support.
    """

    def __init__(self, repository: TaskRepository):
        """Initialize task manager with repository."""
        self.repository = repository

    def create_task(
        self,
        user_id: UUID,
        title: str,
        description: str = ""
    ) -> TaskEntity:
        """
        Create a new task for a user.

        Args:
            user_id: Owner's user ID
            title: Task title (1-200 characters)
            description: Optional task description (0-1000 characters)

        Returns:
            Created TaskEntity

        Raises:
            InvalidTaskDataError: If validation fails
        """
        # Validate inputs (reuse Phase 1 validation)
        TaskEntity.validate_title_string(title)
        TaskEntity.validate_description_string(description)

        # Create task in database
        task = self.repository.create(user_id, title, description)

        # Return as domain entity
        return TaskEntity(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    def get_task(self, task_id: int, user_id: UUID) -> TaskEntity:
        """
        Get a task by ID (user-filtered).

        Args:
            task_id: Task ID
            user_id: Owner's user ID

        Returns:
            TaskEntity

        Raises:
            TaskNotFoundError: If task not found or not owned by user
        """
        task = self.repository.get_by_id(task_id, user_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        return TaskEntity(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    def list_tasks(
        self,
        user_id: UUID,
        completed: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[TaskEntity]:
        """
        List all tasks for a user.

        Args:
            user_id: Owner's user ID
            completed: Optional filter by completion status
            limit: Maximum tasks to return
            offset: Number of tasks to skip

        Returns:
            List of TaskEntity objects
        """
        tasks = self.repository.list_all(user_id, completed, limit, offset)
        return [
            TaskEntity(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            for task in tasks
        ]

    def update_task(
        self,
        task_id: int,
        user_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> TaskEntity:
        """
        Update task fields (user-filtered).

        Args:
            task_id: Task ID
            user_id: Owner's user ID
            title: New title (if provided)
            description: New description (if provided)
            completed: New completion status (if provided)

        Returns:
            Updated TaskEntity

        Raises:
            TaskNotFoundError: If task not found or not owned by user
            InvalidTaskDataError: If validation fails
        """
        # Validate inputs if provided
        if title is not None:
            TaskEntity.validate_title_string(title)
        if description is not None:
            TaskEntity.validate_description_string(description)

        # Update task in database
        task = self.repository.update(task_id, user_id, title, description, completed)
        if task is None:
            raise TaskNotFoundError(task_id)

        return TaskEntity(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    def toggle_complete(self, task_id: int, user_id: UUID) -> TaskEntity:
        """
        Toggle task completion status (user-filtered).

        Args:
            task_id: Task ID
            user_id: Owner's user ID

        Returns:
            Updated TaskEntity

        Raises:
            TaskNotFoundError: If task not found or not owned by user
        """
        task = self.repository.toggle_complete(task_id, user_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        return TaskEntity(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    def delete_task(self, task_id: int, user_id: UUID) -> None:
        """
        Delete a task (user-filtered).

        Args:
            task_id: Task ID
            user_id: Owner's user ID

        Raises:
            TaskNotFoundError: If task not found or not owned by user
        """
        success = self.repository.delete(task_id, user_id)
        if not success:
            raise TaskNotFoundError(task_id)

    def count_tasks(
        self,
        user_id: UUID,
        completed: Optional[bool] = None
    ) -> int:
        """
        Count tasks for a user.

        Args:
            user_id: Owner's user ID
            completed: Optional filter by completion status

        Returns:
            Number of tasks
        """
        return self.repository.count(user_id, completed)
