#!/usr/bin/env python3
"""Compare physical-key workload on a UTF-8 corpus; this does not measure human speed."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYSICAL = {}
for row, prefix in (("QWERTYUIOP", "AD"), ("ASDFGHJKL", "AC"), ("ZXCVBNM", "AB"), ("1234567890", "AE")):
    PHYSICAL.update({f"{prefix}{i:02}": key for i, key in enumerate(row, 1)})
PHYSICAL.update({"AD11": "[", "AD12": "]", "AC10": ";", "AC11": "'", "AB08": ",",
                 "AB09": ".", "AB10": "/", "AE11": "-", "AE12": "=", "BKSL": "\\", "TLDE": chr(96)})
ASCII = dict(zip(("exclam at numbersign dollar percent asciicircum ampersand asterisk "
                  "parenleft parenright minus underscore equal plus bracketleft bracketright "
                  "braceleft braceright semicolon colon apostrophe quotedbl comma less period "
                  "greater slash question backslash bar grave asciitilde space").split(),
                 list("!@#$%^&*()-_=+[]{};:'\",<.>/?\\|" + chr(96) + "~ ")))

def onnoy():
    layout = json.loads((ROOT / "layout/onnoy.json").read_text(encoding="utf-8"))
    result = {key: values[:] for key, values in layout["keys"].items()}
    result.update({key: [*values, None, None] for key, values in layout["passthrough"].items()})
    return result

def xkb(text, name):
    match = re.search(r'xkb_symbols\s+"' + re.escape(name) + r'"\s*\{', text)
    if not match:
        raise ValueError("Missing XKB variant " + name)
    block = text[match.end():].split("\n};", 1)[0]
    result = {"SPACE": [" ", " ", None, None]}
    for physical, content in re.findall(r'key\s*<([^>]+)>\s*\{\s*\[([^\]]+)\]', block):
        key = PHYSICAL.get(physical)
        if not key:
            continue
        values = []
        for token in content.split(",")[:4]:
            symbol = token.strip().split()[0]
            if re.fullmatch(r'U[0-9A-Fa-f]{4,6}', symbol):
                values.append(chr(int(symbol[1:], 16)))
            else:
                values.append(ASCII.get(symbol, symbol if len(symbol) == 1 else None))
        result[key] = (values + [None] * 4)[:4]
    return result

def variant(base, kind):
    layout = {key: value[:] for key, value in base.items()}
    if kind == "slash":
        layout["/"] = ["্", "?", "/", None]
    if kind == "altgr-f":
        layout["F"][2] = "্"
    return layout

def measure(text, layout, shift_weight=.5, altgr_weight=1):
    text = unicodedata.normalize("NFD", text)
    outputs = {}
    for key, layers in layout.items():
        for level, value in enumerate(layers):
            if value:
                output = unicodedata.normalize("NFD", value)
                cost = 1 + shift_weight * (level in (1, 3)) + altgr_weight * (level in (2, 3))
                outputs.setdefault(output, []).append((cost, key, level))
    dp = [(float("inf"), float("inf"), ()) for _ in range(len(text) + 1)]
    dp[-1] = (0, 0, ())
    for i in range(len(text) - 1, -1, -1):
        tail = dp[i + 1]
        best = (tail[0] + 1, tail[1], tail[2])
        for output, candidates in outputs.items():
            if text.startswith(output, i):
                following = dp[i + len(output)]
                for cost, key, layer in candidates:
                    score = (following[0], following[1] + cost, ((key, layer),) + following[2])
                    if score[:2] < best[:2]:
                        best = score
        dp[i] = best
    unavailable, effort, strokes = dp[0]
    return {"unavailable_codepoints": unavailable, "nfd_codepoints": len(text),
            "physical_chords": len(strokes),
            "shift_chords": sum(layer in (1, 3) for _, layer in strokes),
            "altgr_chords": sum(layer in (2, 3) for _, layer in strokes),
            "weighted_effort": round(effort, 2)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=ROOT / "tests/data/demo-bengali.txt")
    parser.add_argument("--xkb", type=Path, default=Path("/usr/share/X11/xkb/symbols/in"))
    parser.add_argument("--shift-weight", type=float, default=.5)
    parser.add_argument("--altgr-weight", type=float, default=1)
    args = parser.parse_args()
    if args.shift_weight < 0 or args.altgr_weight < 0:
        parser.error("Modifier weights must not be negative")
    corpus = args.corpus.read_text(encoding="utf-8")
    ours = onnoy()
    layouts = {"Onnoy": ours, "Onnoy/slash-virama": variant(ours, "slash"),
               "Onnoy/AltGr+F-virama": variant(ours, "altgr-f")}
    if args.xkb.exists():
        source = args.xkb.read_text(encoding="utf-8")
        layouts["Probhat"] = xkb(source, "ben_probhat")
        layouts["KaGaPa"] = xkb(source, "ben-kagapa")
    print(json.dumps({"corpus": str(args.corpus),
                      "warning": "Small demo is illustrative, not representative; compare only equal coverage.",
                      "results": {name: measure(corpus, mapping, args.shift_weight, args.altgr_weight)
                                  for name, mapping in layouts.items()}},
                     ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
