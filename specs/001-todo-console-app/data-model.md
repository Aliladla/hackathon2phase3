# Data Model: Todo Console App (Phase 1)

**Date**: 2025-02-15
**Feature**: 001-todo-console-app
**Purpose**: Define entities, validation rules, and state transitions

## Overview

This document defines the data model for Phase 1 of the Todo application. The model is intentionally simple and framework-agnostic to enable reuse in Phase 2 (web app with database) and Phase 3 (AI chatbot).

## Entities

### Task

**Description**: Represents a single todo item with title, description, and completion status.

**Attributes**:

| Attribute | Type | Required | Constraints | Default | Description |
|-----------|------|----------|-------------|---------|-------------|
| `id` | int | Yes | Positive integer, unique | Auto-assigned | Unique identifier for the task |
| `title` | str | Yes | 1-200 characters, non-empty | None | Short description of the task |
| `description` | str | No | 0-1000 characters | Empty string | Detailed description of the task |
| `completed` | bool | Yes | True or False | False | Whether the task is completed |
| `created_at` | datetime | Yes | Valid datetime | Current time | When the task was created |

**Validation Rules** (from spec FR-001, FR-007):

1. **Title Validation**:
   - MUST NOT be empty or whitespace-only
   - MUST be between 1 and 200 characters (after stripping whitespace)
   - Error: "Title cannot be empty" or "Title too long (max 200 characters)"

2. **Description Validation**:
   - MAY be empty (optional field)
   - MUST NOT exceed 1000 characters
   - Error: "Description too long (max 1000 characters)"

3. **ID Validation**:
   - MUST be a positive integer (> 0)
   - MUST be unique within the task collection
   - Auto-assigned by TaskManager, not user-provided

4. **Completed Validation**:
   - MUST be boolean (True or False)
   - Defaults to False on creation

**Python Implementation** (dataclass):

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Task:
    """Immutable task entity."""
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    def __post_init__(self):
        """Validate task data after initialization."""
        # Validate ID
        if self.id <= 0:
            raise ValueError("Task ID must be positive")

        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Title too long (max 200 characters)")

        # Validate description
        if len(self.description) > 1000:
            raise ValueError("Description too long (max 1000 characters)")
```

**Immutability Rationale**:
- Tasks are frozen (immutable) to prevent accidental modification
- Updates create new Task instances with modified fields
- Simplifies reasoning about state changes
- Prevents bugs from shared mutable state

---

## State Transitions

### Task Completion Status

**States**:
- `incomplete` (completed=False) - Initial state
- `complete` (completed=True) - Task is done

**Transitions**:

```
incomplete ──[mark_complete]──> complete
    ^                              |
    └────────[mark_incomplete]─────┘
```

**Rules**:
1. New tasks start in `incomplete` state
2. Tasks can transition between states unlimited times
3. No validation required for state transitions (always allowed)
4. Marking an already-complete task as complete is idempotent (no error)

---

## Relationships

### Phase 1 (Current)
- **No relationships** - Tasks are independent entities
- Tasks stored in flat collection (dict)
- No user ownership (single-user application)

### Phase 2 (Future)
- **Task → User** (many-to-one): Each task belongs to one user
- Add `user_id` field to Task entity
- Filter tasks by authenticated user

### Phase 3 (Future)
- **Task → Conversation** (many-to-one): Tasks created via AI chat
- Optional `conversation_id` for audit trail
- No impact on core task operations

---

## Validation Error Handling

**Error Types**:

```python
class TodoError(Exception):
    """Base exception for todo application."""
    pass

class InvalidTaskDataError(TodoError):
    """Raised when task data fails validation."""
    pass

class TaskNotFoundError(TodoError):
    """Raised when task ID does not exist."""
    pass
```

**Validation Timing**:
1. **Creation**: Validate title and description before creating Task
2. **Update**: Validate new title/description before creating updated Task
3. **Lookup**: Validate task ID exists before operations

**User-Facing Error Messages** (from spec FR-008):
- "Title cannot be empty"
- "Title too long (max 200 characters)"
- "Description too long (max 1000 characters)"
- "Task not found (ID: {id})"
- "Invalid task ID"

---

## Data Constraints Summary

| Constraint | Rule | Enforcement |
|------------|------|-------------|
| Unique IDs | Each task has unique positive integer ID | TaskManager auto-increment |
| Title required | Title must be 1-200 chars, non-empty | Task.__post_init__ validation |
| Description optional | Description 0-1000 chars | Task.__post_init__ validation |
| Boolean completion | completed is True or False | Python type system |
| Immutable tasks | Tasks cannot be modified after creation | dataclass(frozen=True) |

---

## Storage Schema (In-Memory)

**Phase 1 Implementation**:

```python
class MemoryRepository:
    def __init__(self):
        self._tasks: dict[int, Task] = {}  # task_id -> Task
        self._next_id: int = 1              # Auto-increment counter
```

**Operations Complexity**:
- Create: O(1) - dict insertion
- Read by ID: O(1) - dict lookup
- Read all: O(n) - iterate dict values
- Update: O(1) - dict replacement
- Delete: O(1) - dict deletion

**Phase 2 Migration** (Database Schema):

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

---

## Acceptance Criteria Mapping

| Spec Requirement | Data Model Support |
|------------------|-------------------|
| FR-001: Add task with title + description | Task entity with validated title/description fields |
| FR-002: Unique auto-assigned ID | Auto-increment counter in repository |
| FR-003: Display ID, title, status | All fields accessible via Task attributes |
| FR-004: Mark complete/incomplete | completed boolean field with state transitions |
| FR-005: Delete by ID | ID-based dict lookup and removal |
| FR-006: Update title/description | Create new Task with updated fields (immutable) |
| FR-007: Validate non-empty title | __post_init__ validation raises ValueError |
| FR-008: Clear error messages | Custom exception types with descriptive messages |

---

## Testing Strategy

**Unit Tests** (test_task.py):
- Valid task creation
- Title validation (empty, too long, valid)
- Description validation (empty OK, too long, valid)
- ID validation (negative, zero, positive)
- Immutability enforcement

**Integration Tests** (test_memory_repository.py):
- ID auto-increment behavior
- Unique ID enforcement
- CRUD operations with validation
- Error handling for invalid data

---

## Summary

The data model is intentionally minimal for Phase 1:
- Single entity (Task) with 5 attributes
- Simple validation rules (length constraints)
- Immutable design for safety
- Framework-agnostic for Phase 2/3 reuse

All validation rules map directly to functional requirements in spec.md. No complex relationships or business logic required for Phase 1.
