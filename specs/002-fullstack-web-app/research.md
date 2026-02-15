# Research & Technical Decisions: Todo Full-Stack Web Application (Phase 2)

**Date**: 2025-02-15
**Feature**: 002-fullstack-web-app
**Purpose**: Document technical decisions, rationale, and alternatives for Phase 2

## Overview

Phase 2 transforms the Phase 1 console app into a multi-user web application. Key decisions involve authentication strategy, database design, API architecture, and frontend framework choices.

## Technical Decisions

### 1. Monorepo vs Separate Repositories

**Decision**: Monorepo with `backend/` and `frontend/` directories

**Rationale**:
- Single repository simplifies hackathon submission
- Easier to coordinate changes across frontend and backend
- Shared documentation and specs in one place
- Phase 1 code can be referenced/reused from same repo
- Simpler CI/CD setup for hackathon timeline

**Alternatives Considered**:
- Separate repos - Rejected: More complex coordination, multiple submissions
- Monorepo with workspaces (Nx, Turborepo) - Rejected: Overkill for 2 projects

---

### 2. Authentication Strategy

**Decision**: JWT tokens with Better Auth (frontend) and python-jose (backend)

**Rationale**:
- Stateless authentication (no server-side sessions)
- JWT tokens can be validated by backend without database lookup
- Better Auth provides React hooks and Next.js integration
- 7-day token expiration balances security and UX
- Industry-standard approach for frontend/backend separation

**Implementation**:
```
1. User signs up/in → Backend issues JWT token
2. Frontend stores JWT in httpOnly cookie (Better Auth)
3. Frontend includes JWT in Authorization header for API calls
4. Backend validates JWT signature and extracts user_id
5. Backend filters all queries by authenticated user_id
```

**Alternatives Considered**:
- Session-based auth - Rejected: Requires server-side state, doesn't scale well
- OAuth2 only - Rejected: Too complex for Phase 2, can add in Phase 3
- Magic links - Rejected: Requires email service, out of scope

---

### 3. Database Choice

**Decision**: Neon Serverless PostgreSQL

**Rationale**:
- Required by hackathon specification
- Serverless: No server management, auto-scaling
- PostgreSQL: Robust, ACID compliant, excellent SQLModel support
- Free tier sufficient for hackathon (1GB storage, 100 hours compute)
- Built-in connection pooling
- Easy integration with FastAPI via SQLModel

**Schema Design**:
```sql
-- Users table (managed by auth system)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tasks table (extends Phase 1 Task)
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

**Alternatives Considered**:
- SQLite - Rejected: Not suitable for multi-user web app
- MongoDB - Rejected: Spec requires PostgreSQL
- Supabase - Rejected: Neon specified in requirements

---

### 4. Backend Framework

**Decision**: FastAPI with SQLModel ORM

**Rationale**:
- Required by hackathon specification
- FastAPI: Modern, fast, automatic OpenAPI docs, async support
- SQLModel: Type-safe ORM, Pydantic integration, excellent for PostgreSQL
- Reuses Phase 1 domain logic (Task, TaskManager) with minimal changes
- Built-in data validation via Pydantic
- Excellent developer experience with type hints

**API Architecture**:
- RESTful endpoints following standard conventions
- JWT middleware for authentication
- Automatic request/response validation
- CORS middleware for frontend communication
- Structured error responses

**Alternatives Considered**:
- Django REST Framework - Rejected: Heavier, more opinionated
- Flask - Rejected: Less modern, no built-in async support

---

### 5. Frontend Framework

**Decision**: Next.js 16+ (App Router) with TypeScript and Tailwind CSS

**Rationale**:
- Required by hackathon specification
- Next.js App Router: Modern React patterns, server components, file-based routing
- TypeScript: Type safety, better IDE support, catches errors early
- Tailwind CSS: Rapid UI development, responsive design, consistent styling
- Vercel deployment: Free hosting, automatic HTTPS, excellent Next.js support

**Architecture**:
- Route groups for auth pages vs protected pages
- Server components for static content
- Client components for interactive forms
- API client layer (Axios) for backend communication
- Better Auth for authentication state management

**Alternatives Considered**:
- Create React App - Rejected: No SSR, less modern
- Vue.js/Nuxt - Rejected: Spec requires Next.js
- Remix - Rejected: Less mature ecosystem

---

### 6. Authentication Library (Frontend)

**Decision**: Better Auth

**Rationale**:
- Required by hackathon specification
- Modern authentication library for Next.js
- Built-in JWT support
- React hooks for auth state
- Handles token storage and refresh
- Good TypeScript support

**Integration**:
- Better Auth client configured with backend API URL
- JWT tokens stored in httpOnly cookies
- Automatic token inclusion in API requests
- Auth state available via React hooks

**Alternatives Considered**:
- NextAuth.js - Rejected: Better Auth specified in requirements
- Custom JWT handling - Rejected: Reinventing the wheel, error-prone

---

### 7. Phase 1 Code Reuse Strategy

**Decision**: Copy and adapt Phase 1 domain logic to backend

**Rationale**:
- Phase 1 Task entity and TaskManager contain validated business logic
- Validation rules (title 1-200 chars, description 0-1000 chars) stay the same
- Exception handling patterns can be reused
- Saves development time, reduces bugs

**Adaptations Needed**:
1. **Task Entity**: Add user_id field, change to SQLModel for database
2. **TaskManager**: Add user_id parameter to all methods for filtering
3. **Repository**: Replace MemoryRepository with DatabaseRepository (SQLModel)
4. **Exceptions**: Keep same exception types, adapt error messages

**Migration Path**:
```python
# Phase 1 (in-memory)
task_manager.create_task(title="Buy milk", description="")

# Phase 2 (database + multi-user)
task_manager.create_task(user_id=user.id, title="Buy milk", description="")
```

**Alternatives Considered**:
- Rewrite from scratch - Rejected: Wastes time, introduces new bugs
- Import Phase 1 as library - Rejected: Too complex for hackathon timeline

---

### 8. API Design Pattern

**Decision**: RESTful API with standard HTTP methods

**Rationale**:
- Industry standard, well-understood
- Maps naturally to CRUD operations
- FastAPI has excellent REST support
- Easy to test with standard HTTP clients
- Clear semantics (GET, POST, PUT, DELETE, PATCH)

**Endpoint Structure**:
```
POST   /api/auth/signup          - Create account
POST   /api/auth/signin          - Sign in
POST   /api/auth/signout         - Sign out
GET    /api/users/{user_id}/tasks      - List user's tasks
POST   /api/users/{user_id}/tasks      - Create task
GET    /api/users/{user_id}/tasks/{id} - Get task details
PUT    /api/users/{user_id}/tasks/{id} - Update task
DELETE /api/users/{user_id}/tasks/{id} - Delete task
PATCH  /api/users/{user_id}/tasks/{id}/complete - Toggle completion
```

**Alternatives Considered**:
- GraphQL - Rejected: Overkill for simple CRUD, adds complexity
- RPC-style - Rejected: Less standard, harder to document

---

### 9. Password Security

**Decision**: Passlib with bcrypt hashing

**Rationale**:
- Industry-standard password hashing
- Bcrypt is slow by design (prevents brute force)
- Passlib provides simple API
- Automatic salt generation
- Compatible with FastAPI

**Implementation**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password on signup
hashed = pwd_context.hash(plain_password)

# Verify password on signin
is_valid = pwd_context.verify(plain_password, hashed)
```

**Alternatives Considered**:
- Plain text - Rejected: Completely insecure
- SHA256 - Rejected: Too fast, vulnerable to brute force
- Argon2 - Rejected: Bcrypt is more standard, sufficient for Phase 2

---

### 10. CORS Configuration

**Decision**: Enable CORS in FastAPI for frontend origin

**Rationale**:
- Frontend (Vercel) and backend (Railway/Render) on different domains
- Browser enforces same-origin policy
- CORS middleware allows cross-origin requests
- Restrict to specific frontend origin for security

**Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],  # Production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Alternatives Considered**:
- Proxy through Next.js - Rejected: Adds latency, more complex
- Same-domain deployment - Rejected: Harder to manage, less flexible

---

## Dependencies Summary

### Backend Dependencies
```toml
[project.dependencies]
fastapi = "^0.115.0"
sqlmodel = "^0.0.22"
pydantic = "^2.10.0"
python-jose = "^3.3.0"  # JWT
passlib = "^1.7.4"      # Password hashing
bcrypt = "^4.2.0"       # Passlib backend
psycopg2-binary = "^2.9.10"  # PostgreSQL driver
uvicorn = "^0.32.0"     # ASGI server
python-multipart = "^0.0.12"  # Form data
alembic = "^1.14.0"     # Database migrations

[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.28.0",  # FastAPI TestClient
]
```

### Frontend Dependencies
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "typescript": "^5.7.0",
    "tailwindcss": "^4.0.0",
    "better-auth": "^1.0.0",
    "axios": "^1.7.0",
    "react-hook-form": "^7.54.0",
    "zod": "^3.24.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "eslint": "^9.0.0",
    "prettier": "^3.4.0"
  }
}
```

---

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| JWT token theft | Use httpOnly cookies, HTTPS only, short expiration |
| SQL injection | Use SQLModel parameterized queries, never string concatenation |
| User data leaks | Always filter by user_id, thorough testing of user isolation |
| CORS misconfiguration | Whitelist specific frontend origin, test cross-origin requests |
| Database connection pool exhaustion | Use Neon's built-in pooling, implement connection limits |
| Password brute force | Use bcrypt (slow hashing), consider rate limiting in future |

---

## Performance Considerations

**Backend**:
- Database indexes on user_id and completed columns
- Connection pooling via Neon
- Async FastAPI endpoints for concurrent requests
- Pagination for large task lists (future enhancement)

**Frontend**:
- Next.js App Router for optimal loading
- Client-side caching of task list
- Optimistic UI updates (update UI before API response)
- Lazy loading of components

---

## Deployment Strategy

**Backend** (Railway or Render):
- Environment variables for DATABASE_URL, JWT_SECRET
- Automatic HTTPS
- Health check endpoint: GET /health
- Database migrations run on deployment

**Frontend** (Vercel):
- Environment variables for NEXT_PUBLIC_API_URL
- Automatic HTTPS and CDN
- Preview deployments for testing
- Edge runtime for optimal performance

---

## Conclusion

All technical decisions align with hackathon requirements and Phase 1 architecture. The monorepo structure with FastAPI backend and Next.js frontend provides a solid foundation for Phase 2, while reusing Phase 1 domain logic saves development time. JWT authentication and PostgreSQL database enable multi-user support with proper data isolation.

**Ready for Phase 1 Design**: Proceed to data-model.md and API contracts generation.
