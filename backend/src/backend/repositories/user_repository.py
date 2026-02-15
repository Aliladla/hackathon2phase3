"""User repository for database operations."""
from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from backend.models.user import User


class UserRepository:
    """Repository for User entity operations."""

    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session

    def create(self, email: str, password_hash: str) -> User:
        """
        Create a new user account.

        Args:
            email: User's email address (unique)
            password_hash: Bcrypt-hashed password

        Returns:
            Created User entity
        """
        user = User(email=email.lower(), password_hash=password_hash)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            User entity if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email (case-insensitive).

        Args:
            email: User's email address

        Returns:
            User entity if found, None otherwise
        """
        statement = select(User).where(User.email == email.lower())
        return self.session.exec(statement).first()

    def exists_by_email(self, email: str) -> bool:
        """
        Check if email is already registered.

        Args:
            email: Email address to check

        Returns:
            True if email exists, False otherwise
        """
        return self.get_by_email(email) is not None
