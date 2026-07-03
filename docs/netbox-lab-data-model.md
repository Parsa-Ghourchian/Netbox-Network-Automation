# NetBox Lab Data Model

This document describes the initial Source of Truth data model used by the lab.

## Site

| Name | Slug |
| --- | --- |
| LAB-DC1 | lab-dc1 |

## Device Roles

| Role | Purpose |
| --- | --- |
| Edge Router | WAN and edge routing |
| Core Switch | Core/distribution switching |
| Linux Server | Linux-based network service host |

## Manufacturers

| Manufacturer |
| --- |
| MikroTik |
| Cisco |
| Linux |

## Platforms

| Platform | Vendor |
| --- | --- |
| RouterOS | MikroTik |
| Cisco IOS XE | Cisco |
| Linux | Linux |

## Devices

| Device | Platform | Role |
| --- | --- | --- |
| mt-r1 | RouterOS | Edge Router |
| cisco-r1 | Cisco IOS XE | Core Switch |
| linux-srv1 | Linux | Linux Server |

## VLANs

| VLAN ID | Name | Purpose |
| --- | --- | --- |
| 10 | MGMT | Management network |
| 20 | USERS | User access network |
| 30 | SERVERS | Server network |

## Prefixes

| Prefix | Purpose |
| --- | --- |
| 10.10.10.0/24 | Management subnet |
| 10.20.10.0/24 | User subnet |
| 10.30.10.0/24 | Server subnet |
| 192.0.2.0/30 | Lab WAN subnet |

## IP Address Plan

| Device | Interface | IP Address | Purpose |
| --- | --- | --- | --- |
| mt-r1 | ether1 | 192.0.2.1/30 | WAN |
| mt-r1 | ether2 | 10.10.10.1/24 | Management |
| mt-r1 | ether3 | 10.20.10.1/24 | Users gateway |
| cisco-r1 | GigabitEthernet1 | 10.10.10.2/24 | Management |
| cisco-r1 | GigabitEthernet2 | 10.20.10.254/24 | User VLAN |
| linux-srv1 | ens33 | 10.10.10.10/24 | Management |
| linux-srv1 | ens34 | 10.30.10.10/24 | Server network |
