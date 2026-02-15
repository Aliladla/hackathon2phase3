# Research & Technical Decisions: Todo Console App (Phase 1)

**Date**: 2025-02-15
**Feature**: 001-todo-console-app
**Purpose**: Document technical decisions, rationale, and alternatives considered

## Overview

This document captures all technical decisions made during the planning phase for Phase 1 of the Todo Hackathon project. Since Phase 1 requirements are straightforward (in-memory console app), most decisions align with constitution requirements and industry best practices.

## Technical Decisions

### 1. Language & Runtime

**Decision**: Python 3.13+

**Rationale**:
- Required by hackathon specification
- Latest stable Python with performance improvements
- Excellent standard library for CLI applications
- Native dataclass support for domain entities
- Type hints for better code quality

**Alternatives Considered**: None (specified in requirements)

---

### 2. Package Management

**Decision**: UV package manager

**Rationale**:
- Required by constitution (Principle VI: Fast Iteration with UV)
- Faster dependency resolution than pip
- Automatic virtual environment management
- Simpler workflow: `uv init`, `uv add`, `uv run`
- Better for rapid hackathon development

**Alternatives Considered**:
- pip + venv (traditional approach) - Rejected: slower, more manual steps
- Poetry - Rejected: not specified in constitution

---

### 3. Storage Strategy

**Decision**: In-memory storage using Python dict

**Rationale**:
- Phase 1 requirement: no persistence needed
- O(1) lookup by task ID (dict key)
- Simple implementation, no external dependencies
- Easy to replace with database in Phase 2
- Sufficient for 100+ tasks performance goal

**Implementation Details**:
```python
# Internal storage structure
tasks: dict[int, Task] = {}  # task_id -> Task object
next_id: int = 1  # Auto-incrementing ID counter
```

**Alternatives Considered**:
- List storage - Rejected: O(n) lookup, inefficient for ID-based operations
- SQLite - Rejected: unnecessary complexity for Phase 1, adds dependency

---

### 4. Testing Framework

**Decision**: pytest

**Rationale**:
- Industry standard for Python testing
- Simple, readable test syntax
- Excellent fixture support for test setup
- Built-in assertion introspection
- Required by constitution (Principle II: Test-First Development)

**Test Organization**:
- Unit tests: Domain logic (Task, TaskManager)
- Integration tests: Storage + domain interaction
- E2E tests: Full CLI workflows

**Alternatives Considered**:
- unittest (stdlib) - Rejected: more verbose, less modern
- nose2 - Rejected: less actively maintained than pytest

---

### 5. Architecture Pattern

**Decision**: 3-layer modular architecture (Domain, Storage, Presentation)

**Rationale**:
- Required by constitution (Principle III: Modular Architecture)
- Enables Phase 2/3 reuse of domain logic
- Clear separation of concerns
- Domain layer is framework-agnostic
- Easy to test each layer independently

**Layer Responsibilities**:
1. **Domain** (`src/todo/domain/`): Pure business logic, no I/O
   - Task entity (dataclass)
   - TaskManager (CRUD operations)

2. **Storage** (`src/todo/storage/`): Data persistence abstraction
   - MemoryRepository (in-memory implementation)
   - Interface can be swapped for DB in Phase 2

3. **Presentation** (`src/todo/cli/`): User interaction
   - Menu (interactive CLI)
   - Display (output formatting)

**Alternatives Considered**:
- Monolithic single-file approach - Rejected: not reusable for Phase 2/3
- MVC pattern - Rejected: overkill for console app, web-centric pattern

---

### 6. CLI Interface Design

**Decision**: Interactive menu with numbered options

**Rationale**:
- Required by constitution (Principle IV: Simple CLI Interface)
- User-friendly for non-technical users
- No need to remember command syntax
- Clear visual feedback
- Easy to implement and test

**Menu Structure**:
```
=== Todo App ===
1. View all tasks
2. Add new task
3. Mark task complete/incomplete
4. Update task
5. Delete task
6. Exit

Enter choice (1-6):
```

**Alternatives Considered**:
- Command-line arguments (`todo add "title"`) - Rejected: less user-friendly, harder to discover features
- REPL with commands - Rejected: more complex to implement

---

### 7. Task Entity Design

**Decision**: Python dataclass with validation

**Rationale**:
- Immutable by default (frozen=True for safety)
- Built-in __init__, __repr__, __eq__
- Type hints for clarity
- Validation in __post_init__
- No external dependencies

**Entity Structure**:
```python
@dataclass(frozen=True)
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

**Validation Rules** (from spec FR-001, FR-007):
- Title: 1-200 characters, required
- Description: 0-1000 characters, optional
- ID: positive integer, auto-assigned

**Alternatives Considered**:
- Pydantic models - Rejected: adds dependency, overkill for Phase 1
- Plain dict - Rejected: no type safety, error-prone
- NamedTuple - Rejected: less flexible than dataclass

---

### 8. Error Handling Strategy

**Decision**: Custom exception hierarchy + user-friendly messages

**Rationale**:
- Required by spec (FR-008: clear error messages)
- Exceptions for domain errors (TaskNotFound, InvalidTitle)
- CLI layer catches and displays user-friendly messages
- Errors to stderr, success to stdout (constitution requirement)

**Exception Hierarchy**:
```python
class TodoError(Exception): pass
class TaskNotFoundError(TodoError): pass
class InvalidTaskDataError(TodoError): pass
```

**Alternatives Considered**:
- Return codes/tuples - Rejected: less Pythonic, harder to trace
- Generic exceptions - Rejected: less specific error handling

---

### 9. ID Generation Strategy

**Decision**: Auto-incrementing integer counter

**Rationale**:
- Simple, predictable IDs (1, 2, 3, ...)
- No collisions in single-user, in-memory context
- Easy for users to reference tasks
- Sufficient for Phase 1 scope

**Implementation**:
```python
self.next_id = 1
# On task creation:
task_id = self.next_id
self.next_id += 1
```

**Alternatives Considered**:
- UUID - Rejected: overkill, harder for users to type
- Hash-based - Rejected: unnecessary complexity

---

### 10. Performance Optimization

**Decision**: Minimal optimization, focus on correctness

**Rationale**:
- Performance goal: 100 tasks, <2 seconds for list view
- Dict lookup is O(1), list iteration is O(n) - both fast enough
- Premature optimization violates constitution (Principle V: Minimal Viable)
- Can optimize in Phase 2 if needed

**Measured Approach**:
- Use dict for O(1) ID lookup
- Simple list comprehension for filtering
- No caching, no indexing (unnecessary for 100 tasks)

**Alternatives Considered**:
- Complex indexing structures - Rejected: premature optimization
- Lazy loading - Rejected: all data in memory anyway

---

## Dependencies Summary

### Runtime Dependencies
- **None** - Uses only Python standard library

### Development Dependencies
- **pytest** - Testing framework
- **pytest-cov** (optional) - Code coverage reporting

### Rationale for Zero Runtime Dependencies
- Simplifies deployment and distribution
- Faster startup time
- Easier to understand and maintain
- Aligns with "Minimal Viable Implementation" principle
- Phase 2 will add FastAPI, SQLModel, etc.

---

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| Data loss on exit | Document clearly in README; expected behavior for Phase 1 |
| ID collision after many deletes | Use monotonic counter (never reuse IDs) |
| Memory exhaustion with many tasks | Test with 100+ tasks; acceptable limit for Phase 1 |
| Poor CLI usability | User testing with clear menu options and error messages |

---

## Phase 2/3 Considerations

**Reusability Design**:
- Domain layer (`task.py`, `task_manager.py`) will be imported by:
  - Phase 2: FastAPI endpoints
  - Phase 3: MCP tools for AI agent

**Migration Path**:
- Storage layer interface allows swapping MemoryRepository for DatabaseRepository
- Domain logic remains unchanged
- CLI can coexist with web UI and AI chatbot

**No Rework Required**:
- Domain entities are framework-agnostic
- Business rules encoded in domain layer
- Only storage and presentation layers change in Phase 2/3

---

## Conclusion

All technical decisions align with constitution principles and hackathon requirements. No unresolved clarifications remain. Architecture is designed for rapid Phase 1 delivery while enabling clean Phase 2/3 extension.

**Ready for Phase 1 Design**: Proceed to data-model.md and contracts generation.
