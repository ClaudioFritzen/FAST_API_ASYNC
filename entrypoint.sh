#!/bin/sh
set -e

echo "Running migrations..."
poetry run alembic upgrade head

echo "Starting API..."
poetry run uvicorn fast_zero_async.app:app --host 0.0.0.0 --port 8000
