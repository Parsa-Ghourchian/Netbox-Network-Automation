#!/usr/bin/env bash
set -euo pipefail

# Seed NetBox with the default lab data model.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"

cd "${PROJECT_ROOT}"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "ERROR: Python virtual environment not found."
  echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r automation/python/requirements.txt"
  exit 1
fi

source "${VENV_DIR}/bin/activate"
python automation/python/seed_netbox_lab.py
