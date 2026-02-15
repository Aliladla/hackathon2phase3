"""JWT token utilities using python-jose."""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from uuid import UUID
from backend.config import settings


def create_token(user_id: UUID, email: str) -> tuple[str, datetime]:
    """
    Create a JWT token for a user.

    Args:
        user_id: User's unique identifier
        email: User's email address

    Returns:
        Tuple of (token string, expiration datetime)
    """
    expires_at = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRATION_DAYS)

    payload = {
        "user_id": str(user_id),
        "email": email,
        "exp": expires_at,
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, expires_at


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded payload dict if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def extract_user_id(token: str) -> Optional[UUID]:
    """
    Extract user_id from a JWT token.

    Args:
        token: JWT token string

    Returns:
        User UUID if token is valid, None otherwise
    """
    payload = decode_token(token)
    if payload is None:
        return None

    try:
        user_id = UUID(payload.get("user_id"))
        return user_id
    except (ValueError, TypeError):
        return None
