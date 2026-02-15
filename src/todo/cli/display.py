"""Display utilities for CLI output."""
from typing import List
from ..domain.task import Task


def format_task(task: Task, show_description: bool = False) -> str:
    """Format a single task for display."""
    status = "[✓]" if task.completed else "[ ]"
    result = f"[{task.id}] {status} {task.title}"

    if show_description and task.description:
        result += f"\n    Description: {task.description}"

    return result


def display_tasks(tasks: List[Task]) -> None:
    """Display all tasks."""
    if not tasks:
        print("\nNo tasks found. Add your first task!\n")
        return

    print("\n=== All Tasks ===")
    for task in tasks:
        print(format_task(task))

    completed = sum(1 for t in tasks if t.completed)
    pending = len(tasks) - completed
    print(f"\nTotal: {len(tasks)} tasks ({completed} completed, {pending} pending)\n")


def display_task_details(task: Task) -> None:
    """Display detailed task information."""
    status = "Complete" if task.completed else "Incomplete"
    print(f"\n✓ Task ID: {task.id}")
    print(f"  Title: {task.title}")
    print(f"  Description: {task.description if task.description else '(none)'}")
    print(f"  Status: {status}")
    print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n")


def display_error(message: str) -> None:
    """Display an error message."""
    print(f"\n✗ Error: {message}\n")


def display_success(message: str) -> None:
    """Display a success message."""
    print(f"\n✓ {message}\n")
