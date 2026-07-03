#!/usr/bin/env bash
set -euo pipefail

# Run Ansible playbooks with the project's ansible.cfg and environment variables.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PROJECT_ROOT
VENV_DIR="${PROJECT_ROOT}/.venv"
ENV_FILE="${PROJECT_ROOT}/.env"
ANSIBLE_DIR="${PROJECT_ROOT}/automation/ansible"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "ERROR: Python virtual environment not found."
  echo "Run: python3 -m venv .venv"
  exit 1
fi

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "ERROR: .env file not found."
  echo "Run: cp .env.example .env"
  exit 1
fi

source "${VENV_DIR}/bin/activate"

# Export variables from .env for Ansible lookup('env', ...)
set -a
source "${ENV_FILE}"
set +a

export ANSIBLE_CONFIG="${ANSIBLE_DIR}/ansible.cfg"

cd "${ANSIBLE_DIR}"

ansible-playbook "$@"
