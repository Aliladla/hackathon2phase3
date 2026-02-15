"""FastAPI server for chatbot REST API."""
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from chatbot.agent import TodoAgent
from chatbot.conversation import SessionStore, ConversationContext
from chatbot.config import settings


app = FastAPI(
    title="Todo Chatbot API",
    description="Natural language task management chatbot",
    version="1.0.0"
)

# Global session store
session_store = SessionStore()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User message", min_length=1)
    session_id: Optional[UUID] = Field(None, description="Session ID for continuing conversation")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Agent's response")
    session_id: UUID = Field(..., description="Session ID for this conversation")


class SessionResponse(BaseModel):
    """Response model for session creation."""
    session_id: UUID = Field(..., description="New session ID")
    message: str = Field(..., description="Success message")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Todo Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "backend_url": settings.BACKEND_API_URL,
        "model": settings.OPENAI_MODEL
    }


@app.post("/sessions", response_model=SessionResponse)
async def create_session():
    """
    Create a new conversation session.

    Returns:
        SessionResponse with new session ID
    """
    context = session_store.create_session()

    return SessionResponse(
        session_id=context.session_id,
        message="Session created successfully"
    )


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: UUID):
    """
    Delete a conversation session.

    Args:
        session_id: Session ID to delete

    Returns:
        Success message
    """
    session_store.delete_session(session_id)

    return {
        "message": f"Session {session_id} deleted successfully"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    authorization: str = Header(..., description="Bearer JWT token")
):
    """
    Process a chat message.

    Args:
        request: Chat request with message and optional session_id
        authorization: JWT token in Authorization header (Bearer token)

    Returns:
        ChatResponse with agent's response and session ID

    Raises:
        HTTPException: If session not found or authentication fails
    """
    # Extract JWT token from Authorization header
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Expected 'Bearer <token>'"
        )

    jwt_token = authorization.replace("Bearer ", "").strip()

    if not jwt_token:
        raise HTTPException(
            status_code=401,
            detail="JWT token is required"
        )

    # Get or create session
    if request.session_id:
        context = session_store.get_session(request.session_id)
        if not context:
            raise HTTPException(
                status_code=404,
                detail=f"Session {request.session_id} not found or expired"
            )
    else:
        context = session_store.create_session()

    # Initialize agent
    agent = TodoAgent(jwt_token=jwt_token, context=context)

    try:
        # Process message
        response = await agent.process_message(request.message)

        # Update session in store
        session_store.update_session(context)

        return ChatResponse(
            response=response,
            session_id=context.session_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )


@app.get("/sessions/{session_id}/context")
async def get_session_context(session_id: UUID):
    """
    Get conversation context for a session.

    Args:
        session_id: Session ID

    Returns:
        Session context information

    Raises:
        HTTPException: If session not found
    """
    context = session_store.get_session(session_id)

    if not context:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found or expired"
        )

    return {
        "session_id": context.session_id,
        "message_count": len(context.messages),
        "last_task_id": context.last_task_id,
        "last_operation": context.last_operation,
        "created_at": context.created_at.isoformat(),
        "updated_at": context.updated_at.isoformat(),
        "expires_at": context.expires_at.isoformat()
    }


@app.post("/sessions/cleanup")
async def cleanup_expired_sessions():
    """
    Clean up expired sessions.

    Returns:
        Success message
    """
    session_store.cleanup_expired()

    return {
        "message": "Expired sessions cleaned up successfully"
    }


if __name__ == "__main__":
    import uvicorn

    port = settings.CHATBOT_PORT

    print(f"Starting Todo Chatbot API on port {port}...")
    print(f"Backend API: {settings.BACKEND_API_URL}")
    print(f"OpenAI Model: {settings.OPENAI_MODEL}")

    uvicorn.run(
        "chatbot.server.app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
