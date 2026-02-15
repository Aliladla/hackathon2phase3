"""In-memory repository for task storage."""
from typing import List, Optional, Dict
from datetime import datetime
from ..domain.task import Task
from ..domain.exceptions import TaskNotFoundError


class MemoryRepository:
    """In-memory storage for tasks."""

    def __init__(self):
        """Initialize empty storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task with auto-assigned ID."""
        task_id = self._next_id
        self._next_id += 1

        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now()
        )
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by its ID."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks, ordered by creation time."""
        return sorted(self._tasks.values(), key=lambda t: t.created_at)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        old_task = self._tasks[task_id]
        new_title = title if title is not None else old_task.title
        new_description = description if description is not None else old_task.description

        updated_task = Task(
            id=old_task.id,
            title=new_title,
            description=new_description,
            completed=old_task.completed,
            created_at=old_task.created_at
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        old_task = self._tasks[task_id]
        updated_task = Task(
            id=old_task.id,
            title=old_task.title,
            description=old_task.description,
            completed=True,
            created_at=old_task.created_at
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        old_task = self._tasks[task_id]
        updated_task = Task(
            id=old_task.id,
            title=old_task.title,
            description=old_task.description,
            completed=False,
            created_at=old_task.created_at
        )
        self._tasks[task_id] = updated_task
        return updated_task
