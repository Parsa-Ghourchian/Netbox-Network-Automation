#!/usr/bin/env python3
"""
Compliance checker for the NetBox-driven Network Automation Lab.

This script compares desired configuration generated from NetBox
against actual configuration collected from backups or current snapshots.

Desired state:
- automation/generated-configs/

Actual state options:
- automation/backups/
- automation/compliance/current/

Reports:
- automation/reports/diff/
- automation/reports/compliance/
"""

from __future__ import annotations

import argparse
import difflib
import html
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATED_ROOT = PROJECT_ROOT / "automation" / "generated-configs"
BACKUP_ROOT = PROJECT_ROOT / "automation" / "backups"
CURRENT_ROOT = PROJECT_ROOT / "automation" / "compliance" / "current"

DIFF_REPORT_ROOT = PROJECT_ROOT / "automation" / "reports" / "diff"
COMPLIANCE_REPORT_ROOT = PROJECT_ROOT / "automation" / "reports" / "compliance"


PLATFORMS = {
    "mikrotik": {
        "extension": ".rsc",
        "desired_dir": GENERATED_ROOT / "mikrotik",
        "backup_dir": BACKUP_ROOT / "mikrotik",
        "current_dir": CURRENT_ROOT / "mikrotik",
    },
    "cisco": {
        "extension": ".cfg",
        "desired_dir": GENERATED_ROOT / "cisco",
        "backup_dir": BACKUP_ROOT / "cisco",
        "current_dir": CURRENT_ROOT / "cisco",
    },
    "linux": {
        "extension": ".yaml",
        "desired_dir": GENERATED_ROOT / "linux",
        "backup_dir": BACKUP_ROOT / "linux",
        "current_dir": CURRENT_ROOT / "linux",
    },
}


@dataclass
class ComplianceResult:
    platform: str
    device: str
    desired_file: str
    actual_file: Optional[str]
    status: str
    diff_file: Optional[str]
    diff_lines: int


def utc_now() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def normalize_lines(content: str) -> List[str]:
    """Normalize config content before comparison.

    This keeps the comparison strict enough for network config drift detection,
    while removing trailing whitespace noise.
    """
    return [line.rstrip() for line in content.splitlines()]


def read_lines(path: Path) -> List[str]:
    """Read and normalize a config file."""
    return normalize_lines(path.read_text(encoding="utf-8"))


def ensure_report_dirs() -> None:
    """Create report directories."""
    DIFF_REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    COMPLIANCE_REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    for platform in PLATFORMS:
        (DIFF_REPORT_ROOT / platform).mkdir(parents=True, exist_ok=True)


def find_latest_backup(platform: str, device: str) -> Optional[Path]:
    """Find the latest backup file for a device."""
    platform_data = PLATFORMS[platform]
    backup_dir = platform_data["backup_dir"]
    extension = platform_data["extension"]

    if not backup_dir.exists():
        return None

    candidates = sorted(
        backup_dir.glob(f"{device}-*{extension}"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )

    if not candidates:
        return None

    return candidates[0]


def find_current_snapshot(platform: str, device: str) -> Optional[Path]:
    """Find a current snapshot file for a device."""
    platform_data = PLATFORMS[platform]
    current_dir = platform_data["current_dir"]
    extension = platform_data["extension"]

    candidate = current_dir / f"{device}{extension}"

    if candidate.exists():
        return candidate

    return None


def build_diff(
    desired_path: Path,
    actual_path: Path,
    platform: str,
    device: str,
) -> tuple[Optional[Path], int]:
    """Build a unified diff file if there is drift."""
    desired_lines = read_lines(desired_path)
    actual_lines = read_lines(actual_path)

    diff = list(
        difflib.unified_diff(
            actual_lines,
            desired_lines,
            fromfile=f"actual/{actual_path.name}",
            tofile=f"desired/{desired_path.name}",
            lineterm="",
        )
    )

    if not diff:
        return None, 0

    diff_path = DIFF_REPORT_ROOT / platform / f"{device}.diff"
    diff_path.write_text("\n".join(diff) + "\n", encoding="utf-8")

    return diff_path, len(diff)


def compare_device(platform: str, desired_path: Path, actual_source: str) -> ComplianceResult:
    """Compare one desired config file against actual state."""
    device = desired_path.stem

    if actual_source == "backups":
        actual_path = find_latest_backup(platform, device)
    elif actual_source == "current":
        actual_path = find_current_snapshot(platform, device)
    else:
        raise ValueError(f"Unsupported actual source: {actual_source}")

    if actual_path is None:
        return ComplianceResult(
            platform=platform,
            device=device,
            desired_file=str(desired_path.relative_to(PROJECT_ROOT)),
            actual_file=None,
            status="MISSING_ACTUAL",
            diff_file=None,
            diff_lines=0,
        )

    diff_path, diff_lines = build_diff(
        desired_path=desired_path,
        actual_path=actual_path,
        platform=platform,
        device=device,
    )

    status = "COMPLIANT" if diff_lines == 0 else "NON_COMPLIANT"

    return ComplianceResult(
        platform=platform,
        device=device,
        desired_file=str(desired_path.relative_to(PROJECT_ROOT)),
        actual_file=str(actual_path.relative_to(PROJECT_ROOT)),
        status=status,
        diff_file=str(diff_path.relative_to(PROJECT_ROOT)) if diff_path else None,
        diff_lines=diff_lines,
    )


def run_compliance(actual_source: str) -> List[ComplianceResult]:
    """Run compliance checks for all supported platforms."""
    ensure_report_dirs()

    results: List[ComplianceResult] = []

    for platform, platform_data in PLATFORMS.items():
        desired_dir = platform_data["desired_dir"]
        extension = platform_data["extension"]

        if not desired_dir.exists():
            print(f"SKIPPED: Desired directory not found: {desired_dir.relative_to(PROJECT_ROOT)}")
            continue

        desired_files = sorted(desired_dir.glob(f"*{extension}"))

        if not desired_files:
            print(f"SKIPPED: No desired config files found for {platform}")
            continue

        for desired_path in desired_files:
            result = compare_device(
                platform=platform,
                desired_path=desired_path,
                actual_source=actual_source,
            )
            results.append(result)

    return results


def write_json_report(results: List[ComplianceResult], actual_source: str) -> Path:
    """Write JSON compliance report."""
    report = {
        "generated_at": utc_now(),
        "actual_source": actual_source,
        "summary": summarize(results),
        "results": [asdict(result) for result in results],
    }

    path = COMPLIANCE_REPORT_ROOT / "compliance-report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path


def write_text_report(results: List[ComplianceResult], actual_source: str) -> Path:
    """Write human-readable compliance summary."""
    summary = summarize(results)

    lines = [
        "NetBox-driven Network Automation Lab - Compliance Summary",
        "=" * 64,
        f"Generated at: {utc_now()}",
        f"Actual source: {actual_source}",
        "",
        f"Total devices:     {summary['total']}",
        f"Compliant:         {summary['compliant']}",
        f"Non-compliant:     {summary['non_compliant']}",
        f"Missing actual:    {summary['missing_actual']}",
        "",
        "Details:",
        "-" * 64,
    ]

    for result in results:
        lines.append(
            f"{result.platform:<10} {result.device:<20} {result.status:<15} "
            f"diff_lines={result.diff_lines:<4} "
            f"actual={result.actual_file or '-'}"
        )

    path = COMPLIANCE_REPORT_ROOT / "compliance-summary.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_html_report(results: List[ComplianceResult], actual_source: str) -> Path:
    """Write simple HTML compliance report."""
    summary = summarize(results)

    rows = []

    for result in results:
        status_class = {
            "COMPLIANT": "ok",
            "NON_COMPLIANT": "bad",
            "MISSING_ACTUAL": "warn",
        }.get(result.status, "warn")

        diff_link = result.diff_file or "-"

        rows.append(
            "<tr>"
            f"<td>{html.escape(result.platform)}</td>"
            f"<td>{html.escape(result.device)}</td>"
            f"<td class='{status_class}'>{html.escape(result.status)}</td>"
            f"<td>{result.diff_lines}</td>"
            f"<td>{html.escape(result.desired_file)}</td>"
            f"<td>{html.escape(result.actual_file or '-')}</td>"
            f"<td>{html.escape(diff_link)}</td>"
            "</tr>"
        )

    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Compliance Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; font-size: 14px; }}
    th {{ background: #f4f4f4; text-align: left; }}
    .ok {{ color: #0a7a28; font-weight: bold; }}
    .bad {{ color: #b00020; font-weight: bold; }}
    .warn {{ color: #b26a00; font-weight: bold; }}
    .summary {{ margin-bottom: 24px; }}
    code {{ background: #f4f4f4; padding: 2px 4px; }}
  </style>
</head>
<body>
  <h1>NetBox-driven Network Automation Lab - Compliance Report</h1>

  <div class="summary">
    <p><strong>Generated at:</strong> {html.escape(utc_now())}</p>
    <p><strong>Actual source:</strong> <code>{html.escape(actual_source)}</code></p>
    <p>
      <strong>Total:</strong> {summary['total']} |
      <strong>Compliant:</strong> {summary['compliant']} |
      <strong>Non-compliant:</strong> {summary['non_compliant']} |
      <strong>Missing actual:</strong> {summary['missing_actual']}
    </p>
  </div>

  <table>
    <thead>
      <tr>
        <th>Platform</th>
        <th>Device</th>
        <th>Status</th>
        <th>Diff Lines</th>
        <th>Desired File</th>
        <th>Actual File</th>
        <th>Diff File</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""

    path = COMPLIANCE_REPORT_ROOT / "compliance-report.html"
    path.write_text(content, encoding="utf-8")
    return path


def summarize(results: List[ComplianceResult]) -> Dict[str, int]:
    """Summarize compliance results."""
    return {
        "total": len(results),
        "compliant": sum(1 for result in results if result.status == "COMPLIANT"),
        "non_compliant": sum(1 for result in results if result.status == "NON_COMPLIANT"),
        "missing_actual": sum(1 for result in results if result.status == "MISSING_ACTUAL"),
    }


def print_summary(results: List[ComplianceResult], report_paths: List[Path]) -> None:
    """Print summary to stdout."""
    summary = summarize(results)

    print("\nCompliance summary:")
    print(f"  Total devices:  {summary['total']}")
    print(f"  Compliant:      {summary['compliant']}")
    print(f"  Non-compliant:  {summary['non_compliant']}")
    print(f"  Missing actual: {summary['missing_actual']}")

    print("\nDevice results:")
    for result in results:
        print(f"  [{result.status}] {result.platform}/{result.device}")

    print("\nReports:")
    for path in report_paths:
        print(f"  {path.relative_to(PROJECT_ROOT)}")

    print("\nDiff files:")
    for result in results:
        if result.diff_file:
            print(f"  {result.diff_file}")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Compare NetBox-generated desired configs with actual configs."
    )

    parser.add_argument(
        "--actual-source",
        choices=["backups", "current"],
        default="backups",
        help="Use latest backups or current snapshots as actual state.",
    )

    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Exit with code 2 if non-compliant or missing actual configs are found.",
    )

    return parser.parse_args()


def main() -> int:
    """Run compliance check."""
    args = parse_args()

    results = run_compliance(actual_source=args.actual_source)

    json_report = write_json_report(results, args.actual_source)
    text_report = write_text_report(results, args.actual_source)
    html_report = write_html_report(results, args.actual_source)

    print_summary(results, [json_report, text_report, html_report])

    summary = summarize(results)

    if args.fail_on_drift and (
        summary["non_compliant"] > 0 or summary["missing_actual"] > 0
    ):
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
