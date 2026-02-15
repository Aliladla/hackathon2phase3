# API Endpoints Specification: Todo Full-Stack Web Application (Phase 2)

**Date**: 2025-02-15
**Feature**: 002-fullstack-web-app
**Purpose**: Define RESTful API contracts for authentication and task management

## Overview

This document specifies all HTTP endpoints for the Phase 2 backend API. The API follows RESTful conventions with JWT-based authentication. All endpoints return JSON responses with consistent error handling.

**Base URL**: `http://localhost:8000` (development) or `https://api.yourdomain.com` (production)

**API Version**: v1 (no versioning in URL for Phase 2, can add `/v1` prefix in future)

---

## Authentication Endpoints

### POST /api/auth/signup

Create a new user account.

**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| email | string | Yes | Valid email format, max 255 chars |
| password | string | Yes | Minimum 8 characters |

**Success Response** (201 Created):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2025-02-15T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-02-22T10:30:00Z"
}
```

**Error Responses**:

- **400 Bad Request** - Invalid input
```json
{
  "error": "validation_error",
  "message": "Invalid email format",
  "details": {
    "field": "email",
    "constraint": "email_format"
  }
}
```

- **409 Conflict** - Email already registered
```json
{
  "error": "email_exists",
  "message": "Email already registered"
}
```

**Validation Rules**:
- Email must be valid RFC 5322 format
- Email is case-insensitive (stored lowercase)
- Password minimum 8 characters
- Password can contain any printable characters

---

### POST /api/auth/signin

Authenticate existing user and issue JWT token.

**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| email | string | Yes | Valid email format |
| password | string | Yes | Any length |

**Success Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2025-02-15T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-02-22T10:30:00Z"
}
```

**Error Responses**:

- **400 Bad Request** - Missing fields
```json
{
  "error": "validation_error",
  "message": "Email and password are required"
}
```

- **401 Unauthorized** - Invalid credentials
```json
{
  "error": "invalid_credentials",
  "message": "Invalid email or password"
}
```

**Security Notes**:
- Do not reveal whether email exists or password is wrong (generic error)
- Rate limiting recommended (not implemented in Phase 2)
- Password is verified using bcrypt

---

### POST /api/auth/signout

Sign out current user (invalidate token on client side).

**Authentication**: Required (JWT token in Authorization header)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "message": "Signed out successfully"
}
```

**Error Responses**:

- **401 Unauthorized** - Missing or invalid token
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

**Implementation Note**:
- Phase 2 uses stateless JWT (no server-side session storage)
- Signout is client-side only (delete token from storage)
- Token remains valid until expiration (7 days)
- Token blacklisting can be added in future phases

---

## Task Management Endpoints

All task endpoints require JWT authentication. The `user_id` is extracted from the JWT token, ensuring users can only access their own tasks.

### GET /api/tasks

List all tasks for the authenticated user.

**Authentication**: Required (JWT token)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| completed | boolean | No | - | Filter by completion status (true/false) |
| limit | integer | No | 100 | Maximum tasks to return (1-1000) |
| offset | integer | No | 0 | Number of tasks to skip (pagination) |

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-02-15T10:30:00Z",
      "updated_at": "2025-02-15T10:30:00Z"
    },
    {
      "id": 2,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Finish project",
      "description": "",
      "completed": true,
      "created_at": "2025-02-14T09:00:00Z",
      "updated_at": "2025-02-15T11:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

**Empty List Response** (200 OK):
```json
{
  "tasks": [],
  "total": 0,
  "limit": 100,
  "offset": 0
}
```

**Error Responses**:

- **401 Unauthorized** - Missing or invalid token
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

- **400 Bad Request** - Invalid query parameters
```json
{
  "error": "validation_error",
  "message": "Invalid limit value",
  "details": {
    "field": "limit",
    "constraint": "must be between 1 and 1000"
  }
}
```

---

### GET /api/tasks/{task_id}

Get a specific task by ID (user-filtered).

**Authentication**: Required (JWT token)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| task_id | integer | Task ID |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T10:30:00Z"
}
```

**Error Responses**:

- **401 Unauthorized** - Missing or invalid token
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

- **404 Not Found** - Task not found or belongs to another user
```json
{
  "error": "task_not_found",
  "message": "Task not found"
}
```

**Security Note**: Returns 404 for both non-existent tasks and tasks belonging to other users (prevents information leakage)

---

### POST /api/tasks

Create a new task for the authenticated user.

**Authentication**: Required (JWT token)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | Yes | 1-200 characters, no leading/trailing whitespace |
| description | string | No | 0-1000 characters, defaults to empty string |

**Success Response** (201 Created):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T10:30:00Z"
}
```

**Error Responses**:

- **401 Unauthorized** - Missing or invalid token
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

- **400 Bad Request** - Validation error
```json
{
  "error": "validation_error",
  "message": "Title must be between 1 and 200 characters",
  "details": {
    "field": "title",
    "constraint": "length",
    "min": 1,
    "max": 200
  }
}
```

**Validation Rules** (from Phase 1):
- Title: Required, 1-200 characters, trimmed
- Description: Optional, 0-1000 characters, defaults to ""
- Completed: Always false for new tasks
- User ID: Extracted from JWT token (not in request body)

---

### PUT /api/tasks/{task_id}

Update an existing task (full update).

**Authentication**: Required (JWT token)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| task_id | integer | Task ID |

**Request Body**:
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "completed": false
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | Yes | 1-200 characters |
| description | string | No | 0-1000 characters |
| completed | boolean | No | true/false, defaults to current value |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "completed": false,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T12:00:00Z"
}
```

**Error Responses**:

- **401 Unauthorized** - Missing or invalid token
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

- **404 Not Found** - Task not found or belongs to another user
```json
{
  "error": "task_not_found",
  "message": "Task not found"
}
```

- **400 Bad Request** - Validation error
```json
{
  "error": "validation_error",
  "message": "Title cannot be empty",
  "details": {
    "field": "title",
    "constraint": "required"
  }
}
```

**Implementation Note**: updated_at timestamp is automatically updated by database trigger

---

### PATCH /api/tasks/{task_id}

Partially update a task (only specified fields).

**Authentication**: Required (JWT token)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| task_id | integer | Task ID |

**Request Body** (all fields optional):
```json
{
  "title": "Updated title"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | No | 1-200 characters if provided |
| description | string | No | 0-1000 characters if provided |
| completed | boolean | No | true/false if provided |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated title",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T12:30:00Z"
}
```

**Error Responses**: Same as PUT /api/tasks/{task_id}

---

### PATCH /api/tasks/{task_id}/complete

Toggle task completion status (convenience endpoint).

**Authentication**: Required (JWT token)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| task_id | integer | Task ID |

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-02-15T10:30:00Z",
  "updated_at": "2025-02-15T13:00:00Z"
}
```

**Error Responses**: Same as GET /api/tasks/{task_id}

**Implementation Note**: Toggles completed field (false → true, true → false)

---

### DELETE /api/tasks/{task_id}

Delete a task permanently.

**Authentication**: Required (JWT token)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| task_id | integer | Task ID |

**Success Response** (204 No Content):
```
(empty body)
```

**Error Responses**:

- **401 Unauthorized** - Missing or invalid token
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

- **404 Not Found** - Task not found or belongs to another user
```json
{
  "error": "task_not_found",
  "message": "Task not found"
}
```

**Implementation Note**: Returns 204 even if task was already deleted (idempotent)

---

## Health Check Endpoint

### GET /health

Check API health status (for monitoring and deployment).

**Authentication**: None (public endpoint)

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-02-15T10:30:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

**Error Response** (503 Service Unavailable):
```json
{
  "status": "unhealthy",
  "timestamp": "2025-02-15T10:30:00Z",
  "version": "1.0.0",
  "database": "disconnected",
  "error": "Database connection failed"
}
```

---

## Common Response Patterns

### Success Responses

All successful responses include:
- Appropriate HTTP status code (200, 201, 204)
- JSON body (except 204 No Content)
- Content-Type: application/json header

### Error Responses

All error responses follow this structure:
```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "field_name",
    "constraint": "constraint_type"
  }
}
```

**Standard Error Codes**:
| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | validation_error | Invalid input data |
| 401 | unauthorized | Missing or invalid authentication |
| 403 | forbidden | Authenticated but not authorized |
| 404 | task_not_found | Task does not exist or access denied |
| 404 | user_not_found | User does not exist |
| 409 | email_exists | Email already registered |
| 500 | internal_error | Unexpected server error |

---

## Authentication Flow

### JWT Token Structure

**Header**:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "exp": 1708603800,
  "iat": 1707999000
}
```

**Token Expiration**: 7 days from issuance

**Token Validation**:
1. Verify signature using secret key
2. Check expiration (exp claim)
3. Extract user_id from payload
4. Use user_id for all database queries

### Authorization Header Format

```
Authorization: Bearer <jwt_token>
```

**Example**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTUwZTg0MDAtZTI5Yi00MWQ0LWE3MTYtNDQ2NjU1NDQwMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA4NjAzODAwLCJpYXQiOjE3MDc5OTkwMDB9.signature
```

---

## CORS Configuration

**Allowed Origins**: Frontend domain (e.g., https://your-frontend.vercel.app)

**Allowed Methods**: GET, POST, PUT, PATCH, DELETE, OPTIONS

**Allowed Headers**: Authorization, Content-Type

**Credentials**: Allowed (for cookies if needed in future)

**Example CORS Headers**:
```
Access-Control-Allow-Origin: https://your-frontend.vercel.app
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Credentials: true
```

---

## Rate Limiting (Future Enhancement)

Not implemented in Phase 2, but recommended for production:

- Authentication endpoints: 5 requests per minute per IP
- Task endpoints: 100 requests per minute per user
- Health check: Unlimited

---

## API Testing Examples

### cURL Examples

**Signup**:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass123"}'
```

**Signin**:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass123"}'
```

**Create Task**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread"}'
```

**List Tasks**:
```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Update Task**:
```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title","description":"Updated description","completed":true}'
```

**Delete Task**:
```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## OpenAPI Specification (Swagger)

FastAPI automatically generates OpenAPI documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Conclusion

This API specification defines all endpoints needed for Phase 2 multi-user todo application. All endpoints follow RESTful conventions with consistent error handling and JWT authentication. The API is designed to be consumed by the Next.js frontend and can be extended in Phase 3 for AI chatbot integration.

**Key Features**:
- RESTful design with standard HTTP methods
- JWT-based authentication with 7-day expiration
- User isolation enforced at API layer
- Consistent error responses
- Automatic OpenAPI documentation via FastAPI
- Ready for frontend integration

**Ready for Quickstart Guide**: Proceed to quickstart.md
