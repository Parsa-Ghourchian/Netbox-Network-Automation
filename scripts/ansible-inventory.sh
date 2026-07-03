#!/usr/bin/env bash
set -euo pipefail

# Show Ansible inventory using the project's ansible.cfg.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"
ANSIBLE_DIR="${PROJECT_ROOT}/automation/ansible"

source "${VENV_DIR}/bin/activate"

export ANSIBLE_CONFIG="${ANSIBLE_DIR}/ansible.cfg"

cd "${ANSIBLE_DIR}"

ansible-inventory "$@"
