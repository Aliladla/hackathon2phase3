# TaskManager Interface Contract

**Purpose**: Define the contract for task management operations that all implementations must follow.

**Version**: 1.0.0 (Phase 1)

## Overview

This contract defines the interface for the TaskManager component, which handles all task CRUD operations. The interface is implementation-agnostic and can be backed by in-memory storage (Phase 1), database (Phase 2), or any other storage mechanism.

## Interface Definition

```python
from typing import Protocol, List, Optional
from datetime import datetime
from ..domain.task import Task

class TaskManagerProtocol(Protocol):
    """Protocol defining the contract for task management operations."""

    def create_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task with auto-assigned ID.

        Args:
            title: Task title (1-200 characters, required)
            description: Task description (0-1000 characters, optional)

        Returns:
            Task: Newly created task with unique ID and created_at timestamp

        Raises:
            InvalidTaskDataError: If title is empty or exceeds length limits
            InvalidTaskDataError: If description exceeds length limits
        """
        ...

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The requested task

        Raises:
            TaskNotFoundError: If task with given ID does not exist
        """
        ...

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List[Task]: All tasks, ordered by creation time (oldest first)
                       Empty list if no tasks exist
        """
        ...

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update a task's title and/or description.

        Args:
            task_id: Unique task identifier
            title: New title (if provided, must be 1-200 characters)
            description: New description (if provided, must be 0-1000 characters)

        Returns:
            Task: Updated task with new values

        Raises:
            TaskNotFoundError: If task with given ID does not exist
            InvalidTaskDataError: If title is empty or exceeds length limits
            InvalidTaskDataError: If description exceeds length limits

        Notes:
            - If title is None, existing title is preserved
            - If description is None, existing description is preserved
            - At least one of title or description must be provided
        """
        ...

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id: Unique task identifier

        Raises:
            TaskNotFoundError: If task with given ID does not exist

        Notes:
            - Deletion is permanent (no soft delete in Phase 1)
            - Deleted task IDs are not reused
        """
        ...

    def mark_complete(self, task_id: int) -> Task:
        """
        Mark a task as complete.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: Updated task with completed=True

        Raises:
            TaskNotFoundError: If task with given ID does not exist

        Notes:
            - Idempotent: marking an already-complete task has no effect
        """
        ...

    def mark_incomplete(self, task_id: int) -> Task:
        """
        Mark a task as incomplete.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: Updated task with completed=False

        Raises:
            TaskNotFoundError: If task with given ID does not exist

        Notes:
            - Idempotent: marking an already-incomplete task has no effect
        """
        ...
```

## Operation Contracts

### create_task

**Preconditions**:
- title is a non-empty string (after stripping whitespace)
- title length is between 1 and 200 characters
- description length is between 0 and 1000 characters

**Postconditions**:
- New task is created with unique auto-assigned ID
- Task has completed=False
- Task has created_at set to current timestamp
- Task is retrievable via get_task() and get_all_tasks()

**Invariants**:
- Task IDs are unique and never reused
- Task IDs are positive integers
- IDs are assigned sequentially (1, 2, 3, ...)

---

### get_task

**Preconditions**:
- task_id is a positive integer
- Task with given ID exists in storage

**Postconditions**:
- Returns the exact task with matching ID
- Task data is unchanged (read-only operation)

**Invariants**:
- Same ID always returns same task (until deleted or updated)

---

### get_all_tasks

**Preconditions**: None

**Postconditions**:
- Returns list of all existing tasks
- Tasks are ordered by created_at (oldest first)
- Empty list if no tasks exist

**Invariants**:
- List contains no duplicates
- All returned tasks have valid data

---

### update_task

**Preconditions**:
- task_id exists in storage
- If title provided: non-empty, 1-200 characters
- If description provided: 0-1000 characters
- At least one of title or description is provided

**Postconditions**:
- Task with given ID has updated title and/or description
- Other task attributes (id, completed, created_at) are unchanged
- Updated task is retrievable with new values

**Invariants**:
- Task ID never changes
- created_at timestamp never changes
- completed status is not affected by update

---

### delete_task

**Preconditions**:
- task_id exists in storage

**Postconditions**:
- Task with given ID no longer exists
- get_task(task_id) raises TaskNotFoundError
- Task does not appear in get_all_tasks()
- Deleted ID is never reused for new tasks

**Invariants**:
- Other tasks are unaffected
- Total task count decreases by 1

---

### mark_complete / mark_incomplete

**Preconditions**:
- task_id exists in storage

**Postconditions**:
- Task completed status is set to True (mark_complete) or False (mark_incomplete)
- Other task attributes are unchanged
- Updated task is retrievable with new status

**Invariants**:
- Operations are idempotent
- Task ID, title, description, created_at are unchanged

---

## Error Handling Contract

### Exception Hierarchy

```python
class TodoError(Exception):
    """Base exception for all todo application errors."""
    pass

class InvalidTaskDataError(TodoError):
    """Raised when task data fails validation."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class TaskNotFoundError(TodoError):
    """Raised when task ID does not exist."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task not found (ID: {task_id})")
```

### Error Conditions

| Operation | Error Condition | Exception | Message |
|-----------|----------------|-----------|---------|
| create_task | Empty title | InvalidTaskDataError | "Title cannot be empty" |
| create_task | Title > 200 chars | InvalidTaskDataError | "Title too long (max 200 characters)" |
| create_task | Description > 1000 chars | InvalidTaskDataError | "Description too long (max 1000 characters)" |
| get_task | ID not found | TaskNotFoundError | "Task not found (ID: {id})" |
| update_task | ID not found | TaskNotFoundError | "Task not found (ID: {id})" |
| update_task | Empty title | InvalidTaskDataError | "Title cannot be empty" |
| update_task | Title > 200 chars | InvalidTaskDataError | "Title too long (max 200 characters)" |
| update_task | Description > 1000 chars | InvalidTaskDataError | "Description too long (max 1000 characters)" |
| delete_task | ID not found | TaskNotFoundError | "Task not found (ID: {id})" |
| mark_complete | ID not found | TaskNotFoundError | "Task not found (ID: {id})" |
| mark_incomplete | ID not found | TaskNotFoundError | "Task not found (ID: {id})" |

---

## Performance Contract

**Phase 1 Requirements** (in-memory storage):

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| create_task | O(1) | O(1) | Dict insertion |
| get_task | O(1) | O(1) | Dict lookup by ID |
| get_all_tasks | O(n) | O(n) | Iterate all tasks |
| update_task | O(1) | O(1) | Dict replacement |
| delete_task | O(1) | O(1) | Dict deletion |
| mark_complete | O(1) | O(1) | Dict replacement |
| mark_incomplete | O(1) | O(1) | Dict replacement |

**Performance Goals**:
- Handle 100+ tasks without noticeable degradation
- get_all_tasks() completes in < 2 seconds for 100 tasks
- All single-task operations complete in < 100ms

---

## Thread Safety

**Phase 1**: Not thread-safe (single-user, single-threaded CLI application)

**Phase 2**: Must add thread safety for web server (multiple concurrent requests)

---

## Testing Contract

**Required Test Coverage**:

1. **Happy Path Tests**:
   - Create task with title only
   - Create task with title and description
   - Get existing task
   - Get all tasks (empty, single, multiple)
   - Update title only
   - Update description only
   - Update both title and description
   - Delete existing task
   - Mark task complete
   - Mark task incomplete

2. **Error Path Tests**:
   - Create with empty title
   - Create with title too long
   - Create with description too long
   - Get non-existent task
   - Update non-existent task
   - Update with empty title
   - Update with title too long
   - Update with description too long
   - Delete non-existent task
   - Mark complete non-existent task
   - Mark incomplete non-existent task

3. **Edge Case Tests**:
   - Title exactly 200 characters
   - Description exactly 1000 characters
   - Mark already-complete task as complete (idempotent)
   - Mark already-incomplete task as incomplete (idempotent)
   - Delete task then try to get it
   - Create many tasks (100+) and verify IDs are unique

---

## Implementation Notes

**Phase 1 Implementation** (MemoryRepository):
- Uses dict[int, Task] for O(1) operations
- Auto-increment counter for ID generation
- No persistence (data lost on exit)

**Phase 2 Migration** (DatabaseRepository):
- Same interface, different implementation
- Uses SQLModel + PostgreSQL
- Add user_id filtering
- Add transaction support

**Phase 3 Extension** (MCP Tools):
- MCP tools call TaskManager methods
- Same interface, no changes needed
- Add conversation_id for audit trail

---

## Version History

- **1.0.0** (2025-02-15): Initial contract for Phase 1
  - Basic CRUD operations
  - In-memory storage
  - Single-user, single-threaded
