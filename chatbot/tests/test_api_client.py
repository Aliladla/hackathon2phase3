"""Unit tests for API client."""
import pytest
from unittest.mock import AsyncMock, patch
from httpx import Response, HTTPStatusError, Request
from chatbot.api.client import APIClient, APIError, AuthenticationError, NotFoundError


@pytest.mark.asyncio
async def test_api_client_initialization(mock_jwt_token):
    """Test API client initialization."""
    client = APIClient(jwt_token=mock_jwt_token)

    assert client.jwt_token == mock_jwt_token
    assert client.base_url == "http://localhost:8000"
    assert "Authorization" in client.headers
    assert client.headers["Authorization"] == f"Bearer {mock_jwt_token}"
    assert client.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_get_request_success(mock_jwt_token):
    """Test successful GET request."""
    client = APIClient(jwt_token=mock_jwt_token)

    mock_response_data = {"id": 1, "title": "Test task"}

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = Response(
            status_code=200,
            json=mock_response_data,
            request=Request("GET", "http://localhost:8000/api/tasks/1")
        )
        mock_get.return_value = mock_response

        result = await client.get("/api/tasks/1")

        assert result == mock_response_data
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_post_request_success(mock_jwt_token):
    """Test successful POST request."""
    client = APIClient(jwt_token=mock_jwt_token)

    request_data = {"title": "New task", "description": "Test description"}
    mock_response_data = {"id": 1, **request_data}

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = Response(
            status_code=201,
            json=mock_response_data,
            request=Request("POST", "http://localhost:8000/api/tasks")
        )
        mock_post.return_value = mock_response

        result = await client.post("/api/tasks", data=request_data)

        assert result == mock_response_data
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_patch_request_success(mock_jwt_token):
    """Test successful PATCH request."""
    client = APIClient(jwt_token=mock_jwt_token)

    request_data = {"title": "Updated task"}
    mock_response_data = {"id": 1, "title": "Updated task"}

    with patch("httpx.AsyncClient.patch") as mock_patch:
        mock_response = Response(
            status_code=200,
            json=mock_response_data,
            request=Request("PATCH", "http://localhost:8000/api/tasks/1")
        )
        mock_patch.return_value = mock_response

        result = await client.patch("/api/tasks/1", data=request_data)

        assert result == mock_response_data
        mock_patch.assert_called_once()


@pytest.mark.asyncio
async def test_delete_request_success(mock_jwt_token):
    """Test successful DELETE request."""
    client = APIClient(jwt_token=mock_jwt_token)

    with patch("httpx.AsyncClient.delete") as mock_delete:
        mock_response = Response(
            status_code=204,
            request=Request("DELETE", "http://localhost:8000/api/tasks/1")
        )
        mock_delete.return_value = mock_response

        await client.delete("/api/tasks/1")

        mock_delete.assert_called_once()


@pytest.mark.asyncio
async def test_authentication_error(mock_jwt_token):
    """Test authentication error handling."""
    client = APIClient(jwt_token=mock_jwt_token)

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = Response(
            status_code=401,
            json={"detail": "Unauthorized"},
            request=Request("GET", "http://localhost:8000/api/tasks")
        )
        mock_get.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            await client.get("/api/tasks")

        assert "Authentication failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_not_found_error(mock_jwt_token):
    """Test not found error handling."""
    client = APIClient(jwt_token=mock_jwt_token)

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = Response(
            status_code=404,
            json={"detail": "Task not found"},
            request=Request("GET", "http://localhost:8000/api/tasks/999")
        )
        mock_get.return_value = mock_response

        with pytest.raises(NotFoundError) as exc_info:
            await client.get("/api/tasks/999")

        assert "Resource not found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_server_error(mock_jwt_token):
    """Test server error handling."""
    client = APIClient(jwt_token=mock_jwt_token)

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = Response(
            status_code=500,
            json={"detail": "Internal server error"},
            request=Request("GET", "http://localhost:8000/api/tasks")
        )
        mock_get.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            await client.get("/api/tasks")

        assert "API request failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_with_params(mock_jwt_token):
    """Test GET request with query parameters."""
    client = APIClient(jwt_token=mock_jwt_token)

    mock_response_data = {"tasks": [], "total": 0}

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = Response(
            status_code=200,
            json=mock_response_data,
            request=Request("GET", "http://localhost:8000/api/tasks")
        )
        mock_get.return_value = mock_response

        result = await client.get("/api/tasks", params={"completed": True, "limit": 10})

        assert result == mock_response_data
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args.kwargs["params"] == {"completed": True, "limit": 10}
