"""Task manager - business logic for task operations."""
from typing import List, Optional
from datetime import datetime
from .task import Task
from .exceptions import InvalidTaskDataError, TaskNotFoundError


class TaskManager:
    """Manages task operations using a repository."""

    def __init__(self, repository):
        """Initialize with a repository."""
        self._repository = repository

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task with auto-assigned ID."""
        # Validate title
        if not title or not title.strip():
            raise InvalidTaskDataError("Title cannot be empty")
        if len(title) > 200:
            raise InvalidTaskDataError("Title too long (max 200 characters)")

        # Validate description
        if len(description) > 1000:
            raise InvalidTaskDataError("Description too long (max 1000 characters)")

        return self._repository.create_task(title.strip(), description)

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by its ID."""
        return self._repository.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        return self._repository.get_all_tasks()

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description."""
        if title is not None:
            if not title or not title.strip():
                raise InvalidTaskDataError("Title cannot be empty")
            if len(title) > 200:
                raise InvalidTaskDataError("Title too long (max 200 characters)")
            title = title.strip()

        if description is not None and len(description) > 1000:
            raise InvalidTaskDataError("Description too long (max 1000 characters)")

        return self._repository.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID."""
        self._repository.delete_task(task_id)

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete."""
        return self._repository.mark_complete(task_id)

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete."""
        return self._repository.mark_incomplete(task_id)
