#!/usr/bin/env python3
"""Add TOML-defined conjunct shortcuts to Kalamine's native output files.

Kalamine's key cells represent one Unicode scalar. Windows/macOS can emit
sequences directly; modern libxkbcommon supports multiple keysyms per level.
Legacy xkbcomp loses multi-keysym levels, so the standalone X11 keymap is
intentionally left unchanged.
"""
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from kalamine.layout import KeyboardLayout, load_layout
from kalamine.utils import SCAN_CODES

from sequences import altgr_sequences

ROOT = Path(__file__).resolve().parents[1]
SCAN = {"KeyG": "22", "KeyK": "25"}
MAC_CODE = {"KeyG": "5", "KeyK": "40"}


def replace_once(data: str, pattern: str, replacement, label: str) -> str:
    result, n = re.subn(pattern, replacement, data, count=1, flags=re.MULTILINE)
    if n != 1:
        raise ValueError(f"Missing generated {label}: {pattern}")
    return result


def apply(source: Path, dist: Path) -> None:
    layout = KeyboardLayout(load_layout(source))
    sequences = altgr_sequences(source, layout)
    if not sequences:
        return
    if set(sequences) - set(SCAN):
        raise ValueError("Native ligature shortcut lacks scan-code assignment")

    # MSKLC uses %% and a LIGATURE table for multi-unit Unicode output.
    klc = dist / "onnoy.klc"
    windows = klc.read_text(encoding="utf-16")
    for code, output in sequences.items():
        scan = SCAN[code]
        def patch_klc(match, output=output):
            fields = match.group(0).split("\t")
            if fields[7] != "-1":
                raise ValueError(f"Native AltGr key {code} is already assigned")
            fields[7] = "%%"
            return "\t".join(fields)
        windows = replace_once(
            windows, rf"^{scan}\t[^\r\n]+$", patch_klc, f"KLC {code}"
        )
    ligatures = ["LIGATURE"]
    for code, output in sorted(sequences.items()):
        letter = code[3:]
        ligatures.append("\t".join([letter, "6", *(f"{ord(c):04X}" for c in output)]))
    windows = replace_once(
        windows, r"^KEYNAME //\{\{\{$",
        "\n".join(ligatures) + "\n\nKEYNAME //{{{", "KLC ligatures"
    )
    with klc.open("w", encoding="utf-16", newline="\r\n") as handle:
        handle.write(windows)

    # macOS's Option map is index 3; its output attribute supports strings.
    mac = dist / "onnoy.keylayout"
    xml = mac.read_text(encoding="utf-8")
    xml = replace_once(xml, r'maxout="1"', 'maxout="3"', "macOS maxout")
    start = xml.index('<keyMap index="3">')
    end = xml.index("</keyMap>", start)
    option_map = xml[start:end]
    for code, output in sequences.items():
        ident = MAC_CODE[code]
        def patch_mac(match, output=output):
            if match.group(2) != "&#x0010;":
                raise ValueError(f"macOS Option key {code} already assigned")
            return match.group(1) + output + match.group(3)
        option_map = replace_once(
            option_map,
            rf'(<key code="{ident}"\s+output=")([^"]*)("\s*/>)',
            patch_mac, f"macOS {code}"
        )
    xml = xml[:start] + option_map + xml[end:]
    ET.fromstring(xml)  # fail on invalid XML
    mac.write_text(xml, encoding="utf-8")

    # AutoHotkey v1.1: input text directly, not one code point at a time.
    ahk = dist / "onnoy.ahk"
    ahk_text = ahk.read_text(encoding="utf-8-sig")
    shortcuts = ["; Conjunct shortcuts"]
    for code, output in sorted(sequences.items()):
        shortcuts.append(f"<^>!SC{SCAN[code]}::SendInput, {{Text}}{output}")
    ahk_text = replace_once(
        ahk_text, r"^; Special Keys$",
        "\n".join(shortcuts) + "\n\n; Special Keys", "AutoHotkey shortcuts"
    )
    ahk.write_text(ahk_text, encoding="utf-8")

    # Multi-keysyms require modern libxkbcommon. The legacy X11 keymap is
    # left untouched because xkbcomp silently discards these sequences.
    xkb = dist / "onnoy.xkb_symbols"
    symbols = xkb.read_text(encoding="utf-8")
    for code, output in sequences.items():
        key_name = "AC05" if code == "KeyG" else "AC08"
        def patch_xkb(match, output=output):
            return (match.group(1) + "{ " +
                    ", ".join("U" + f"{ord(c):04X}" for c in output) +
                    " }" + match.group(2))
        symbols = replace_once(
            symbols,
            rf'^(\s*key <{key_name}> \{{\[\s*[^,]+,\s*[^,]+,\s*)VoidSymbol(\s*,[^\r\n]*\]\}};.*)$',
            patch_xkb, f"XKB {code}"
        )
    xkb.write_text(symbols, encoding="utf-8")


if __name__ == "__main__":
    apply(ROOT / "layout.toml", ROOT / "dist")
