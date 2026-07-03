# Config Generation

This project generates network configuration files from NetBox Source of Truth data.

## Flow

```text
NetBox API -> Python Client -> Jinja2 Templates -> Generated Configs
Supported Platforms
Platform	NetBox Platform Slug	Output
MikroTik RouterOS	routeros	.rsc
Cisco IOS XE	cisco-ios-xe	.cfg
Linux	linux	.yaml
Generate Configs
make generate-configs
Output Paths
automation/generated-configs/mikrotik/
automation/generated-configs/cisco/
automation/generated-configs/linux/
Safety

Generated configs are not pushed automatically.
Every output must be reviewed before being applied to a network device or host.
