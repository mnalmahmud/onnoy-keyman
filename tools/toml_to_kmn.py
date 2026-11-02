#!/usr/bin/env python3
"""Compile Kalamine's layout.toml to Keyman source (no duplicated key mappings)."""

import argparse
from pathlib import Path

from kalamine.layout import KeyboardLayout, load_layout
from kalamine.utils import LAYER_KEYS, SCAN_CODES, Layer

ROOT = Path(__file__).resolve().parents[1]
LAYERS = (
    (Layer.BASE, ""),
    (Layer.SHIFT, "SHIFT "),
    (Layer.ALTGR, "RALT "),
    (Layer.ALTGR_SHIFT, "SHIFT RALT "),
)
SPECIAL_KEYS = {
    "Backquote": "K_BKQUOTE", "Minus": "K_HYPHEN", "Equal": "K_EQUAL",
    "BracketLeft": "K_LBRKT", "BracketRight": "K_RBRKT",
    "Backslash": "K_BKSLASH", "Semicolon": "K_COLON",
    "Quote": "K_QUOTE", "Comma": "K_COMMA", "Period": "K_PERIOD",
    "Slash": "K_SLASH", "IntlBackslash": "K_oE2", "Space": "K_SPACE",
}


def keyman_key(browser_code: str) -> str:
    """Use Kalamine's physical key IDs, not the characters on those keys."""
    if browser_code.startswith("Key"):
        return "K_" + browser_code[3:]
    if browser_code.startswith("Digit"):
        return "K_" + browser_code[5:]
    return SPECIAL_KEYS[browser_code]


def render(layout: KeyboardLayout) -> str:
    if layout.dead_keys:
        raise ValueError("Onnoy is direct Unicode; Keyman dead-key rules are unsupported")

    lines = [
        "c Generated from layout.toml by tools/toml_to_kmn.py — DO NOT EDIT.",
        "store(&VERSION) '15.0'",
        "store(&NAME) 'Onnoy'",
        "store(&KEYBOARDVERSION) '1.0'",
        "store(&TARGETS) 'any'",
        "store(&layoutfile) 'onnoy.keyman-touch-layout'",
        "begin Unicode > use(main)",
        "",
        "group(main) using keys",
    ]
    for position in LAYER_KEYS:
        if position.startswith("-"):
            continue
        # Skip keys absent from the chosen physical geometry, not empty layers.
        if not any(position in layout.layers[layer] for layer, _ in LAYERS):
            continue

        key = keyman_key(SCAN_CODES["web"][position])
        for layer, modifiers in LAYERS:
            char = layout.layers[layer].get(position)
            if char is not None and len(char) != 1:
                raise ValueError(f"Expected one Unicode codepoint: {position} / {layer}")
            output = f"U+{ord(char):04X}" if char is not None else "nul"
            lines.append(f"+ [{modifiers}{key}] > {output}")
    return "\n".join(lines) + "\n"


def generate(source: Path) -> str:
    return render(KeyboardLayout(load_layout(source)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=ROOT / "layout.toml")
    parser.add_argument("output", nargs="?", type=Path, default=ROOT / "keyman/onnoy.kmn")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(generate(args.source), encoding="utf-8")


if __name__ == "__main__":
    main()
