# ─── Builder stage ───────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /src

# Copy only dependency manifests first (layer-cache friendly)
# NOTE: .env is intentionally NOT copied here.
#       Secrets must be injected at runtime via -e / --env-file / secrets manager.
COPY pyproject.toml uv.lock ./

# Install dependencies (without the project itself)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Now copy application source
COPY src/ ./src/
COPY server.py sync_data.py sanitize_data.py ./
COPY README.md ./

# Install the project package
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ─── Runtime stage ────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runner

# OCI Image Labels (standard metadata for registries and scanners)
LABEL org.opencontainers.image.title="StockAgent" \
      org.opencontainers.image.description="Hierarchical Multi-Agent System for Top 5 US Stock Selection" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.authors="Lavanya Cheshani <lavanyacheshani5@gmail.com>" \
      org.opencontainers.image.url="https://github.com/Lavanyacheshani/StockAgent" \
      org.opencontainers.image.source="https://github.com/Lavanyacheshani/StockAgent" \
      org.opencontainers.image.licenses="MIT"

# Create a non-root user for security
RUN addgroup --gid 1000 appgroup && \
    adduser --uid 1000 --gid 1000 --disabled-password --gecos "" appuser

WORKDIR /src

COPY --from=builder --chown=1000:1000 /src /src

# Activate the virtual environment
ENV PYTHONPATH="/src" \
    PATH="/src/.venv/bin:$PATH" \
    VIRTUAL_ENV="/src/.venv"

# Outputs directory (mount a volume here in production)
RUN mkdir -p /src/outputs && chown 1000:1000 /src/outputs

USER appuser

# Health check — verifies the API server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
