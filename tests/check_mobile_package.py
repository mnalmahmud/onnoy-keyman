"""Validate that the distributed KMP contains mobile JS and package metadata."""
from pathlib import Path
from zipfile import ZipFile
import json

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "dist" / "keyman" / "onnoy.kmp"

def main():
    assert PACKAGE.is_file(), "Missing compiled .kmp package"
    with ZipFile(PACKAGE) as archive:
        files = {name.rsplit("/",1)[-1]:name for name in archive.namelist()}
        for expected in ("onnoy.js","onnoy.kmx","kmp.json"):
            assert expected in files, f"Missing {expected} from mobile Keyman package"
        metadata=json.loads(archive.read(files["kmp.json"]).decode("utf-8-sig"))
        assert metadata.get("keyboards"), "Package does not declare a keyboard"
        javascript=archive.read(files["onnoy.js"])
        assert b"phone" in javascript, "Compiled mobile keyboard does not contain a phone layout"
        print("Validated KMP: desktop keyboard, mobile JS, embedded phone layout, metadata")

if __name__=="__main__":
    main()
