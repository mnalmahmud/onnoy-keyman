#!/usr/bin/env python3
"""Compatibility entry point; canonical generation is now scripts/build.py."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
cmd="check" if "--check" in sys.argv else "generate"
raise SystemExit(subprocess.call([sys.executable,str(ROOT/"scripts/build.py"),cmd]))
