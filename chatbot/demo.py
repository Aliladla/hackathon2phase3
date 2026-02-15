"""Demo script showcasing chatbot capabilities.

This script demonstrates the chatbot's natural language understanding
and task management capabilities with a pre-scripted conversation.

Usage:
    python demo.py --jwt-token YOUR_JWT_TOKEN
"""
import asyncio
import sys
from chatbot.agent import TodoAgent
from chatbot.conversation import ConversationContext
from chatbot.config import settings


async def run_demo(jwt_token: str):
    """
    Run a demonstration conversation with the chatbot.

    Args:
        jwt_token: JWT token for Phase 2 backend authentication
    """
    print("\n" + "=" * 70)
    print("🤖 Todo Chatbot Demo - Natural Language Task Management")
    print("=" * 70)
    print(f"\n📡 Backend: {settings.BACKEND_API_URL}")
    print(f"🤖 Model: {settings.OPENAI_MODEL}")
    print("\n" + "=" * 70 + "\n")

    # Create conversation context and agent
    context = ConversationContext()
    agent = TodoAgent(jwt_token=jwt_token, context=context)

    # Demo conversation script
    demo_messages = [
        ("Hello!", "Greeting the chatbot"),
        ("Add a task to buy groceries", "Creating first task"),
        ("Also add a task to call dentist", "Creating second task"),
        ("And one more: pay electricity bill", "Creating third task"),
        ("Show me my tasks", "Listing all tasks"),
        ("Mark task 1 as complete", "Completing first task"),
        ("Update task 2 description to Schedule cleaning appointment", "Updating task"),
        ("What are my incomplete tasks?", "Filtering tasks"),
        ("Delete task 3", "Deleting a task"),
        ("Show me all my tasks again", "Final task list"),
    ]

    for i, (message, description) in enumerate(demo_messages, 1):
        print(f"\n{'─' * 70}")
        print(f"Step {i}: {description}")
        print(f"{'─' * 70}")
        print(f"\n👤 User: {message}")
        print("\n🤖 Assistant: ", end="", flush=True)

        try:
            response = await agent.process_message(message)
            print(response)

            # Show context info
            if context.last_task_id:
                print(f"\n   📝 Context: Last task ID = {context.last_task_id}, "
                      f"Operation = {context.last_operation}")

            # Pause between messages for readability
            await asyncio.sleep(1)

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            break

    # Summary
    print("\n" + "=" * 70)
    print("📊 Demo Summary")
    print("=" * 70)
    print(f"Total messages exchanged: {len(context.messages)}")
    print(f"Session ID: {context.session_id}")
    print(f"Session expires at: {context.expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n✅ Demo completed successfully!")
    print("=" * 70 + "\n")


async def main():
    """Main entry point for demo script."""
    # Check for JWT token
    if len(sys.argv) < 2 or not sys.argv[1].startswith("--jwt-token="):
        print("\n❌ Error: JWT token required")
        print("\nUsage:")
        print("  python demo.py --jwt-token=YOUR_JWT_TOKEN")
        print("\nGet a JWT token by signing in to Phase 2 backend:")
        print("  curl -X POST http://localhost:8000/api/auth/signin \\")
        print("    -H 'Content-Type: application/json' \\")
        print("    -d '{\"email\": \"user@example.com\", \"password\": \"password\"}'")
        print()
        sys.exit(1)

    jwt_token = sys.argv[1].split("=", 1)[1]

    # Validate configuration
    if not settings.OPENAI_API_KEY:
        print("\n❌ Error: OPENAI_API_KEY environment variable is required")
        print("Set it in your .env file or environment")
        sys.exit(1)

    if not settings.BACKEND_API_URL:
        print("\n❌ Error: BACKEND_API_URL environment variable is required")
        print("Set it in your .env file or environment")
        sys.exit(1)

    # Run demo
    try:
        await run_demo(jwt_token)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
