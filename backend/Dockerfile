FROM python:3.12-slim

# Crée le user AVEC son home directory (-m = make home)
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

ARG DEV=false
RUN if [ "$DEV" = "true" ]; \
    then uv sync --frozen; \
    else uv sync --frozen --no-dev; \
    fi

COPY . .

RUN chown -R appuser:appuser /app

# Ajoute le venv au PATH : uvicorn, pytest, alembic directement accessibles
ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]