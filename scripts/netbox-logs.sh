#!/usr/bin/env bash
set -euo pipefail

# Follow NetBox application logs.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NETBOX_DIR="${PROJECT_ROOT}/docker/netbox/netbox-docker"

cd "${NETBOX_DIR}"
docker compose logs -f netbox
