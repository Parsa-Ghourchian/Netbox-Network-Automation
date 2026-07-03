#!/usr/bin/env bash
set -euo pipefail

# Basic security scan for accidental secret leakage.
# This is not a replacement for professional secret scanning tools,
# but it helps catch obvious mistakes before committing to GitHub.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "Running basic security scan..."

FAILED=0

echo
echo "Checking that .env is not tracked by Git..."
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "ERROR: .env is tracked by Git. Remove it with: git rm --cached .env"
  FAILED=1
else
  echo "OK: .env is not tracked."
fi

echo
echo "Checking for obvious secrets in tracked files..."
SECRET_PATTERNS=(
  "NETBOX_TOKEN=nbt_"
  "NETBOX_TOKEN=012345"
  "MIKROTIK_PASSWORD="
  "CISCO_PASSWORD="
  "LINUX_PASSWORD="
  "Admin@123456"
)

for pattern in "${SECRET_PATTERNS[@]}"; do
  if git grep -n "${pattern}" -- . ':!.env.example' ':!docs/netbox-local-setup.md' >/tmp/security-scan-match.txt 2>/dev/null; then
    echo "WARNING: Potential secret pattern found: ${pattern}"
    cat /tmp/security-scan-match.txt
    FAILED=1
  fi
done

rm -f /tmp/security-scan-match.txt

echo
echo "Checking ignored runtime directories..."
RUNTIME_PATHS=(
  "automation/generated-configs"
  "automation/backups"
  "automation/reports"
  "automation/compliance/current"
)

for path in "${RUNTIME_PATHS[@]}"; do
  if git ls-files "${path}" | grep -q .; then
    echo "ERROR: Runtime path has tracked files: ${path}"
    git ls-files "${path}"
    FAILED=1
  else
    echo "OK: ${path} is not tracked."
  fi
done

echo
if [[ "${FAILED}" -ne 0 ]]; then
  echo "Security scan failed."
  exit 1
fi

echo "Security scan passed."
