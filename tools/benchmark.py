#!/usr/bin/env python3
"""Compare physical-key workload on a UTF-8 corpus; this does not measure human speed."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Allow standalone script invocation: python tools/benchmark.py
import sys
sys.path.insert(0, str(ROOT))
PHYSICAL = {}
for row, prefix in (("QWERTYUIOP", "AD"), ("ASDFGHJKL", "AC"), ("ZXCVBNM", "AB"), ("1234567890", "AE")):
    PHYSICAL.update({f"{prefix}{i:02}": key for i, key in enumerate(row, 1)})
PHYSICAL.update({"AD11": "[", "AD12": "]", "AC10": ";", "AC11": "'", "AB08": ",",
                 "AB09": ".", "AB10": "/", "AE11": "-", "AE12": "=", "BKSL": "\\", "TLDE": chr(96)})
ASCII = {"exclam":"!","at":"@","numbersign":"#","dollar":"$","percent":"%","asciicircum":"^","ampersand":"&","asterisk":"*","parenleft":"(","parenright":")","minus":"-","underscore":"_","equal":"=","plus":"+","bracketleft":"[","bracketright":"]","braceleft":"{","braceright":"}","semicolon":";","colon":":","apostrophe":"'","quotedbl":"\"","comma":",","less":"<","period":".","greater":">","slash":"/","question":"?","backslash":"\\","bar":"|","grave":"`","asciitilde":"~","space":" "}

def onnoy():
    from onnoy.model import resolve

    # Benchmarks use printable US key labels, unlike the canonical JSON.
    # Translate key IDs once so the same physical-key model is used for
    # Onnoy, legacy variants, Probhat, and KaGaPa.
    symbols = {
        "GRAVE": "`", "MINUS": "-", "EQUAL": "=",
        "LBRACKET": "[", "RBRACKET": "]", "BACKSLASH": "\\",
        "SEMICOLON": ";", "APOSTROPHE": "'", "COMMA": ",",
        "PERIOD": ".", "SLASH": "/", "SPACE": " ",
    }
    return {
        symbols.get(key, key): list(values)
        for key, values in resolve().items()
    }


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
    if kind == "shift-f":
        layout["/"] = ["/", "?", None, None]
        layout["F"][1] = "্"
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
    size = len(text)
    scores = [(float("inf"), float("inf"))] * (size + 1)
    scores[size] = (0, 0)
    chosen = [None] * size
    for i in range(size - 1, -1, -1):
        scores[i] = (scores[i + 1][0] + 1, scores[i + 1][1])
        chosen[i] = (i + 1, None)
        for output, candidates in outputs.items():
            if text.startswith(output, i):
                j = i + len(output)
                for cost, key, level in candidates:
                    score = (scores[j][0], scores[j][1] + cost)
                    if score < scores[i]:
                        scores[i], chosen[i] = score, (j, (key, level))
    strokes = []
    i = 0
    while i < size:
        i, stroke = chosen[i]
        if stroke:
            strokes.append(stroke)
    physical = [key for key, _ in strokes]
    positions = {}
    for rownum, row in enumerate(("1234567890-=", "QWERTYUIOP[]", "ASDFGHJKL;'", "ZXCVBNM,./")):
        for x, key in enumerate(row):
            positions[key] = (x + rownum * .25, rownum)
    finger_rows = ("1234567890", "QWERTYUIOP", "ASDFGHJKL;", "ZXCVBNM,./")
    fingers = {}
    for row in finger_rows:
        for x, key in enumerate(row):
            fingers[key] = ("L" if x < len(row) / 2 else "R",
                            min(x, len(row) - 1 - x, 3))
    same_finger = sum(fingers.get(a) == fingers.get(b) for a, b in zip(physical, physical[1:])
                      if a in fingers and b in fingers)
    hand_alternation = sum(fingers[a][0] != fingers[b][0] for a, b in zip(physical, physical[1:])
                           if a in fingers and b in fingers)
    travel = sum(((positions[a][0] - positions[b][0]) ** 2
                  + (positions[a][1] - positions[b][1]) ** 2) ** .5
                 for a, b in zip(physical, physical[1:])
                 if a in positions and b in positions)
    return {"unavailable_codepoints": scores[0][0], "nfd_codepoints": size,
            "physical_chords": len(strokes),
            "shift_chords": sum(layer in (1, 3) for _, layer in strokes),
            "altgr_chords": sum(layer in (2, 3) for _, layer in strokes),
            "same_finger_pairs_approx": same_finger,
            "hand_alternations_approx": hand_alternation,
            "sequential_key_distance_approx": round(travel, 1),
            "weighted_effort": round(scores[0][1], 2)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=ROOT / "tools/demo-bengali.txt")
    parser.add_argument("--xkb", type=Path, default=Path("/usr/share/X11/xkb/symbols/in"))
    parser.add_argument("--shift-weight", type=float, default=.5)
    parser.add_argument("--altgr-weight", type=float, default=1)
    args = parser.parse_args()
    if args.shift_weight < 0 or args.altgr_weight < 0:
        parser.error("Modifier weights must not be negative")
    corpus = args.corpus.read_text(encoding="utf-8")
    ours = onnoy()
    layouts = {"Onnoy": ours, "Onnoy/legacy-Shift+F": variant(ours, "shift-f"),
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
