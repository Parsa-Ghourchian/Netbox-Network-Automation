#!/usr/bin/env bash
set -euo pipefail

# Prepare demo current-state files from generated configs.
# This simulates actual device configs for compliance testing.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GENERATED_DIR="${PROJECT_ROOT}/automation/generated-configs"
CURRENT_DIR="${PROJECT_ROOT}/automation/compliance/current"

rm -rf "${CURRENT_DIR}"
mkdir -p "${CURRENT_DIR}/mikrotik" "${CURRENT_DIR}/cisco" "${CURRENT_DIR}/linux"

cp "${GENERATED_DIR}/mikrotik/"*.rsc "${CURRENT_DIR}/mikrotik/" 2>/dev/null || true
cp "${GENERATED_DIR}/cisco/"*.cfg "${CURRENT_DIR}/cisco/" 2>/dev/null || true
cp "${GENERATED_DIR}/linux/"*.yaml "${CURRENT_DIR}/linux/" 2>/dev/null || true

# Introduce a small intentional drift in the MikroTik current snapshot.
# This allows the compliance report to demonstrate NON_COMPLIANT output.
if [[ -f "${CURRENT_DIR}/mikrotik/mt-r1.rsc" ]]; then
  sed -i 's/User VLAN gateway interface./User VLAN gateway interface. DRIFTED-BY-DEMO/' "${CURRENT_DIR}/mikrotik/mt-r1.rsc"
fi

echo "Demo current-state files prepared in: automation/compliance/current"
