"""Entry point for the todo console application."""
from .storage.memory_repository import MemoryRepository
from .domain.task_manager import TaskManager
from .cli.menu import TodoMenu


def main():
    """Main entry point."""
    # Initialize components
    repository = MemoryRepository()
    task_manager = TaskManager(repository)
    menu = TodoMenu(task_manager)

    # Run the application
    try:
        menu.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}\n")


if __name__ == "__main__":
    main()
