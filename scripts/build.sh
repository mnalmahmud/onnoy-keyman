#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate.py --check
python3 verify_keyman.py
mkdir -p build
kmc build source/onnoy.kmn -o build/onnoy.kmx
test -s build/onnoy.kmx
test -s build/onnoy.js
kmc build source/onnoy.kps -o build/onnoy.kmp
test -s build/onnoy.kmp
python3 scripts/verify_build.py
