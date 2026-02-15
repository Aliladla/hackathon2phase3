"""API client for Phase 2 backend communication."""
import httpx
from typing import Optional, Dict, Any
from chatbot.config import settings


class APIClient:
    """Async HTTP client for Phase 2 backend API."""

    def __init__(self, jwt_token: str):
        """
        Initialize API client with JWT token.

        Args:
            jwt_token: JWT authentication token from Phase 2
        """
        self.base_url = settings.BACKEND_API_URL
        self.jwt_token = jwt_token
        self.timeout = settings.BACKEND_API_TIMEOUT
        self.headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make GET request to backend API.

        Args:
            endpoint: API endpoint (e.g., "/api/tasks")
            params: Optional query parameters

        Returns:
            Response data as dictionary

        Raises:
            APIError: If request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                params=params,
                headers=self.headers
            )
            self._handle_response(response)
            return response.json()

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make POST request to backend API.

        Args:
            endpoint: API endpoint
            data: Request body data

        Returns:
            Response data as dictionary
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}{endpoint}",
                json=data,
                headers=self.headers
            )
            self._handle_response(response)
            return response.json()

    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make PUT request to backend API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.put(
                f"{self.base_url}{endpoint}",
                json=data,
                headers=self.headers
            )
            self._handle_response(response)
            return response.json()

    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PATCH request to backend API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.patch(
                f"{self.base_url}{endpoint}",
                json=data,
                headers=self.headers
            )
            self._handle_response(response)
            return response.json()

    async def delete(self, endpoint: str) -> None:
        """Make DELETE request to backend API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(
                f"{self.base_url}{endpoint}",
                headers=self.headers
            )
            self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> None:
        """
        Handle API response and raise appropriate errors.

        Args:
            response: HTTP response object

        Raises:
            AuthenticationError: If authentication fails (401)
            NotFoundError: If resource not found (404)
            APIError: For other errors
        """
        if response.status_code == 401:
            raise AuthenticationError("Authentication failed. Token may be expired.")
        elif response.status_code == 404:
            raise NotFoundError("Resource not found")
        elif response.status_code >= 400:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except:
                error_detail = response.text
            raise APIError(f"API error ({response.status_code}): {error_detail}")


class APIError(Exception):
    """Base exception for API errors."""
    pass


class AuthenticationError(APIError):
    """Raised when authentication fails."""
    pass


class NotFoundError(APIError):
    """Raised when resource is not found."""
    pass
