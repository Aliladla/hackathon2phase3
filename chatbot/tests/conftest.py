"""Test configuration and shared fixtures."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from chatbot.api.client import APIClient
from chatbot.conversation import ConversationContext, SessionStore
from chatbot.mcp.executor import MCPToolExecutor


@pytest.fixture
def mock_jwt_token():
    """Fixture for mock JWT token."""
    return "mock_jwt_token_12345"


@pytest.fixture
def mock_api_client(mock_jwt_token):
    """Fixture for mock API client."""
    client = AsyncMock(spec=APIClient)
    client.jwt_token = mock_jwt_token
    client.base_url = "http://localhost:8000"
    return client


@pytest.fixture
def conversation_context():
    """Fixture for conversation context."""
    return ConversationContext()


@pytest.fixture
def session_store():
    """Fixture for session store."""
    return SessionStore()


@pytest.fixture
def mcp_executor(mock_api_client):
    """Fixture for MCP tool executor."""
    return MCPToolExecutor(api_client=mock_api_client)


@pytest.fixture
def mock_openai_client():
    """Fixture for mock OpenAI client."""
    client = AsyncMock()

    # Mock chat completion response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mock response"
    mock_response.choices[0].message.tool_calls = None

    client.chat.completions.create = AsyncMock(return_value=mock_response)

    return client


@pytest.fixture
def sample_task():
    """Fixture for sample task data."""
    return {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": False,
        "user_id": str(uuid4()),
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
    }


@pytest.fixture
def sample_task_list():
    """Fixture for sample task list."""
    return {
        "tasks": [
            {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "user_id": str(uuid4()),
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            },
            {
                "id": 2,
                "title": "Call dentist",
                "description": "Schedule appointment",
                "completed": True,
                "user_id": str(uuid4()),
                "created_at": "2024-01-14T09:00:00Z",
                "updated_at": "2024-01-15T11:00:00Z"
            }
        ],
        "total": 2,
        "limit": 100,
        "offset": 0
    }
