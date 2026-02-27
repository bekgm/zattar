# Docker Setup Guide

This project includes Docker configuration for containerized deployment of the entire stack.

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Git (for cloning the repository)

## Services

The `docker-compose.yml` orchestrates three services:

1. **PostgreSQL Database** (`postgres`): Port 5432
   - Username: `zattar_user`
   - Password: `zattar_password`
   - Database: `zattar_db`

2. **Backend API** (`backend`): Port 4500
   - FastAPI application
   - Depends on PostgreSQL service

3. **Frontend Application** (`frontend`): Port 9000
   - React/Vite application
   - Depends on Backend service

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd zattar
```

### 2. Start All Services

```bash
docker-compose up
```

Or to run in detached mode (background):

```bash
docker-compose up -d
```

### 3. Access the Application

- **Frontend**: http://localhost:9000
- **Backend API**: http://localhost:4500
- **API Documentation (Swagger UI)**: http://localhost:4500/docs
- **ReDoc**: http://localhost:4500/redoc

### 4. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### 5. Stop Services

```bash
docker-compose down
```

To also remove volumes (database data):

```bash
docker-compose down -v
```

## Development Workflow

### Building Images Locally

```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Rebuilding After Code Changes

Since `docker-compose.yml` mounts volumes for development:

```bash
# For backend changes (Python), the uvicorn reload will pick them up automatically
# For frontend changes (JavaScript/TypeScript), you may need to rebuild:

docker-compose up --build
```

### Running One-Off Commands

```bash
# Interactive Python shell in backend
docker-compose exec backend python

# Install a new Python package
docker-compose exec backend pip install <package-name>

# Frontend npm commands
docker-compose exec frontend npm install <package-name>
```

## Environment Configuration

### Backend Environment Variables

Edit `docker-compose.yml` or create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://zattar_user:zattar_password@postgres:5432/zattar_db
JWT_SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:9000,http://localhost:3000
ALLOWED_ORIGINS=http://localhost:9000,http://localhost:3000
```

### Frontend Environment Variables

Edit `frontend/.env`:

```env
VITE_API_URL=http://localhost:4500
```

## Production Deployment

For production, update the `docker-compose.yml`:

1. **Use environment files**:

```bash
docker-compose --env-file .env.production up -d
```

2. **Configure a reverse proxy** (nginx):

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
  depends_on:
    - backend
    - frontend
```

3. **Use a production database URL** with proper credentials

4. **Set security headers** in environment variables

5. **Enable HTTPS** with SSL certificates

## Troubleshooting

### Port Already in Use

If ports 4500, 9000, or 5432 are already in use:

```bash
# Change ports in docker-compose.yml
# For example, to use different ports:
ports:
  - "8000:4500"  # Backend
  - "3000:9000"  # Frontend
  - "5433:5432"  # PostgreSQL
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose logs postgres

# Connect to PostgreSQL manually
docker-compose exec postgres psql -U zattar_user -d zattar_db
```

### Clearing Data

To start fresh with a clean database:

```bash
docker-compose down -v
docker-compose up
```

### Rebuilding Everything

```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

## Performance Tips

- Use `.dockerignore` files to exclude unnecessary files from the build context
- Multi-stage builds for frontend (already implemented)
- Volume mounts for development code (already configured)
- Use `COMPOSE_PARALLEL_PULL=1` for faster image downloads

## Security Considerations

- Change default PostgreSQL credentials in production
- Use strong JWT secret key (at least 32 characters)
- Never commit production credentials to version control
- Use Docker secrets for sensitive data in Swarm mode
- Implement rate limiting in nginx/reverse proxy
- Enable CORS only for trusted origins

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [React with Docker](https://create-react-app.dev/docs/deployment/#docker)
