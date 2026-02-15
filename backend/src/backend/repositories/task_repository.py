"""Task repository for database operations with user filtering."""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import Session, select
from backend.models.task import Task


class TaskRepository:
    """Repository for Task entity operations with user isolation."""

    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session

    def create(self, user_id: UUID, title: str, description: str = "") -> Task:
        """
        Create a new task for a user.

        Args:
            user_id: Owner's user ID
            title: Task title (1-200 characters)
            description: Optional task description (0-1000 characters)

        Returns:
            Created Task entity
        """
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip(),
            completed=False,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_by_id(self, task_id: int, user_id: UUID) -> Optional[Task]:
        """
        Get task by ID (user-filtered for security).

        Args:
            task_id: Task ID
            user_id: Owner's user ID

        Returns:
            Task entity if found and owned by user, None otherwise
        """
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        return self.session.exec(statement).first()

    def list_all(
        self,
        user_id: UUID,
        completed: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Task]:
        """
        List all tasks for a user with optional filtering.

        Args:
            user_id: Owner's user ID
            completed: Optional filter by completion status
            limit: Maximum tasks to return (1-1000)
            offset: Number of tasks to skip (pagination)

        Returns:
            List of Task entities
        """
        statement = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            statement = statement.where(Task.completed == completed)

        statement = statement.offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def count(self, user_id: UUID, completed: Optional[bool] = None) -> int:
        """
        Count tasks for a user.

        Args:
            user_id: Owner's user ID
            completed: Optional filter by completion status

        Returns:
            Number of tasks
        """
        statement = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            statement = statement.where(Task.completed == completed)

        return len(list(self.session.exec(statement).all()))

    def update(
        self,
        task_id: int,
        user_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Task]:
        """
        Update task fields (user-filtered for security).

        Args:
            task_id: Task ID
            user_id: Owner's user ID
            title: New title (if provided)
            description: New description (if provided)
            completed: New completion status (if provided)

        Returns:
            Updated Task entity if found and owned by user, None otherwise
        """
        task = self.get_by_id(task_id, user_id)
        if task is None:
            return None

        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        if completed is not None:
            task.completed = completed

        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def toggle_complete(self, task_id: int, user_id: UUID) -> Optional[Task]:
        """
        Toggle task completion status (user-filtered for security).

        Args:
            task_id: Task ID
            user_id: Owner's user ID

        Returns:
            Updated Task entity if found and owned by user, None otherwise
        """
        task = self.get_by_id(task_id, user_id)
        if task is None:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int, user_id: UUID) -> bool:
        """
        Delete task (user-filtered for security).

        Args:
            task_id: Task ID
            user_id: Owner's user ID

        Returns:
            True if task was deleted, False if not found or not owned by user
        """
        task = self.get_by_id(task_id, user_id)
        if task is None:
            return False

        self.session.delete(task)
        self.session.commit()
        return True
