"""Configuration management for the chatbot service."""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Chatbot settings loaded from environment variables."""

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    # Phase 2 Backend Configuration
    BACKEND_API_URL: str = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    BACKEND_API_TIMEOUT: int = int(os.getenv("BACKEND_API_TIMEOUT", "30"))

    # Chatbot Configuration
    CHATBOT_PORT: int = int(os.getenv("CHATBOT_PORT", "8001"))
    CHATBOT_DEBUG: bool = os.getenv("CHATBOT_DEBUG", "False").lower() == "true"
    MAX_CONTEXT_MESSAGES: int = int(os.getenv("MAX_CONTEXT_MESSAGES", "10"))
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))

    def validate(self) -> None:
        """Validate required configuration values."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not self.OPENAI_API_KEY.startswith("sk-"):
            raise ValueError("OPENAI_API_KEY must start with 'sk-'")
        if not self.BACKEND_API_URL:
            raise ValueError("BACKEND_API_URL environment variable is required")


# Global settings instance
settings = Settings()
