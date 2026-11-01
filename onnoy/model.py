"""Validate and resolve Onnoy's sparse, key-centric JSON specification.

The canonical file records intentional overrides only. Missing alphabet levels
produce no text; missing digit/symbol levels resolve through plain-US reference
(Base/Shift) and are empty at higher levels. The resolver is the only place
where character-producing fallback occurs.
"""
from pathlib import Path
import json
from .hardware import ALPHABET, STANDARD, ISO_EXTRA, LAYERS
from .reference import PAIRS

ROOT = Path(__file__).resolve().parents[1]
LAYOUT_PATH = ROOT / "layout.json"

def load(path=LAYOUT_PATH):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate(data)
    return data

def validate(data):
    if not isinstance(data, dict) or set(data) != {"name", "keys"} or data["name"] != "Onnoy":
        raise ValueError("Expected Onnoy layout with exactly name and keys")
    if not isinstance(data["keys"], dict):
        raise ValueError("keys must be a mapping")
    known = set(STANDARD) - {"SPACE"}
    if not set(data["keys"]) <= known:
        raise ValueError("Unknown key(s): " + str(sorted(set(data["keys"]) - known)))
    if not set(ALPHABET) <= set(data["keys"]):
        raise ValueError("Missing alphabetic keys")
    for key, values in data["keys"].items():
        if not isinstance(values, dict) or not values or not set(values) <= set(LAYERS):
            raise ValueError("Invalid levels on " + key)
        for level, output in values.items():
            if not isinstance(output, str) or len(output) != 1:
                raise ValueError("Every explicit output must be one Unicode scalar: " + key + "." + level)
            n = ord(output)
            if 0xD800 <= n <= 0xDFFF or n > 0x10FFFF:
                raise ValueError("Invalid Unicode scalar: " + key + "." + level)
    # Every explicit character has one canonical position.
    # Ordinary reference punctuation remains excluded.
    positions = {}
    for key, values in data["keys"].items():
        for level, output in values.items():
            if output in positions:
                raise ValueError("Unexpected duplicate output " + repr(output))
            positions[output] = (key, level)

def resolve(data=None, geometry="ansi"):
    if geometry not in ("ansi", "iso"):
        raise ValueError("geometry must be ansi or iso")
    data = load() if data is None else data
    validate(data)
    active = STANDARD + ((ISO_EXTRA,) if geometry == "iso" else ())
    result = {}
    for key in active:
        explicit = data["keys"].get(key, {})
        if key == "SPACE":
            fallback = (" ", " ", " ", " ")
        elif key in ALPHABET:
            fallback = (None, None, None, None)
        else:
            base, shift = PAIRS[key]
            fallback = (base, shift, None, None)
        result[key] = tuple(explicit.get(layer, fallback[i]) for i, layer in enumerate(LAYERS))
    return result
