#!/usr/bin/env python3
"""Verify the complete generated Keyman keymap against the canonical JSON."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORDER = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890."
mapping = json.loads((ROOT / "layout/onnoy.json").read_text(encoding="utf-8"))["keys"]
source = (ROOT / "source/onnoy.kmn").read_text(encoding="utf-8")

rule = re.compile(
    r"^\+ \[(?:(SHIFT) )?(?:(RALT) )?K_([A-Z0-9]+)\] > "
    r"(nul|U\+[0-9A-F]{4,6}(?: U\+[0-9A-F]{4,6})*)$",
    re.MULTILINE,
)
found = {}
for shift, altgr, key, output in rule.findall(source):
    slot = (key, int(bool(shift)) + 2 * int(bool(altgr)))
    if slot in found:
        raise SystemExit(f"Duplicate Keyman rule: {slot}")
    found[slot] = output

if len(found) != 4 * len(ORDER):
    raise SystemExit(f"Expected {4 * len(ORDER)} rules, got {len(found)}")

for key in ORDER:
    for layer, value in enumerate(mapping[key]):
        expected = "nul" if value is None else " ".join(f"U+{ord(c):04X}" for c in value)
        slot = ("PERIOD" if key == "." else key, layer)
        if found.get(slot) != expected:
            raise SystemExit(f"Mismatch at {slot}: expected {expected}, got {found.get(slot)}")

# Guard the deliberate R mapping and the approved family/shortcut decisions.
for key, expected in {
    "Q": ["ড", "ঢ", "ড়", "ঢ়"],
    "W": ["ট", "ঠ", None, None],
    "R": ["র", "ৃ", "ঋ", "ৰ"],
    "X": ["ষ", "ক্ষ", None, None],
    "G": ["গ", "ঘ", "জ্ঞ", None],
    "Y": ["য", "য়", "্য", None],
}.items():
    if mapping[key] != expected:
        raise SystemExit(f"Unexpected canonical assignment for {key}")

ET.parse(ROOT / "source/onnoy.kps")
print("Keyman rules and approved Onnoy mapping verified")
