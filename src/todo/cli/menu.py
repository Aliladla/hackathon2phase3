"""CLI menu interface for the todo application."""
from ..domain.task_manager import TaskManager
from ..domain.exceptions import TodoError, InvalidTaskDataError, TaskNotFoundError
from .display import display_tasks, display_task_details, display_error, display_success


class TodoMenu:
    """Interactive CLI menu for todo operations."""

    def __init__(self, task_manager: TaskManager):
        """Initialize with a task manager."""
        self.task_manager = task_manager

    def run(self):
        """Run the main menu loop."""
        print("\n" + "=" * 40)
        print("  Welcome to Todo Console App - Phase 1")
        print("=" * 40)

        while True:
            self.display_menu()
            choice = input("Enter choice (1-6): ").strip()

            if choice == "1":
                self.view_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.toggle_completion()
            elif choice == "4":
                self.update_task()
            elif choice == "5":
                self.delete_task()
            elif choice == "6":
                print("\nGoodbye! All tasks will be lost (in-memory storage).\n")
                break
            else:
                display_error("Invalid choice. Please enter 1-6.")

    def display_menu(self):
        """Display the main menu."""
        print("\n=== Todo App ===")
        print("1. View all tasks")
        print("2. Add new task")
        print("3. Mark task complete/incomplete")
        print("4. Update task")
        print("5. Delete task")
        print("6. Exit")
        print()

    def view_tasks(self):
        """View all tasks."""
        try:
            tasks = self.task_manager.get_all_tasks()
            display_tasks(tasks)
        except TodoError as e:
            display_error(str(e))

    def add_task(self):
        """Add a new task."""
        try:
            print("\n--- Add New Task ---")
            title = input("Enter task title: ").strip()
            description = input("Enter description (optional, press Enter to skip): ").strip()

            task = self.task_manager.create_task(title, description)
            display_success("Task created successfully!")
            display_task_details(task)
        except InvalidTaskDataError as e:
            display_error(str(e))
        except TodoError as e:
            display_error(str(e))

    def toggle_completion(self):
        """Mark a task as complete or incomplete."""
        try:
            print("\n--- Mark Task Complete/Incomplete ---")
            task_id_str = input("Enter task ID: ").strip()

            if not task_id_str.isdigit():
                display_error("Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id_str)

            # Show current task
            task = self.task_manager.get_task(task_id)
            print(f"\nCurrent status: {'Complete' if task.completed else 'Incomplete'}")

            choice = input("Mark as (c)omplete or (i)ncomplete? ").strip().lower()

            if choice == "c":
                updated_task = self.task_manager.mark_complete(task_id)
                display_success("Task marked as complete!")
            elif choice == "i":
                updated_task = self.task_manager.mark_incomplete(task_id)
                display_success("Task marked as incomplete!")
            else:
                display_error("Invalid choice. Please enter 'c' or 'i'.")
                return

            display_task_details(updated_task)
        except TaskNotFoundError as e:
            display_error(str(e))
        except TodoError as e:
            display_error(str(e))

    def update_task(self):
        """Update a task's title or description."""
        try:
            print("\n--- Update Task ---")
            task_id_str = input("Enter task ID: ").strip()

            if not task_id_str.isdigit():
                display_error("Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id_str)

            # Show current task
            task = self.task_manager.get_task(task_id)
            print(f"\nCurrent title: {task.title}")
            print(f"Current description: {task.description if task.description else '(none)'}")

            new_title = input("\nNew title (press Enter to keep current): ").strip()
            new_description = input("New description (press Enter to keep current): ").strip()

            # Use None if user pressed Enter (keep current)
            title_to_update = new_title if new_title else None
            description_to_update = new_description if new_description else None

            if title_to_update is None and description_to_update is None:
                display_error("No changes made. At least one field must be updated.")
                return

            updated_task = self.task_manager.update_task(
                task_id,
                title=title_to_update,
                description=description_to_update
            )
            display_success("Task updated successfully!")
            display_task_details(updated_task)
        except TaskNotFoundError as e:
            display_error(str(e))
        except InvalidTaskDataError as e:
            display_error(str(e))
        except TodoError as e:
            display_error(str(e))

    def delete_task(self):
        """Delete a task."""
        try:
            print("\n--- Delete Task ---")
            task_id_str = input("Enter task ID: ").strip()

            if not task_id_str.isdigit():
                display_error("Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id_str)

            # Show task before deletion
            task = self.task_manager.get_task(task_id)
            print(f"\nTask to delete: [{task.id}] {task.title}")

            confirm = input("Are you sure you want to delete this task? (y/n): ").strip().lower()

            if confirm == "y":
                self.task_manager.delete_task(task_id)
                display_success(f"Task ID {task_id} has been deleted.")
            else:
                print("\nDeletion cancelled.\n")
        except TaskNotFoundError as e:
            display_error(str(e))
        except TodoError as e:
            display_error(str(e))
