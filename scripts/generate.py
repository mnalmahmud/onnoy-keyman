#!/usr/bin/env python3
"""Generate native Linux XKB, macOS keylayout, and Windows KLC sources.
The sole character mapping lives in layout/onnoy.json.
"""
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORDER = "QWERTYUIOP[]ASDFGHJKL;ZXCVBNM1234567890=."
KEY_ORDER = tuple(ORDER) + ("SPACE",)
# Platform exports are pinned at build time; no native runtime dependency.
MAC_BASE = ROOT / "layout/platform-bases/macos-us.keylayout"
WIN_BASE = ROOT / "layout/platform-bases/windows-us.klc"

XKB = dict(zip("QWERTYUIOP", "AD01 AD02 AD03 AD04 AD05 AD06 AD07 AD08 AD09 AD10".split()))
XKB.update(dict(zip("ASDFGHJKL", "AC01 AC02 AC03 AC04 AC05 AC06 AC07 AC08 AC09".split())))
XKB.update(dict(zip("ZXCVBNM", "AB01 AB02 AB03 AB04 AB05 AB06 AB07".split())))
XKB.update(dict(zip("1234567890", "AE01 AE02 AE03 AE04 AE05 AE06 AE07 AE08 AE09 AE10".split())))
XKB["["] = "AD11"
XKB["]"] = "AD12"
XKB[";"] = "AC10"
XKB["="] = "AE12"
XKB["."] = "AB09"
XKB["SPACE"] = "SPCE"
SCAN = dict(zip("1234567890", "02 03 04 05 06 07 08 09 0A 0B".split()))
SCAN.update(dict(zip("QWERTYUIOP", "10 11 12 13 14 15 16 17 18 19".split())))
SCAN.update(dict(zip("ASDFGHJKL", "1E 1F 20 21 22 23 24 25 26".split())))
SCAN.update(dict(zip("ZXCVBNM", "2C 2D 2E 2F 30 31 32".split())))
SCAN["["] = "1A"
SCAN["]"] = "1B"
SCAN[";"] = "27"
SCAN["="] = "0D"
SCAN["."] = "34"
SCAN["SPACE"] = "39"
MAC = dict(zip("ASDFGHJKL", [0,1,2,3,5,4,38,40,37]))
MAC.update(dict(zip("QWERTYUIOP", [12,13,14,15,17,16,32,34,31,35])))
MAC.update(dict(zip("ZXCVBNM", [6,7,8,9,11,45,46])))
MAC.update(dict(zip("1234567890", [18,19,20,21,23,22,26,28,25,29])))
MAC["["] = 33
MAC["]"] = 30
MAC[";"] = 41
MAC["="] = 24
MAC["."] = 47
MAC["SPACE"] = 49
# Physical scan codes remain platform metadata; printable outputs live in layout/onnoy.json.
PUNCT_META = [
 ("29", "OEM_3", 50, "`"), ("0C", "OEM_MINUS", 27, "-"),
 ("2B", "OEM_5", 42, "\\"), ("28", "OEM_7", 39, "'"),
 ("33", "OEM_COMMA", 43, ","), ("35", "OEM_2", 44, "/"),
]
LAYOUT = json.loads((ROOT / "layout/onnoy.json").read_text(encoding="utf-8"))
def mapping():
    data = LAYOUT
    assert data["layers"] == ["base", "shift", "altgr", "shift_altgr"]
    assert set(data["passthrough"]) <= {entry[3] for entry in PUNCT_META}
    assert all(len(values) == 4 and all(v is None or isinstance(v, str) and len(v) == 1
                                         for v in values)
               for values in data["passthrough"].values())
    m = data["keys"]
    # Equal/plus inherit the pinned US source rather than a Bengali override.
    assert set(m) == set(ORDER) - {"="}
    assert all(isinstance(v, list) and len(v) == 4 and
               all(x is None or isinstance(x, str) and 1 <= len(x) <= 4 for x in v)
               for v in m.values())
    assert m["Q"] == ["দ", "ধ", None, None]
    assert m["D"] == ["ড", "ঢ", None, None]
    assert m["W"] == ["ূ", "ঊ", "ৱ", None]
    assert m["R"] == ["র", "ড়", None, None]
    assert sum(value == "ঢ়" for values in m.values() for value in values) == 1
    assert m["T"] == ["ট", "ঠ", "ৎ", None]
    assert m["F"] == ["ত", "থ", None, None]
    assert m["P"] == ["প", "ফ", None, None]
    assert m["B"] == ["ব", "ভ", None, None]
    assert m["V"] == ["অ", "ৗ", None, None]
    assert m["Y"] == ["ী", "ঈ", "য়", None]
    assert m["Z"] == ["য", None, None, None]
    assert sum(v == "য়" for vs in m.values() for v in vs) == 1
    assert m["X"] == ["শ", "ঢ়", None, None]
    assert m["N"] == ["ন", "ণ", "\u200c", "ঞ"]
    assert m["M"] == ["ম", "ঙ", "ং", None]
    assert m["S"][:2] == ["স", "ষ"]
    assert m["A"] == ["া", "আ", None, None]
    assert m["H"] == ["হ", "ঃ", None, None]
    assert m["J"] == ["জ", "ঝ", "\u200d", None]
    assert all(sum(v == ch for vs in m.values() for v in vs) == 1
               for ch in ("\u200d", "\u200c", "ঞ", "ঁ", "ং", "ঙ"))
    assert m["L"] == ["ল", None, "ঁ", None]
    assert m["["] == ["ৈ", "ঐ", "[", "{"]
    assert m["]"] == ["ৌ", "ঔ", "]", "}"]
    assert m[";"] == ["ৃ", "ঋ", ";", ":"]
    assert m["."] == ["।", ">", ".", None]
    assert m["O"][:2] == ["ো", "ও"]
    assert m["4"][1] == "৳" and m["4"][3] == "$"
    assert "SPACE" not in m
    assert data["passthrough"][","] == [",", "<", "়", "𑷰"]
    assert data["passthrough"]["/"] == ["্", "?", "/", None]
    assert data["passthrough"]["'"] == ["'", '"', None, None]
    assert all(key not in data["passthrough"] for key in (chr(96), "-", "\\"))
    return {**m, **data["passthrough"]}


def linux(m):
    """Native XKB symbols: no input method, compose engine, or custom runtime."""
    if any(value is not None and len(value) != 1 for values in m.values() for value in values):
        raise ValueError("Native XKB needs one Unicode scalar per key; multi-codepoint output unsupported")
    s = [
        "// Generated from layout/onnoy.json; do not edit.",
        "default partial alphanumeric_keys",
        'xkb_symbols "basic" {',
        '    include "us(basic)"',
        '    name[Group1] = "Bengali (Onnoy)";',
        '    include "level3(ralt_switch)"',
    ]
    for key in KEY_ORDER + tuple(x[3] for x in PUNCT_META):
        if key not in LAYOUT["keys"] and key not in LAYOUT["passthrough"]:
            continue  # Inherit untouched key directly from us(basic).
        symbols = ", ".join("VoidSymbol" if value is None else (
            "space" if value == " " else "U%04X" % ord(value)) for value in m[key])
        s.append('    key <%s> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ %s ] }; // %s'
                 % ((XKB[key] if key in XKB else {"`": "TLDE", "-": "AE11", "\\": "BKSL", "\'": "AC11", ",": "AB08", "/": "AB10"}[key]), symbols, key))
    return "\n".join(s + ["};", ""])


def utf16_units(value):
    raw = value.encode("utf-16-le")
    return [int.from_bytes(raw[i:i+2], "little") for i in range(0, len(raw), 2)]

def windows(m):
    """Patch an actual exported US MSKLC source, preserving Ctrl and scan codes."""
    source = WIN_BASE.read_text(encoding="utf-8-sig").splitlines()
    first = next(i for i, s in enumerate(source) if s.startswith("LAYOUT"))
    last = next(i for i, s in enumerate(source) if s.startswith("KEYNAME"))
    desc = next(i for i, s in enumerate(source) if s.startswith("DESCRIPTIONS"))
    scan_keys = {sc.upper(): key for key, sc in SCAN.items()}
    scan_keys.update({sc.upper(): key for sc, vk, mac, key in PUNCT_META})
    rows = []
    for line in source[first + 1:last]:
        parts = line.split("//", 1)[0].split()
        if len(parts) >= 6 and len(parts[0]) == 2 and all(ch in "0123456789abcdefABCDEF" for ch in parts[0]):
            rows.append(parts[:6])
    assert len(rows) >= 45
    code = lambda v: "-1" if v is None else ("%%" if len(utf16_units(v)) > 1 else "%04x" % ord(v))
    norm = lambda v: "%04x" % ord(v) if len(v) == 1 and v != "-" else v
    result = ['KBD\tonnoy\t"Onnoy"', '',
              'COPYRIGHT "(c) 2026 Muhtasham Nawr al-Mahmud"',
              'COMPANY "Muhtasham Nawr al-Mahmud"',
              'LOCALENAME "bn-BD"', 'LOCALEID "00000845"', 'VERSION 1.2', '',
              'SHIFTSTATE', '0\t// Base', '1\t// Shift', '2\t// Ctrl',
              '6\t// AltGr', '7\t// Shift+AltGr', '', 'LAYOUT',
              '//SC VK_ Cap 0 1 2 6 7']
    ligatures = []
    seen = set()
    for sc, vk, cap, base, shift, ctrl in rows:
        key = scan_keys.get(sc.upper())
        if key is not None:
            seen.add(key)
        if key in m:
            vals = m[key]
            cap = "0"
            values = [code(vals[0]), code(vals[1]), norm(ctrl), code(vals[2]), code(vals[3])]
            for slot, val in enumerate([vals[0], vals[1], None, vals[2], vals[3]]):
                if val is not None and len(utf16_units(val)) > 1:
                    ligatures.append("%s\t%d\t%s" %
                                     (vk, slot, " ".join("%04x" % u for u in utf16_units(val))))
        else:
            # Copy the reference's Base, Shift and Ctrl values.
            values = [norm(base), norm(shift), norm(ctrl),
                      "0020" if key == "SPACE" else "-1",
                      "0020" if key == "SPACE" else "-1"]
        result.append("%s\t%s\t%s\t%s\t// %s" %
                      (sc.upper(), vk, cap, " ".join(values), key or "US base"))
    assert set(m) <= seen, "Unknown Onnoy key in MSKLC US reference"
    if ligatures:
        result += ['', 'LIGATURE', '//VK_ Mod# Char0 Char1 Char2 Char3']
        result += ligatures
    result += ['', *source[last:desc], 'DESCRIPTIONS',
               '0845\tBengali (Onnoy)', 'LANGUAGENAMES',
               '0845\tBangla (Bangladesh)', 'ENDKBD', '']
    return "\r\n".join(result)


def macos(m):
    """Inherit unchanged keys via Apple's baseMapSet and baseIndex."""
    import copy
    source = ET.parse(MAC_BASE).getroot()
    base = source.find("./keyMapSet[@id='OnnoyUSBase']")
    assert base is not None and len(base.findall("keyMap")) == 5
    root = ET.Element("keyboard", {"group": "126", "id": "-15231",
                                  "name": "Onnoy", "maxout": "1"})
    layouts = ET.SubElement(root, "layouts")
    ET.SubElement(layouts, "layout", {"first": "0", "last": "17",
                "modifiers": "OnnoyModifiers", "mapSet": "OnnoyMap"})
    mods = ET.SubElement(root, "modifierMap",
                         {"id": "OnnoyModifiers", "defaultIndex": "0"})
    conditions = [["", "caps"], ["anyShift caps?"], ["anyOption caps?"],
                  ["anyShift anyOption caps?"],
                  ["command anyShift? caps? anyOption? anyControl?"],
                  ["anyControl command? anyShift? caps? anyOption?"]]
    for i, names in enumerate(conditions):
        n = ET.SubElement(mods, "keyMapSelect", {"mapIndex": str(i)})
        for name in names:
            ET.SubElement(n, "modifier", {"keys": name})
    maps = ET.SubElement(root, "keyMapSet", {"id": "OnnoyMap"})
    root.append(copy.deepcopy(base))
    for tag in ("actions", "terminators"):
        node = source.find(tag)
        if node is not None:
            root.append(copy.deepcopy(node))
    codes = dict(MAC)
    codes.update({key: code for sc, vk, code, key in PUNCT_META})
    for index in range(6):
        node = ET.SubElement(maps, "keyMap", {"index": str(index),
                              "baseMapSet": "OnnoyUSBase",
                              "baseIndex": str(min(index, 4))})
        if index < 4:
            for key, vals in m.items():
                ET.SubElement(node, "key",
                              {"code": str(codes[key]), "output": vals[index] or ""})
        # Command/Control retain the US reference's native shortcut behavior.
    ET.indent(root, space="  ")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">\n'
            + ET.tostring(root, encoding="unicode") + "\n")


def main():
    m=mapping()
    outputs={
      "dist/linux/symbols/onnoy":linux(m),
      "dist/windows/onnoy.klc":windows(m),
      "dist/macos/Onnoy.keylayout":macos(m),
    }
    check="--check" in sys.argv
    for path,content in outputs.items():
        p=ROOT/path
        raw=content.encode("utf-8")
        if check:
            if not p.exists() or p.read_bytes()!=raw: raise SystemExit("Generated file out of date: "+path)
        else:
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(raw)
        print(("Verified " if check else "Generated ")+path)
if __name__=="__main__": main()
