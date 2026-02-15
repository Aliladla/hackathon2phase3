#!/usr/bin/env python3
"""Quick start script for Phase 3 chatbot.

This script helps you get started with the chatbot by:
1. Checking prerequisites
2. Validating configuration
3. Testing connectivity
4. Running a sample conversation

Usage:
    python quickstart.py
"""
import asyncio
import sys
import os
from pathlib import Path


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("\n" + "=" * 70)
    print("🔍 Checking Prerequisites")
    print("=" * 70 + "\n")

    issues = []

    # Check Python version
    if sys.version_info < (3, 13):
        issues.append(f"❌ Python 3.13+ required (found {sys.version_info.major}.{sys.version_info.minor})")
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        issues.append("❌ .env file not found (copy from .env.example)")
    else:
        print("✅ .env file exists")

    # Check if dependencies are installed
    try:
        import openai
        print(f"✅ openai package installed (version {openai.__version__})")
    except ImportError:
        issues.append("❌ openai package not installed (run: uv sync)")

    try:
        import httpx
        print(f"✅ httpx package installed")
    except ImportError:
        issues.append("❌ httpx package not installed (run: uv sync)")

    try:
        import fastapi
        print(f"✅ fastapi package installed")
    except ImportError:
        issues.append("❌ fastapi package not installed (run: uv sync)")

    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key == "sk-your-openai-api-key-here":
        issues.append("❌ OPENAI_API_KEY not configured in .env")
    else:
        print(f"✅ OPENAI_API_KEY configured ({openai_key[:10]}...)")

    backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    print(f"✅ BACKEND_API_URL: {backend_url}")

    if issues:
        print("\n" + "=" * 70)
        print("⚠️  Issues Found:")
        print("=" * 70)
        for issue in issues:
            print(f"  {issue}")
        print("\n" + "=" * 70)
        return False

    print("\n✅ All prerequisites met!")
    return True


async def test_backend_connectivity():
    """Test connectivity to Phase 2 backend."""
    print("\n" + "=" * 70)
    print("🔌 Testing Backend Connectivity")
    print("=" * 70 + "\n")

    from dotenv import load_dotenv
    load_dotenv()

    backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")

    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{backend_url}/health", timeout=5.0)
            if response.status_code == 200:
                print(f"✅ Backend is reachable at {backend_url}")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"⚠️  Backend returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Cannot connect to backend at {backend_url}")
        print(f"   Error: {str(e)}")
        print("\n   Make sure Phase 2 backend is running:")
        print("   cd backend && uv run uvicorn app.main:app")
        return False


async def test_openai_connectivity():
    """Test connectivity to OpenAI API."""
    print("\n" + "=" * 70)
    print("🤖 Testing OpenAI API Connectivity")
    print("=" * 70 + "\n")

    from dotenv import load_dotenv
    load_dotenv()

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Simple test call
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10
        )

        print("✅ OpenAI API is accessible")
        print(f"   Model: gpt-3.5-turbo")
        print(f"   Response: {response.choices[0].message.content}")
        return True

    except Exception as e:
        print(f"❌ Cannot connect to OpenAI API")
        print(f"   Error: {str(e)}")
        print("\n   Check your OPENAI_API_KEY in .env file")
        return False


def get_jwt_token():
    """Prompt user for JWT token."""
    print("\n" + "=" * 70)
    print("🔑 JWT Token Required")
    print("=" * 70 + "\n")

    print("To use the chatbot, you need a JWT token from Phase 2 backend.")
    print("\nHow to get a JWT token:")
    print("1. Sign in to Phase 2 backend (http://localhost:8000)")
    print("2. Use the /api/auth/signin endpoint")
    print("3. Copy the JWT token from the response")
    print("\nExample:")
    print("  curl -X POST http://localhost:8000/api/auth/signin \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"email\": \"user@example.com\", \"password\": \"password\"}'")
    print()

    token = input("Enter your JWT token (or 'skip' to skip demo): ").strip()

    if token.lower() == "skip":
        return None

    if not token:
        print("❌ JWT token is required")
        return None

    return token


async def run_sample_conversation(jwt_token):
    """Run a sample conversation with the chatbot."""
    print("\n" + "=" * 70)
    print("💬 Running Sample Conversation")
    print("=" * 70 + "\n")

    try:
        from chatbot.agent import TodoAgent
        from chatbot.conversation import ConversationContext

        context = ConversationContext()
        agent = TodoAgent(jwt_token=jwt_token, context=context)

        # Sample messages
        messages = [
            "Hello!",
            "Add a task to test the chatbot",
            "Show me my tasks"
        ]

        for i, message in enumerate(messages, 1):
            print(f"\n[{i}] 👤 User: {message}")
            print(f"    🤖 Assistant: ", end="", flush=True)

            response = await agent.process_message(message)
            print(response)

            await asyncio.sleep(1)

        print("\n✅ Sample conversation completed successfully!")
        print(f"   Session ID: {context.session_id}")
        print(f"   Messages exchanged: {len(context.messages)}")

        return True

    except Exception as e:
        print(f"\n❌ Sample conversation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("🚀 Phase 3 Chatbot - Quick Start")
    print("=" * 70)

    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n⚠️  Please fix the issues above before continuing.")
        sys.exit(1)

    # Step 2: Test backend connectivity
    backend_ok = await test_backend_connectivity()

    # Step 3: Test OpenAI connectivity
    openai_ok = await test_openai_connectivity()

    if not backend_ok or not openai_ok:
        print("\n⚠️  Some connectivity tests failed.")
        print("You can still proceed, but the chatbot may not work correctly.")
        proceed = input("\nContinue anyway? (yes/no): ").strip().lower()
        if proceed not in ["yes", "y"]:
            sys.exit(1)

    # Step 4: Get JWT token and run sample conversation
    jwt_token = get_jwt_token()

    if jwt_token:
        success = await run_sample_conversation(jwt_token)

        if success:
            print("\n" + "=" * 70)
            print("🎉 Quick Start Complete!")
            print("=" * 70)
            print("\nNext steps:")
            print("1. Run interactive console: uv run python -m chatbot")
            print("2. Run REST API server: uv run uvicorn chatbot.server.app:app --reload")
            print("3. Run demo script: uv run python demo.py --jwt-token=YOUR_TOKEN")
            print("4. Run tests: uv run pytest")
            print()
        else:
            print("\n⚠️  Sample conversation failed. Check the error above.")
    else:
        print("\n" + "=" * 70)
        print("✅ Prerequisites Check Complete")
        print("=" * 70)
        print("\nYour environment is ready!")
        print("\nTo start using the chatbot:")
        print("1. Get a JWT token from Phase 2 backend")
        print("2. Run: uv run python -m chatbot")
        print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Quick start interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Quick start failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
