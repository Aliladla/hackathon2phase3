"""Custom exceptions for the todo application."""


class TodoError(Exception):
    """Base exception for all todo application errors."""
    pass


class InvalidTaskDataError(TodoError):
    """Raised when task data fails validation."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TaskNotFoundError(TodoError):
    """Raised when task ID does not exist."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task not found (ID: {task_id})")
