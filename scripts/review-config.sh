#!/usr/bin/env bash
set -euo pipefail

# Review a generated configuration before pushing it.

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <platform> <device>"
  echo
  echo "Examples:"
  echo "  $0 mikrotik mt-r1"
  echo "  $0 cisco cisco-r1"
  echo "  $0 linux linux-srv1"
  exit 1
fi

PLATFORM="$1"
DEVICE="$2"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "${PLATFORM}" in
  mikrotik)
    CONFIG_FILE="${PROJECT_ROOT}/automation/generated-configs/mikrotik/${DEVICE}.rsc"
    ;;
  cisco)
    CONFIG_FILE="${PROJECT_ROOT}/automation/generated-configs/cisco/${DEVICE}.cfg"
    ;;
  linux)
    CONFIG_FILE="${PROJECT_ROOT}/automation/generated-configs/linux/${DEVICE}.yaml"
    ;;
  *)
    echo "ERROR: Unsupported platform: ${PLATFORM}"
    echo "Supported platforms: mikrotik, cisco, linux"
    exit 1
    ;;
esac

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "ERROR: Config file not found: ${CONFIG_FILE}"
  echo "Run: make generate-configs"
  exit 1
fi

echo "Reviewing generated config:"
echo "${CONFIG_FILE}"
echo
echo "============================================================"
cat "${CONFIG_FILE}"
echo "============================================================"
