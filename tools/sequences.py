"""Shared multi-character shortcuts from the canonical layout.toml."""
import tomllib
from pathlib import Path

from kalamine.utils import SCAN_CODES, Layer


def altgr_sequences(source: Path, layout) -> dict[str, str]:
    config = tomllib.loads(source.read_text(encoding="utf-8"))
    entries = config.get("sequences", {}).get("altgr", {})
    positions = {code: pos for pos, code in SCAN_CODES["web"].items()}
    result = {}
    for letter, output in entries.items():
        code = "Key" + letter
        if len(letter) != 1 or not letter.isascii() or not letter.isupper():
            raise ValueError(f"Invalid AltGr shortcut: {letter}")
        if code not in positions or not isinstance(output, str) or len(output) < 2:
            raise ValueError(f"Invalid Unicode sequence for {letter}")
        if positions[code] in layout.layers[Layer.ALTGR]:
            raise ValueError(f"AltGr+{letter} already has an output")
        result[code] = output
    return result
