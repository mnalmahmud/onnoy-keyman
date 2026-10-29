#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Validate the single-source mapping before compiling anything.
python3 scripts/generate.py --check
python3 -m unittest discover -s tests -p 'test_layout.py'

mkdir -p build
kmc build source/onnoy.kmn -o build/onnoy.kmx
kmc build source/onnoy.kps -o build/onnoy.kmp

python3 -m unittest discover -s tests -p 'test_build.py'
