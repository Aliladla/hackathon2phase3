# Implementation Plan: Todo Full-Stack Web Application (Phase 2)

**Branch**: `002-fullstack-web-app` | **Date**: 2025-02-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web-app/spec.md`

## Summary

Build a multi-user web application with authentication and database persistence. Frontend uses Next.js 16+ with TypeScript and Tailwind CSS. Backend uses FastAPI with SQLModel ORM connected to Neon PostgreSQL. Implement all 5 Basic Level task management features (Add, Delete, Update, View, Mark Complete) as RESTful API endpoints with JWT authentication. Reuse Phase 1 domain logic (Task entity, TaskManager) in FastAPI backend, adapted for multi-user support with user_id filtering.

**Technical Approach**: Monorepo structure with separate frontend and backend. Backend extends Phase 1 domain logic with database persistence and user authentication. Frontend provides responsive web UI with Better Auth for authentication. RESTful API with JWT tokens for secure communication.

## Technical Context

**Frontend:**
- **Language/Version**: TypeScript 5.x with Next.js 16+ (App Router)
- **Primary Dependencies**: React 19, Tailwind CSS 4.x, Better Auth, React Hook Form, Axios
- **Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- **Performance Goals**: First Contentful Paint < 1.5s, Time to Interactive < 3s
- **Constraints**: Responsive design (320px minimum width), client-side validation

**Backend:**
- **Language/Version**: Python 3.13+
- **Primary Dependencies**: FastAPI, SQLModel, Pydantic, python-jose (JWT), passlib (password hashing)
- **Storage**: Neon Serverless PostgreSQL
- **Testing**: pytest with FastAPI TestClient
- **Target Platform**: Linux server (Railway/Render)
- **Performance Goals**: API response time < 500ms p95, handle 100 concurrent users
- **Constraints**: Stateless API (JWT-based auth), CORS enabled for frontend

**Project Type**: Web application (frontend + backend monorepo)
**Scale/Scope**: Multi-user (100+ users), 1000+ tasks per user, 6 user stories

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| **I. Spec-Driven Development** | Follow Specify → Plan → Tasks → Implement workflow | ✅ PASS | Currently in Plan phase after Specify |
| **II. Test-First Development** | TDD with pytest (backend) and Jest/Vitest (frontend) | ✅ PASS | Tests before implementation for both layers |
| **III. Modular Architecture** | Reuse Phase 1 domain logic, clear frontend/backend separation | ✅ PASS | Backend reuses Phase 1 domain, frontend is separate layer |
| **IV. Simple CLI Interface** | N/A for Phase 2 (web interface) | ✅ PASS | Web UI replaces CLI, principle not applicable |
| **V. Minimal Viable Implementation** | Only Basic Level features + authentication | ✅ PASS | No intermediate/advanced features |
| **VI. Fast Iteration with UV** | Use UV for backend Python dependencies | ✅ PASS | UV for backend, npm/pnpm for frontend |

**Gate Result**: ✅ ALL CHECKS PASSED - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Technical decisions and rationale
├── data-model.md        # Phase 1: Entity definitions and relationships
├── quickstart.md        # Phase 1: Setup and usage instructions
├── contracts/           # Phase 1: API contracts
│   └── api-endpoints.md # RESTful API specification
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
hackathon2phase1/        # Project root (monorepo)
├── .gitignore
├── README.md
│
├── backend/             # FastAPI backend
│   ├── pyproject.toml   # UV project configuration
│   ├── .python-version  # Python 3.13
│   ├── alembic.ini      # Database migrations config
│   │
│   ├── src/
│   │   └── backend/
│   │       ├── __init__.py
│   │       ├── main.py          # FastAPI app entry point
│   │       ├── config.py        # Environment configuration
│   │       │
│   │       ├── domain/          # Reused from Phase 1
│   │       │   ├── __init__.py
│   │       │   ├── task.py      # Task entity (adapted for DB)
│   │       │   ├── task_manager.py  # Business logic
│   │       │   └── exceptions.py    # Custom exceptions
│   │       │
│   │       ├── models/          # SQLModel database models
│   │       │   ├── __init__.py
│   │       │   ├── user.py      # User model
│   │       │   └── task.py      # Task model with user_id
│   │       │
│   │       ├── repositories/    # Database access layer
│   │       │   ├── __init__.py
│   │       │   ├── user_repository.py
│   │       │   └── task_repository.py
│   │       │
│   │       ├── api/             # API routes
│   │       │   ├── __init__.py
│   │       │   ├── auth.py      # Authentication endpoints
│   │       │   └── tasks.py     # Task CRUD endpoints
│   │       │
│   │       ├── middleware/      # Middleware
│   │       │   ├── __init__.py
│   │       │   └── auth.py      # JWT authentication middleware
│   │       │
│   │       └── database.py      # Database connection
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Pytest fixtures
│   │   ├── unit/                # Unit tests
│   │   │   ├── test_task.py
│   │   │   └── test_task_manager.py
│   │   ├── integration/         # Integration tests
│   │   │   ├── test_repositories.py
│   │   │   └── test_database.py
│   │   └── api/                 # API endpoint tests
│   │       ├── test_auth.py
│   │       └── test_tasks.py
│   │
│   └── alembic/                 # Database migrations
│       ├── versions/
│       └── env.py
│
└── frontend/            # Next.js frontend
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── next.config.ts
    │
    ├── src/
    │   ├── app/                 # Next.js App Router
    │   │   ├── layout.tsx       # Root layout
    │   │   ├── page.tsx         # Home/redirect
    │   │   ├── (auth)/          # Auth route group
    │   │   │   ├── signin/
    │   │   │   │   └── page.tsx
    │   │   │   └── signup/
    │   │   │       └── page.tsx
    │   │   └── (app)/           # Protected route group
    │   │       └── tasks/
    │   │           └── page.tsx
    │   │
    │   ├── components/          # React components
    │   │   ├── ui/              # Reusable UI components
    │   │   │   ├── Button.tsx
    │   │   │   ├── Input.tsx
    │   │   │   └── Card.tsx
    │   │   ├── auth/            # Auth components
    │   │   │   ├── SignInForm.tsx
    │   │   │   └── SignUpForm.tsx
    │   │   └── tasks/           # Task components
    │   │       ├── TaskList.tsx
    │   │       ├── TaskItem.tsx
    │   │       ├── TaskForm.tsx
    │   │       └── TaskActions.tsx
    │   │
    │   ├── lib/                 # Utilities
    │   │   ├── api.ts           # API client (Axios)
    │   │   ├── auth.ts          # Better Auth config
    │   │   └── utils.ts         # Helper functions
    │   │
    │   └── types/               # TypeScript types
    │       ├── task.ts
    │       └── user.ts
    │
    └── tests/                   # Frontend tests
        ├── components/
        └── integration/
```

**Structure Decision**: Monorepo with separate frontend and backend directories selected because:
- Clear separation of concerns (frontend/backend)
- Independent deployment (Vercel for frontend, Railway/Render for backend)
- Backend reuses Phase 1 domain logic in `backend/src/backend/domain/`
- Frontend and backend can be developed in parallel
- Single repository simplifies Phase 2 development and submission

## Complexity Tracking

> **No violations detected** - All constitution principles satisfied without exceptions.

---

## Phase 0: Research & Technical Decisions

See [research.md](./research.md) for detailed technical decisions and rationale.

## Phase 1: Design Artifacts

- **Data Model**: [data-model.md](./data-model.md) - User and Task entities with relationships
- **Contracts**: [contracts/](./contracts/) - RESTful API endpoints specification
- **Quickstart**: [quickstart.md](./quickstart.md) - Setup and usage guide

## Next Steps

1. ✅ Specification complete (spec.md)
2. ✅ Planning complete (this file)
3. ⏭️ Run `/sp.tasks` to generate implementation tasks
4. ⏭️ Run `/sp.implement` to execute tasks with TDD workflow
