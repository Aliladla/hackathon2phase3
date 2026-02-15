# Todo AI Chatbot - Phase 3

AI-powered conversational interface for todo management using OpenAI Agents SDK and MCP tools.

## Overview

Phase 3 transforms the todo application into an intelligent chatbot that understands natural language commands. Users can manage their tasks through conversational interactions powered by OpenAI's GPT-4.

## Features

- **Natural Language Understanding**: Speak naturally - "Add a task to buy groceries" instead of structured commands
- **Context-Aware Conversations**: References like "mark that task complete" work based on conversation history
- **OpenAI GPT-4 Integration**: Powered by GPT-4-turbo-preview for accurate intent recognition
- **MCP Tools**: Structured API communication with Phase 2 backend
- **Session Management**: 30-minute session expiration with automatic cleanup
- **Multiple Interfaces**: Interactive console and REST API server
- **Comprehensive Testing**: Unit, integration, and end-to-end tests

## Architecture

```
┌─────────────────┐
│  User Input     │
│  (Natural Lang) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OpenAI Agent   │
│  (GPT-4)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MCP Tools      │
│  (6 tools)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Phase 2 API    │
│  (FastAPI)      │
└─────────────────┘
```

## Prerequisites

- **Python 3.13+** with UV package manager
- **OpenAI API Key** - Get one at https://platform.openai.com/api-keys
- **Phase 2 Backend** - Must be running at http://localhost:8000
- **JWT Token** - Obtain by signing in to Phase 2 backend

## Installation

1. **Navigate to chatbot directory**:
   ```bash
   cd chatbot
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

4. **Edit .env file** with your credentials:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key-here
   OPENAI_MODEL=gpt-4-turbo-preview
   BACKEND_API_URL=http://localhost:8000
   CHATBOT_PORT=8001
   MAX_CONTEXT_MESSAGES=10
   SESSION_TIMEOUT_MINUTES=30
   ```

## Usage

### Interactive Console (Recommended)

The console interface provides a conversational experience:

```bash
uv run python -m chatbot
```

**Example conversation**:
```
You: Add a task to buy groceries
🤖 Assistant: I've added 'Buy groceries' to your list. It's task #1.

You: Show me my tasks
🤖 Assistant: You have 1 task:
1. Buy groceries (not completed)

You: Mark that task as complete
🤖 Assistant: Done! I've marked task #1 (Buy groceries) as complete. Great job!

You: exit
👋 Goodbye! Your tasks are saved in the backend.
```

### REST API Server

For programmatic access or web integration:

```bash
uv run uvicorn chatbot.server.app:app --reload --port 8001
```

**API Endpoints**:

- `POST /chat` - Send a message to the chatbot
- `POST /sessions` - Create a new conversation session
- `GET /sessions/{session_id}/context` - Get session context
- `DELETE /sessions/{session_id}` - Delete a session
- `GET /health` - Health check

**Example API usage**:
```bash
# Create session
curl -X POST http://localhost:8001/sessions

# Send message
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk", "session_id": "SESSION_ID"}'
```

## Natural Language Commands

The chatbot understands various phrasings:

**Create tasks**:
- "Add a task to buy milk"
- "Create a new task: Call dentist"
- "I need to remember to pay bills"

**View tasks**:
- "Show me my tasks"
- "What's on my todo list?"
- "List all my tasks"

**Mark complete**:
- "Mark task 5 as complete"
- "I finished task 3"
- "Complete that task"

**Update tasks**:
- "Change task 2 title to Buy groceries and snacks"
- "Update task 4 description to Include eggs and milk"

**Delete tasks**:
- "Delete task 7"
- "Remove that task"
- "Get rid of task 3"

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run Specific Test Types

```bash
# Unit tests only (fast)
uv run pytest -m unit

# Integration tests
uv run pytest -m integration

# End-to-end tests (requires backend)
uv run pytest -m e2e
```

### Coverage Report

```bash
# Terminal report
uv run pytest --cov=chatbot --cov-report=term-missing

# HTML report (opens in browser)
uv run pytest --cov=chatbot --cov-report=html
open htmlcov/index.html
```

### Test Structure

- `tests/conftest.py` - Shared fixtures and configuration
- `tests/test_api_client.py` - API client unit tests
- `tests/test_mcp_executor.py` - MCP tool executor tests
- `tests/test_conversation_context.py` - Context management tests
- `tests/test_agent.py` - OpenAI agent tests
- `tests/test_integration.py` - Integration tests

## Project Structure

```
chatbot/
├── src/chatbot/
│   ├── __init__.py
│   ├── __main__.py           # Interactive console entry point
│   ├── config.py             # Environment configuration
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py          # OpenAI agent implementation
│   │   └── prompts.py        # System prompts and templates
│   ├── api/
│   │   ├── __init__.py
│   │   └── client.py         # Phase 2 API client
│   ├── conversation/
│   │   ├── __init__.py
│   │   └── context.py        # Session and context management
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── schemas.py        # MCP tool definitions
│   │   └── executor.py       # MCP tool executor
│   └── server/
│       ├── __init__.py
│       └── app.py            # FastAPI REST server
├── tests/                    # Comprehensive test suite
├── pyproject.toml           # Project dependencies
├── pytest.ini               # Pytest configuration
├── .env.example             # Environment template
└── README.md                # This file
```

## MCP Tools

The chatbot uses 6 MCP tools to communicate with Phase 2 backend:

1. **create_task** - Create a new task
2. **list_tasks** - List tasks with optional filtering
3. **get_task** - Get a specific task by ID
4. **update_task** - Update task properties
5. **delete_task** - Delete a task
6. **toggle_complete** - Toggle task completion status

See `specs/003-ai-chatbot/contracts/mcp-tools.md` for detailed specifications.

## Troubleshooting

### "OPENAI_API_KEY environment variable is required"
- Ensure `.env` file exists with valid OpenAI API key
- Check that the key starts with `sk-`

### "BACKEND_API_URL environment variable is required"
- Verify Phase 2 backend is running at http://localhost:8000
- Check `.env` file has correct BACKEND_API_URL

### "Your session has expired"
- JWT token from Phase 2 has expired
- Sign in again to Phase 2 backend to get a new token

### "Authentication failed"
- JWT token is invalid or malformed
- Ensure you're using the correct token from Phase 2 backend

### Tests failing
- Ensure all dependencies are installed: `uv sync`
- Check that pytest and pytest-asyncio are available
- Run with verbose output: `uv run pytest -v`

## Documentation

Complete documentation available in `specs/003-ai-chatbot/`:

- **spec.md** - Feature specification with user stories
- **plan.md** - Technical architecture and implementation strategy
- **research.md** - Technical decisions and rationale
- **data-model.md** - Data structures and schemas
- **contracts/mcp-tools.md** - MCP tool specifications
- **quickstart.md** - Setup and usage guide
- **tasks.md** - Implementation task breakdown

## Development

### Adding New MCP Tools

1. Define tool schema in `src/chatbot/mcp/schemas.py`
2. Implement executor method in `src/chatbot/mcp/executor.py`
3. Add tool to `ALL_TOOLS` list
4. Update system prompt in `src/chatbot/agent/prompts.py`
5. Add tests in `tests/test_mcp_executor.py`

### Modifying System Prompts

Edit `src/chatbot/agent/prompts.py` to customize:
- Agent personality and tone
- Response templates
- Error messages
- Context formatting

### Extending Context Management

Modify `src/chatbot/conversation/context.py` to:
- Add new context fields
- Change session timeout
- Adjust message history limit
- Add custom context methods

## Performance

- **Response Time**: Typically 1-3 seconds (depends on OpenAI API)
- **Session Limit**: 30 minutes of inactivity
- **Message History**: Last 10 messages per session
- **Concurrent Sessions**: Unlimited (in-memory storage)

## Security

- JWT tokens are passed securely in Authorization headers
- No sensitive data stored in conversation context
- Session expiration prevents stale sessions
- API client validates all responses

## License

MIT

## Contributing

This is a hackathon project. For production use, consider:
- Persistent session storage (Redis, database)
- Rate limiting and request throttling
- Enhanced error handling and retry logic
- Monitoring and observability
- User authentication and authorization
- Cost optimization for OpenAI API calls
