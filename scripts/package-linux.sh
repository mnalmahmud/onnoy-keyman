#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate.py --check
mkdir -p build/native/linux/onnoy
cp dist/linux/symbols/onnoy dist/linux/Onnoy.XCompose build/native/linux/onnoy/
cp scripts/install-linux.sh build/native/linux/onnoy/install.sh
tar -czf build/onnoy-linux.tar.gz -C build/native/linux onnoy
echo "Created build/onnoy-linux.tar.gz"
