# Safe Config Push

This project supports controlled configuration push using Ansible.

## Safety Model

Configuration push is intentionally protected by multiple gates:

1. Generated config must exist.
2. Operator must review generated config.
3. Push requires an explicit approval variable.
4. Target device must be specified.
5. A pre-change backup is collected before push.
6. Linux Netplan is staged only and not applied automatically.

## Review Generated Config

```bash
make review-config PLATFORM=mikrotik DEVICE=mt-r1
make review-config PLATFORM=cisco DEVICE=cisco-r1
make review-config PLATFORM=linux DEVICE=linux-srv1
