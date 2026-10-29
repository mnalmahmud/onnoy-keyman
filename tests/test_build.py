"""Tests for compiled Keyman artifacts; run after scripts/build.sh compiles them."""
import unittest
from pathlib import Path
from zipfile import ZipFile, is_zipfile

ROOT = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    def test_compiled_files_are_not_empty(self):
        for name in ("onnoy.js", "onnoy.kmx", "onnoy.kmp"):
            with self.subTest(file=name):
                path = ROOT / "build" / name
                self.assertTrue(path.is_file(), f"Missing {path}")
                self.assertGreater(path.stat().st_size, 100, f"Empty {path}")

    def test_package_contains_compiled_keyboard(self):
        package = ROOT / "build" / "onnoy.kmp"
        self.assertTrue(is_zipfile(package), f"Not a valid Keyman package: {package}")
        with ZipFile(package) as archive:
            self.assertIn("onnoy.kmx", [name.rsplit("/", 1)[-1].lower()
                                         for name in archive.namelist()])

    def test_platform_sources_exist(self):
        for path in (
            "dist/linux/symbols/onnoy",
            "dist/linux/Onnoy.XCompose",
            "dist/macos/Onnoy.keylayout",
            "dist/windows/onnoy.klc",
        ):
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())


if __name__ == "__main__":
    unittest.main()
