"""Build and verify Onnoy keyboards from the canonical layout."""

import argparse
from pathlib import Path
import subprocess
import sys
import unittest

from .backends import keyman, linux, macos, touch, web, windows
from .model import load, resolve

ROOT = Path(__file__).resolve().parents[1]


def generate(check=False):
    mapping = resolve(geometry="iso")
    outputs = {
        "dist/linux/symbols/onnoy": linux.render(mapping),
        "dist/windows/onnoy.klc": windows.render(mapping),
        "dist/macos/Onnoy.keylayout": macos.render(mapping),
        "dist/keyman/onnoy.kmn": keyman.render(mapping),
        "dist/keyman/onnoy.kps": keyman.package_source(),
        "dist/keyman/onnoy.keyman-touch-layout": touch.render(mapping),
        "dist/web/layout.json": web.render(mapping),
    }
    for name, content in outputs.items():
        path = ROOT / name
        rendered = content.encode("utf-8")
        if check:
            if not path.is_file() or path.read_bytes() != rendered:
                raise SystemExit(f"Missing or outdated generated file: {name}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(rendered)
        print(f'{"Verified" if check else "Generated"} {name}')


def test(browser=False, package_check=False):
    generate()
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / "tests"), pattern="test_onnoy.py"
    )
    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
        raise SystemExit(1)

    if browser or package_check:
        # unittest discovery imported the single test file as test_onnoy.
        checks = sys.modules["test_onnoy"]
        if package_check:
            checks.verify_mobile_package()
        if browser:
            checks.browser_smoke()


def package(target):
    generate()
    if target == "keyman":
        for name in ("onnoy.kmn", "onnoy.kps"):
            subprocess.run(
                ["npx", "--no-install", "kmc", "build", str(ROOT / "dist/keyman" / name)],
                check=True,
            )
        return
    commands = {
        "linux": ["bash", str(ROOT / "tools/package-linux.sh")],
        "macos": ["bash", str(ROOT / "tools/package-macos.sh")],
        "windows": [
            "powershell" if sys.platform == "win32" else "pwsh",
            "-File",
            str(ROOT / "tools/package-windows.ps1"),
        ],
    }
    subprocess.run(commands[target], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("validate", "generate", "check", "test", "package")
    )
    parser.add_argument("--target", choices=("linux", "macos", "windows", "keyman"))
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--package-check", action="store_true")
    args = parser.parse_args()

    if args.command != "test" and (args.browser or args.package_check):
        parser.error("--browser and --package-check require the test command")
    if args.command != "package" and args.target:
        parser.error("--target requires the package command")

    if args.command == "validate":
        data = load()
        for geometry in ("ansi", "iso"):
            resolve(data, geometry)
        print("Mapping contract valid")
    elif args.command == "generate":
        generate()
    elif args.command == "check":
        generate(check=True)
    elif args.command == "test":
        test(browser=args.browser, package_check=args.package_check)
    else:
        if args.target is None:
            parser.error("package requires --target")
        package(args.target)


if __name__ == "__main__":
    main()
