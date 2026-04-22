# Makefile
.PHONY: backend frontend test docker-dev docker-prod docker-down

setup:
	uv run utils/clean_pipeline.py
	cd backend && uv pip install -r requirements.txt
	cd frontend && npm install
	wslview http://localhost:8000/docs
	wslview http://localhost:3000

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
dev:
	docker compose up --build

prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

dockerdown:
	docker compose down

# Database
migration:
	cd backend && uv run alembic revision --autogenerate -m "$(msg)"

migrate:
	cd backend && uv run alembic upgrade head

seed:
	cd backend && uv run python seed.py

dbreset:
	docker compose -f docker-compose.dev.yml down -v
	docker compose -f docker-compose.dev.yml up db -d
	sleep 3
	cd backend && uv run alembic upgrade head

# utils
convert:
	cd backend && uv run python convert_excel.py
