#!/usr/bin/env bash
set -euo pipefail

# Run compliance check between desired configs and actual configs.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"

cd "${PROJECT_ROOT}"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "ERROR: Python virtual environment not found."
  echo "Run: python3 -m venv .venv"
  exit 1
fi

source "${VENV_DIR}/bin/activate"

python automation/python/compliance_check.py "$@"
