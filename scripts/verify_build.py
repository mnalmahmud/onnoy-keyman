#!/usr/bin/env python3
"""Verify required Keyman build artifacts, including the packaged .kmx."""
from pathlib import Path
from zipfile import ZipFile, is_zipfile

ROOT = Path(__file__).resolve().parents[1]
for name in ("onnoy.kmp", "onnoy.kmx", "onnoy.js"):
    path = ROOT / "build" / name
    if not path.is_file() or path.stat().st_size < 100:
        raise SystemExit(f"Missing or empty compiled artifact: {path}")
package = ROOT / "build/onnoy.kmp"
if not is_zipfile(package):
    raise SystemExit(f"Not a valid Keyman package: {package}")
with ZipFile(package) as archive:
    names = archive.namelist()
    if not any(name.lower().endswith("onnoy.kmx") for name in names):
        raise SystemExit("Keyman package is missing onnoy.kmx")
if "onnoy.js" not in (ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8"):
    raise SystemExit("Build workflow does not include the web keyboard")
print("Compiled Keyman outputs verified")
