#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python -m pytest -q
.venv/bin/ruff check src tests
.venv/bin/mypy src
npm run check
npm run test:browser
.venv/bin/python -m build
