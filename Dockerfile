FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .

COPY uv.lock* .

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
