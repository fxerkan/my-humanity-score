---
name: mhs-dev-env
description: >
  Start, check, and manage the My Humanity Score (MHS) local development environment.
  Use this skill whenever the user wants to: start the dev stack ("docker up",
  "start the app", "run locally", "bring up MHS", "spin up the environment"),
  check service health ("is postgres running", "check redis", "are services up"),
  run the test suite ("run tests", "pytest", "npm test", "run all tests"),
  view logs ("show logs", "tail api logs", "what's the API saying"),
  reset the database ("reset db", "fresh database", "wipe and restart"),
  or troubleshoot startup issues. Always use this skill — it knows the exact
  Docker Compose service names, ports, and health check commands for this project.
---

# MHS Dev Environment Management

The My Humanity Score / MHS stack runs in Docker Compose with 6 services.
All commands run from the project root: `/Users/erkan.ciftci/repo_local/my-humanity-score/`

## Services at a glance

| Service | Port | What it is |
|---|---|---|
| `web` | 3000 | Next.js 15 frontend |
| `api` | 8000 | FastAPI backend |
| `postgres` | 5432 | PostgreSQL 16 (primary DB) |
| `redis` | 6379 | Redis 7 (cache + Celery broker) |
| `neo4j` | 7474 (HTTP), 7687 (Bolt) | Neo4j graph DB |
| `worker` | — | Celery worker (same image as api) |
| `flower` | 5555 | Celery Flower monitoring (dev only) |

## Starting the stack

```bash
docker compose up -d           # Start all services detached
docker compose up              # Start with logs in foreground
docker compose up api web      # Start specific services only
```

After starting, verify health:
```bash
curl -s http://localhost:8000/health | python3 -m json.tool
# Expected: {"status": "ok", "version": "1.0.0"}

curl -s http://localhost:3000
# Expected: HTML response (Next.js)
```

## Checking service status

```bash
docker compose ps                          # All service states
docker compose ps --format json            # Machine-readable
docker inspect mhs-api --format '{{.State.Health.Status}}'  # Single service health
```

### Quick health check (run all at once)
```bash
# PostgreSQL
docker compose exec postgres pg_isready -U mhs -d mhs

# Redis
docker compose exec redis redis-cli ping   # Expected: PONG

# Neo4j
curl -s http://localhost:7474              # Expected: JSON response

# API
curl -s http://localhost:8000/health

# Web
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000  # Expected: 200
```

## Viewing logs

```bash
docker compose logs -f                     # All services, follow
docker compose logs -f api                 # API only
docker compose logs -f api worker          # API + Celery worker
docker compose logs --tail=50 api          # Last 50 lines
```

## Running tests

### Backend (pytest)
```bash
# From project root:
docker compose exec api pytest                           # All tests
docker compose exec api pytest tests/unit/              # Unit only
docker compose exec api pytest tests/integration/       # Integration only
docker compose exec api pytest --cov=apps/api --cov-report=term-missing
docker compose exec api pytest -x                       # Stop on first failure
docker compose exec api pytest -k "test_auth"           # Filter by name
```

Or outside Docker (with venv):
```bash
cd apps/api && uv run pytest
```

### Frontend (vitest)
```bash
docker compose exec web npm run test                    # Vitest
docker compose exec web npm run test:coverage
docker compose exec web npm run build                   # Type check + build
docker compose exec web npm run lint
```

### E2E (Playwright) — requires full stack running
```bash
npx playwright test                                     # All E2E tests
npx playwright test --ui                               # Interactive UI
npx playwright test auth.spec.ts                       # Specific file
```

## Database operations

### Run migrations
```bash
docker compose exec api alembic upgrade head            # Apply all migrations
docker compose exec api alembic downgrade -1            # Rollback one
docker compose exec api alembic current                 # Show current revision
docker compose exec api alembic history                 # Show migration history
```

### Connect to PostgreSQL
```bash
docker compose exec postgres psql -U mhs -d mhs        # Interactive psql
docker compose exec postgres psql -U mhs -d mhs -c "SELECT COUNT(*) FROM users;"
```

### Reset database (destructive — dev only)
```bash
docker compose down -v                                  # Stop + delete volumes
docker compose up -d postgres                           # Restart postgres
docker compose exec api alembic upgrade head            # Re-run migrations
```

### Seed test data
```bash
docker compose exec api python -m scripts.seed          # If seed script exists
```

## Stopping the stack

```bash
docker compose stop                   # Stop (keeps volumes)
docker compose down                   # Stop + remove containers
docker compose down -v                # Stop + remove containers + volumes (data loss!)
```

## Common issues and fixes

### Port already in use
```bash
lsof -i :8000 | grep LISTEN            # Find what's using port 8000
kill -9 <PID>                          # Kill it
```

### Container won't start / crash loop
```bash
docker compose logs api | tail -30     # Read the error
docker compose up api                  # Run in foreground to see error live
```

### Migration errors
```bash
docker compose exec api alembic current    # Check current state
docker compose exec api alembic history    # See all revisions
# If "Multiple heads" error:
docker compose exec api alembic heads
docker compose exec api alembic merge heads  # Merge conflicting heads
```

### Node modules missing (web service)
```bash
docker compose exec web npm install
# Or rebuild the image:
docker compose build web && docker compose up -d web
```

### Python dependency missing (api service)
```bash
docker compose exec api uv pip install <package>
# Or rebuild:
docker compose build api && docker compose up -d api
```

### Redis connection refused
```bash
docker compose restart redis
docker compose exec api python -c "import redis; r=redis.from_url('redis://redis:6379'); print(r.ping())"
```

## Useful shortcuts

```bash
# Tail API + worker together (most useful for task debugging)
docker compose logs -f api worker

# Run a one-off Python command
docker compose exec api python -c "from services.mhs_calculator import MHSCalculator; print('OK')"

# Open a shell in a container
docker compose exec api bash
docker compose exec web sh

# Check environment variables loaded in container
docker compose exec api env | grep -E "DATABASE|REDIS|SECRET"

# Celery: check active tasks
docker compose exec worker celery -A celery_app inspect active

# Neo4j browser (open in browser)
open http://localhost:7474
```

## Environment setup (first time)

If `.env` doesn't exist yet:
```bash
cp .env.example .env
# Edit .env and fill in required values (JWT_SECRET at minimum for dev)
```

Required for basic dev (others can be left empty to start):
- `DATABASE_URL` — already set in docker-compose.yml defaults
- `REDIS_URL` — already set in docker-compose.yml defaults  
- `JWT_SECRET` — generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
