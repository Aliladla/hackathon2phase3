# Tasks: Todo Console App (Phase 1)

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per constitution (Principle II: Test-First Development with TDD approach)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/todo/`, `tests/` at repository root
- Paths follow plan.md structure: domain/, storage/, cli/ layers

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Initialize UV project with Python 3.13 in project root
- [ ] T002 Create project structure per plan.md: src/todo/{domain,storage,cli}/, tests/{unit,integration,e2e}/
- [ ] T003 [P] Add pytest and pytest-cov as dev dependencies via uv add --dev
- [ ] T004 [P] Create pyproject.toml with project metadata and dependencies
- [ ] T005 [P] Create .python-version file specifying 3.13
- [ ] T006 [P] Create README.md with project overview and setup instructions
- [ ] T007 [P] Create all __init__.py files for Python packages

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain entities and infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create custom exception classes (TodoError, InvalidTaskDataError, TaskNotFoundError) in src/todo/domain/exceptions.py
- [ ] T009 [P] Create Task entity dataclass with validation in src/todo/domain/task.py
- [ ] T010 [P] Write unit tests for Task entity validation in tests/unit/test_task.py (RED phase)
- [ ] T011 Implement Task entity to pass validation tests in src/todo/domain/task.py (GREEN phase)
- [ ] T012 Create TaskManager interface protocol in src/todo/domain/task_manager.py
- [ ] T013 Create MemoryRepository class skeleton in src/todo/storage/memory_repository.py
- [ ] T014 Create CLI display utilities in src/todo/cli/display.py (format task output, status indicators)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can see all their tasks in a clear list with ID, title, and completion status

**Independent Test**: Create sample tasks in memory and display them; verify empty list message when no tasks exist

### Tests for User Story 1 (TDD - RED phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T015 [P] [US1] Write unit test for get_all_tasks() in tests/unit/test_task_manager.py
- [ ] T016 [P] [US1] Write integration test for MemoryRepository.get_all_tasks() in tests/integration/test_memory_repository.py
- [ ] T017 [P] [US1] Write E2E test for view tasks CLI command in tests/e2e/test_cli_operations.py

### Implementation for User Story 1 (GREEN phase)

- [ ] T018 [US1] Implement MemoryRepository.get_all_tasks() method in src/todo/storage/memory_repository.py
- [ ] T019 [US1] Implement TaskManager.get_all_tasks() in src/todo/domain/task_manager.py
- [ ] T020 [US1] Create CLI menu structure in src/todo/cli/menu.py with option 1 (View tasks)
- [ ] T021 [US1] Implement view_tasks() function in src/todo/cli/menu.py (calls TaskManager, uses display utilities)
- [ ] T022 [US1] Create __main__.py entry point in src/todo/__main__.py with menu loop
- [ ] T023 [US1] Verify all US1 tests pass (GREEN phase complete)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can view tasks (empty list initially)

---

## Phase 4: User Story 2 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add a new task with a title and optional description

**Independent Test**: Add a task via CLI, verify it appears in the task list with correct details

### Tests for User Story 2 (TDD - RED phase)

- [ ] T024 [P] [US2] Write unit test for create_task() with valid data in tests/unit/test_task_manager.py
- [ ] T025 [P] [US2] Write unit test for create_task() with invalid data (empty title, too long) in tests/unit/test_task_manager.py
- [ ] T026 [P] [US2] Write integration test for MemoryRepository.create_task() in tests/integration/test_memory_repository.py
- [ ] T027 [P] [US2] Write E2E test for add task CLI command in tests/e2e/test_cli_operations.py

### Implementation for User Story 2 (GREEN phase)

- [ ] T028 [US2] Implement MemoryRepository.create_task() with ID auto-increment in src/todo/storage/memory_repository.py
- [ ] T029 [US2] Implement TaskManager.create_task() with validation in src/todo/domain/task_manager.py
- [ ] T030 [US2] Add menu option 2 (Add task) to CLI menu in src/todo/cli/menu.py
- [ ] T031 [US2] Implement add_task() function in src/todo/cli/menu.py (prompts for title/description, calls TaskManager)
- [ ] T032 [US2] Add error handling and user-friendly messages for validation errors in src/todo/cli/menu.py
- [ ] T033 [US2] Verify all US2 tests pass (GREEN phase complete)

**Checkpoint**: At this point, User Stories 1 AND 2 work together - users can add and view tasks

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can mark tasks as complete or incomplete to track progress

**Independent Test**: Create a task, mark it complete, verify status change in list, mark incomplete again

### Tests for User Story 3 (TDD - RED phase)

- [ ] T034 [P] [US3] Write unit test for mark_complete() in tests/unit/test_task_manager.py
- [ ] T035 [P] [US3] Write unit test for mark_incomplete() in tests/unit/test_task_manager.py
- [ ] T036 [P] [US3] Write unit test for idempotent behavior (mark complete twice) in tests/unit/test_task_manager.py
- [ ] T037 [P] [US3] Write integration test for completion status changes in tests/integration/test_memory_repository.py
- [ ] T038 [P] [US3] Write E2E test for mark complete/incomplete CLI command in tests/e2e/test_cli_operations.py

### Implementation for User Story 3 (GREEN phase)

- [ ] T039 [US3] Implement MemoryRepository.mark_complete() in src/todo/storage/memory_repository.py
- [ ] T040 [US3] Implement MemoryRepository.mark_incomplete() in src/todo/storage/memory_repository.py
- [ ] T041 [US3] Implement TaskManager.mark_complete() in src/todo/domain/task_manager.py
- [ ] T042 [US3] Implement TaskManager.mark_incomplete() in src/todo/domain/task_manager.py
- [ ] T043 [US3] Add menu option 3 (Mark complete/incomplete) to CLI menu in src/todo/cli/menu.py
- [ ] T044 [US3] Implement toggle_completion() function in src/todo/cli/menu.py (prompts for ID and choice)
- [ ] T045 [US3] Add error handling for invalid task IDs in src/todo/cli/menu.py
- [ ] T046 [US3] Verify all US3 tests pass (GREEN phase complete)

**Checkpoint**: Users can now add, view, and mark tasks complete - core todo functionality working

---

## Phase 6: User Story 4 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks they no longer need to keep list relevant

**Independent Test**: Create a task, delete it by ID, verify it no longer appears in list

### Tests for User Story 4 (TDD - RED phase)

- [ ] T047 [P] [US4] Write unit test for delete_task() with valid ID in tests/unit/test_task_manager.py
- [ ] T048 [P] [US4] Write unit test for delete_task() with invalid ID in tests/unit/test_task_manager.py
- [ ] T049 [P] [US4] Write integration test for task deletion in tests/integration/test_memory_repository.py
- [ ] T050 [P] [US4] Write E2E test for delete task CLI command in tests/e2e/test_cli_operations.py

### Implementation for User Story 4 (GREEN phase)

- [ ] T051 [US4] Implement MemoryRepository.delete_task() in src/todo/storage/memory_repository.py
- [ ] T052 [US4] Implement TaskManager.delete_task() in src/todo/domain/task_manager.py
- [ ] T053 [US4] Add menu option 5 (Delete task) to CLI menu in src/todo/cli/menu.py
- [ ] T054 [US4] Implement delete_task() function in src/todo/cli/menu.py (prompts for ID and confirmation)
- [ ] T055 [US4] Add error handling for invalid task IDs in src/todo/cli/menu.py
- [ ] T056 [US4] Verify all US4 tests pass (GREEN phase complete)

**Checkpoint**: Full CRUD operations now available - users can manage their task list completely

---

## Phase 7: User Story 5 - Update Task Details (Priority: P3)

**Goal**: Users can update a task's title or description to correct mistakes or add information

**Independent Test**: Create a task, update its title and/or description, verify changes are reflected

### Tests for User Story 5 (TDD - RED phase)

- [ ] T057 [P] [US5] Write unit test for update_task() with title only in tests/unit/test_task_manager.py
- [ ] T058 [P] [US5] Write unit test for update_task() with description only in tests/unit/test_task_manager.py
- [ ] T059 [P] [US5] Write unit test for update_task() with both title and description in tests/unit/test_task_manager.py
- [ ] T060 [P] [US5] Write unit test for update_task() with invalid data in tests/unit/test_task_manager.py
- [ ] T061 [P] [US5] Write integration test for task updates in tests/integration/test_memory_repository.py
- [ ] T062 [P] [US5] Write E2E test for update task CLI command in tests/e2e/test_cli_operations.py

### Implementation for User Story 5 (GREEN phase)

- [ ] T063 [US5] Implement MemoryRepository.update_task() in src/todo/storage/memory_repository.py
- [ ] T064 [US5] Implement MemoryRepository.get_task() for retrieving single task in src/todo/storage/memory_repository.py
- [ ] T065 [US5] Implement TaskManager.update_task() with validation in src/todo/domain/task_manager.py
- [ ] T066 [US5] Implement TaskManager.get_task() in src/todo/domain/task_manager.py
- [ ] T067 [US5] Add menu option 4 (Update task) to CLI menu in src/todo/cli/menu.py
- [ ] T068 [US5] Implement update_task() function in src/todo/cli/menu.py (prompts for ID and new values)
- [ ] T069 [US5] Add error handling for invalid task IDs and validation errors in src/todo/cli/menu.py
- [ ] T070 [US5] Verify all US5 tests pass (GREEN phase complete)

**Checkpoint**: All 5 Basic Level features complete - full Phase 1 functionality delivered

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T071 [P] Add menu option 6 (Exit) with goodbye message in src/todo/cli/menu.py
- [ ] T072 [P] Improve CLI display formatting (colors, borders, clear screen) in src/todo/cli/display.py
- [ ] T073 [P] Add input validation for menu choices in src/todo/cli/menu.py
- [ ] T074 [P] Update README.md with complete usage instructions and examples
- [ ] T075 [P] Create demo script showing all 5 operations in action
- [ ] T076 Run full test suite with coverage report (uv run pytest --cov=src/todo)
- [ ] T077 Verify test coverage >80% for domain logic
- [ ] T078 Manual testing following quickstart.md validation scenarios
- [ ] T079 [P] Code cleanup and refactoring (remove dead code, improve naming)
- [ ] T080 Final verification: All acceptance criteria from spec.md met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) after Phase 2
  - Or sequentially in priority order: US1 → US2 → US3 → US4 → US5
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - No dependencies on other stories (but works with US1)
- **User Story 3 (P2)**: Can start after Foundational - Works with US1 and US2 but independently testable
- **User Story 4 (P3)**: Can start after Foundational - Works with US1 but independently testable
- **User Story 5 (P3)**: Can start after Foundational - Works with US1 but independently testable

### Within Each User Story

- Tests (RED phase) MUST be written and FAIL before implementation
- Implementation (GREEN phase) makes tests pass
- Repository layer before TaskManager layer
- TaskManager before CLI layer
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T003, T004, T005, T006, T007 can run in parallel
- **Phase 2 (Foundational)**: T009, T010 can run in parallel (different files)
- **Within each User Story**: All test tasks marked [P] can run in parallel (RED phase)
- **Across User Stories**: After Phase 2, all user stories can start in parallel (if team capacity allows)
- **Phase 8 (Polish)**: T071, T072, T073, T074, T075, T079 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (RED phase):
Task T015: "Write unit test for get_all_tasks() in tests/unit/test_task_manager.py"
Task T016: "Write integration test for MemoryRepository.get_all_tasks() in tests/integration/test_memory_repository.py"
Task T017: "Write E2E test for view tasks CLI command in tests/e2e/test_cli_operations.py"

# Then implement sequentially (GREEN phase):
Task T018: "Implement MemoryRepository.get_all_tasks()"
Task T019: "Implement TaskManager.get_all_tasks()"
Task T020: "Create CLI menu structure"
Task T021: "Implement view_tasks() function"
Task T022: "Create __main__.py entry point"
Task T023: "Verify all US1 tests pass"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T014) - CRITICAL
3. Complete Phase 3: User Story 1 - View Tasks (T015-T023)
4. Complete Phase 4: User Story 2 - Add Tasks (T024-T033)
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy/demo if ready - users can add and view tasks (minimal viable todo app)

### Incremental Delivery

1. Setup + Foundational → Foundation ready (T001-T014)
2. Add User Story 1 → Test independently → Can view tasks (T015-T023)
3. Add User Story 2 → Test independently → Can add and view tasks (T024-T033) - **MVP!**
4. Add User Story 3 → Test independently → Can mark complete (T034-T046)
5. Add User Story 4 → Test independently → Can delete tasks (T047-T056)
6. Add User Story 5 → Test independently → Can update tasks (T057-T070)
7. Polish → Final validation (T071-T080)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T014)
2. Once Foundational is done:
   - Developer A: User Story 1 (T015-T023)
   - Developer B: User Story 2 (T024-T033)
   - Developer C: User Story 3 (T034-T046)
3. Stories complete and integrate independently
4. Continue with US4 and US5 in parallel or sequentially

---

## Task Summary

**Total Tasks**: 80 tasks across 8 phases

**Task Count by Phase**:
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 7 tasks
- Phase 3 (US1 - View): 9 tasks (3 tests + 6 implementation)
- Phase 4 (US2 - Add): 10 tasks (4 tests + 6 implementation)
- Phase 5 (US3 - Mark Complete): 13 tasks (5 tests + 8 implementation)
- Phase 6 (US4 - Delete): 10 tasks (4 tests + 6 implementation)
- Phase 7 (US5 - Update): 14 tasks (6 tests + 8 implementation)
- Phase 8 (Polish): 10 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phase

**Independent Test Criteria**:
- US1: View empty list and list with tasks
- US2: Add task and verify it appears in list
- US3: Mark task complete/incomplete and verify status change
- US4: Delete task and verify it's removed from list
- US5: Update task and verify changes are reflected

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2) = 33 tasks
This delivers a minimal viable todo app where users can add and view tasks.

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story follows TDD: RED (tests first) → GREEN (implementation) → REFACTOR (polish)
- Tests MUST fail before implementation (RED phase)
- Verify tests pass after implementation (GREEN phase)
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution requires TDD approach - all test tasks are mandatory
