"""Task entity - core domain model."""
from dataclasses import dataclass
from datetime import datetime
from .exceptions import InvalidTaskDataError


@dataclass(frozen=True)
class Task:
    """Immutable task entity."""
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    def __post_init__(self):
        """Validate task data after initialization."""
        # Validate ID
        if self.id <= 0:
            raise InvalidTaskDataError("Task ID must be positive")

        # Validate title
        if not self.title or not self.title.strip():
            raise InvalidTaskDataError("Title cannot be empty")
        if len(self.title) > 200:
            raise InvalidTaskDataError("Title too long (max 200 characters)")

        # Validate description
        if len(self.description) > 1000:
            raise InvalidTaskDataError("Description too long (max 1000 characters)")
