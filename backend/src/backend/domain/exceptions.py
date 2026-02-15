"""Custom exceptions for the todo application (reused from Phase 1)."""


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


class UserNotFoundError(TodoError):
    """Raised when user ID does not exist."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User not found (ID: {user_id})")


class EmailAlreadyExistsError(TodoError):
    """Raised when email is already registered."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email already registered: {email}")


class InvalidCredentialsError(TodoError):
    """Raised when authentication credentials are invalid."""

    def __init__(self):
        super().__init__("Invalid email or password")
