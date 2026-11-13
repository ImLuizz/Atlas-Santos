#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/../backend"

echo "==> Starting Atlas Santos Background Worker..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

python3 -m app.worker.main "$@"

