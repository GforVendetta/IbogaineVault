#!/usr/bin/env bash
# setup.sh — IbogaineVault environment setup
# Installs dependencies and verifies vault integrity.

set -euo pipefail

echo "Installing dependencies..."
pip install pyyaml

echo ""
echo "Running vault validation..."
python3 validate_vault.py --summary

echo ""
echo "Setup complete."
