"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session
from uuid import UUID
from datetime import datetime
from backend.database import get_session
from backend.repositories.user_repository import UserRepository
from backend.utils.password import hash_password, verify_password
from backend.utils.jwt import create_token
from backend.domain.exceptions import EmailAlreadyExistsError, InvalidCredentialsError

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# Request/Response Models
class SignUpRequest(BaseModel):
    """Sign up request body."""
    email: EmailStr
    password: str = Field(min_length=8, description="Minimum 8 characters")


class SignInRequest(BaseModel):
    """Sign in request body."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User data in responses."""
    id: UUID
    email: str
    created_at: datetime


class AuthResponse(BaseModel):
    """Authentication response with user and token."""
    user: UserResponse
    token: str
    expires_at: datetime


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignUpRequest,
    session: Session = Depends(get_session)
):
    """
    Create a new user account.

    - **email**: Valid email address (unique)
    - **password**: Minimum 8 characters

    Returns user data and JWT token.
    """
    user_repo = UserRepository(session)

    # Check if email already exists
    if user_repo.exists_by_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    password_hash = hash_password(request.password)

    # Create user
    user = user_repo.create(request.email, password_hash)

    # Generate JWT token
    token, expires_at = create_token(user.id, user.email)

    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        ),
        token=token,
        expires_at=expires_at
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    request: SignInRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate existing user and issue JWT token.

    - **email**: Registered email address
    - **password**: User's password

    Returns user data and JWT token.
    """
    user_repo = UserRepository(session)

    # Get user by email
    user = user_repo.get_by_email(request.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token, expires_at = create_token(user.id, user.email)

    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        ),
        token=token,
        expires_at=expires_at
    )


@router.post("/signout", response_model=MessageResponse)
async def signout():
    """
    Sign out current user.

    Note: This is a client-side operation. The JWT token should be
    deleted from client storage. The token remains valid until expiration.
    """
    return MessageResponse(message="Signed out successfully")
