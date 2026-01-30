# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies with poetry
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY . .

# Copy example env and rename it to .env (do not bake secrets into image)
COPY .env.example .env

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Copy Python packages AND executables from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=builder /app /app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

# Create logs directory
RUN mkdir -p /app/logs

EXPOSE 7935

# Use shell form to enable log redirection
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port 7935 2>&1 | tee /app/logs/server.log
