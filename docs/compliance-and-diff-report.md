# Compliance and Diff Report

This project supports configuration compliance checks by comparing NetBox-generated desired configuration against actual device configuration.

## Concept

```text
NetBox Source of Truth -> Generated Config -> Desired State
Device Backup / Current Snapshot -> Actual State
Desired State vs Actual State -> Diff + Compliance Report

Actual Sources

The compliance checker supports two actual-state sources:

Source	Description
current	Uses files from automation/compliance/current/
backups	Uses the latest backup file from automation/backups/
Demo Mode

Prepare demo current snapshots:

make compliance-demo-current

Run compliance check against demo current state:

make compliance-check-current

The demo intentionally introduces drift in the MikroTik config to demonstrate a non-compliant result.

Backup Mode

Run compliance check against latest collected backups:

make compliance-check-backups

Strict mode:

make compliance-check-backups-strict

Strict mode exits with a non-zero code if drift or missing actual configs are detected.

Reports

Reports are written to:

automation/reports/compliance/
automation/reports/diff/

Generated report files:

File	Purpose
compliance-summary.txt	Human-readable summary
compliance-report.json	Machine-readable report
compliance-report.html	Browser-friendly report
*.diff	Per-device unified diff
