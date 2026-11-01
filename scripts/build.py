#!/usr/bin/env python3
"""Build Onnoy native sources, Keyman source, and browser reference data."""
from pathlib import Path
import argparse
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from onnoy.model import load,resolve
from onnoy.backends import linux,windows,macos,keyman,web

def generate(geometry="iso",check=False):
    data=load()
    layout=resolve(data,geometry)
    outputs={
       "dist/linux/symbols/onnoy":linux.render(layout),
       "dist/windows/onnoy.klc":windows.render(layout),
       "dist/macos/Onnoy.keylayout":macos.render(layout),
       "dist/keyman/onnoy.kmn":keyman.render(layout),
       "dist/keyman/onnoy.kps":keyman.package_source(),
       "dist/web/layout.json":web.render(layout)
    }
    for path,content in outputs.items():
        dest=ROOT/path
        raw=content.encode("utf-8")
        if check:
            if not dest.is_file() or dest.read_bytes()!=raw:
                raise SystemExit("Outdated or missing: "+path)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(raw)
        print(("Verified " if check else "Generated ")+path)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("validate","generate","check","test","package"))
    parser.add_argument("--target",choices=("linux","macos","windows","keyman"))
    args=parser.parse_args()
    if args.command=="validate":
        from onnoy.hardware import STANDARD,ISO_EXTRA
        data=load()
        for geometry in ("ansi","iso"): resolve(data,geometry)
        print("Mapping contract valid")
    elif args.command in ("generate","check"):
        generate(check=args.command=="check")
    elif args.command=="test":
        import unittest
        generate()
        suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"),pattern="test_*.py",top_level_dir=str(ROOT))
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():raise SystemExit(1)
    elif args.command=="package":
        import subprocess
        if args.target is None: parser.error("package requires --target")
        generate()
        if args.target=="keyman":
            subprocess.run(["npx","--no-install","kmc","build",str(ROOT/"dist/keyman/onnoy.kmn")],check=True)
            subprocess.run(["npx","--no-install","kmc","build",str(ROOT/"dist/keyman/onnoy.kps")],check=True)
        elif args.target=="linux":
            subprocess.run(["bash",str(ROOT/"scripts/package-linux.sh")],check=True)
        elif args.target=="macos":
            subprocess.run(["bash",str(ROOT/"scripts/package-macos.sh")],check=True)
        else:
            subprocess.run(["pwsh","-File",str(ROOT/"scripts/package-windows.ps1")],check=True)

if __name__=="__main__":main()
