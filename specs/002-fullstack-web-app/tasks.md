# Implementation Tasks: Todo Full-Stack Web Application (Phase 2)

**Branch**: `002-fullstack-web-app` | **Date**: 2025-02-15
**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Summary

This document breaks down Phase 2 implementation into actionable tasks organized by user story. Each phase represents a complete, independently testable increment of functionality.

**Total Tasks**: 95 tasks across 9 phases
**Estimated Effort**: 3-4 days for full implementation
**MVP Scope**: Phases 1-5 (Setup + US1 + US2 + US3) = 52 tasks

---

## Task Organization

Tasks are organized by user story to enable independent implementation and testing:

- **Phase 1**: Setup (12 tasks) - Project initialization and configuration
- **Phase 2**: Foundational (15 tasks) - Database models and auth middleware (blocking for all stories)
- **Phase 3**: US1 - User Authentication (13 tasks) - Signup, signin, signout
- **Phase 4**: US2 - View Tasks (12 tasks) - List user's tasks
- **Phase 5**: US3 - Add Task (10 tasks) - Create tasks via web form
- **Phase 6**: US4 - Mark Complete (8 tasks) - Toggle completion status
- **Phase 7**: US5 - Update Task (10 tasks) - Edit task details
- **Phase 8**: US6 - Delete Task (8 tasks) - Remove tasks
- **Phase 9**: Polish & Cross-Cutting (7 tasks) - Error handling, responsive design

**Parallel Execution**: Tasks marked with [P] can run in parallel with other [P] tasks in the same phase.

---

## Phase 1: Setup (Project Initialization)

**Goal**: Initialize monorepo structure with backend and frontend projects

**Independent Test**: Both backend and frontend servers start without errors

### Backend Setup

- [ ] T001 Create backend directory structure per plan.md (backend/src/backend/, backend/tests/)
- [ ] T002 Initialize UV project in backend/ with pyproject.toml
- [ ] T003 Add backend dependencies to pyproject.toml (fastapi, sqlmodel, pydantic, python-jose, passlib, bcrypt, psycopg2-binary, uvicorn, python-multipart, alembic)
- [ ] T004 Add backend dev dependencies (pytest, pytest-asyncio, httpx)
- [ ] T005 Create backend/.env.example with DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS, CORS_ORIGINS
- [ ] T006 Create backend/.gitignore with __pycache__/, *.pyc, .venv/, venv/, dist/, *.egg-info/, .env, .DS_Store

### Frontend Setup

- [ ] T007 Create frontend directory structure per plan.md (frontend/src/app/, frontend/src/components/, frontend/src/lib/, frontend/src/types/)
- [ ] T008 Initialize Next.js 16+ project in frontend/ with TypeScript and Tailwind CSS
- [ ] T009 Add frontend dependencies to package.json (next, react, react-dom, typescript, tailwindcss, better-auth, axios, react-hook-form, zod)
- [ ] T010 Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, NEXT_PUBLIC_APP_NAME
- [ ] T011 Create frontend/.gitignore with node_modules/, .next/, dist/, build/, *.log, .env*, .DS_Store
- [ ] T012 Create root README.md with Phase 2 overview and quickstart instructions

---

## Phase 2: Foundational (Database & Auth Infrastructure)

**Goal**: Set up database models, migrations, and JWT authentication middleware (blocking for all user stories)

**Independent Test**: Database tables created, JWT middleware validates tokens correctly

### Database Models

- [ ] T013 [P] Create backend/src/backend/database.py with SQLModel engine and session management
- [ ] T014 [P] Create backend/src/backend/models/user.py with User SQLModel (id, email, password_hash, created_at)
- [ ] T015 [P] Create backend/src/backend/models/task.py with Task SQLModel (id, user_id, title, description, completed, created_at, updated_at)
- [ ] T016 Initialize Alembic in backend/ with alembic init alembic
- [ ] T017 Create Alembic migration 001_initial_schema.py with users and tasks tables
- [ ] T018 Add database indexes to migration (idx_users_email, idx_tasks_user_id, idx_tasks_completed, idx_tasks_user_completed)
- [ ] T019 Add updated_at trigger to migration for tasks table

### Repositories

- [ ] T020 [P] Create backend/src/backend/repositories/user_repository.py with UserRepository (create, get_by_id, get_by_email, exists_by_email)
- [ ] T021 [P] Create backend/src/backend/repositories/task_repository.py with TaskRepository (create, get_by_id, list_all, update, delete, toggle_complete) - all methods filter by user_id

### Authentication Infrastructure

- [ ] T022 Create backend/src/backend/config.py with environment variable loading (DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS, CORS_ORIGINS)
- [ ] T023 Create backend/src/backend/middleware/auth.py with JWT token validation middleware (extract user_id from token)
- [ ] T024 Create backend/src/backend/api/dependencies.py with get_current_user dependency (extracts user_id from JWT)
- [ ] T025 Create backend/src/backend/utils/password.py with password hashing functions (hash_password, verify_password using passlib/bcrypt)
- [ ] T026 Create backend/src/backend/utils/jwt.py with JWT token functions (create_token, decode_token using python-jose)
- [ ] T027 Create backend/src/backend/main.py with FastAPI app, CORS middleware, and health check endpoint

---

## Phase 3: US1 - User Authentication (P1 - MVP)

**Goal**: Users can create accounts, sign in, and sign out

**User Story**: As a new user, I want to create an account and sign in so I can access my personal todo list from any device.

**Independent Test**: User can signup, signin, signout, and JWT token is issued/validated correctly

### Backend - Auth Endpoints

- [ ] T028 [US1] Create backend/src/backend/api/auth.py with router setup
- [ ] T029 [US1] Implement POST /api/auth/signup endpoint (validate email/password, hash password, create user, return JWT token)
- [ ] T030 [US1] Implement POST /api/auth/signin endpoint (validate credentials, verify password, return JWT token)
- [ ] T031 [US1] Implement POST /api/auth/signout endpoint (return success message - client-side token deletion)
- [ ] T032 [US1] Add auth router to main.py with /api/auth prefix

### Frontend - Auth UI

- [ ] T033 [P] [US1] Create frontend/src/types/user.ts with User and AuthResponse types
- [ ] T034 [P] [US1] Create frontend/src/lib/api.ts with Axios client configured with base URL and auth interceptors
- [ ] T035 [P] [US1] Create frontend/src/lib/auth.ts with Better Auth configuration (JWT storage, token refresh)
- [ ] T036 [US1] Create frontend/src/app/(auth)/layout.tsx with auth pages layout (centered form, no navigation)
- [ ] T037 [US1] Create frontend/src/components/auth/SignUpForm.tsx with email/password form using react-hook-form and zod validation
- [ ] T038 [US1] Create frontend/src/app/(auth)/signup/page.tsx with SignUpForm and signup API call
- [ ] T039 [US1] Create frontend/src/components/auth/SignInForm.tsx with email/password form
- [ ] T040 [US1] Create frontend/src/app/(auth)/signin/page.tsx with SignInForm and signin API call

### Integration & Testing

- [ ] T041 [US1] Test signup flow: create account, receive JWT token, verify user in database
- [ ] T042 [US1] Test signin flow: authenticate with correct credentials, receive JWT token
- [ ] T043 [US1] Test error handling: duplicate email (409), invalid credentials (401), validation errors (400)

---

## Phase 4: US2 - View Tasks (P1 - MVP)

**Goal**: Signed-in users can view all their tasks in a web interface

**User Story**: As a signed-in user, I want to see all my tasks in a web interface so I can manage my todo list from any browser.

**Independent Test**: User can sign in and see their task list (empty or populated), other users' tasks are not visible

### Backend - List Tasks Endpoint

- [ ] T044 [US2] Create backend/src/backend/api/tasks.py with router setup
- [ ] T045 [US2] Implement GET /api/tasks endpoint with user_id filtering (extract user_id from JWT via dependency)
- [ ] T046 [US2] Add query parameters to GET /api/tasks (completed filter, limit, offset for pagination)
- [ ] T047 [US2] Implement GET /api/tasks/{task_id} endpoint with user_id filtering (return 404 if not found or wrong user)
- [ ] T048 [US2] Add tasks router to main.py with /api/tasks prefix and auth dependency

### Frontend - Task List UI

- [ ] T049 [P] [US2] Create frontend/src/types/task.ts with Task and TaskListResponse types
- [ ] T050 [P] [US2] Create frontend/src/components/ui/Card.tsx with reusable card component (Tailwind CSS)
- [ ] T051 [US2] Create frontend/src/app/(app)/layout.tsx with protected pages layout (navigation with signout button)
- [ ] T052 [US2] Create frontend/src/components/tasks/TaskItem.tsx with task display (title, description, completion status, actions)
- [ ] T053 [US2] Create frontend/src/components/tasks/TaskList.tsx with task list rendering (map over tasks, empty state)
- [ ] T054 [US2] Create frontend/src/app/(app)/tasks/page.tsx with task list page (fetch tasks on mount, display TaskList)

### Integration & Testing

- [ ] T055 [US2] Test view tasks: user sees only their tasks, empty state for new users, populated list for existing tasks

---

## Phase 5: US3 - Add Task (P1 - MVP)

**Goal**: Signed-in users can add new tasks through a web form

**User Story**: As a signed-in user, I want to add a new task through a web form so I can track things I need to do.

**Independent Test**: User can submit task form, task appears in list immediately, validation errors are shown

### Backend - Create Task Endpoint

- [ ] T056 [US3] Create backend/src/backend/domain/task.py with Task entity validation (reuse from Phase 1, adapt for user_id)
- [ ] T057 [US3] Create backend/src/backend/domain/task_manager.py with TaskManager business logic (reuse from Phase 1, add user_id parameter)
- [ ] T058 [US3] Create backend/src/backend/domain/exceptions.py with custom exceptions (InvalidTaskDataError, TaskNotFoundError - reuse from Phase 1)
- [ ] T059 [US3] Implement POST /api/tasks endpoint with user_id from JWT (validate title 1-200 chars, description 0-1000 chars)
- [ ] T060 [US3] Add validation error responses (400) with field-specific error messages

### Frontend - Add Task Form

- [ ] T061 [P] [US3] Create frontend/src/components/ui/Input.tsx with reusable input component (Tailwind CSS)
- [ ] T062 [P] [US3] Create frontend/src/components/ui/Button.tsx with reusable button component (Tailwind CSS, loading state)
- [ ] T063 [US3] Create frontend/src/components/tasks/TaskForm.tsx with title/description form using react-hook-form and zod validation
- [ ] T064 [US3] Add TaskForm to frontend/src/app/(app)/tasks/page.tsx above task list
- [ ] T065 [US3] Implement optimistic UI update (add task to list immediately, rollback on error)

### Integration & Testing

- [ ] T066 [US3] Test add task: submit form with valid data, task appears in list, database updated
- [ ] T067 [US3] Test validation: empty title shows error, title > 200 chars shows error, description > 1000 chars shows error

---

## Phase 6: US4 - Mark Complete (P2)

**Goal**: Signed-in users can mark tasks as complete or incomplete

**User Story**: As a signed-in user, I want to mark tasks as complete or incomplete through the web interface so I can track my progress.

**Independent Test**: User can toggle task completion, status updates immediately, visual indicator changes

### Backend - Toggle Complete Endpoint

- [ ] T068 [US4] Implement PATCH /api/tasks/{task_id}/complete endpoint (toggle completed field, return updated task)
- [ ] T069 [US4] Add user_id filtering to ensure user can only toggle their own tasks (return 404 for other users' tasks)

### Frontend - Complete Checkbox

- [ ] T070 [US4] Add checkbox to TaskItem component for completion status
- [ ] T071 [US4] Implement toggle complete handler in TaskItem (call API, update local state)
- [ ] T072 [US4] Add visual indicator for completed tasks (strikethrough title, different background color)
- [ ] T073 [US4] Implement optimistic UI update (toggle immediately, rollback on error)

### Integration & Testing

- [ ] T074 [US4] Test mark complete: click checkbox, task status updates, visual indicator changes
- [ ] T075 [US4] Test mark incomplete: click checkbox on completed task, status reverts, visual indicator changes

---

## Phase 7: US5 - Update Task (P2)

**Goal**: Signed-in users can update task title and description

**User Story**: As a signed-in user, I want to update a task's title or description through the web interface so I can correct mistakes or add information.

**Independent Test**: User can edit task, changes are saved, validation errors are shown

### Backend - Update Task Endpoint

- [ ] T076 [US5] Implement PUT /api/tasks/{task_id} endpoint (full update with title, description, completed)
- [ ] T077 [US5] Implement PATCH /api/tasks/{task_id} endpoint (partial update, only specified fields)
- [ ] T078 [US5] Add validation to update endpoints (title 1-200 chars, description 0-1000 chars)
- [ ] T079 [US5] Add user_id filtering to ensure user can only update their own tasks

### Frontend - Edit Task Form

- [ ] T080 [US5] Add edit mode state to TaskItem component (toggle between view and edit)
- [ ] T081 [US5] Create inline edit form in TaskItem with title/description inputs
- [ ] T082 [US5] Implement save handler (call PUT /api/tasks/{id}, update local state)
- [ ] T083 [US5] Implement cancel handler (revert to original values, exit edit mode)
- [ ] T084 [US5] Add edit button to TaskItem actions

### Integration & Testing

- [ ] T085 [US5] Test update task: edit title, save, changes reflected in list and database
- [ ] T086 [US5] Test validation: empty title shows error, changes not saved

---

## Phase 8: US6 - Delete Task (P3)

**Goal**: Signed-in users can delete tasks permanently

**User Story**: As a signed-in user, I want to delete tasks I no longer need through the web interface so my list stays relevant.

**Independent Test**: User can delete task, task is removed from list and database, confirmation prompt is shown

### Backend - Delete Task Endpoint

- [ ] T087 [US6] Implement DELETE /api/tasks/{task_id} endpoint (return 204 No Content on success)
- [ ] T088 [US6] Add user_id filtering to ensure user can only delete their own tasks (return 404 for other users' tasks)

### Frontend - Delete Button

- [ ] T089 [US6] Add delete button to TaskItem actions
- [ ] T090 [US6] Implement delete confirmation dialog (modal or browser confirm)
- [ ] T091 [US6] Implement delete handler (call DELETE /api/tasks/{id}, remove from local state)
- [ ] T092 [US6] Implement optimistic UI update (remove immediately, rollback on error)

### Integration & Testing

- [ ] T093 [US6] Test delete task: click delete, confirm, task removed from list and database
- [ ] T094 [US6] Test cancel delete: click delete, cancel confirmation, task remains in list

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Improve user experience with error handling, loading states, and responsive design

**Independent Test**: Application handles errors gracefully, shows loading indicators, works on mobile devices

### Cross-Cutting Improvements

- [ ] T095 [P] Add loading states to all API calls (spinner or skeleton screens)
- [ ] T096 [P] Add error notifications for failed API calls (toast or alert component)
- [ ] T097 [P] Add success notifications for successful actions (task added, updated, deleted)
- [ ] T098 [P] Implement responsive design for mobile (320px minimum width, touch-friendly buttons)
- [ ] T099 [P] Add form validation feedback (inline error messages, field highlighting)
- [ ] T100 [P] Add empty state illustrations (no tasks, no search results)
- [ ] T101 [P] Add keyboard shortcuts (Enter to submit forms, Escape to cancel)

---

## Dependencies & Execution Order

### Critical Path (Must Complete in Order)

1. **Phase 1 (Setup)** → Blocks all other phases
2. **Phase 2 (Foundational)** → Blocks all user story phases
3. **Phase 3 (US1 - Auth)** → Blocks all task management phases (US2-US6)
4. **Phase 4 (US2 - View)** → Recommended before US3-US6 (need to see tasks to test other features)
5. **Phases 5-8 (US3-US6)** → Can be done in any order after US2
6. **Phase 9 (Polish)** → Can be done anytime, recommended last

### Parallel Opportunities

**Within Phase 2 (Foundational)**:
- T013, T014, T015 (models) can run in parallel
- T020, T021 (repositories) can run in parallel after models

**Within Phase 3 (US1 - Auth)**:
- T033, T034, T035 (frontend types/utils) can run in parallel
- T037, T039 (auth forms) can run in parallel

**Within Phase 4 (US2 - View)**:
- T049, T050 (frontend types/components) can run in parallel

**Within Phase 5 (US3 - Add)**:
- T056, T057, T058 (backend domain logic) can run in parallel
- T061, T062 (UI components) can run in parallel

**Within Phase 9 (Polish)**:
- All tasks (T095-T101) can run in parallel

---

## Implementation Strategy

### MVP First (Phases 1-5)

Focus on core value delivery:
1. Setup project structure (Phase 1)
2. Build authentication foundation (Phases 2-3)
3. Enable viewing tasks (Phase 4)
4. Enable adding tasks (Phase 5)

**MVP Deliverable**: Users can sign up, sign in, view tasks, and add tasks (52 tasks)

### Incremental Delivery (Phases 6-8)

Add task management features incrementally:
1. Mark complete (Phase 6) - 8 tasks
2. Update task (Phase 7) - 10 tasks
3. Delete task (Phase 8) - 8 tasks

**Full Feature Set**: All 6 user stories implemented (78 tasks)

### Polish & Optimization (Phase 9)

Improve user experience:
1. Error handling and notifications
2. Loading states and feedback
3. Responsive design for mobile
4. Keyboard shortcuts

**Production Ready**: Polished application ready for deployment (85 tasks)

---

## Testing Strategy

### Unit Tests (Backend)

- Task entity validation (title length, description length)
- Password hashing and verification
- JWT token creation and validation
- Repository methods (CRUD operations)

### Integration Tests (Backend)

- Auth endpoints (signup, signin, signout)
- Task endpoints (create, list, get, update, delete, toggle)
- User isolation (cannot access other users' tasks)
- Database constraints (foreign keys, unique emails)

### Component Tests (Frontend)

- Auth forms (validation, submission)
- Task list rendering (empty state, populated list)
- Task item actions (complete, edit, delete)
- Form validation (error messages, field highlighting)

### End-to-End Tests

- Complete user flows (signup → add task → mark complete → delete)
- Authentication persistence (refresh page, remain signed in)
- User isolation (create two users, verify task separation)

---

## Validation Checklist

After completing all tasks, verify:

- [ ] All 6 user stories are implemented and testable
- [ ] All 23 functional requirements from spec.md are met
- [ ] All 10 success criteria from spec.md are achieved
- [ ] Backend API matches contracts/api-endpoints.md specification
- [ ] Database schema matches data-model.md specification
- [ ] Frontend UI is responsive (320px minimum width)
- [ ] User isolation is enforced (users cannot see other users' tasks)
- [ ] Authentication works (signup, signin, signout, token persistence)
- [ ] All CRUD operations work (create, read, update, delete tasks)
- [ ] Error handling is graceful (validation errors, network errors, auth errors)

---

## Notes

- All tasks follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- Tasks marked [P] can run in parallel with other [P] tasks in the same phase
- Tasks marked [US1]-[US6] belong to specific user stories
- Setup and Foundational phases have no story labels (shared infrastructure)
- Polish phase has no story labels (cross-cutting concerns)
- Each phase is independently testable with clear acceptance criteria
- MVP scope (Phases 1-5) delivers core value in 52 tasks
- Full implementation (Phases 1-9) completes all features in 101 tasks

**Ready for Implementation**: Run `/sp.implement` to execute tasks with TDD workflow
