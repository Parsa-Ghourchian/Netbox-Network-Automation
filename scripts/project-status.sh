#!/usr/bin/env bash
set -euo pipefail

# Show a quick project status summary.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "Project: netbox-network-automation-lab"
echo "Root: ${PROJECT_ROOT}"
echo

echo "Version:"
cat VERSION
echo

echo "Git status:"
git status --short
echo

echo "Docker:"
docker --version || true
docker compose version || true
echo

echo "NetBox containers:"
if [[ -d "docker/netbox/netbox-docker" ]]; then
  (cd docker/netbox/netbox-docker && docker compose ps) || true
else
  echo "NetBox Docker directory not found."
fi

echo
echo "Generated configs:"
find automation/generated-configs -type f 2>/dev/null | sort || true

echo
echo "Reports:"
find automation/reports -type f 2>/dev/null | sort || true
