"""Regression tests for vowel placement research only."""
import json
from pathlib import Path
import tempfile
import unittest
from scripts.evaluate_vowels import get_layout, measure


class StudyTests(unittest.TestCase):
    def test_nfd_handles_decomposed_dotted_letters_and_nonbmp(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            layout = {"layers": ["base", "shift", "altgr", "shift_altgr"],
                      "keys": {"Q": ["ড", "ড়", None, None],
                               "F": ["্", None, "𑷰", None],
                               "I": ["ি", "ই", "ী", "ঈ"]}}
            (root / "layout.json").write_text(json.dumps(layout, ensure_ascii=False), encoding="utf-8")
            (root / "text.txt").write_text("ড় ড় ি ই ী ঈ ক𑷰", encoding="utf-8")
            output = measure(root / "text.txt", get_layout(root / "layout.json"))
            self.assertEqual(output["layers"], {"Shift": 3, "Base": 1, "AltGr": 2, "Shift+AltGr": 1})
            self.assertEqual(output["unmapped_codepoints"], {"ক": 1})
            self.assertEqual(output["vowel_counts"], {"ি": 1, "ই": 1, "ী": 1, "ঈ": 1})


if __name__ == "__main__":
    unittest.main()
