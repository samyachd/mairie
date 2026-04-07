# Makefile
.PHONY: backend frontend test docker-dev docker-prod docker-down
# Backend
backend:
	cd backend && uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
frontend:
	cd frontend && npm run dev

# Tests
test:
	cd backend && uv run pytest

# Docker
dockerdev:
	docker-compose -f docker-compose.dev.yml up

dockerprod:
	docker-compose -f docker-compose.prod.yml up -d

dockerdown:
	docker-compose down