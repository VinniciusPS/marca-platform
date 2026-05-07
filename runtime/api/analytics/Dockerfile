FROM python:3.11-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

# Instalação de dependências
RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    "sqlalchemy[asyncio]>=2.0.0" \
    asyncpg \
    psycopg2-binary \
    pydantic-settings \
    python-dotenv

COPY services/api/analytics/ .

ENV PYTHONPATH=/usr/app:/usr/app/src

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]