#!/usr/bin/env bash
set -euo pipefail

# Remove runtime-generated files.
# This does not delete NetBox Docker volumes or source code.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "Cleaning runtime-generated files..."

rm -rf automation/generated-configs/*
rm -rf automation/reports/*
rm -rf automation/compliance/current/*
rm -rf automation/compliance/baseline/*

echo "Runtime cleanup completed."
