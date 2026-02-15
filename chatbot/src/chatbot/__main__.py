"""Interactive console interface for the Todo chatbot."""
import asyncio
import sys
from uuid import UUID
from chatbot.agent import TodoAgent
from chatbot.conversation import ConversationContext, SessionStore
from chatbot.config import settings


class ConsoleInterface:
    """Interactive console interface for chatbot."""

    def __init__(self):
        """Initialize the console interface."""
        self.session_store = SessionStore()
        self.current_context: ConversationContext | None = None
        self.agent: TodoAgent | None = None

    def print_welcome(self) -> None:
        """Print welcome message."""
        print("\n" + "=" * 60)
        print("🤖 Todo Chatbot - Natural Language Task Management")
        print("=" * 60)
        print("\nWelcome! I can help you manage your tasks using natural language.")
        print("\nExamples:")
        print("  - 'Add a task to buy groceries'")
        print("  - 'Show me my tasks'")
        print("  - 'Mark task 5 as complete'")
        print("  - 'Update task 3 title to Buy milk and eggs'")
        print("  - 'Delete task 7'")
        print("\nType 'exit' or 'quit' to end the session.")
        print("=" * 60 + "\n")

    def get_jwt_token(self) -> str:
        """
        Prompt user for JWT token.

        Returns:
            JWT token string
        """
        print("Please provide your JWT token from Phase 2 backend.")
        print("(You can get this by signing in at the backend API)")
        print()

        token = input("JWT Token: ").strip()

        if not token:
            print("❌ Error: JWT token is required.")
            sys.exit(1)

        return token

    async def start_session(self, jwt_token: str) -> None:
        """
        Start a new conversation session.

        Args:
            jwt_token: JWT token for authentication
        """
        # Create conversation context
        self.current_context = self.session_store.create_session()

        # Initialize agent
        self.agent = TodoAgent(
            jwt_token=jwt_token,
            context=self.current_context
        )

        print(f"\n✅ Session started (ID: {self.current_context.session_id})")
        print(f"📡 Connected to backend: {settings.BACKEND_API_URL}")
        print(f"🤖 Using model: {settings.OPENAI_MODEL}\n")

    async def run_conversation_loop(self) -> None:
        """Run the main conversation loop."""
        if not self.agent or not self.current_context:
            print("❌ Error: Session not initialized.")
            return

        while True:
            try:
                # Check if session expired
                if self.current_context.is_expired():
                    print("\n⏰ Your session has expired. Please restart the chatbot.")
                    break

                # Get user input
                user_input = input("You: ").strip()

                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\n👋 Goodbye! Your tasks are saved in the backend.")
                    break

                # Skip empty input
                if not user_input:
                    continue

                # Process message with agent
                print("🤖 Assistant: ", end="", flush=True)
                response = await self.agent.process_message(user_input)
                print(response)
                print()

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'exit' to quit.\n")

    async def run(self) -> None:
        """Run the console interface."""
        self.print_welcome()

        # Get JWT token
        jwt_token = self.get_jwt_token()

        # Start session
        await self.start_session(jwt_token)

        # Run conversation loop
        await self.run_conversation_loop()

        # Cleanup
        if self.current_context:
            self.session_store.delete_session(self.current_context.session_id)


async def main() -> None:
    """Main entry point."""
    # Validate configuration
    if not settings.OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY environment variable is required.")
        print("Please set it in your .env file or environment.")
        sys.exit(1)

    if not settings.BACKEND_API_URL:
        print("❌ Error: BACKEND_API_URL environment variable is required.")
        print("Please set it in your .env file or environment.")
        sys.exit(1)

    # Run console interface
    interface = ConsoleInterface()
    await interface.run()


if __name__ == "__main__":
    asyncio.run(main())
