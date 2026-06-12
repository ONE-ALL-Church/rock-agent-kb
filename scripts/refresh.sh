#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv sync --extra dev
uv run kb refresh
uv run --extra dev pytest
uv run kb report-refresh
