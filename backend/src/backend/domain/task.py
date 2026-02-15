"""Task entity with validation (adapted from Phase 1 for multi-user support)."""
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from backend.domain.exceptions import InvalidTaskDataError


@dataclass
class TaskEntity:
    """
    Task entity with validation rules (reused from Phase 1).

    Validation Rules:
    - Title: Required, 1-200 characters, no leading/trailing whitespace
    - Description: Optional, 0-1000 characters
    - User ID: Required (new in Phase 2)
    """

    id: int
    user_id: UUID
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        """Validate task data after initialization."""
        self._validate_title()
        self._validate_description()

    def _validate_title(self):
        """Validate title field."""
        if not self.title or not self.title.strip():
            raise InvalidTaskDataError("Title cannot be empty")

        if len(self.title) > 200:
            raise InvalidTaskDataError(
                f"Title too long ({len(self.title)} characters, max 200)"
            )

    def _validate_description(self):
        """Validate description field."""
        if len(self.description) > 1000:
            raise InvalidTaskDataError(
                f"Description too long ({len(self.description)} characters, max 1000)"
            )

    @staticmethod
    def validate_title_string(title: str) -> None:
        """
        Validate title string before creating task.

        Args:
            title: Title string to validate

        Raises:
            InvalidTaskDataError: If title is invalid
        """
        if not title or not title.strip():
            raise InvalidTaskDataError("Title cannot be empty")

        if len(title) > 200:
            raise InvalidTaskDataError(
                f"Title too long ({len(title)} characters, max 200)"
            )

    @staticmethod
    def validate_description_string(description: str) -> None:
        """
        Validate description string before creating task.

        Args:
            description: Description string to validate

        Raises:
            InvalidTaskDataError: If description is invalid
        """
        if len(description) > 1000:
            raise InvalidTaskDataError(
                f"Description too long ({len(description)} characters, max 1000)"
            )
