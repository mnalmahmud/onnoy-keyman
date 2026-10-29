#!/usr/bin/env bash
set -euo pipefail
python3 verify_keyman.py
mkdir -p build
kmc build source/onnoy.kmn -o build/onnoy.kmx
test -s build/onnoy.kmx
test -s build/onnoy.js
kmc build source/onnoy.kps -o build/onnoy.kmp
test -s build/onnoy.kmp
