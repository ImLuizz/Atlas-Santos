#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/../backend"

echo "==> Starting Atlas Santos Backend (FastAPI)..."
if [ ! -d ".venv" ]; then
    echo "Virtualenv not found. Creating .venv..."
    if command -v uv >/dev/null 2>&1; then
        uv venv --python 3.12 .venv
        source .venv/bin/activate
        uv pip install -e ".[dev]"
    else
        python3 -m venv .venv
        source .venv/bin/activate
        pip install --upgrade pip
        pip install -e ".[dev]"
    fi
else
    source .venv/bin/activate
fi

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

