# Makefile for NetBox-driven Network Automation Lab
# Use this file to keep common operational commands simple and repeatable.

PROJECT_NAME=netbox-network-automation-lab

.PHONY: help tree docker-version compose-version netbox-up netbox-down netbox-status netbox-logs netbox-seed generate-configs ansible-version ansible-inventory ansible-collections ansible-connectivity backup-mikrotik backup-cisco backup-linux compliance-demo-current compliance-check-current compliance-check-backups compliance-check-backups-strict review-config push-mikrotik push-cisco stage-linux-netplan validate security-scan clean-runtime project-status

help:
	@echo "Available commands:"
	@echo "  make tree                  Show project directory tree"
	@echo "  make docker-version        Show Docker version"
	@echo "  make compose-version       Show Docker Compose version"
	@echo "  make netbox-up             Start NetBox Docker stack"
	@echo "  make netbox-down           Stop NetBox Docker stack"
	@echo "  make netbox-status         Show NetBox Docker stack status"
	@echo "  make netbox-logs           Follow NetBox application logs"
	@echo "  make netbox-seed           Seed NetBox with lab data"
	@echo "  make generate-configs      Generate configs from NetBox Source of Truth"
	@echo "  make ansible-version       Show Ansible version"
	@echo "  make ansible-inventory     Show parsed Ansible inventory"
	@echo "  make ansible-connectivity  Run connectivity checks"
	@echo "  make backup-mikrotik       Backup MikroTik RouterOS config"
	@echo "  make backup-cisco          Backup Cisco running config"
	@echo "  make backup-linux          Backup Linux network state"
	@echo "  make ansible-collections   Show installed Ansible collections"
	@echo "  make compliance-demo-current       Prepare demo current configs with intentional drift"
	@echo "  make compliance-check-current      Compare generated configs with current snapshots"
	@echo "  make compliance-check-backups      Compare generated configs with latest backups"
	@echo "  make compliance-check-backups-strict  Same as backups check, but fails on drift"
	@echo "  make review-config PLATFORM=<platform> DEVICE=<device>      Review generated config"
	@echo "  make push-mikrotik DEVICE=<device> APPROVE=YES_I_UNDERSTAND Push MikroTik config safely"
	@echo "  make push-cisco DEVICE=<device> APPROVE=YES_I_UNDERSTAND    Push Cisco config safely"
	@echo "  make stage-linux-netplan DEVICE=<device> APPROVE=YES_I_UNDERSTAND Stage Linux Netplan only"
	@echo "  make validate              Run full project validation"
	@echo "  make security-scan         Run basic secret/runtime scan"
	@echo "  make clean-runtime         Remove generated runtime files"
	@echo "  make project-status        Show project status summary"

tree:
	tree -L 4

docker-version:
	docker --version

compose-version:
	docker compose version

netbox-up:
	./scripts/netbox-up.sh

netbox-down:
	./scripts/netbox-down.sh

netbox-status:
	./scripts/netbox-status.sh

netbox-logs:
	./scripts/netbox-logs.sh

netbox-seed:
	./scripts/netbox-seed.sh

generate-configs:
	./scripts/generate-configs.sh

ansible-version:
	@./.venv/bin/ansible --version

ansible-inventory:
	./scripts/ansible-inventory.sh --list

ansible-collections:
	@./.venv/bin/ansible-galaxy collection list -p automation/ansible/collections | grep -E "ansible.netcommon|community.routeros|cisco.ios"

ansible-connectivity:
	./scripts/ansible-playbook.sh playbooks/connectivity_check.yml

backup-mikrotik:
	./scripts/ansible-playbook.sh playbooks/backup_mikrotik.yml

backup-cisco:
	./scripts/ansible-playbook.sh playbooks/backup_cisco.yml

backup-linux:
	./scripts/ansible-playbook.sh playbooks/backup_linux_network.yml

compliance-demo-current:
	./scripts/prepare-demo-current.sh

compliance-check-current:
	./scripts/compliance-check.sh --actual-source current

compliance-check-backups:
	./scripts/compliance-check.sh --actual-source backups

compliance-check-backups-strict:
	./scripts/compliance-check.sh --actual-source backups --fail-on-drift
review-config:
	@test -n "$(PLATFORM)" || (echo "ERROR: PLATFORM is required. Example: make review-config PLATFORM=mikrotik DEVICE=mt-r1" && exit 1)
	@test -n "$(DEVICE)" || (echo "ERROR: DEVICE is required. Example: make review-config PLATFORM=mikrotik DEVICE=mt-r1" && exit 1)
	./scripts/review-config.sh "$(PLATFORM)" "$(DEVICE)"

push-mikrotik:
	@test -n "$(DEVICE)" || (echo "ERROR: DEVICE is required. Example: make push-mikrotik DEVICE=mt-r1 APPROVE=YES_I_UNDERSTAND" && exit 1)
	@test "$(APPROVE)" = "YES_I_UNDERSTAND" || (echo "ERROR: APPROVE=YES_I_UNDERSTAND is required" && exit 1)
	./scripts/ansible-playbook.sh playbooks/push_mikrotik.yml -e target_device="$(DEVICE)" -e approve_push="$(APPROVE)"

push-cisco:
	@test -n "$(DEVICE)" || (echo "ERROR: DEVICE is required. Example: make push-cisco DEVICE=cisco-r1 APPROVE=YES_I_UNDERSTAND" && exit 1)
	@test "$(APPROVE)" = "YES_I_UNDERSTAND" || (echo "ERROR: APPROVE=YES_I_UNDERSTAND is required" && exit 1)
	./scripts/ansible-playbook.sh playbooks/push_cisco.yml -e target_device="$(DEVICE)" -e approve_push="$(APPROVE)"

stage-linux-netplan:
	@test -n "$(DEVICE)" || (echo "ERROR: DEVICE is required. Example: make stage-linux-netplan DEVICE=linux-srv1 APPROVE=YES_I_UNDERSTAND" && exit 1)
	@test "$(APPROVE)" = "YES_I_UNDERSTAND" || (echo "ERROR: APPROVE=YES_I_UNDERSTAND is required" && exit 1)
	./scripts/ansible-playbook.sh playbooks/stage_linux_netplan.yml -e target_device="$(DEVICE)" -e approve_push="$(APPROVE)"
validate:
	./scripts/validate-project.sh

security-scan:
	./scripts/security-scan.sh

clean-runtime:
	./scripts/clean-runtime.sh

project-status:
	./scripts/project-status.sh
