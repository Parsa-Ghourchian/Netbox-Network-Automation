#!/usr/bin/env python3
"""
Generate network device configurations from NetBox Source of Truth data.

Generated outputs:
- MikroTik RouterOS script
- Cisco IOS-like configuration
- Linux Netplan YAML

This script is read-only against NetBox.
It does not push configuration to any network device.
"""

from __future__ import annotations

import ipaddress
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from netbox_client.client import NetBoxClient


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

TEMPLATE_DIR = PROJECT_ROOT / "automation" / "templates"
OUTPUT_DIR = PROJECT_ROOT / "automation" / "generated-configs"

load_dotenv(ENV_FILE)

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000").rstrip("/")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")

if not NETBOX_TOKEN:
    print("ERROR: NETBOX_TOKEN is not set. Please check your .env file.", file=sys.stderr)
    sys.exit(1)


def cidr_to_netmask(address: str) -> str:
    """Convert CIDR address to dotted decimal netmask."""
    interface = ipaddress.ip_interface(address)
    return str(interface.network.netmask)


def ip_without_prefix(address: str) -> str:
    """Return IP address without prefix length."""
    interface = ipaddress.ip_interface(address)
    return str(interface.ip)


def is_ipv4(address: str) -> bool:
    """Return True if the address is IPv4."""
    return ipaddress.ip_interface(address).version == 4


def ensure_directories() -> None:
    """Create output directories if they do not exist."""
    for path in [
        OUTPUT_DIR / "mikrotik",
        OUTPUT_DIR / "cisco",
        OUTPUT_DIR / "linux",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def load_netbox_data(client: NetBoxClient) -> Dict[str, List[Dict[str, Any]]]:
    """Load required Source of Truth data from NetBox."""
    print("Loading data from NetBox API...")

    data = {
        "devices": client.list_all("dcim/devices"),
        "interfaces": client.list_all("dcim/interfaces"),
        "ip_addresses": client.list_all("ipam/ip-addresses"),
        "vlans": client.list_all("ipam/vlans"),
        "prefixes": client.list_all("ipam/prefixes"),
    }

    print(f"Loaded devices: {len(data['devices'])}")
    print(f"Loaded interfaces: {len(data['interfaces'])}")
    print(f"Loaded IP addresses: {len(data['ip_addresses'])}")
    print(f"Loaded VLANs: {len(data['vlans'])}")
    print(f"Loaded prefixes: {len(data['prefixes'])}")

    return data


def get_platform_slug(device: Dict[str, Any]) -> str:
    """Return platform slug from a NetBox device object."""
    platform = device.get("platform")

    if not platform:
        return ""

    return platform.get("slug", "")


def build_device_context(
    device: Dict[str, Any],
    interfaces: List[Dict[str, Any]],
    ip_addresses: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build template context for a single device."""
    device_id = device["id"]

    device_interfaces = [
        interface
        for interface in interfaces
        if interface.get("device", {}).get("id") == device_id
    ]

    enriched_interfaces = []

    for interface in device_interfaces:
        interface_id = interface["id"]

        interface_ips = []
        for ip in ip_addresses:
            assigned_object = ip.get("assigned_object") or {}

            if assigned_object.get("id") == interface_id:
                address = ip["address"]

                ip_data = {
                    "address": address,
                    "ip": ip_without_prefix(address),
                    "netmask": cidr_to_netmask(address),
                    "is_ipv4": is_ipv4(address),
                    "description": ip.get("description") or "",
                    "interface_name": interface["name"],
                }

                interface_ips.append(ip_data)

        enriched = {
            "id": interface["id"],
            "name": interface["name"],
            "type": interface.get("type", {}).get("value") or interface.get("type"),
            "enabled": interface.get("enabled", True),
            "description": interface.get("description") or "",
            "ip_addresses": interface_ips,
        }

        enriched_interfaces.append(enriched)

    all_device_ips = [
        ip
        for interface in enriched_interfaces
        for ip in interface["ip_addresses"]
    ]

    return {
        "device": {
            "id": device["id"],
            "name": device["name"],
            "status": device.get("status", {}).get("value"),
            "role": (device.get("role") or {}).get("name"),
            "platform": (device.get("platform") or {}).get("name"),
            "platform_slug": get_platform_slug(device),
            "site": (device.get("site") or {}).get("name"),
        },
        "interfaces": enriched_interfaces,
        "ip_addresses": all_device_ips,
    }


def render_template(template_name: str, context: Dict[str, Any]) -> str:
    """Render a Jinja2 template."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(template_name)
    return template.render(**context)


def write_output(path: Path, content: str) -> None:
    """Write generated configuration to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(f"Generated: {path.relative_to(PROJECT_ROOT)}")


def generate_for_device(context: Dict[str, Any]) -> None:
    """Generate configuration based on device platform."""
    device = context["device"]
    platform_slug = device["platform_slug"]
    device_name = device["name"]

    if platform_slug == "routeros":
        content = render_template("mikrotik/routeros.rsc.j2", context)
        write_output(OUTPUT_DIR / "mikrotik" / f"{device_name}.rsc", content)
        return

    if platform_slug == "cisco-ios-xe":
        content = render_template("cisco/ios.cfg.j2", context)
        write_output(OUTPUT_DIR / "cisco" / f"{device_name}.cfg", content)
        return

    if platform_slug == "linux":
        content = render_template("linux/netplan.yaml.j2", context)
        write_output(OUTPUT_DIR / "linux" / f"{device_name}.yaml", content)
        return

    print(f"SKIPPED: {device_name} has unsupported platform: {platform_slug}")


def main() -> None:
    """Generate configs for all supported NetBox devices."""
    ensure_directories()

    client = NetBoxClient(base_url=NETBOX_URL, token=NETBOX_TOKEN)
    client.get("")

    data = load_netbox_data(client)

    print("\nGenerating configuration files...")

    for device in data["devices"]:
        context = build_device_context(
            device=device,
            interfaces=data["interfaces"],
            ip_addresses=data["ip_addresses"],
        )

        generate_for_device(context)

    print("\nConfig generation completed successfully.")


if __name__ == "__main__":
    main()
