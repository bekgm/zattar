# Zattar Backend

Scalable, production-ready marketplace backend for Kazakhstan.

## Tech Stack

- FastAPI 0.104+
- PostgreSQL with async SQLAlchemy 2.0
- Redis for caching
- JWT authentication
- WebSockets for real-time chat

## Project Structure

```
backend/
├── app/
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic validation schemas
│   ├── services/         # Business logic layer
│   ├── repositories/     # Data access layer
│   ├── api/              # API endpoints (v1)
│   ├── websocket/        # Real-time chat
│   ├── core/             # Database, security, dependencies
│   ├── utils/            # Utilities and helpers
│   ├── config.py         # Configuration
│   └── main.py           # FastAPI app entry
├── requirements.txt
├── .env.example
└── README.md
```

## Architecture Principles

- **Clean Architecture**: Separation of concerns (models, services, repositories, handlers)
- **Service Layer**: All business logic isolated and testable
- **Repository Pattern**: Data access abstraction
- **Dependency Injection**: FastAPI dependencies for loose coupling
- **Async/Await**: 100% async throughout the stack
- **State Machine**: Safe Deal uses explicit state transitions

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run migrations (if using Alembic)
alembic upgrade head

# Start server
python -m app.main
# or
uvicorn app.main:app --reload
```

## Key Features

- User registration + JWT auth
- Listing CRUD with full-text search
- Real-time chat with WebSockets
- Safe Deal (escrow) system with state machine
