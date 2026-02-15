# Todo Application - Hackathon Project

**Evolution of Todo**: Multi-phase hackathon project building from console app to AI-powered web application

## Current Status

- ✅ **Phase 1**: Console application with in-memory storage (COMPLETED)
- ✅ **Phase 2**: Full-stack web application with authentication and database (COMPLETED)
- ✅ **Phase 3**: AI-powered chatbot interface with OpenAI integration (COMPLETED)

## Phase 3: AI-Powered Chatbot Interface

Natural language task management powered by OpenAI GPT-4 and MCP tools.

### Features

- ✅ Natural language understanding ("Add a task to buy milk")
- ✅ Context-aware conversations (remembers last task mentioned)
- ✅ OpenAI GPT-4-turbo-preview integration
- ✅ 6 MCP tools for structured API communication
- ✅ Session management (30-minute expiration)
- ✅ Interactive console interface
- ✅ REST API server for programmatic access
- ✅ Comprehensive test suite (77 tests)

### Tech Stack

**Chatbot Service:**
- Python 3.13+ with OpenAI Agents SDK
- OpenAI GPT-4-turbo-preview
- MCP (Model Context Protocol) tools
- FastAPI REST API server
- Async HTTP client (httpx)
- JWT authentication integration
- In-memory session storage

### Natural Language Commands

- **Create**: "Add a task to buy groceries"
- **View**: "Show me my tasks"
- **Complete**: "Mark task 5 as complete"
- **Update**: "Change task 3 title to Buy groceries"
- **Delete**: "Delete task 7"
- **Context**: "Mark that task complete" (uses conversation context)

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

### Phase 3 Setup (AI Chatbot)

**Prerequisites:**
- Python 3.13+, UV package manager
- OpenAI API key (get from https://platform.openai.com/api-keys)
- Phase 2 backend running at http://localhost:8000
- JWT token from Phase 2 backend

**Chatbot Setup:**
```bash
cd chatbot

# Create .env file from example
cp .env.example .env
# Edit .env with your OPENAI_API_KEY and BACKEND_API_URL

# Install dependencies
uv sync

# Validate setup
uv run python validate.py

# Run tests
uv run pytest

# Start interactive console
uv run python -m chatbot

# Or start REST API server
uv run uvicorn chatbot.server.app:app --reload --port 8001
```

Chatbot available at:
- Console: Interactive CLI interface
- API: http://localhost:8001
- Docs: http://localhost:8001/docs

**Get JWT Token:**
```bash
# Sign in to Phase 2 backend to get JWT token
curl -X POST http://localhost:8000/api/auth/signin \
  -H 'Content-Type: application/json' \
  -d '{"email": "user@example.com", "password": "password"}'
```

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

### Phase 3 (AI Chatbot)

**Interactive Console:**
```bash
cd chatbot
uv run python -m chatbot
# Enter JWT token when prompted
```

**Example Conversation:**
```
You: Add a task to buy groceries
🤖: I've added 'Buy groceries' to your list. It's task #1.

You: Show me my tasks
🤖: You have 1 task:
1. Buy groceries (not completed)

You: Mark that task as complete
🤖: Done! I've marked task #1 (Buy groceries) as complete. Great job!
```

**REST API:**
```bash
# Start server
uv run uvicorn chatbot.server.app:app --reload --port 8001

# Send message
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}'
```

**Demo Script:**
```bash
uv run python demo.py --jwt-token=YOUR_JWT_TOKEN
```

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

### Phase 3 Chatbot API

Full API documentation available at http://localhost:8001/docs (Swagger UI)

**Chatbot Endpoints:**
- `POST /chat` - Send message to chatbot (requires JWT token)
- `POST /sessions` - Create new conversation session
- `GET /sessions/{session_id}/context` - Get session context
- `DELETE /sessions/{session_id}` - Delete session
- `POST /sessions/cleanup` - Cleanup expired sessions
- `GET /health` - Health check

### Phase 2 Backend API

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

**Phase 3 Chatbot Tests:**
```bash
cd chatbot

# Run all tests
uv run pytest -v

# Run with coverage
uv run pytest --cov=chatbot --cov-report=html

# Run specific test types
uv run pytest -m unit          # Unit tests only (fast)
uv run pytest -m integration   # Integration tests
uv run pytest -m e2e           # E2E tests (requires backend + OpenAI API)

# Run specific test file
uv run pytest tests/test_agent.py -v
```

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

### Phase 3 Architecture (AI Chatbot)

**System Flow:**
```
User Input (Natural Language)
    ↓
OpenAI Agent (GPT-4)
    ↓
MCP Tools (6 tools)
    ↓
API Client (JWT Auth)
    ↓
Phase 2 Backend API
```

**Components:**
- **Agent Layer** (`chatbot/src/chatbot/agent/`): OpenAI integration, prompt management
- **MCP Tools Layer** (`chatbot/src/chatbot/mcp/`): 6 structured tools (create, list, get, update, delete, toggle)
- **API Client** (`chatbot/src/chatbot/api/`): Async HTTP client with JWT authentication
- **Conversation Context** (`chatbot/src/chatbot/conversation/`): Session management, message history
- **Server Layer** (`chatbot/src/chatbot/server/`): FastAPI REST API for programmatic access
- **Console Interface** (`chatbot/src/chatbot/__main__.py`): Interactive CLI

**MCP Tools:**
1. `create_task` - Create new tasks
2. `list_tasks` - List tasks with filtering
3. `get_task` - Get specific task by ID
4. `update_task` - Update task properties
5. `delete_task` - Delete tasks
6. `toggle_complete` - Toggle completion status

### Phase 2 Architecture (Full-Stack Web App)

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

### Phase 1 Architecture (Console App)

- **Domain Layer** (`src/todo/domain/`): Core business logic
- **Storage Layer** (`src/todo/storage/`): In-memory repository
- **CLI Layer** (`src/todo/cli/`): User interface

## Project Documentation

Detailed documentation in `specs/` and component directories:

**Phase 3 (AI Chatbot):**
- `chatbot/README.md` - Comprehensive chatbot guide (400+ lines)
- `chatbot/GETTING_STARTED.md` - Quick start guide
- `chatbot/IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `chatbot/CHANGELOG.md` - Version history
- `specs/003-ai-chatbot/spec.md` - Feature specification (6 user stories)
- `specs/003-ai-chatbot/plan.md` - Implementation plan
- `specs/003-ai-chatbot/research.md` - Technical decisions (10 decisions)
- `specs/003-ai-chatbot/data-model.md` - Conversation context and MCP schemas
- `specs/003-ai-chatbot/contracts/mcp-tools.md` - MCP tool specifications
- `specs/003-ai-chatbot/quickstart.md` - Setup guide
- `specs/003-ai-chatbot/tasks.md` - Implementation tasks (65 tasks)

**Phase 2 (Full-Stack Web App):**
- `specs/002-fullstack-web-app/spec.md` - Feature specification
- `specs/002-fullstack-web-app/plan.md` - Implementation plan
- `specs/002-fullstack-web-app/research.md` - Technical decisions
- `specs/002-fullstack-web-app/data-model.md` - Database schema
- `specs/002-fullstack-web-app/contracts/api-endpoints.md` - API specification
- `specs/002-fullstack-web-app/quickstart.md` - Setup guide
- `specs/002-fullstack-web-app/tasks.md` - Implementation tasks

**Phase 1 (Console App):**
- `specs/001-todo-console-app/spec.md` - Feature specification
- `specs/001-todo-console-app/plan.md` - Implementation plan

## Deployment

**Recommended Platforms:**
- **Phase 3 Chatbot**: Railway, Render, or Fly.io (Python service)
- **Phase 2 Backend**: Railway or Render (Python FastAPI)
- **Phase 2 Frontend**: Vercel (Next.js)
- **Database**: Neon (serverless PostgreSQL)

**Phase 3 Deployment Notes:**
- Set environment variables: `OPENAI_API_KEY`, `BACKEND_API_URL`
- Chatbot can be deployed as standalone service
- REST API server runs on configurable port (default: 8001)
- In-memory sessions (consider Redis for production)

See deployment guides:
- Phase 3: `chatbot/README.md` (deployment section)
- Phase 2: `specs/002-fullstack-web-app/quickstart.md`

## License

MIT
