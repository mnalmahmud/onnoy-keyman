#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate.py --check
if ! command -v pkgbuild >/dev/null 2>&1; then
  echo "pkgbuild requires macOS" >&2
  exit 1
fi
root="build/native/macos/root/Library/Keyboard Layouts"
mkdir -p "$root"
cp dist/macos/Onnoy.keylayout "$root/"
pkgbuild --root build/native/macos/root --identifier org.onnoy.keyboard.layout --version 2.1 --install-location / build/onnoy-macos.pkg
echo "Created build/onnoy-macos.pkg (unsigned; enable in Input Sources after installation)"
