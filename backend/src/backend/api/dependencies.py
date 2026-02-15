"""API dependencies for dependency injection."""
from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException, status, Header
from sqlmodel import Session
from backend.database import get_session
from backend.utils.jwt import extract_user_id


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    session: Session = Depends(get_session)
) -> UUID:
    """
    Extract and validate current user from JWT token.

    Args:
        authorization: Authorization header with Bearer token
        session: Database session

    Returns:
        User UUID from validated token

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]

    # Extract user_id from token
    user_id = extract_user_id(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
