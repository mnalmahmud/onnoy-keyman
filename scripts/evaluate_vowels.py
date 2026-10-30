#!/usr/bin/env python3
"""Read independent language corpora and audit Onnoy keyboard layer reachability.

No corpus is included in the repository. The report is a keyboard-modifier proxy,
not a human typing-speed measurement, and never pools different languages.
"""
import argparse
import bz2
from collections import Counter
import gzip
import json
import lzma
from pathlib import Path
import sys
import unicodedata

LAYERS = ("Base", "Shift", "AltGr", "Shift+AltGr")
VOWELS = tuple("অআইঈউঊঋএঐওঔািীুূৃেৈোৌৗ")
VOWEL_BY_NORMALIZED = {unicodedata.normalize("NFD", v): v for v in VOWELS}
BENGALI = lambda c: 0x0980 <= ord(c) <= 0x09FF or 0x11DF0 <= ord(c) <= 0x11DFF


def get_layout(path):
    layout = json.loads(Path(path).read_text(encoding="utf-8"))
    if layout.get("layers") != ["base", "shift", "altgr", "shift_altgr"]:
        raise ValueError(f"Not a four-layer Onnoy layout: {path}")
    outputs = {}
    for key, slots in layout["keys"].items():
        if len(slots) != 4:
            raise ValueError(f"Expected four layers for {key}")
        for layer, value in enumerate(slots):
            if value:
                normalized = unicodedata.normalize("NFD", value)
                # Prefer fewer simultaneous modifiers; break ties by layer number.
                if normalized not in outputs or (layer.bit_count(), layer) < (
                        outputs[normalized][0].bit_count(), outputs[normalized][0]):
                    outputs[normalized] = (layer, key)
    if not outputs:
        raise ValueError("Layout contains no outputs")
    first = {}
    for output in sorted(outputs, key=len, reverse=True):
        first.setdefault(output[0], []).append(output)
    return outputs, first


def open_corpus(path):
    path = Path(path)
    suffix = path.suffix.lower()
    handler = {".gz": gzip.open, ".bz2": bz2.open, ".xz": lzma.open}.get(suffix, open)
    return handler(path, "rt", encoding="utf-8", errors="replace")


def measure(path, index, jsonl_field=None, max_lines=None):
    choices, lookup = index
    layers, missing, vowels = Counter(), Counter(), Counter()
    examined = lines = found = 0
    with open_corpus(path) as stream:
        for raw in stream:
            if max_lines is not None and lines >= max_lines:
                break
            if jsonl_field:
                obj = json.loads(raw)
                raw = obj[jsonl_field]
                if not isinstance(raw, str):
                    continue
            text = unicodedata.normalize("NFD", raw)
            lines += 1
            examined += sum(BENGALI(c) for c in text)
            pos = 0
            while pos < len(text):
                char = text[pos]
                if not BENGALI(char):
                    pos += 1
                    continue
                for out in lookup.get(char, ()):
                    if text.startswith(out, pos):
                        layer, _ = choices[out]
                        layers[LAYERS[layer]] += 1
                        found += 1
                        # Explicit conjunct shortcuts count as one output event.
                        vowel = VOWEL_BY_NORMALIZED.get(out)
                        if vowel:
                            vowels[vowel] += 1
                        pos += len(out)
                        break
                else:
                    missing[char] += 1
                    pos += 1
    return {"lines": lines, "bengali_codepoints_scanned": examined,
            "mapped_output_events": found, "layers": dict(layers),
            "unmapped_codepoints": dict(missing), "vowel_counts": dict(vowels)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", default="layout/onnoy.json", help="Reference layout")
    parser.add_argument("--candidate", help="Optional proposed layout for comparison")
    parser.add_argument("--corpus", action="append", required=True, metavar="LANG=PATH",
                        help="Labeled UTF-8 corpus (.txt, .gz, .xz, .bz2 or JSONL)")
    parser.add_argument("--jsonl-field", help="JSONL field containing text (for all corpora)")
    parser.add_argument("--output", help="Write JSON report to this path")
    parser.add_argument("--max-lines", type=int, help="Optional pilot limit; first N lines may not be representative")
    args = parser.parse_args(argv)
    if args.max_lines is not None and args.max_lines <= 0:
        parser.error("--max-lines must be positive")
    baseline = get_layout(args.layout)
    candidate = get_layout(args.candidate) if args.candidate else None
    reports = []
    for entry in args.corpus:
        if "=" not in entry:
            parser.error("Each --corpus must be LANGUAGE=PATH")
        language, filename = entry.split("=", 1)
        if not language or not filename:
            parser.error("Each --corpus must be LANGUAGE=PATH")
        item = {"language": language, "source": filename,
                "current": measure(filename, baseline, args.jsonl_field, args.max_lines)}
        if candidate:
            item["candidate"] = measure(filename, candidate, args.jsonl_field, args.max_lines)
        reports.append(item)
    report = {"caveat": "Counts measure mapped output events by layer, not actual human effort or typing speed. Compare languages separately; audit genre and orthography.",
              "reference": args.layout, "candidate": args.candidate,
              "max_lines": args.max_lines, "corpora": reports}
    result = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
