# Ansible Automation

This directory contains Ansible automation for the NetBox-driven Network Automation Lab.

## Scope

Current supported tasks:

- Inventory validation
- MikroTik connectivity check
- Cisco connectivity check
- Linux connectivity check
- MikroTik configuration backup
- Cisco configuration backup
- Linux network state backup

## Safety

Generated configs are not pushed automatically.

Configuration push playbooks will be added separately and must be reviewed before execution.

## Required Environment Variables

Credentials are loaded from the root `.env` file by `scripts/ansible-playbook.sh`.

```env
MIKROTIK_USER=admin
MIKROTIK_PASSWORD=change_me
MIKROTIK_PORT=22

CISCO_USER=admin
CISCO_PASSWORD=change_me
CISCO_PORT=22
CISCO_ENABLE=false
CISCO_ENABLE_PASSWORD=

LINUX_USER=parsa
LINUX_PASSWORD=change_me
LINUX_PORT=22
