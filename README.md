# 🧠 NetBox-Driven Network Automation Lab

![NetBox](https://img.shields.io/badge/NetBox-Source_of_Truth-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)
![Python](https://img.shields.io/badge/Python-Automation-3776AB.svg)
![Ansible](https://img.shields.io/badge/Ansible-Network_Automation-red.svg)
![MikroTik](https://img.shields.io/badge/MikroTik-RouterOS-orange.svg)
![Cisco](https://img.shields.io/badge/Cisco-IOS_XE-1BA0D7.svg)
![Linux](https://img.shields.io/badge/Linux-Netplan-black.svg)
![Status](https://img.shields.io/badge/Status-Lab_Ready-brightgreen.svg)

**NetBox-Driven Network Automation Lab** is a production-style network automation project that uses **NetBox as the Source of Truth** to model network infrastructure, generate device configurations, perform backups, check compliance, produce diff reports, and safely push configuration using Ansible.

The project demonstrates a complete network automation workflow:

```text
NetBox Source of Truth
        ↓
Python API Automation
        ↓
Jinja2 Config Generation
        ↓
Ansible Backup / Push
        ↓
Compliance Check
        ↓
Diff Report
```

This lab is designed for network engineers, DevOps engineers, infrastructure engineers, and automation learners who want to understand how a real Source-of-Truth-driven network automation pipeline works.

---

## 🚀 Features

* **NetBox as Source of Truth:** Model sites, devices, platforms, interfaces, VLANs, prefixes, and IP addresses
* **Dockerized NetBox:** Run NetBox locally with Docker Compose
* **Python API Automation:** Read network inventory and IPAM data from the NetBox REST API
* **Config Generation:** Generate device configuration files from NetBox data using Jinja2 templates
* **Multi-Platform Support:** Generate configs for MikroTik RouterOS, Cisco IOS-like devices, and Linux Netplan
* **Ansible Inventory:** Manage MikroTik, Cisco, and Linux targets through a clean Ansible inventory
* **Configuration Backup:** Collect current configuration from network devices before changes
* **Compliance Check:** Compare generated desired state against current or backed-up actual state
* **Diff Reports:** Produce human-readable, JSON, HTML, and unified diff reports
* **Safe Config Push:** Push configuration only with explicit approval and pre-change backup
* **Security-Aware Structure:** Secrets, generated outputs, backups, logs, and vendored collections are excluded from Git
* **Validation Workflow:** Includes project validation, security scan, and runtime cleanup scripts
* **GitHub-Friendly Layout:** Clean structure, documentation, scripts, Makefile targets, and roadmap

---

## 🧩 Architecture

```text
                         +----------------------+
                         |      NetBox UI       |
                         | Source of Truth      |
                         +----------+-----------+
                                    |
                                    | REST API
                                    v
                         +----------------------+
                         | Python Automation    |
                         | API Reader / Parser  |
                         +----------+-----------+
                                    |
                                    | Jinja2 Templates
                                    v
       +----------------------------+----------------------------+
       |                            |                            |
       v                            v                            v
+-------------+              +-------------+              +-------------+
| MikroTik    |              | Cisco IOS   |              | Linux       |
| .rsc Config |              | .cfg Config |              | Netplan YAML|
+------+------+              +------+------+              +------+------+
       |                            |                            |
       |                            |                            |
       v                            v                            v
+-------------+              +-------------+              +-------------+
| Ansible     |              | Ansible     |              | Ansible     |
| Backup/Push |              | Backup/Push |              | Stage Only  |
+------+------+              +------+------+              +------+------+
       |                            |                            |
       +----------------------------+----------------------------+
                                    |
                                    v
                         +----------------------+
                         | Compliance Engine    |
                         | Diff + HTML Reports  |
                         +----------------------+
```

---

## 🔁 Automation Flow

```text
1. Define network data in NetBox
2. Seed lab devices, VLANs, prefixes, interfaces, and IPs
3. Generate desired configuration from NetBox
4. Review generated configuration
5. Backup actual device configuration
6. Compare desired state vs actual state
7. Generate compliance and diff reports
8. Push configuration only with explicit approval
```

---

## 🛠️ Tech Stack

| Layer                    | Technology                             |
| ------------------------ | -------------------------------------- |
| Source of Truth          | NetBox                                 |
| Container Runtime        | Docker Engine                          |
| Orchestration            | Docker Compose                         |
| Automation Language      | Python                                 |
| API Integration          | NetBox REST API                        |
| Templating               | Jinja2                                 |
| Configuration Management | Ansible                                |
| MikroTik Automation      | `community.routeros`                   |
| Cisco Automation         | `cisco.ios`                            |
| Network CLI Transport    | `ansible.netcommon`                    |
| Linux Network Config     | Netplan                                |
| Reports                  | JSON, HTML, text summary, unified diff |
| Target Environment       | Local Ubuntu / Linux workstation       |

---

## 📂 Project Structure

```text
.
├── automation
│   ├── ansible
│   │   ├── ansible.cfg
│   │   ├── group_vars
│   │   │   ├── cisco.yml
│   │   │   ├── linux_hosts.yml
│   │   │   └── mikrotik.yml
│   │   ├── inventory
│   │   │   └── lab.yml
│   │   ├── playbooks
│   │   │   ├── backup_cisco.yml
│   │   │   ├── backup_linux_network.yml
│   │   │   ├── backup_mikrotik.yml
│   │   │   ├── connectivity_check.yml
│   │   │   ├── push_cisco.yml
│   │   │   ├── push_mikrotik.yml
│   │   │   └── stage_linux_netplan.yml
│   │   ├── requirements.txt
│   │   ├── requirements.yml
│   │   └── README.md
│   ├── python
│   │   ├── compliance_check.py
│   │   ├── generate_configs.py
│   │   ├── netbox_client
│   │   │   ├── client.py
│   │   │   └── __init__.py
│   │   ├── requirements.txt
│   │   └── seed_netbox_lab.py
│   └── templates
│       ├── cisco
│       │   └── ios.cfg.j2
│       ├── linux
│       │   └── netplan.yaml.j2
│       └── mikrotik
│           └── routeros.rsc.j2
├── docs
│   ├── compliance-and-diff-report.md
│   ├── config-generation.md
│   ├── netbox-lab-data-model.md
│   ├── netbox-local-setup.md
│   └── safe-config-push.md
├── scripts
│   ├── ansible-inventory.sh
│   ├── ansible-playbook.sh
│   ├── clean-runtime.sh
│   ├── compliance-check.sh
│   ├── generate-configs.sh
│   ├── netbox-down.sh
│   ├── netbox-logs.sh
│   ├── netbox-seed.sh
│   ├── netbox-status.sh
│   ├── netbox-up.sh
│   ├── prepare-demo-current.sh
│   ├── project-status.sh
│   ├── review-config.sh
│   ├── security-scan.sh
│   └── validate-project.sh
├── .editorconfig
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── Makefile
├── README.md
└── VERSION
```

---

## 📦 Main Components

| Component           | Purpose                                                                 |
| ------------------- | ----------------------------------------------------------------------- |
| NetBox              | Source of Truth for network inventory, IPAM, VLANs, and device metadata |
| Python Client       | Reads NetBox API data and prepares automation context                   |
| Jinja2 Templates    | Generate device-specific configuration files                            |
| Ansible Inventory   | Defines MikroTik, Cisco, and Linux automation targets                   |
| Backup Playbooks    | Collect current configuration/state before changes                      |
| Compliance Engine   | Compares desired config against actual config                           |
| Diff Reports        | Shows exact configuration drift                                         |
| Safe Push Playbooks | Push or stage config only after explicit approval                       |
| Makefile            | Provides simple operational commands                                    |
| Validation Scripts  | Check project health, security, and runtime behavior                    |

---

## 🌐 Local URLs

| Service         | URL                                            |
| --------------- | ---------------------------------------------- |
| NetBox UI       | `http://localhost:8000`                        |
| NetBox API      | `http://localhost:8000/api/`                   |
| NetBox API Docs | `http://localhost:8000/api/schema/swagger-ui/` |

---

## ⚙️ Prerequisites

Before running this project, make sure your machine has:

* Ubuntu or another Linux distribution
* Docker Engine
* Docker Compose plugin
* Python 3
* Git
* Make
* curl
* jq
* At least 4 GB RAM recommended

Check basic requirements:

```bash
docker --version
docker compose version
python3 --version
git --version
make --version
jq --version
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
https://github.com/Parsa-Ghourchian/Netbox-Network-Automation.git
cd Netbox-Network-Automation
```

Or, if you are working locally:

```bash
cd ~/project/netbox-network-automation-lab
```

---

### 2. Create Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install --upgrade pip
pip install -r automation/python/requirements.txt
pip install -r automation/ansible/requirements.txt
```

---

### 3. Install Ansible Collections

```bash
ansible-galaxy collection install \
  -r automation/ansible/requirements.yml \
  -p automation/ansible/collections
```

Verify collections:

```bash
make ansible-collections
```

Expected collections:

```text
ansible.netcommon
community.routeros
cisco.ios
```

---

### 4. Prepare Environment File

```bash
cp .env.example .env
nano .env
```

Example:

```env
NETBOX_URL=http://localhost:8000
NETBOX_TOKEN=change_me

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
```

Do not commit `.env`.

---

## 🐳 NetBox Setup

This project expects NetBox Docker to be cloned locally under:

```text
docker/netbox/netbox-docker/
```

The upstream NetBox Docker repository is intentionally not committed into this repository.

### 1. Clone NetBox Docker

```bash
mkdir -p docker/netbox

git clone -b release \
  https://github.com/netbox-community/netbox-docker.git \
  docker/netbox/netbox-docker
```

---

### 2. Create Docker Compose Override

```bash
cd docker/netbox/netbox-docker
cp docker-compose.override.yml.example docker-compose.override.yml
nano docker-compose.override.yml
```

Minimal local override:

```yaml
services:
  netbox:
    ports:
      - "8000:8080"
    environment:
      SKIP_SUPERUSER: "false"
      SUPERUSER_NAME: "admin"
      SUPERUSER_EMAIL: "admin@example.local"
      SUPERUSER_PASSWORD: "change_me"
```

Return to project root:

```bash
cd ../../../
```

---

### 3. Start NetBox

```bash
make netbox-up
```

Check status:

```bash
make netbox-status
```

Open NetBox:

```text
http://localhost:8000
```

---

## 🔐 NetBox API Token

After NetBox is running, create a token and save it in `.env`.

### Provision Token

```bash
TOKEN_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  http://localhost:8000/api/users/tokens/provision/ \
  --data '{
    "username": "admin",
    "password": "change_me"
  }')

echo "$TOKEN_RESPONSE" | jq
```

Build token value:

```bash
export NEW_NETBOX_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '
  if (.token // "") | startswith("nbt_") then
    .token
  elif (.key and .token) then
    "nbt_\(.key).\(.token)"
  else
    empty
  end
')

echo "$NEW_NETBOX_TOKEN"
```

Update `.env`:

```bash
sed -i "s#^NETBOX_TOKEN=.*#NETBOX_TOKEN=${NEW_NETBOX_TOKEN}#" .env
```

Test API:

```bash
source .env

curl -s \
  -H "Authorization: Bearer $NETBOX_TOKEN" \
  -H "Accept: application/json" \
  "$NETBOX_URL/api/" | jq
```

---

## 🧬 Seed NetBox Lab Data

Seed initial lab data into NetBox:

```bash
make netbox-seed
```

This creates:

```text
Site
Manufacturers
Device Roles
Device Types
Platforms
Devices
Interfaces
VLANs
Prefixes
IP Addresses
```

Expected lab devices:

```text
mt-r1
cisco-r1
linux-srv1
```

Expected VLANs:

```text
10 MGMT
20 USERS
30 SERVERS
```

---

## 🧾 Lab Data Model

| Object Type       | Example         |
| ----------------- | --------------- |
| Site              | `LAB-DC1`       |
| MikroTik Device   | `mt-r1`         |
| Cisco Device      | `cisco-r1`      |
| Linux Host        | `linux-srv1`    |
| Management VLAN   | `10 MGMT`       |
| Users VLAN        | `20 USERS`      |
| Servers VLAN      | `30 SERVERS`    |
| Management Prefix | `10.10.10.0/24` |
| Users Prefix      | `10.20.10.0/24` |
| Servers Prefix    | `10.30.10.0/24` |

More details:

```text
docs/netbox-lab-data-model.md
```

---

## ⚙️ Generate Configuration

Generate configs from NetBox Source of Truth:

```bash
make generate-configs
```

Generated outputs:

```text
automation/generated-configs/mikrotik/mt-r1.rsc
automation/generated-configs/cisco/cisco-r1.cfg
automation/generated-configs/linux/linux-srv1.yaml
```

Review MikroTik config:

```bash
cat automation/generated-configs/mikrotik/mt-r1.rsc
```

Review Cisco config:

```bash
cat automation/generated-configs/cisco/cisco-r1.cfg
```

Review Linux Netplan config:

```bash
cat automation/generated-configs/linux/linux-srv1.yaml
```

Generated configuration files are runtime outputs and are not committed to Git.

---

## 📄 Example Generated MikroTik Config

```routeros
# Generated by NetBox-driven Network Automation Lab
/system identity set name="mt-r1"

/interface ethernet set [ find default-name=ether1 ] comment="WAN uplink interface."
/interface ethernet set [ find default-name=ether2 ] comment="Management interface."
/interface ethernet set [ find default-name=ether3 ] comment="User VLAN gateway interface."

/ip address remove [ find comment="NetBox: mt-r1 ether1" ]
/ip address add address=192.0.2.1/30 interface=ether1 comment="NetBox: mt-r1 ether1"

/ip address remove [ find comment="NetBox: mt-r1 ether2" ]
/ip address add address=10.10.10.1/24 interface=ether2 comment="NetBox: mt-r1 ether2"

/ip address remove [ find comment="NetBox: mt-r1 ether3" ]
/ip address add address=10.20.10.1/24 interface=ether3 comment="NetBox: mt-r1 ether3"
```

---

## 📄 Example Generated Cisco Config

```cisco
hostname cisco-r1

interface GigabitEthernet1
 description Management interface.
 no shutdown
 ip address 10.10.10.2 255.255.255.0
!

interface GigabitEthernet2
 description User VLAN interface.
 no shutdown
 ip address 10.20.10.254 255.255.255.0
!
```

---

## 📄 Example Generated Linux Netplan Config

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:
      dhcp4: false
      addresses:
        - 10.10.10.10/24
    ens34:
      dhcp4: false
      addresses:
        - 10.30.10.10/24
```

---

## 🧪 Health Check

### Check NetBox

```bash
make netbox-status
curl -I http://localhost:8000
```

Expected response:

```text
HTTP/1.1 200 OK
```

or:

```text
HTTP/1.1 302 Found
```

---

### Check NetBox API

```bash
source .env

curl -s \
  -H "Authorization: Bearer $NETBOX_TOKEN" \
  -H "Accept: application/json" \
  "$NETBOX_URL/api/" | jq
```

---

### Check Seeded Devices

```bash
source .env

curl -s \
  -H "Authorization: Bearer $NETBOX_TOKEN" \
  "$NETBOX_URL/api/dcim/devices/" | jq '.results[] | .name'
```

Expected:

```text
"mt-r1"
"cisco-r1"
"linux-srv1"
```

---

### Check Ansible Inventory

```bash
make ansible-inventory
```

Expected hosts:

```text
mt-r1
cisco-r1
linux-srv1
```

---

## 🤖 Ansible Automation

### Inventory

Inventory file:

```text
automation/ansible/inventory/lab.yml
```

Default lab hosts:

| Group         | Host         | IP            |
| ------------- | ------------ | ------------- |
| `mikrotik`    | `mt-r1`      | `10.10.10.1`  |
| `cisco`       | `cisco-r1`   | `10.10.10.2`  |
| `linux_hosts` | `linux-srv1` | `10.10.10.10` |

Update these IPs to match your lab environment.

---

### Connectivity Check

Only run this if your lab devices are reachable:

```bash
make ansible-connectivity
```

---

## 💾 Configuration Backup

### MikroTik Backup

```bash
make backup-mikrotik
```

Output:

```text
automation/backups/mikrotik/
```

---

### Cisco Backup

```bash
make backup-cisco
```

Output:

```text
automation/backups/cisco/
```

---

### Linux Network State Backup

```bash
make backup-linux
```

Output:

```text
automation/backups/linux/
```

Backup files are runtime artifacts and are not committed to Git.

---

## ✅ Compliance Check and Diff Report

The compliance engine compares:

```text
Generated Config = Desired State
Actual Config    = Backup or Current Snapshot
```

### Demo Compliance Mode

Prepare demo current-state files:

```bash
make compliance-demo-current
```

Run compliance check:

```bash
make compliance-check-current
```

Expected result:

```text
Total devices:  3
Compliant:      2
Non-compliant:  1
Missing actual: 0
```

The demo intentionally introduces a small MikroTik drift to demonstrate a non-compliant result.

---

### Backup Compliance Mode

If you have real backups:

```bash
make compliance-check-backups
```

Strict mode:

```bash
make compliance-check-backups-strict
```

Strict mode exits with a non-zero code if drift or missing actual configs are detected.

---

### Reports

Reports are generated under:

```text
automation/reports/compliance/
automation/reports/diff/
```

Report types:

| File                     | Purpose                            |
| ------------------------ | ---------------------------------- |
| `compliance-summary.txt` | Human-readable summary             |
| `compliance-report.json` | Machine-readable compliance data   |
| `compliance-report.html` | Browser-friendly compliance report |
| `*.diff`                 | Per-device unified diff            |

Open HTML report:

```bash
xdg-open automation/reports/compliance/compliance-report.html
```

---

## 🚦 Safe Config Push

Configuration push is intentionally protected by multiple safety gates.

Safety model:

```text
1. Generate config
2. Review config
3. Specify target device
4. Require explicit approval
5. Backup current device config
6. Push or stage config
```

---

### Review Config

```bash
make review-config PLATFORM=mikrotik DEVICE=mt-r1
make review-config PLATFORM=cisco DEVICE=cisco-r1
make review-config PLATFORM=linux DEVICE=linux-srv1
```

---

### Push MikroTik Config

Only run this if the MikroTik device is reachable and credentials are correct:

```bash
make push-mikrotik DEVICE=mt-r1 APPROVE=YES_I_UNDERSTAND
```

---

### Push Cisco Config

Only run this if the Cisco device is reachable and credentials are correct:

```bash
make push-cisco DEVICE=cisco-r1 APPROVE=YES_I_UNDERSTAND
```

---

### Stage Linux Netplan

Linux Netplan is staged only. It is not applied automatically.

```bash
make stage-linux-netplan DEVICE=linux-srv1 APPROVE=YES_I_UNDERSTAND
```

Remote staged path:

```text
/tmp/99-netbox-lab.yaml
```

This avoids accidentally breaking SSH connectivity.

---

## 🧰 Useful Commands

### NetBox

```bash
make netbox-up
make netbox-down
make netbox-status
make netbox-logs
make netbox-seed
```

### Config Generation

```bash
make generate-configs
make review-config PLATFORM=mikrotik DEVICE=mt-r1
```

### Ansible

```bash
make ansible-version
make ansible-collections
make ansible-inventory
make ansible-connectivity
```

### Backup

```bash
make backup-mikrotik
make backup-cisco
make backup-linux
```

### Compliance

```bash
make compliance-demo-current
make compliance-check-current
make compliance-check-backups
make compliance-check-backups-strict
```

### Safe Push

```bash
make push-mikrotik DEVICE=mt-r1 APPROVE=YES_I_UNDERSTAND
make push-cisco DEVICE=cisco-r1 APPROVE=YES_I_UNDERSTAND
make stage-linux-netplan DEVICE=linux-srv1 APPROVE=YES_I_UNDERSTAND
```

### Project Operations

```bash
make project-status
make security-scan
make validate
make clean-runtime
```

---

## 🧹 Clean Runtime Files

Remove generated runtime outputs:

```bash
make clean-runtime
```

This removes:

```text
automation/generated-configs/*
automation/reports/*
automation/compliance/current/*
automation/compliance/baseline/*
```

It does not remove NetBox Docker volumes or source code.

---

## 🧪 Project Validation

Run full validation:

```bash
make validate
```

Validation checks:

```text
Required files
Required directories
Python virtual environment
Docker and Docker Compose
NetBox HTTP availability
.env presence
Config generation
Ansible inventory
Compliance demo
Security scan
```

---

## 🔒 Security Notes

This project is designed for local labs, learning, demos, and controlled internal environments.

Important rules:

* Do not commit `.env`
* Do not commit real API tokens
* Do not commit device passwords
* Do not commit generated configs
* Do not commit backups
* Do not commit reports
* Do not commit Ansible collections
* Do not commit NetBox Docker upstream repository
* Review generated configs before applying them
* Always keep out-of-band access for network devices
* Test in lab before using anything against production devices

Ignored runtime paths:

```text
.env
.env.*
automation/ansible/collections/
automation/generated-configs/
automation/backups/
automation/reports/
automation/compliance/current/
automation/compliance/baseline/
docker/netbox/netbox-docker/
logs/
__pycache__/
```

Run security scan:

```bash
make security-scan
```

---

## 🛠️ Troubleshooting

### NetBox does not start

Check containers:

```bash
cd docker/netbox/netbox-docker
docker compose ps
docker compose logs -f netbox
```

If the database was initialized with old credentials during lab testing, reset the stack:

```bash
docker compose down -v --remove-orphans
docker compose up -d
```

Warning: this removes local NetBox database data.

---

### NetBox API returns 403

If you see:

```text
Invalid v1 token
```

Use a NetBox v2 token and send it as:

```text
Authorization: Bearer nbt_xxxxx.xxxxx
```

Update `.env`:

```env
NETBOX_TOKEN=nbt_xxxxx.xxxxx
```

---

### Config generation fails

Run:

```bash
make netbox-status
make netbox-seed
make generate-configs
```

Check token:

```bash
source .env

curl -s \
  -H "Authorization: Bearer $NETBOX_TOKEN" \
  "$NETBOX_URL/api/" | jq
```

---

### Ansible collections are missing

Install again:

```bash
ansible-galaxy collection install \
  -r automation/ansible/requirements.yml \
  -p automation/ansible/collections
```

Verify:

```bash
make ansible-collections
```

---

### Ansible cannot connect to MikroTik

Check:

```bash
ping 10.10.10.1
ssh admin@10.10.10.1
```

Verify `.env`:

```env
MIKROTIK_USER=admin
MIKROTIK_PASSWORD=change_me
MIKROTIK_PORT=22
```

Then run:

```bash
make ansible-connectivity
```

---

### Ansible cannot connect to Cisco

Check:

```bash
ping 10.10.10.2
ssh admin@10.10.10.2
```

Verify `.env`:

```env
CISCO_USER=admin
CISCO_PASSWORD=change_me
CISCO_PORT=22
CISCO_ENABLE=false
CISCO_ENABLE_PASSWORD=
```

---

### Linux Netplan was staged but not applied

This is expected.

The project only copies the generated Netplan file to:

```text
/tmp/99-netbox-lab.yaml
```

It does not apply the file automatically to avoid breaking network access.

---

### Generated configs are missing from GitHub

This is expected.

Generated configs are runtime artifacts and are ignored by Git.

Generate them locally:

```bash
make generate-configs
```

---

## 📚 Documentation

| Document                             | Purpose                       |
| ------------------------------------ | ----------------------------- |
| `docs/netbox-local-setup.md`         | Local NetBox setup notes      |
| `docs/netbox-lab-data-model.md`      | Lab data model                |
| `docs/config-generation.md`          | Config generation workflow    |
| `docs/compliance-and-diff-report.md` | Compliance and diff reporting |
| `docs/safe-config-push.md`           | Safe push workflow            |

---

## 🖼️ Screenshots

Recommended screenshots to add:

```text
docs/images/netbox-devices.png
docs/images/netbox-ipam.png
docs/images/generated-configs.png
docs/images/compliance-report.png
docs/images/diff-report.png
```

Suggested GitHub section after adding screenshots:

```markdown
## Screenshots

### NetBox Devices

![NetBox Devices](docs/images/netbox-devices.png)

### Compliance Report

![Compliance Report](docs/images/compliance-report.png)
```

---

## 🧭 Roadmap

Possible future improvements:

* Add GitHub Actions validation workflow
* Add containerized automation runner
* Add dynamic Ansible inventory from NetBox
* Add NetBox custom fields for automation intent
* Add support for Juniper JunOS
* Add support for Arista EOS
* Add Batfish-style validation workflow
* Add rollback playbooks
* Add pre-change and post-change validation
* Add Slack/Telegram notification for compliance drift
* Add lightweight web UI for reports
* Add diagrams under `docs/diagrams/`
* Add screenshots under `docs/images/`
* Add example generated configs under `docs/examples/`
* Add Terraform integration for infrastructure intent
* Add CI-based secret scanning

---

## ⚠️ Production Usage Warning

This is a production-style lab, not a drop-in production deployment.

Before using this workflow in a production network:

* Validate all templates
* Test against lab devices
* Add rollback strategy
* Add change approval process
* Use strong secrets
* Use SSH keys where possible
* Restrict device access
* Use out-of-band management
* Add monitoring and alerting
* Add CI/CD validation
* Add peer review before config push

---

## 📄 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## ✨ Project Summary

**NetBox-Driven Network Automation Lab** is a complete Source-of-Truth-driven network automation project.

It shows how NetBox can be used as the central inventory and IPAM system, how Python can generate network configurations from NetBox data, how Ansible can back up and safely push configurations, and how compliance checks can detect drift between desired and actual device state.

This project demonstrates practical skills in:

```text
NetBox
Docker
Python API Automation
Jinja2 Templates
Ansible Network Automation
MikroTik RouterOS
Cisco IOS
Linux Networking
Configuration Backup
Compliance Checking
Diff Reporting
GitHub Project Documentation
```

It is designed to be clean enough for GitHub, practical enough for a real lab, and strong enough to showcase network automation engineering skills.
