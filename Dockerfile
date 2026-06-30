# Use a lightweight python image with uv pre-installed for fast building
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependencies definitions
COPY pyproject.toml uv.lock ./

# Install dependencies (excluding dev dependencies)
RUN uv sync --frozen --no-dev --no-install-project

# Final stage - keep container size small
FROM python:3.12-alpine

WORKDIR /app

# Copy the virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Add virtual environment binaries to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy source code and assets
COPY src/ ./src
COPY db/ ./db
COPY scripts/ ./scripts

# Environment configurations
ENV PYTHONPATH=src
ENV DB_PATH=/app/db/parking.db
ENV PORT=8000

# Expose server port
EXPOSE 8000

# Command to run the ADK web server
CMD ["adk", "web", "--port", "8000", "--host", "0.0.0.0"]
