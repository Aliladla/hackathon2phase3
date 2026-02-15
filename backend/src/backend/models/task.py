"""Task database model."""
from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """Task entity for todo items with user ownership."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="")
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2025-02-15T10:30:00Z",
                "updated_at": "2025-02-15T10:30:00Z",
            }
        }
