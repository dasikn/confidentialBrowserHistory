FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files and sync
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the rest of the application code
COPY . .

EXPOSE 8001 8002

CMD uv run python mcp_server.py & uv run uvicorn api:app --host 0.0.0.0 --port 8002 & wait