#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m onnoy check
mkdir -p build/native/linux/onnoy
cp dist/linux/symbols/onnoy build/native/linux/onnoy/
cp tools/install-linux.sh build/native/linux/onnoy/install.sh
chmod +x build/native/linux/onnoy/install.sh
tar -czf build/onnoy-linux-native.tar.gz -C build/native/linux onnoy
echo "Created build/onnoy-linux-native.tar.gz (native XKB, no IME)"
