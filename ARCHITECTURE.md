"""
Zattar - Marketplace Architecture Guide
========================================

This document provides an overview of the complete Zattar marketplace architecture.

## Backend Architecture

### 1. Models Layer (app/models/)
- Defines SQLAlchemy ORM models
- Includes all database schema
- Safe Deal uses State Machine pattern (can_transition_to, transition_to methods)
- Relationships properly configured with back_populates

Example structure:
- User: Authentication, profiles, ratings
- Listing: Products with images, search support
- Conversation: Chat conversations between buyer/seller
- Message: Individual messages with read status
- SafeDeal: Escrow transactions with explicit state transitions

### 2. Repository Layer (app/repositories/)
BaseRepository pattern for generic CRUD operations:
- get_by_id(id)
- get_all(skip, limit)
- create(obj_in)
- update(id, obj_in)
- delete(id)
- exists(**filters)

Specific repositories extend BaseRepository with custom queries:
- UserRepository: get_by_email, get_by_username, get_active_users
- ListingRepository: search, get_by_seller, get_by_category, get_by_city
- ConversationRepository: get_or_create, get_by_user, get_by_listing
- MessageRepository: get_by_conversation, mark_as_read
- SafeDealRepository: get_by_buyer, get_by_seller, get_expired

### 3. Service Layer (app/services/)
Business logic encapsulation:
- UserService: Authentication, profile management, blocking
- ListingService: CRUD, search, filtering, view counting
- ChatService: Conversation management, messaging, read status
- SafeDealService: Deal initiation, state transitions, expiration handling

Services handle:
- Input validation
- Authorization checks
- Business rule enforcement
- Database orchestration

### 4. API Layer (app/api/v1/endpoints/)
REST endpoints organized by resource:
- users.py: Register, login, get profile, update profile
- listings.py: CRUD, search, mark sold
- chat.py: Conversations, messages, read status
- safe_deals.py: Initiate, transition, get deals

Each endpoint:
- Validates input (Pydantic schemas)
- Calls appropriate service
- Returns response with proper status codes

### 5. WebSocket Layer (app/websocket/)
Real-time chat implementation:
- ConnectionManager: Manages active WebSocket connections per conversation
- Routes: WebSocket endpoint with JSON message handling
- Supports: Messages, typing indicators, user join/leave events

### 6. Core Layer (app/core/)
Infrastructure & utilities:
- database.py: SQLAlchemy session management, DB initialization
- security.py: JWT creation/validation, password hashing
- dependencies.py: Dependency injection for auth, session
- exceptions.py: Custom HTTP exceptions

## Frontend Architecture

### 1. API Client Layer (src/api/)
Axios-based API communication:
- client.ts: Base configuration, interceptors, auth token handling
- auth.ts: Authentication endpoints
- listings.ts: Listing operations
- chat.ts: Chat endpoints
- deals.ts: Safe Deal endpoints

Features:
- Automatic token injection in Authorization header
- Token refresh on 401
- Error handling

### 2. State Management (src/stores/)
Zustand stores for state:
- authStore: User, tokens, authentication actions
- uiStore: UI state (sidebar, filters, etc.)
- chatStore: Current conversation, messages

Stores are persistent and can be logged with devtools middleware.

### 3. Components Layer
Organized by type:
- common/: Reusable UI components (Button, Card, Input, Alert)
- layouts/: Page layouts (MainLayout, Header, Footer)

Each component:
- Uses TypeScript for type safety
- Implements Framer Motion animations where appropriate
- Integrates with Zustand stores
- Handles loading & error states

### 4. Features (src/features/)
Feature modules with related components:
- listings/: ListingsPage, ListingCard, ListingDetailPage
- chat/: ChatWindow, ConversationsList
- deals/: SafeDealPage

Each feature is self-contained and can be developed independently.

### 5. Router (src/router/)
React Router v6 configuration:
- Route organization by feature
- Nested routes where appropriate
- Layout wrappers

### 6. Design System (src/styles/)
Global styles with TailwindCSS:
- Color palette defined in tailwind.config.js
- Component utility classes in index.css
- Responsive design with Tailwind breakpoints

## Safe Deal State Machine

State transitions (in safe_deal.py model):

```
PENDING
├── → SHIPPED (seller action)
├── → CANCELLED
└── → DISPUTED

SHIPPED
├── → COMPLETED (buyer action)
├── → CANCELLED
└── → DISPUTED

COMPLETED (terminal)
└── → DISPUTED

DISPUTED (terminal, no further transitions)

CANCELLED (terminal, no further transitions)
```

Implementation:
- Model includes can_transition_to() and transition_to() methods
- Service validates authority for each transition
- Timestamps recorded for each state change
- Automatic expiration handling

## Authentication Flow

### Registration
1. User submits email, phone, username, password
2. Backend validates input and checks duplicates
3. Creates user with hashed password
4. Returns access + refresh tokens
5. Frontend stores tokens in localStorage

### Login
1. User submits email + password
2. Backend verifies credentials
3. Returns access + refresh tokens
4. Frontend stores tokens

### Token Usage
1. Every request includes Authorization: Bearer {access_token}
2. Backend validates token and extracts user_id
3. On 401, frontend attempts refresh (implement token refresh endpoint)
4. If refresh fails, redirect to login

## Search & Filtering

Listing search supports:
- Query (full-text on title + description)
- City filtering
- Category filtering
- Price range (min/max)
- Condition (new/used)
- Sorting (by created_at, price, views)
- Pagination (skip, limit)

Implemented in ListingRepository.search() with dynamic query building.

## Chat Flow

1. Buyer clicks "Contact Seller" on listing
2. Frontend calls startConversation() → creates or retrieves conversation
3. Both parties can send messages
4. WebSocket provides real-time delivery
5. Messages persist in database
6. Read status tracked per-user

## Real-Time Features

WebSocket chat endpoint:
- Connected users per conversation
- Message broadcasting
- Typing indicators
- User join/leave notifications
- Graceful disconnect handling

## Security Considerations

Backend:
- Password hashing with bcrypt (10 rounds)
- JWT token expiration (30 min access, 7 day refresh)
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention (parameterized queries)
- Account lockout after N failed attempts

Frontend:
- XSS prevention (React auto-escapes)
- Tokens stored in localStorage (can be enhanced with HTTPOnly cookies)
- HTTPS enforced in production
- Content Security Policy headers

## Performance Optimizations

Backend:
- Indexed database columns for common queries
- Async/await throughout
- Connection pooling
- Query pagination
- Redis caching (can be added)

Frontend:
- Code splitting with React.lazy
- Image lazy loading
- Component memoization
- TanStack Query caching
- Zustand for efficient state updates

## Testing Strategy

Backend:
- Unit tests for services
- Integration tests for repositories
- API endpoint tests with pytest
- Mock database for unit tests

Frontend:
- Component tests with React Testing Library
- Store tests with Zustand
- Integration tests for features
- E2E tests with Cypress (optional)

## Error Handling

Backend (app/core/exceptions.py):
- NotFoundError (404)
- UnauthorizedError (401)
- ForbiddenError (403)
- ValidationError (422)
- ConflictError (409)
- RateLimitError (429)

Frontend:
- API client errors caught in try/catch
- Toast notifications for user feedback
- Error states in components
- Logging for debugging

## Deployment Checklist

Backend:
- [ ] Set SECRET_KEY to long random string
- [ ] Use PostgreSQL in production (not SQLite)
- [ ] Configure Redis for caching
- [ ] Set ENVIRONMENT to "production"
- [ ] Set DEBUG to False
- [ ] Configure ALLOWED_ORIGINS for CORS
- [ ] Set up S3 credentials for image storage
- [ ] Use environment variables, not .env file
- [ ] Set up reverse proxy (nginx)
- [ ] Enable HTTPS
- [ ] Configure logging to files
- [ ] Set up monitoring & alerting

Frontend:
- [ ] Run npm run build
- [ ] Test production build locally
- [ ] Configure API_URL to production backend
- [ ] Deploy to CDN or server
- [ ] Enable gzip compression
- [ ] Set cache headers appropriately
- [ ] Enable HTTPS
- [ ] Monitor error rates

## Future Enhancements

- Image optimization & resizing
- Advanced search with Elasticsearch
- Recommendation engine
- Payment integration (Stripe/Payoneer)
- Review/rating system refinement
- Seller verification badges
- Two-factor authentication
- Notification system (email/SMS)
- Admin dashboard
- Analytics & reporting
- Mobile app (React Native)
- Progressive Web App (PWA) features
"""
