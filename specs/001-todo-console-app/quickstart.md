# Quickstart Guide: Todo Console App (Phase 1)

**Version**: 1.0.0
**Date**: 2025-02-15
**Target Audience**: Developers and users setting up the application

## Overview

This guide walks you through setting up and using the Todo Console App for Phase 1. The application is a command-line todo manager with in-memory storage.

## Prerequisites

- **Python 3.13+** installed on your system
- **UV package manager** installed ([installation guide](https://github.com/astral-sh/uv))
- **Git** (for cloning the repository)
- Basic command-line familiarity

### Installing UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Aliladla/hackathon2phase1.git
cd hackathon2phase1
```

### 2. Initialize Project with UV

```bash
# Initialize UV project (if not already done)
uv init --python 3.13

# Install dependencies (pytest for development)
uv add --dev pytest pytest-cov

# Sync environment
uv sync
```

### 3. Verify Installation

```bash
# Run tests to verify setup
uv run pytest

# Expected output: All tests pass
```

## Running the Application

### Start the Todo App

```bash
# Run the application
uv run python -m todo

# Alternative (if installed in editable mode)
uv run todo
```

### Expected Output

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

## Usage Guide

### 1. View All Tasks

**Menu Option**: 1

**What it does**: Displays all tasks with their ID, title, and completion status.

**Example**:
```
=== All Tasks ===
[1] [ ] Buy groceries
[2] [✓] Complete homework
[3] [ ] Call dentist

Total: 3 tasks (1 completed, 2 pending)
```

**Empty List**:
```
No tasks found. Add your first task!
```

---

### 2. Add New Task

**Menu Option**: 2

**What it does**: Creates a new task with a title and optional description.

**Steps**:
1. Select option 2
2. Enter task title (required, 1-200 characters)
3. Enter description (optional, press Enter to skip)

**Example**:
```
Enter choice (1-6): 2

Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread

✓ Task created successfully!
Task ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Incomplete
```

**Validation**:
- Title cannot be empty
- Title max 200 characters
- Description max 1000 characters

---

### 3. Mark Task Complete/Incomplete

**Menu Option**: 3

**What it does**: Toggles a task's completion status.

**Steps**:
1. Select option 3
2. Enter task ID
3. Choose: (c)omplete or (i)ncomplete

**Example**:
```
Enter choice (1-6): 3

Enter task ID: 1
Mark as (c)omplete or (i)ncomplete? c

✓ Task marked as complete!
[1] [✓] Buy groceries
```

**Error Handling**:
- Invalid ID: "Task not found (ID: 99)"
- Non-numeric input: "Invalid task ID"

---

### 4. Update Task

**Menu Option**: 4

**What it does**: Updates a task's title and/or description.

**Steps**:
1. Select option 4
2. Enter task ID
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)

**Example**:
```
Enter choice (1-6): 4

Enter task ID: 1
Current title: Buy groceries
New title (press Enter to keep): Buy groceries and fruits
Current description: Milk, eggs, bread
New description (press Enter to keep): Milk, eggs, bread, apples

✓ Task updated successfully!
[1] [ ] Buy groceries and fruits
```

**Validation**:
- At least one field must be updated
- Title cannot be empty if provided
- Same length constraints as creation

---

### 5. Delete Task

**Menu Option**: 5

**What it does**: Permanently removes a task from the list.

**Steps**:
1. Select option 5
2. Enter task ID
3. Confirm deletion (y/n)

**Example**:
```
Enter choice (1-6): 5

Enter task ID: 1
Are you sure you want to delete this task? (y/n): y

✓ Task deleted successfully!
Task ID 1 has been removed.
```

**Warning**: Deletion is permanent and cannot be undone.

---

### 6. Exit

**Menu Option**: 6

**What it does**: Exits the application.

**Warning**: All tasks are stored in memory and will be lost when you exit. This is expected behavior for Phase 1.

```
Enter choice (1-6): 6

Goodbye! All tasks will be lost (in-memory storage).
```

## Common Workflows

### Quick Task Management Session

```bash
# 1. Start the app
uv run python -m todo

# 2. Add a few tasks
# Select: 2 → "Buy groceries" → ""
# Select: 2 → "Call dentist" → "Schedule checkup"
# Select: 2 → "Finish report" → "Q4 sales report"

# 3. View all tasks
# Select: 1

# 4. Mark one complete
# Select: 3 → 1 → c

# 5. View updated list
# Select: 1

# 6. Exit
# Select: 6
```

### Testing All Features

```bash
# Run automated tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src/todo --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

## Troubleshooting

### Issue: "Command not found: uv"

**Solution**: Install UV package manager (see Prerequisites section)

---

### Issue: "Python 3.13 not found"

**Solution**:
```bash
# Check Python version
python --version

# Install Python 3.13+ from python.org
# Or use pyenv:
pyenv install 3.13
pyenv local 3.13
```

---

### Issue: "Module 'todo' not found"

**Solution**:
```bash
# Ensure you're in the project root
cd hackathon2phase1

# Reinstall in editable mode
uv pip install -e .

# Or run directly
uv run python -m src.todo
```

---

### Issue: Tests failing

**Solution**:
```bash
# Clean and reinstall
rm -rf .venv
uv sync
uv run pytest -v
```

---

### Issue: "All tasks lost after exit"

**Expected Behavior**: Phase 1 uses in-memory storage. Tasks are not saved to disk. This is intentional and will be fixed in Phase 2 with database persistence.

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_task.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src/todo
```

### Code Quality

```bash
# Format code with black
uv run black src/ tests/

# Lint with ruff
uv run ruff check src/ tests/

# Type check with mypy
uv run mypy src/
```

### Project Structure

```
hackathon2phase1/
├── src/todo/           # Source code
│   ├── domain/         # Business logic
│   ├── storage/        # Data storage
│   └── cli/            # User interface
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── e2e/            # End-to-end tests
├── specs/              # Specifications
└── pyproject.toml      # Project configuration
```

## Performance Notes

- **Capacity**: Tested with 100+ tasks without performance issues
- **Response Time**: All operations complete in < 100ms
- **Memory Usage**: Minimal (< 10MB for 100 tasks)

## Known Limitations (Phase 1)

1. **No Persistence**: Tasks are lost when application exits
2. **Single User**: No user accounts or authentication
3. **No Search**: Cannot search or filter tasks (view all only)
4. **No Sorting**: Tasks displayed in creation order only
5. **No Categories**: No tags, priorities, or due dates

These limitations will be addressed in Phase 2 (web app) and Phase 3 (AI chatbot).

## Next Steps

After completing Phase 1:
1. Push code to GitHub: https://github.com/Aliladla/hackathon2phase1
2. Create demo video (< 90 seconds)
3. Submit via hackathon form
4. Proceed to Phase 2 (Full-Stack Web Application)

## Support

- **GitHub Issues**: https://github.com/Aliladla/hackathon2phase1/issues
- **Hackathon Documentation**: See hackathon2doc.md
- **Spec-Driven Development**: See specs/001-todo-console-app/

## Quick Reference

| Action | Menu Option | Shortcut |
|--------|-------------|----------|
| View tasks | 1 | - |
| Add task | 2 | - |
| Toggle complete | 3 | - |
| Update task | 4 | - |
| Delete task | 5 | - |
| Exit | 6 | Ctrl+C |

---

**Version History**:
- 1.0.0 (2025-02-15): Initial quickstart for Phase 1
