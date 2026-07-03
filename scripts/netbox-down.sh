#!/usr/bin/env bash
set -euo pipefail

# Stop the local NetBox Docker stack without deleting volumes.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NETBOX_DIR="${PROJECT_ROOT}/docker/netbox/netbox-docker"

cd "${NETBOX_DIR}"
docker compose down
