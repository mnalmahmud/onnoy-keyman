#!/usr/bin/env bash
# Install user-local XKB symbols without touching system configuration.
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -f onnoy ]]; then
  echo "Expected the generated 'onnoy' XKB symbols file next to install.sh" >&2
  exit 1
fi
base="${XDG_CONFIG_HOME:-$HOME/.config}/xkb/symbols"
mkdir -p "$base"
cp onnoy "$base/onnoy"
echo "Installed user-local XKB symbols at $base/onnoy"
echo "The next step depends on your desktop environment. On X11, a layout may"
echo "require system XKB registration and an XKB reload; Wayland desktop input"
echo "settings differ. See the README for desktop setup. No extra input-method runtime."
