#!/usr/bin/env bash
set -euo pipefail

# Validate the NetBox-driven Network Automation Lab project.
# This script checks structure, dependencies, NetBox API availability,
# config generation, Ansible inventory, and compliance demo workflow.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "Validating project: ${PROJECT_ROOT}"
echo

fail() {
  echo "ERROR: $1"
  exit 1
}

check_file() {
  local file="$1"
  [[ -f "${file}" ]] || fail "Missing file: ${file}"
  echo "OK: ${file}"
}

check_dir() {
  local dir="$1"
  [[ -d "${dir}" ]] || fail "Missing directory: ${dir}"
  echo "OK: ${dir}"
}

echo "1) Checking required files..."
check_file "README.md"
check_file "Makefile"
check_file ".gitignore"
check_file ".env.example"
check_file "VERSION"
check_file "CHANGELOG.md"
check_file "automation/python/seed_netbox_lab.py"
check_file "automation/python/generate_configs.py"
check_file "automation/python/compliance_check.py"
check_file "automation/ansible/ansible.cfg"
check_file "automation/ansible/inventory/lab.yml"

echo
echo "2) Checking required directories..."
check_dir "automation/python"
check_dir "automation/templates"
check_dir "automation/ansible"
check_dir "docs"
check_dir "scripts"

echo
echo "3) Checking Python virtual environment..."
[[ -x ".venv/bin/python" ]] || fail "Python venv not found. Run: python3 -m venv .venv"
[[ -x ".venv/bin/ansible" ]] || fail "Ansible not found in .venv. Install Ansible requirements."
echo "OK: Python virtual environment"

echo
echo "4) Checking Docker..."
docker --version >/dev/null || fail "Docker is not available"
docker compose version >/dev/null || fail "Docker Compose is not available"
echo "OK: Docker and Docker Compose"

echo
echo "5) Checking NetBox HTTP..."
if curl -fsS -I http://localhost:8000 >/dev/null; then
  echo "OK: NetBox HTTP is reachable"
else
  fail "NetBox is not reachable on http://localhost:8000. Run: make netbox-up"
fi

echo
echo "6) Checking .env..."
[[ -f ".env" ]] || fail ".env not found. Run: cp .env.example .env and configure NETBOX_TOKEN"
grep -q '^NETBOX_URL=' .env || fail "NETBOX_URL missing in .env"
grep -q '^NETBOX_TOKEN=' .env || fail "NETBOX_TOKEN missing in .env"
echo "OK: .env exists"

echo
echo "7) Checking config generation..."
make generate-configs >/tmp/netbox-lab-generate.log
cat /tmp/netbox-lab-generate.log
rm -f /tmp/netbox-lab-generate.log

check_file "automation/generated-configs/mikrotik/mt-r1.rsc"
check_file "automation/generated-configs/cisco/cisco-r1.cfg"
check_file "automation/generated-configs/linux/linux-srv1.yaml"

echo
echo "8) Checking Ansible inventory..."
make ansible-inventory >/tmp/netbox-lab-inventory.json
grep -q "mt-r1" /tmp/netbox-lab-inventory.json || fail "mt-r1 not found in Ansible inventory"
grep -q "cisco-r1" /tmp/netbox-lab-inventory.json || fail "cisco-r1 not found in Ansible inventory"
grep -q "linux-srv1" /tmp/netbox-lab-inventory.json || fail "linux-srv1 not found in Ansible inventory"
rm -f /tmp/netbox-lab-inventory.json
echo "OK: Ansible inventory"

echo
echo "9) Checking compliance demo..."
make compliance-demo-current >/dev/null
make compliance-check-current >/tmp/netbox-lab-compliance.log
cat /tmp/netbox-lab-compliance.log
rm -f /tmp/netbox-lab-compliance.log

check_file "automation/reports/compliance/compliance-summary.txt"
check_file "automation/reports/compliance/compliance-report.json"
check_file "automation/reports/compliance/compliance-report.html"

echo
echo "10) Running security scan..."
./scripts/security-scan.sh

echo
echo "Project validation completed successfully."
