"""The four-layer web reference must preserve empty modifier slots."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from export_web_layout import export


class WebReference(unittest.TestCase):
    def test_all_four_layers(self):
        data = export(ROOT / "layout.toml")
        self.assertEqual(data["layers"], ["base", "shift", "altgr", "shift_altgr"])
        keys = data["keys"]
        self.assertTrue(all(len(values) == 4 for values in keys.values()))
        self.assertEqual(keys["KeyK"][:2], ["ক", "খ"])
        self.assertEqual(keys["KeyQ"][2:], [None, None])
        self.assertEqual(keys["KeyJ"][2], "\u200d")
        self.assertEqual(keys["KeyD"][2], "\u200c")
        self.assertEqual(keys["Backquote"][:2], ["্", "়"])
        self.assertIsNone(keys["KeyL"][2])

    def test_generated_file(self):
        path = ROOT / "dist/onnoy-visualizer.json"
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), export(ROOT / "layout.toml"))


if __name__ == "__main__":
    unittest.main()
