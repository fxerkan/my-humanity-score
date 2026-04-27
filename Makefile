.PHONY: dev dev-full stop logs ps build shell-api shell-web migrate seed lint test help

# ── Dev ────────────────────────────────────────────────────────────────────────
dev:                          ## Start core 3 services: db + api + web
	cp -n .env.example .env 2>/dev/null || true
	docker-compose up --build

dev-full:                     ## Start all services including Redis, Celery, Neo4j
	cp -n .env.example .env 2>/dev/null || true
	docker-compose --profile full up --build

dev-bg:                       ## Start core services in background
	cp -n .env.example .env 2>/dev/null || true
	docker-compose up -d --build

stop:                         ## Stop all services
	docker-compose --profile full down

ps:                           ## Show running containers
	docker-compose ps

logs:                         ## Tail all logs
	docker-compose logs -f

logs-api:                     ## Tail API logs
	docker-compose logs -f api

logs-web:                     ## Tail web logs
	docker-compose logs -f web

# ── Build ─────────────────────────────────────────────────────────────────────
build:                        ## Rebuild all images
	docker-compose build --no-cache

# ── Shell ─────────────────────────────────────────────────────────────────────
shell-api:                    ## Open shell in API container
	docker-compose exec api bash

shell-web:                    ## Open shell in web container
	docker-compose exec web sh

shell-db:                     ## Open psql in DB container
	docker-compose exec db psql -U mhs -d mhs

# ── Database ──────────────────────────────────────────────────────────────────
migrate:                      ## Run Alembic migrations
	docker-compose exec api alembic upgrade head

migrate-down:                 ## Rollback last migration
	docker-compose exec api alembic downgrade -1

migrate-history:              ## Show migration history
	docker-compose exec api alembic history

seed:                         ## Seed demo data (5 users + activities + scores)
	docker-compose exec api python scripts/seed_demo.py

# ── Lint & Test ───────────────────────────────────────────────────────────────
lint:                         ## Run all linters (ruff + mypy + eslint)
	docker-compose exec api ruff check .
	docker-compose exec api mypy .
	docker-compose exec web pnpm lint

test:                         ## Run all tests
	docker-compose exec api pytest
	docker-compose exec web pnpm test

test-api:                     ## Run API tests only
	docker-compose exec api pytest -v

test-web:                     ## Run web tests only
	docker-compose exec web pnpm test

# ── Help ──────────────────────────────────────────────────────────────────────
help:                         ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
