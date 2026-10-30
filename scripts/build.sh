#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate.py
python3 scripts/generate.py --check
python3 -m unittest discover -s tests -p 'test_layout.py'
python3 -m unittest discover -s tests -p 'test_build.py'
python3 -m unittest discover -s tests -p 'test_typing.py'
echo "Native Onnoy sources generated. No Keyman or additional runtime is required."
