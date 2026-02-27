# Zattar - Production-Ready Marketplace Architecture

A complete, scalable marketplace platform for Kazakhstan (similar to OLX) with enterprise-grade architecture.

## Project Structure

```
zattar/
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── listing.py
│   │   │   ├── category.py
│   │   │   ├── chat.py
│   │   │   └── safe_deal.py         # State machine pattern
│   │   ├── schemas/                 # Pydantic validation
│   │   ├── services/                # Business logic layer
│   │   ├── repositories/            # Data access (Repository Pattern)
│   │   ├── api/v1/endpoints/        # REST API endpoints
│   │   ├── websocket/               # Real-time chat
│   │   ├── core/                    # Database, security, dependencies
│   │   ├── utils/                   # Helpers & logging
│   │   ├── config.py                # Configuration management
│   │   └── main.py                  # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
└── frontend/                         # React+TypeScript frontend
    ├── src/
    │   ├── api/                     # API client functions
    │   ├── components/
    │   │   ├── common/              # Reusable UI (Button, Card, Input, Alert)
    │   │   ├── layouts/             # Header, Footer, MainLayout
    │   │   └── ...
    │   ├── features/                # Feature modules (listings, chat, deals)
    │   ├── stores/                  # Zustand stores (auth, ui, chat)
    │   ├── types/                   # TypeScript interfaces
    │   ├── router/                  # React Router config
    │   ├── styles/                  # CSS & design tokens
    │   ├── hooks/                   # Custom hooks
    │   ├── utils/                   # Utilities
    │   ├── App.tsx                  # Root component with Splash Screen
    │   └── main.tsx                 # Entry point
    ├── public/                      # Static assets
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── index.html
    └── README.md
```

## Architecture Principles

### Backend
- **Clean Architecture**: Models → Repositories → Services → API Endpoints
- **Service Layer**: All business logic isolated and testable
- **Repository Pattern**: Data access abstraction & reusability
- **Dependency Injection**: FastAPI Depends() for loose coupling
- **Async/Await**: 100% async throughout (FastAPI + SQLAlchemy 2.0)
- **State Machine**: Safe Deal implements explicit state transitions
- **Error Handling**: Custom exception classes
- **Logging**: Structured logging throughout

### Frontend
- **Feature-Based Structure**: Organized by feature (listings, chat, deals)
- **API Client Layer**: Centralized API calls with axios interceptors
- **State Management**: Zustand for client & server state
- **Custom Hooks**: Reusable logic extraction
- **Component Composition**: Small, focused, reusable components
- **Design System**: Consistent styling with TailwindCSS
- **Type Safety**: 100% TypeScript with strict mode

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLAlchemy 2.0 (async)
- **Auth**: JWT (access + refresh tokens)
- **WebSockets**: FastAPI native WebSockets
- **Validation**: Pydantic v2
- **Hashing**: bcrypt (passlib)
- **Caching**: Redis
- **Storage**: S3-compatible
- **Task Queue**: (optional) Celery

### Frontend
- **Framework**: React 18
- **Language**: TypeScript (strict)
- **Build Tool**: Vite 5
- **Routing**: React Router v6
- **State**: Zustand + TanStack Query
- **Styling**: TailwindCSS + custom design system
- **Animations**: Framer Motion
- **API Client**: Axios with interceptors
- **Icons**: Lucide React

## Core Features

### 1. User System
- Email + phone registration
- JWT authentication (access + refresh)
- Password hashing (bcrypt)
- User profiles with avatars
- Rating system
- Account locking (failed login attempts)

### 2. Listings Management
- CRUD operations (Create, Read, Update, Delete)
- Full-text search (PostgreSQL tsvector)
- Filtering by: city, category, price range, condition
- Image management (up to 10 per listing)
- View tracking
- Status management (active, sold, archived)

### 3. Real-Time Chat
- WebSocket-based messaging
- Automatic conversation creation
- Message persistence
- Typing indicators (optional)
- Read status tracking
- Connection manager for scalability

### 4. Safe Deal (Escrow System)
- **State Machine Pattern**:
  - PENDING → SHIPPED → COMPLETED
  - PENDING → DISPUTED
  - SHIPPED → CANCELLED
- Buyer initiates deal
- Seller ships with tracking
- Buyer confirms delivery
- Automatic timeout handling
- Dispute resolution flow

### 5. Frontend UI/UX
- **Splash Screen**: Animated intro on first load
  - Brown gradient background
  - Centered logo with fade-in
  - Smooth loading bar
  - 2-second duration
  - localStorage-based first visit detection
- **Design System**: Modern, minimalistic, trust-focused
  - Primary: #8B5E3C (Brown)
  - Consistent spacing & rounded corners (8-12px)
  - Soft shadows & transitions
  - Mobile-first responsive
  - Large, clear CTAs

## Getting Started

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Update .env with your settings

# Run database migrations (if using Alembic)
alembic upgrade head

# Start server
uvicorn app.main:app --reload
# Or: python -m app.main
```

**API will be available at**: `http://localhost:8000`
**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional)
cp .env.example .env

# Start dev server
npm run dev
```

**Frontend will be available at**: `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /api/v1/users/register` - Register user
- `POST /api/v1/users/login` - Login user
- `GET /api/v1/users/me` - Get current user

### Listings
- `GET /api/v1/listings` - Search listings
- `POST /api/v1/listings` - Create listing
- `GET /api/v1/listings/{id}` - Get listing detail
- `PATCH /api/v1/listings/{id}` - Update listing
- `DELETE /api/v1/listings/{id}` - Delete listing
- `POST /api/v1/listings/{id}/mark-sold` - Mark as sold

### Chat
- `POST /api/v1/chat/conversations/{listing_id}/{seller_id}` - Start conversation
- `GET /api/v1/chat/conversations` - Get conversations
- `GET /api/v1/chat/conversations/{id}` - Get conversation
- `POST /api/v1/chat/conversations/{id}/messages` - Send message
- `GET /api/v1/chat/conversations/{id}/messages` - Get messages
- `WS /api/v1/ws/chat/{conversation_id}` - WebSocket chat

### Safe Deals
- `POST /api/v1/safe-deals` - Initiate deal
- `GET /api/v1/safe-deals/{id}` - Get deal
- `POST /api/v1/safe-deals/{id}/transition` - Transition status
- `GET /api/v1/safe-deals/buyer/deals` - Get buyer deals
- `GET /api/v1/safe-deals/seller/deals` - Get seller deals

## Security Best Practices

- Password hashing with bcrypt
- JWT with short expiration + refresh tokens
- CORS configuration
- SQL injection prevention (SQLAlchemy parameterized queries)
- XSS protection (React auto-escapes)
- CSRF tokens (via HTTPOnly cookies - optional)
- Rate limiting support (configure as needed)
- Account lockout mechanism
- Input validation (Pydantic)

## Database Schema

### Key Tables
- `users` - User accounts with ratings
- `categories` - Product categories
- `listings` - Product listings with full-text search
- `listing_images` - Images for listings
- `listing_views` - View tracking
- `conversations` - Chat conversations
- `messages` - Chat messages
- `safe_deals` - Escrow transactions with state

**Indexes**: Optimized for common queries (city, category, price, status, dates)

## Testing & Quality

### Backend
- Unit tests for services
- Integration tests for repositories
- API endpoint tests
- Schema validation tests

### Frontend
- Component tests
- Store tests
- Integration tests
- E2E tests

## Performance Optimizations

### Backend
- Async/await throughout
- Connection pooling
- Query optimization with proper indexes
- Redis caching layer
- Pagination on all list endpoints

### Frontend
- Code splitting with React.lazy
- Image optimization
- Bundle analysis
- Lighthouse optimization
- Memoization where needed

## Deployment

### Backend (Production)
```bash
# Using Gunicorn + Uvicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Using Docker
docker build -t zattar-backend .
docker run -p 8000:8000 zattar-backend
```

### Frontend (Production)
```bash
# Build and deploy to CDN/server
npm run build
# dist/ folder ready for deployment

# With Docker
docker build -t zattar-frontend .
docker run -p 80:80 zattar-frontend
```

## Documentation

- Backend detailed docs: [backend/README.md](backend/README.md)
- Frontend detailed docs: [frontend/README.md](frontend/README.md)
- API documentation: Available at `/docs` endpoint after starting backend

## Environment Variables

See `.env.example` in both backend and frontend directories for required variables.

## Contributing

1. Follow the folder structure outlined above
2. Maintain separation of concerns
3. Use TypeScript/type hints
4. Write tests for new features
5. Keep components small and focused

## License

MIT

---

**Built for the Kazakhstan marketplace community**
