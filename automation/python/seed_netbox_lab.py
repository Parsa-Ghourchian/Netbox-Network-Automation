#!/usr/bin/env python3
"""
Seed NetBox with lab data for the NetBox-driven Network Automation Lab.

This script is intentionally idempotent:
- If an object already exists, it will be reused.
- If an object does not exist, it will be created.

NetBox acts as the Source of Truth for:
- Sites
- Manufacturers
- Device roles
- Device types
- Platforms
- Devices
- Interfaces
- VLANs
- Prefixes
- IP addresses
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_FILE)

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000").rstrip("/")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")

if not NETBOX_TOKEN:
    print("ERROR: NETBOX_TOKEN is not set. Please check your .env file.", file=sys.stderr)
    sys.exit(1)

API_BASE = f"{NETBOX_URL}/api"

def build_auth_header(token: str) -> str:
    """Return the correct NetBox Authorization header value.

    NetBox v4.5+ supports v2 API tokens in this format:
    Authorization: Bearer nbt_<key>.<token>

    Legacy v1 tokens use:
    Authorization: Token <token>
    """
    if token.startswith("nbt_"):
        return f"Bearer {token}"

    return f"Token {token}"


HEADERS = {
    "Authorization": build_auth_header(NETBOX_TOKEN),
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def api_url(endpoint: str) -> str:
    """Build a NetBox API URL from a relative endpoint."""
    endpoint = endpoint.strip("/")

    if not endpoint:
        return f"{API_BASE}/"

    return f"{API_BASE}/{endpoint}/"

def request(method: str, endpoint: str, **kwargs: Any) -> requests.Response:
    """Send an HTTP request to NetBox and fail with useful output on error."""
    url = api_url(endpoint)
    response = requests.request(method, url, headers=HEADERS, timeout=30, **kwargs)

    if response.status_code >= 400:
        print(f"\nERROR: NetBox API request failed: {method} {url}", file=sys.stderr)
        print(f"Status: {response.status_code}", file=sys.stderr)
        print(f"Response: {response.text}", file=sys.stderr)
        response.raise_for_status()

    return response


def get_first(endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the first matching object from a NetBox list endpoint."""
    response = request("GET", endpoint, params=params)
    data = response.json()
    results = data.get("results", [])

    if not results:
        return None

    return results[0]


def create_object(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create an object in NetBox."""
    response = request("POST", endpoint, json=payload)
    return response.json()


def get_or_create(
    endpoint: str,
    lookup: Dict[str, Any],
    payload: Dict[str, Any],
    label: str,
) -> Dict[str, Any]:
    """Get an existing object or create it if missing."""
    existing = get_first(endpoint, lookup)

    if existing:
        print(f"EXISTS  {label}: {existing.get('name') or existing.get('display') or existing.get('prefix') or existing.get('address')}")
        return existing

    created = create_object(endpoint, payload)
    print(f"CREATED {label}: {created.get('name') or created.get('display') or created.get('prefix') or created.get('address')}")
    return created


def check_api() -> None:
    """Verify that the NetBox API is reachable and the token works."""
    response = request("GET", "")
    data = response.json()

    if "dcim" not in data or "ipam" not in data:
        raise RuntimeError("Unexpected NetBox API response. API root does not contain dcim/ipam.")

    print(f"NetBox API OK: {NETBOX_URL}")


def seed_site() -> Dict[str, Any]:
    return get_or_create(
        endpoint="dcim/sites",
        lookup={"slug": "lab-dc1"},
        payload={
            "name": "LAB-DC1",
            "slug": "lab-dc1",
            "status": "active",
            "description": "Primary lab site for NetBox-driven network automation.",
        },
        label="Site",
    )


def seed_manufacturers() -> Dict[str, Dict[str, Any]]:
    items = {
        "mikrotik": {"name": "MikroTik", "slug": "mikrotik"},
        "cisco": {"name": "Cisco", "slug": "cisco"},
        "linux": {"name": "Linux", "slug": "linux"},
    }

    manufacturers = {}

    for key, payload in items.items():
        manufacturers[key] = get_or_create(
            endpoint="dcim/manufacturers",
            lookup={"slug": payload["slug"]},
            payload=payload,
            label="Manufacturer",
        )

    return manufacturers


def seed_device_roles() -> Dict[str, Dict[str, Any]]:
    items = {
        "edge_router": {
            "name": "Edge Router",
            "slug": "edge-router",
            "color": "f44336",
            "description": "WAN or edge routing device.",
        },
        "core_switch": {
            "name": "Core Switch",
            "slug": "core-switch",
            "color": "2196f3",
            "description": "Core or distribution switching device.",
        },
        "linux_server": {
            "name": "Linux Server",
            "slug": "linux-server",
            "color": "4caf50",
            "description": "Linux-based network service host.",
        },
    }

    roles = {}

    for key, payload in items.items():
        roles[key] = get_or_create(
            endpoint="dcim/device-roles",
            lookup={"slug": payload["slug"]},
            payload=payload,
            label="Device Role",
        )

    return roles


def seed_device_types(manufacturers: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    items = {
        "mikrotik_ccr": {
            "manufacturer": manufacturers["mikrotik"]["id"],
            "model": "CCR2004-16G-2S+",
            "slug": "ccr2004-16g-2s-plus",
            "part_number": "CCR2004-16G-2S+",
            "description": "MikroTik lab router model.",
        },
        "cisco_csr": {
            "manufacturer": manufacturers["cisco"]["id"],
            "model": "CSR1000v",
            "slug": "csr1000v",
            "part_number": "CSR1000v",
            "description": "Cisco virtual router model.",
        },
        "ubuntu_server": {
            "manufacturer": manufacturers["linux"]["id"],
            "model": "Ubuntu Server",
            "slug": "ubuntu-server",
            "part_number": "Ubuntu",
            "description": "Generic Ubuntu Linux server.",
        },
    }

    device_types = {}

    for key, payload in items.items():
        device_types[key] = get_or_create(
            endpoint="dcim/device-types",
            lookup={"slug": payload["slug"]},
            payload=payload,
            label="Device Type",
        )

    return device_types


def seed_platforms(manufacturers: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    items = {
        "routeros": {
            "name": "RouterOS",
            "slug": "routeros",
            "manufacturer": manufacturers["mikrotik"]["id"],
            "description": "MikroTik RouterOS platform.",
        },
        "iosxe": {
            "name": "Cisco IOS XE",
            "slug": "cisco-ios-xe",
            "manufacturer": manufacturers["cisco"]["id"],
            "description": "Cisco IOS XE platform.",
        },
        "linux": {
            "name": "Linux",
            "slug": "linux",
            "manufacturer": manufacturers["linux"]["id"],
            "description": "Linux networking platform.",
        },
    }

    platforms = {}

    for key, payload in items.items():
        platforms[key] = get_or_create(
            endpoint="dcim/platforms",
            lookup={"slug": payload["slug"]},
            payload=payload,
            label="Platform",
        )

    return platforms


def seed_vlans() -> Dict[str, Dict[str, Any]]:
    items = {
        "mgmt": {
            "vid": 10,
            "name": "MGMT",
            "status": "active",
            "description": "Management VLAN.",
        },
        "users": {
            "vid": 20,
            "name": "USERS",
            "status": "active",
            "description": "User access VLAN.",
        },
        "servers": {
            "vid": 30,
            "name": "SERVERS",
            "status": "active",
            "description": "Server VLAN.",
        },
    }

    vlans = {}

    for key, payload in items.items():
        vlans[key] = get_or_create(
            endpoint="ipam/vlans",
            lookup={"vid": payload["vid"]},
            payload=payload,
            label="VLAN",
        )

    return vlans


def seed_prefixes(vlans: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    items = {
        "mgmt": {
            "prefix": "10.10.10.0/24",
            "status": "active",
            "vlan": vlans["mgmt"]["id"],
            "description": "Management subnet.",
        },
        "users": {
            "prefix": "10.20.10.0/24",
            "status": "active",
            "vlan": vlans["users"]["id"],
            "description": "User access subnet.",
        },
        "servers": {
            "prefix": "10.30.10.0/24",
            "status": "active",
            "vlan": vlans["servers"]["id"],
            "description": "Server subnet.",
        },
        "wan": {
            "prefix": "192.0.2.0/30",
            "status": "active",
            "description": "Documentation WAN subnet for lab edge connectivity.",
        },
    }

    prefixes = {}

    for key, payload in items.items():
        prefixes[key] = get_or_create(
            endpoint="ipam/prefixes",
            lookup={"prefix": payload["prefix"]},
            payload=payload,
            label="Prefix",
        )

    return prefixes


def seed_devices(
    site: Dict[str, Any],
    roles: Dict[str, Dict[str, Any]],
    device_types: Dict[str, Dict[str, Any]],
    platforms: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    items = {
        "mt_r1": {
            "name": "mt-r1",
            "status": "active",
            "site": site["id"],
            "role": roles["edge_router"]["id"],
            "device_type": device_types["mikrotik_ccr"]["id"],
            "platform": platforms["routeros"]["id"],
            "comments": "MikroTik edge router used for automation lab.",
        },
        "cisco_r1": {
            "name": "cisco-r1",
            "status": "active",
            "site": site["id"],
            "role": roles["core_switch"]["id"],
            "device_type": device_types["cisco_csr"]["id"],
            "platform": platforms["iosxe"]["id"],
            "comments": "Cisco IOS XE lab router used for config generation testing.",
        },
        "linux_srv1": {
            "name": "linux-srv1",
            "status": "active",
            "site": site["id"],
            "role": roles["linux_server"]["id"],
            "device_type": device_types["ubuntu_server"]["id"],
            "platform": platforms["linux"]["id"],
            "comments": "Linux host used for network automation validation.",
        },
    }

    devices = {}

    for key, payload in items.items():
        devices[key] = get_or_create(
            endpoint="dcim/devices",
            lookup={"name": payload["name"]},
            payload=payload,
            label="Device",
        )

    return devices


def seed_interface(device: Dict[str, Any], name: str, description: str) -> Dict[str, Any]:
    return get_or_create(
        endpoint="dcim/interfaces",
        lookup={"device_id": device["id"], "name": name},
        payload={
            "device": device["id"],
            "name": name,
            "type": "1000base-t",
            "enabled": True,
            "description": description,
        },
        label="Interface",
    )


def seed_interfaces(devices: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    interfaces = {}

    interface_plan = {
        "mt_r1_ether1": (devices["mt_r1"], "ether1", "WAN uplink interface."),
        "mt_r1_ether2": (devices["mt_r1"], "ether2", "Management interface."),
        "mt_r1_ether3": (devices["mt_r1"], "ether3", "User VLAN gateway interface."),
        "cisco_r1_gi1": (devices["cisco_r1"], "GigabitEthernet1", "Management interface."),
        "cisco_r1_gi2": (devices["cisco_r1"], "GigabitEthernet2", "User VLAN interface."),
        "linux_srv1_ens33": (devices["linux_srv1"], "ens33", "Management interface."),
        "linux_srv1_ens34": (devices["linux_srv1"], "ens34", "Server network interface."),
    }

    for key, args in interface_plan.items():
        interfaces[key] = seed_interface(*args)

    return interfaces


def seed_ip_address(interface: Dict[str, Any], address: str, description: str) -> Dict[str, Any]:
    return get_or_create(
        endpoint="ipam/ip-addresses",
        lookup={"address": address},
        payload={
            "address": address,
            "status": "active",
            "assigned_object_type": "dcim.interface",
            "assigned_object_id": interface["id"],
            "description": description,
        },
        label="IP Address",
    )


def seed_ip_addresses(interfaces: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    ip_addresses = {}

    ip_plan = {
        "mt_r1_wan": (interfaces["mt_r1_ether1"], "192.0.2.1/30", "MikroTik WAN IP."),
        "mt_r1_mgmt": (interfaces["mt_r1_ether2"], "10.10.10.1/24", "MikroTik management IP."),
        "mt_r1_users": (interfaces["mt_r1_ether3"], "10.20.10.1/24", "MikroTik users gateway IP."),
        "cisco_r1_mgmt": (interfaces["cisco_r1_gi1"], "10.10.10.2/24", "Cisco management IP."),
        "cisco_r1_users": (interfaces["cisco_r1_gi2"], "10.20.10.254/24", "Cisco user VLAN IP."),
        "linux_srv1_mgmt": (interfaces["linux_srv1_ens33"], "10.10.10.10/24", "Linux server management IP."),
        "linux_srv1_servers": (interfaces["linux_srv1_ens34"], "10.30.10.10/24", "Linux server network IP."),
    }

    for key, args in ip_plan.items():
        ip_addresses[key] = seed_ip_address(*args)

    return ip_addresses


def main() -> None:
    print("Starting NetBox lab seed process...")
    check_api()

    site = seed_site()
    manufacturers = seed_manufacturers()
    roles = seed_device_roles()
    device_types = seed_device_types(manufacturers)
    platforms = seed_platforms(manufacturers)
    vlans = seed_vlans()
    seed_prefixes(vlans)
    devices = seed_devices(site, roles, device_types, platforms)
    interfaces = seed_interfaces(devices)
    seed_ip_addresses(interfaces)

    print("\nNetBox lab seed completed successfully.")


if __name__ == "__main__":
    main()
