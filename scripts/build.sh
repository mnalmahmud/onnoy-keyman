#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build.py validate
python3 scripts/build.py generate
python3 scripts/build.py check
python3 scripts/build.py test
echo "Onnoy source contract and native/Keyman generators checked."
