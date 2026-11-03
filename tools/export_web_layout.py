#!/usr/bin/env python3
"""Export Kalamine's explicit modifier layers for the Onnoy web visualizer."""
import argparse
import json
from pathlib import Path

from kalamine.layout import KeyboardLayout, load_layout
from kalamine.utils import LAYER_KEYS, SCAN_CODES, Layer
from sequences import altgr_sequences

ROOT = Path(__file__).resolve().parents[1]
LAYERS = (Layer.BASE, Layer.SHIFT, Layer.ALTGR, Layer.ALTGR_SHIFT)


def export(source: Path) -> dict:
    layout = KeyboardLayout(load_layout(source))
    keys = {}
    for position in LAYER_KEYS:
        if position.startswith("-"):
            continue
        if any(position in layout.layers[layer] for layer in LAYERS):
            code = SCAN_CODES["web"][position]
            keys[code] = [layout.layers[layer].get(position) for layer in LAYERS]
    for code, output in altgr_sequences(source, layout).items():
        keys[code][2] = output
    return {
        "name": layout.meta["name"],
        "layers": ["base", "shift", "altgr", "shift_altgr"],
        "keys": keys,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, nargs="?", default=ROOT / "layout.toml")
    parser.add_argument("output", type=Path, nargs="?", default=ROOT / "dist/onnoy-visualizer.json")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(export(args.source), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
