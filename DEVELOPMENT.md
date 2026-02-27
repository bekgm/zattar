# Zattar Development Guide

Complete guide for developing, extending, and maintaining the Zattar marketplace.

## Quick Start

### Backend

```bash
cd backend

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Configure .env with your database URL:
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/zattar

# Run
python -m app.main
# Or with hot reload:
uvicorn app.main:app --reload
```

**Server**: http://localhost:4500
**Docs**: http://localhost:4500/docs

### Frontend

```bash
cd frontend

# Setup
npm install
cp .env.example .env

# VITE_API_URL=http://localhost:4500

# Run
npm run dev
```

**Frontend**: http://localhost:9000

---

## Development Workflow

### Adding a New Feature

#### Step 1: Define Models (Backend)
Create new model in `app/models/`:

```python
# app/models/example.py
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid

class Example(Base):
    __tablename__ = "examples"
    
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    parent_id: Mapped[str] = mapped_column(String(36), ForeignKey("parents.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    parent: Mapped["Parent"] = relationship("Parent", back_populates="examples")
    
    __table_args__ = (
        Index("idx_example_parent_created", "parent_id", "created_at"),
    )
```

Update `app/models/__init__.py` to export the new model.

#### Step 2: Create Schemas (Validation)
Create schemas in `app/schemas/`:

```python
# app/schemas/example.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ExampleCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    parent_id: str

class ExampleResponse(BaseModel):
    id: str
    name: str
    parent_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### Step 3: Create Repository
In `app/repositories/example.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.models.example import Example
from app.repositories.base import BaseRepository

class ExampleRepository(BaseRepository[Example]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Example)
    
    async def get_by_parent(self, parent_id: str) -> List[Example]:
        result = await self.session.execute(
            select(Example).where(Example.parent_id == parent_id)
        )
        return result.scalars().all()
```

#### Step 4: Create Service
In `app/services/example.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.example import ExampleRepository
from app.schemas.example import ExampleCreateRequest
from app.core.exceptions import ValidationError

class ExampleService:
    def __init__(self, session: AsyncSession):
        self.repository = ExampleRepository(session)
    
    async def create(self, data: ExampleCreateRequest):
        return await self.repository.create(data.dict())
    
    async def get(self, example_id: str):
        example = await self.repository.get_by_id(example_id)
        if not example:
            raise ValidationError("Example not found")
        return example
```

#### Step 5: Create API Endpoints
In `app/api/v1/endpoints/examples.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.example import ExampleService
from app.schemas.example import ExampleCreateRequest, ExampleResponse

router = APIRouter()

@router.post("", response_model=ExampleResponse)
async def create_example(
    data: ExampleCreateRequest,
    session: AsyncSession = Depends(get_session)
):
    service = ExampleService(session)
    return await service.create(data)

@router.get("/{example_id}", response_model=ExampleResponse)
async def get_example(
    example_id: str,
    session: AsyncSession = Depends(get_session)
):
    service = ExampleService(session)
    return await service.get(example_id)
```

Update `app/api/v1/__init__.py` to include the new router:

```python
from .endpoints.examples import router as examples_router

api_router.include_router(
    examples_router, 
    prefix="/examples", 
    tags=["examples"]
)
```

#### Step 6: Add Frontend Types
In `src/types/index.ts`:

```typescript
export interface Example {
  id: string
  name: string
  parent_id: string
  created_at: string
}
```

#### Step 7: Create API Client
In `src/api/examples.ts`:

```typescript
import apiClient from './client'
import { Example } from '../types'

export const exampleAPI = {
  create: async (data: {
    name: string
    parent_id: string
  }): Promise<Example> => {
    const response = await apiClient.post('/api/v1/examples', data)
    return response.data
  },

  get: async (exampleId: string): Promise<Example> => {
    const response = await apiClient.get(`/api/v1/examples/${exampleId}`)
    return response.data
  },
}
```

#### Step 8: Create React Components
Create feature in `src/features/examples/`:

```typescript
// src/features/examples/ExampleCard.tsx
import { Example } from '../../types'
import Card from '../../components/common/Card'

export default function ExampleCard({ example }: { example: Example }) {
  return (
    <Card>
      <h3 className="font-semibold">{example.name}</h3>
      <p className="text-sm text-neutral-500">
        {new Date(example.created_at).toLocaleDateString()}
      </p>
    </Card>
  )
}
```

---

## Code Organization Best Practices

### Backend

```
app/
├── models/
│   ├── base.py           # Base class for all models
│   ├── user.py
│   ├── listing.py
│   └── __init__.py       # Export all models
│
├── repositories/
│   ├── base.py           # BaseRepository with generic CRUD
│   ├── user.py           # UserRepository extends BaseRepository
│   └── __init__.py       # Export all repositories
│
├── services/
│   ├── user.py           # Business logic
│   └── __init__.py       # Export all services
│
├── api/v1/endpoints/
│   ├── users.py          # REST endpoints
│   └── __init__.py
│
├── schemas/
│   ├── user.py           # Pydantic validation schemas
│   └── __init__.py
│
├── core/
│   ├── database.py       # DB session management
│   ├── security.py       # JWT, hashing
│   ├── dependencies.py   # DI functions
│   └── exceptions.py     # Custom exceptions
│
├── websocket/
│   ├── manager.py        # Connection management
│   ├── routes.py         # WebSocket endpoints
│   └── __init__.py
│
├── utils/
│   └── __init__.py
│
├── main.py               # FastAPI app
├── config.py             # Settings
└── __init__.py
```

### Frontend

```
src/
├── api/
│   ├── client.ts         # Axios instance with interceptors
│   ├── auth.ts           # Auth endpoints
│   ├── listings.ts
│   └── chat.ts
│
├── components/
│   ├── common/           # Reusable components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   └── layouts/          # Page layouts
│       ├── Header.tsx
│       ├── Footer.tsx
│       └── MainLayout.tsx
│
├── features/             # Feature modules
│   ├── listings/
│   │   ├── ListingCard.tsx
│   │   ├── ListingsPage.tsx
│   │   └── ListingDetailPage.tsx
│   ├── chat/
│   └── deals/
│
├── stores/               # Zustand stores
│   ├── authStore.ts
│   ├── uiStore.ts
│   └── chatStore.ts
│
├── types/                # TypeScript interfaces
│   └── index.ts
│
├── utils/                # Utility functions
│   ├── formatting.ts
│   └── validation.ts
│
├── router/               # Route config
│   └── index.tsx
│
├── hooks/                # Custom hooks
│   └── useLocalStorage.ts
│
├── styles/
│   └── ... (global styles)
│
├── App.tsx               # Root component
└── main.tsx              # Entry point
```

---

## Security Checklist

### Backend
- Use bcrypt for password hashing
- Validate all inputs with Pydantic
- Use parameterized queries (SQLAlchemy default)
- Implement rate limiting for sensitive endpoints
- Use HTTPS in production
- Set CORS allowed origins explicitly
- Use long, random SECRET_KEY
- Set HTTPOnly, Secure flags on cookies
- Implement CSRF protection if using cookies
- Log security events

### Frontend
- React auto-escapes output (XSS prevention)
- Validate input before sending to API
- Store tokens securely (consider HTTPOnly cookies)
- Implement token refresh locally
- Clear sensitive data on logout
- Use HTTPS only in production
- Implement Content Security Policy headers
- Regular security dependency updates

---

## Testing Strategy

### Backend

```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Create tests/conftest.py for fixtures
# Create tests/test_models.py for model tests
# Create tests/test_services.py for service tests
# Create tests/test_endpoints.py for API tests

# Run tests
pytest
pytest -v  # Verbose
pytest --cov=app  # With coverage
```

Example service test:

```python
# tests/test_services.py
import pytest
from app.services.user import UserService
from app.schemas.user import UserRegisterRequest

@pytest.mark.asyncio
async def test_user_registration(session):
    service = UserService(session)
    request = UserRegisterRequest(
        email="test@example.com",
        phone="+77000000000",
        username="testuser",
        password="SecurePass123"
    )
    response = await service.register(request)
    assert response.access_token
    assert response.refresh_token
```

### Frontend

```bash
# Install testing dependencies
npm install -D @testing-library/react @testing-library/jest-dom vitest

# Create __tests__ or .test.ts files next to components
# Run tests
npm run test
```

---

## Commit Message Format

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

Examples:
- `feat(listings): add full-text search`
- `fix(chat): fix message encoding issue`
- `docs(api): update OpenAPI documentation`
- `refactor(services): extract user validation logic`

---

## Debugging Tips

### Backend

```python
# Add logging
from app.utils import get_logger
logger = get_logger(__name__)

logger.info(f"Creating listing: {listing_data}")
logger.error(f"Database error: {str(e)}", exc_info=True)

# Database debugging
# In config.py: DATABASE_ECHO = True  (shows SQL queries)

# Interactive debugging
import pdb; pdb.set_trace()
# Or use VS Code debugger
```

### Frontend

```typescript
// Console logging
console.log('State:', store.getState())
console.error('API Error:', error)

// React DevTools
// Install React DevTools browser extension

// Zustand DevTools
import { devtools } from 'zustand/middleware'

// Network debugging
// Use browser DevTools Network tab
// Check Vite proxy in vite.config.ts
```

---

## Documentation

### API Documentation

FastAPI automatically generates Swagger UI at `/docs` and ReDoc at `/redoc`.

To customize:

```python
app = FastAPI(
    title="Zattar API",
    description="Marketplace API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
```

### Code Documentation

Use docstrings:

```python
"""Module docstring"""

async def create_listing(seller_id: str, data: ListingCreateRequest) -> Listing:
    """
    Create a new listing.
    
    Args:
        seller_id: ID of the listing creator
        data: Listing data
    
    Returns:
        Created listing object
    
    Raises:
        ValidationError: If validation fails
    """
    ...
```

---

## Deployment

### Backend (Docker)

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t zattar-backend .
docker run -p 8000:8000 -e DATABASE_URL=... zattar-backend
```

### Frontend (Docker)

```dockerfile
# Dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
```

```bash
docker build -t zattar-frontend .
docker run -p 80:80 zattar-frontend
```

---

## Performance Tips

### Backend
- Add indexes on frequently filtered/sorted columns
- Use pagination for large datasets
- Implement Redis caching for expensive queries
- Use bulk operations when possible
- Monitor slow query logs

### Frontend
- Lazy load images
- Code splitting with React.lazy()
- Memoize expensive computations
- Use React.memo for pure components
- Monitor with Lighthouse

---

## Contributing

1. Create feature branch: `git checkout -b feat/feature-name`
2. Make changes following the structure above
3. Test thoroughly
4. Commit with conventional messages
5. Push and create PR
6. Request review

---

## Support

For issues:
1. Check existing documentation
2. Review similar implementations
3. Check API documentation at `/docs`
4. Check browser console for frontend errors
5. Check server logs for backend errors

---

**Happy coding!**
