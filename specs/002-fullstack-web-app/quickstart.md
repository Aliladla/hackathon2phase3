# Quickstart Guide: Todo Full-Stack Web Application (Phase 2)

**Date**: 2025-02-15
**Feature**: 002-fullstack-web-app
**Purpose**: Setup and usage instructions for local development and deployment

## Overview

This guide walks you through setting up the Phase 2 full-stack todo application on your local machine and deploying to production. The application consists of a FastAPI backend with Neon PostgreSQL database and a Next.js frontend.

**Estimated Setup Time**: 15-20 minutes

---

## Prerequisites

### Required Software

- **Python**: 3.13 or higher
- **UV**: Latest version (Python package manager)
- **Node.js**: 20.x or higher
- **npm/pnpm**: Latest version (pnpm recommended for faster installs)
- **Git**: For version control
- **PostgreSQL Client** (optional): For database inspection

### Required Accounts

- **Neon Account**: Free tier at https://neon.tech
- **Vercel Account** (optional): For frontend deployment at https://vercel.com
- **Railway/Render Account** (optional): For backend deployment

### Verify Prerequisites

```bash
# Check Python version
python --version  # Should be 3.13+

# Check UV installation
uv --version

# Check Node.js version
node --version  # Should be 20.x+

# Check npm/pnpm
npm --version
# or
pnpm --version

# Check Git
git --version
```

---

## Project Structure

```
hackathon2phase1/
├── backend/             # FastAPI backend
│   ├── src/backend/
│   ├── tests/
│   ├── pyproject.toml
│   └── .env
├── frontend/            # Next.js frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env.local
└── README.md
```

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Neon PostgreSQL Database

1. Go to https://neon.tech and sign up/login
2. Create a new project: "todo-app-phase2"
3. Copy the connection string (looks like: `postgresql://user:password@host/database`)
4. Save it for the next step

### 3. Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# backend/.env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

**IMPORTANT**:
- Replace `DATABASE_URL` with your Neon connection string
- Generate a secure `JWT_SECRET` (use `openssl rand -hex 32` or similar)
- Update `CORS_ORIGINS` with your frontend URL

### 4. Install Dependencies

```bash
# Using UV (recommended)
uv sync

# This will:
# - Create virtual environment
# - Install all dependencies from pyproject.toml
# - Install dev dependencies (pytest, httpx)
```

### 5. Run Database Migrations

```bash
# Initialize Alembic (first time only)
uv run alembic init alembic

# Generate initial migration
uv run alembic revision --autogenerate -m "Initial schema"

# Apply migrations
uv run alembic upgrade head
```

**Verify Migration**:
```bash
# Check tables were created
uv run python -c "from backend.database import engine; from sqlmodel import SQLModel, Session; print('Database connected successfully')"
```

### 6. Run Backend Server

```bash
# Development mode (with auto-reload)
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Verify Backend**:
- Open http://localhost:8000/health (should return `{"status": "healthy"}`)
- Open http://localhost:8000/docs (Swagger UI with all endpoints)
- Open http://localhost:8000/redoc (ReDoc documentation)

### 7. Run Backend Tests (Optional)

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=backend --cov-report=html

# Run specific test file
uv run pytest tests/api/test_auth.py -v
```

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd ../frontend  # From backend directory
# or
cd frontend     # From project root
```

### 2. Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Todo App
```

**For Production**:
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_APP_NAME=Todo App
```

### 3. Install Dependencies

```bash
# Using pnpm (recommended)
pnpm install

# Or using npm
npm install

# Or using yarn
yarn install
```

### 4. Run Frontend Development Server

```bash
# Using pnpm
pnpm dev

# Or using npm
npm run dev

# Or using yarn
yarn dev
```

**Verify Frontend**:
- Open http://localhost:3000
- You should see the signup/signin page
- Check browser console for any errors

### 5. Build for Production (Optional)

```bash
# Create production build
pnpm build

# Test production build locally
pnpm start
```

### 6. Run Frontend Tests (Optional)

```bash
# Run all tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with coverage
pnpm test:coverage
```

---

## Complete Local Development Setup

### Terminal 1: Backend Server

```bash
cd backend
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend Server

```bash
cd frontend
pnpm dev
```

### Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Usage Guide

### 1. Create Account

1. Open http://localhost:3000
2. Click "Sign Up" (or navigate to /signup)
3. Enter email and password (minimum 8 characters)
4. Click "Create Account"
5. You'll be automatically signed in and redirected to tasks page

### 2. Sign In

1. Navigate to http://localhost:3000/signin
2. Enter your email and password
3. Click "Sign In"
4. You'll be redirected to your tasks page

### 3. Add Task

1. On the tasks page, find the "Add Task" form
2. Enter task title (required, 1-200 characters)
3. Optionally enter description (0-1000 characters)
4. Click "Add Task"
5. Task appears in your task list immediately

### 4. View Tasks

- All your tasks are displayed on the main tasks page
- Tasks show: ID, title, description, completion status
- Incomplete tasks and completed tasks may be visually distinguished

### 5. Mark Task Complete/Incomplete

- Click the checkbox or "Complete" button next to a task
- Task status toggles between complete and incomplete
- Visual indicator updates immediately (e.g., strikethrough for completed)

### 6. Update Task

1. Click "Edit" button on a task
2. Modify title and/or description
3. Click "Save"
4. Changes are reflected immediately

### 7. Delete Task

1. Click "Delete" button on a task
2. Confirm deletion in the prompt
3. Task is removed from your list permanently

### 8. Sign Out

- Click "Sign Out" button in the navigation
- You'll be redirected to the signin page
- Your JWT token is cleared from browser storage

---

## API Testing with cURL

### Signup

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Expected Response**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "created_at": "2025-02-15T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-02-22T10:30:00Z"
}
```

### Signin

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Create Task

```bash
# Save token from signup/signin response
TOKEN="your_jwt_token_here"

curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

### List Tasks

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN"
```

### Update Task

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries and cook dinner",
    "description": "Milk, eggs, bread, chicken",
    "completed": false
  }'
```

### Toggle Complete

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: Bearer $TOKEN"
```

### Delete Task

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Deployment

### Backend Deployment (Railway)

1. **Create Railway Account**: https://railway.app
2. **Create New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: Choose your hackathon2phase1 repo
4. **Configure Service**:
   - Root directory: `backend`
   - Build command: `uv sync`
   - Start command: `uv run uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variables**:
   - `DATABASE_URL`: Your Neon connection string
   - `JWT_SECRET`: Your secret key
   - `JWT_ALGORITHM`: HS256
   - `JWT_EXPIRATION_DAYS`: 7
   - `CORS_ORIGINS`: Your Vercel frontend URL
6. **Deploy**: Railway will automatically deploy
7. **Get URL**: Copy your Railway app URL (e.g., `https://your-app.railway.app`)

### Backend Deployment (Render - Alternative)

1. **Create Render Account**: https://render.com
2. **Create New Web Service**: Click "New" → "Web Service"
3. **Connect Repository**: Link your GitHub repo
4. **Configure Service**:
   - Name: todo-backend-phase2
   - Root directory: backend
   - Environment: Python 3
   - Build command: `pip install uv && uv sync`
   - Start command: `uv run uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variables**: Same as Railway
6. **Deploy**: Render will build and deploy
7. **Get URL**: Copy your Render app URL

### Frontend Deployment (Vercel)

1. **Create Vercel Account**: https://vercel.com
2. **Import Project**: Click "Add New" → "Project"
3. **Select Repository**: Choose your hackathon2phase1 repo
4. **Configure Project**:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `pnpm build` (or `npm run build`)
   - Output Directory: `.next`
5. **Add Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: Your Railway/Render backend URL
   - `NEXT_PUBLIC_APP_NAME`: Todo App
6. **Deploy**: Vercel will automatically deploy
7. **Get URL**: Copy your Vercel app URL (e.g., `https://your-app.vercel.app`)

### Update CORS Configuration

After deploying frontend, update backend CORS_ORIGINS:

```bash
# In Railway/Render environment variables
CORS_ORIGINS=https://your-app.vercel.app
```

Redeploy backend for changes to take effect.

---

## Troubleshooting

### Backend Issues

**Problem**: Database connection fails
```
Solution:
1. Verify DATABASE_URL is correct in .env
2. Check Neon database is active (not paused)
3. Ensure ?sslmode=require is in connection string
4. Test connection: uv run python -c "from backend.database import engine; print('Connected')"
```

**Problem**: JWT token validation fails
```
Solution:
1. Verify JWT_SECRET matches between signup and signin
2. Check token hasn't expired (7 days default)
3. Ensure Authorization header format: "Bearer <token>"
4. Check JWT_ALGORITHM is HS256
```

**Problem**: CORS errors in browser
```
Solution:
1. Add frontend URL to CORS_ORIGINS in backend .env
2. Restart backend server after changing .env
3. Check browser console for exact CORS error
4. Verify frontend is using correct API URL
```

**Problem**: Alembic migration fails
```
Solution:
1. Delete alembic/versions/*.py files
2. Drop all tables in database (or create new database)
3. Run: uv run alembic revision --autogenerate -m "Initial schema"
4. Run: uv run alembic upgrade head
```

### Frontend Issues

**Problem**: API calls fail with network error
```
Solution:
1. Verify backend is running (check http://localhost:8000/health)
2. Check NEXT_PUBLIC_API_URL in .env.local
3. Ensure no trailing slash in API URL
4. Check browser console for exact error
```

**Problem**: Authentication not persisting
```
Solution:
1. Check Better Auth configuration
2. Verify JWT token is stored in cookies/localStorage
3. Check token expiration (7 days)
4. Clear browser cookies and try again
```

**Problem**: Build fails
```
Solution:
1. Delete node_modules and package-lock.json
2. Run: pnpm install (or npm install)
3. Check for TypeScript errors: pnpm tsc --noEmit
4. Verify all dependencies are installed
```

### Common Errors

**Error**: `ModuleNotFoundError: No module named 'backend'`
```
Solution: Run commands with 'uv run' prefix or activate virtual environment
```

**Error**: `EADDRINUSE: address already in use :::3000`
```
Solution: Kill process on port 3000 or use different port: pnpm dev -- -p 3001
```

**Error**: `relation "users" does not exist`
```
Solution: Run database migrations: uv run alembic upgrade head
```

---

## Development Tips

### Hot Reload

- **Backend**: FastAPI auto-reloads on file changes (with `--reload` flag)
- **Frontend**: Next.js auto-reloads on file changes (default in dev mode)

### Database Inspection

```bash
# Using psql (if installed)
psql "postgresql://user:password@host/database?sslmode=require"

# List tables
\dt

# View users
SELECT * FROM users;

# View tasks
SELECT * FROM tasks;

# Exit
\q
```

### API Documentation

- **Swagger UI**: http://localhost:8000/docs (interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (clean documentation)
- **OpenAPI JSON**: http://localhost:8000/openapi.json (raw spec)

### Logging

**Backend**:
```python
# Add to backend/main.py for request logging
import logging
logging.basicConfig(level=logging.INFO)
```

**Frontend**:
```typescript
// Check browser console for API calls and errors
console.log('API Response:', response);
```

---

## Testing Checklist

### Manual Testing

- [ ] User can sign up with valid email/password
- [ ] User cannot sign up with duplicate email
- [ ] User can sign in with correct credentials
- [ ] User cannot sign in with wrong password
- [ ] User can add task with title only
- [ ] User can add task with title and description
- [ ] User cannot add task with empty title
- [ ] User can view all their tasks
- [ ] User can mark task as complete
- [ ] User can mark task as incomplete
- [ ] User can update task title
- [ ] User can update task description
- [ ] User can delete task
- [ ] User cannot see other users' tasks
- [ ] User can sign out
- [ ] User remains signed in after page refresh
- [ ] UI is responsive on mobile (320px width)

### Automated Testing

```bash
# Backend tests
cd backend
uv run pytest -v

# Frontend tests
cd frontend
pnpm test
```

---

## Performance Optimization

### Backend

- Database connection pooling (automatic with Neon)
- Index on user_id and completed columns (already in schema)
- Async endpoints for concurrent requests (FastAPI default)

### Frontend

- Next.js App Router for optimal loading
- Client-side caching of task list
- Optimistic UI updates (update UI before API response)
- Image optimization (Next.js automatic)

---

## Security Checklist

- [ ] JWT_SECRET is strong and unique (32+ characters)
- [ ] DATABASE_URL is not committed to git (.env in .gitignore)
- [ ] HTTPS is used in production (automatic with Vercel/Railway)
- [ ] CORS is restricted to frontend domain only
- [ ] Passwords are hashed with bcrypt (never plain text)
- [ ] User isolation is enforced (all queries filter by user_id)
- [ ] SQL injection is prevented (SQLModel parameterized queries)

---

## Next Steps

After completing Phase 2 setup:

1. **Test all features**: Follow the testing checklist above
2. **Deploy to production**: Use Railway + Vercel for hosting
3. **Share with users**: Get feedback on UX and features
4. **Prepare for Phase 3**: AI chatbot integration using same backend API

---

## Support

For issues or questions:
- Check troubleshooting section above
- Review API documentation at http://localhost:8000/docs
- Check browser console for frontend errors
- Check backend logs for API errors

---

## Conclusion

You now have a fully functional multi-user todo application with:
- ✅ User authentication (signup, signin, signout)
- ✅ Task management (add, view, update, delete, mark complete)
- ✅ User isolation (private task lists)
- ✅ Database persistence (Neon PostgreSQL)
- ✅ Modern web UI (Next.js + TypeScript + Tailwind CSS)
- ✅ RESTful API (FastAPI with automatic docs)

**Ready for Task Generation**: Proceed to tasks.md generation with `/sp.tasks`
