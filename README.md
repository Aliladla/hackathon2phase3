# Todo Application - Hackathon Project

**Evolution of Todo**: Multi-phase hackathon project building from console app to AI-powered web application

## Current Status

- ✅ **Phase 1**: Console application with in-memory storage (COMPLETED)
- ✅ **Phase 2**: Full-stack web application with authentication and database (COMPLETED)
- ⏭️ **Phase 3**: AI-powered chatbot interface (UPCOMING)

## Phase 2: Full-Stack Web Application

A modern, multi-user todo application with authentication and database persistence.

### Features

- ✅ User authentication (signup, signin, signout)
- ✅ JWT-based session management (7-day expiration)
- ✅ Task management (add, view, update, delete, mark complete)
- ✅ User isolation (private task lists)
- ✅ Database persistence (Neon PostgreSQL)
- ✅ Responsive web UI (Next.js + TypeScript + Tailwind CSS)
- ✅ RESTful API (FastAPI with automatic docs)

### Tech Stack

**Backend:**
- Python 3.13+ with FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL
- JWT authentication with python-jose
- Bcrypt password hashing

**Frontend:**
- Next.js 16+ (App Router)
- TypeScript 5.7+
- Tailwind CSS 4.x
- Axios HTTP client
- React Hook Form + Zod validation

## Phase 1: Console Application

A command-line todo application with in-memory storage featuring 5 Basic Level operations:
1. View all tasks
2. Add new task
3. Mark task complete/incomplete
4. Update task details
5. Delete task

## Quick Start

### Phase 2 Setup (Full-Stack Web App)

**Prerequisites:**
- Python 3.13+, UV package manager
- Node.js 20+, npm/pnpm
- Neon PostgreSQL account

**Backend Setup:**
```bash
cd backend

# Create .env file from example
cp .env.example .env
# Edit .env with your DATABASE_URL and JWT_SECRET

# Install dependencies
uv sync

# Run migrations
uv run alembic upgrade head

# Start backend server
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

**Frontend Setup:**
```bash
cd frontend

# Create .env.local file from example
cp .env.local.example .env.local
# Edit .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000

# Install dependencies
pnpm install  # or npm install

# Start frontend server
pnpm dev  # or npm run dev
```

Frontend available at: http://localhost:3000

### Phase 1 Setup (Console App)

```bash
# Install dependencies
uv sync

# Run the application
uv run python -m todo
```

## Usage

### Phase 2 (Web Application)

1. **Sign Up**: Create account at http://localhost:3000/signup
2. **Sign In**: Sign in at http://localhost:3000/signin
3. **Manage Tasks**: Add, view, edit, complete, and delete tasks
4. **Sign Out**: Click "Sign Out" in navigation

### Phase 1 (Console Application)

Interactive menu with 6 options:
1. View all tasks
2. Add new task
3. Mark task complete/incomplete
4. Update task
5. Delete task
6. Exit

## API Documentation

Full API documentation available at http://localhost:8000/docs (Swagger UI)

**Key Endpoints:**
- `POST /api/auth/signup` - Create account
- `POST /api/auth/signin` - Sign in
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create task
- `PATCH /api/tasks/{id}/complete` - Toggle completion
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Testing

**Backend Tests:**
```bash
cd backend
uv run pytest
```

**Frontend Tests:**
```bash
cd frontend
pnpm test
```

**Phase 1 Tests:**
```bash
uv run pytest --cov=src/todo --cov-report=html
```

## Architecture

### Phase 2 Architecture

**Backend:**
- **Domain Layer**: Business logic (Task entity, TaskManager - reused from Phase 1)
- **Models Layer**: SQLModel database models (User, Task)
- **Repositories Layer**: Database access (UserRepository, TaskRepository)
- **API Layer**: FastAPI endpoints (auth, tasks)
- **Middleware**: JWT authentication
- **Utils**: Password hashing, JWT tokens

**Frontend:**
- **App Router**: Next.js 16+ file-based routing
- **Components**: Reusable UI components (Button, Input, Card)
- **Auth Components**: SignUpForm, SignInForm
- **Task Components**: TaskForm, TaskItem, TaskList
- **API Client**: Axios with interceptors
- **Types**: TypeScript interfaces

### Phase 1 Architecture

- **Domain Layer** (`src/todo/domain/`): Core business logic
- **Storage Layer** (`src/todo/storage/`): In-memory repository
- **CLI Layer** (`src/todo/cli/`): User interface

## Project Documentation

Detailed documentation in `specs/` directory:

**Phase 2:**
- `specs/002-fullstack-web-app/spec.md` - Feature specification
- `specs/002-fullstack-web-app/plan.md` - Implementation plan
- `specs/002-fullstack-web-app/research.md` - Technical decisions
- `specs/002-fullstack-web-app/data-model.md` - Database schema
- `specs/002-fullstack-web-app/contracts/api-endpoints.md` - API specification
- `specs/002-fullstack-web-app/quickstart.md` - Setup guide
- `specs/002-fullstack-web-app/tasks.md` - Implementation tasks

**Phase 1:**
- `specs/001-todo-console-app/spec.md` - Feature specification
- `specs/001-todo-console-app/plan.md` - Implementation plan

## Deployment

**Recommended Platforms:**
- Backend: Railway or Render
- Frontend: Vercel
- Database: Neon (serverless PostgreSQL)

See `specs/002-fullstack-web-app/quickstart.md` for detailed deployment instructions.

## License

MIT
