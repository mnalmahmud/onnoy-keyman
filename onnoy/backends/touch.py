"""Generate a compact, four-row Keyman phone keyboard from resolved Onnoy.

This file controls *placement*, not Unicode assignments. All printable
outputs come from onnoy.model.resolve(); no Bengali/Assamese character is
maintained here. A phone layout also acts as the tablet fallback in Keyman.
"""
import json
import unicodedata
from ..hardware import KEYMAN

LETTERS = ("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")
DIGITS = "1234567890"
PUNCTUATION = (
    "LBRACKET", "RBRACKET", "SEMICOLON", "SLASH", "APOSTROPHE",
    "MINUS", "EQUAL", "BACKSLASH", "COMMA", "PERIOD",
)
# Additional *positions* for related signs. All characters are still
# retrieved from the existing LBRACKET, RBRACKET and SEMICOLON mappings.
RELATED = {"E": ("LBRACKET",), "O": ("RBRACKET",), "R": ("SEMICOLON",)}

def unicode_key(value):
    if value is None or len(value) != 1:
        raise ValueError("Touch outputs must be individual Unicode scalars")
    return "U_%04X" % ord(value)

def caption(value):
    if value == "\u200d":
        return "ZWJ"
    if value == "\u200c":
        return "ZWNJ"
    if value == " ":
        return "*Sp*"
    if unicodedata.category(value).startswith("M"):
        return "◌" + value
    return value

def popup(value):
    return {"id": unicode_key(value), "text": caption(value)}

def keycap(key, mapping, layer=0, related=()):
    values = mapping[key]
    primary = values[layer]
    if primary is None:
        raise ValueError(f"Missing mobile primary output {key}.{layer}")
    spec = {"id": KEYMAN[key], "text": caption(primary)}
    # Explicit modifier for touch on the Shift display layer.
    if layer:
        spec["layer"] = "shift"
    alternates = []
    for index, value in enumerate(values):
        if index != layer and value is not None:
            alternates.append(value)
    for secondary in related:
        alternates.extend(value for value in mapping[secondary][:2] if value is not None)
    distinct = set()
    subs = []
    for value in alternates:
        if value != primary and value not in distinct:
            subs.append(popup(value))
            distinct.add(value)
    if subs:
        spec["sk"] = subs
        spec["hint"] = caption(alternates[0])
    return spec

def special(name, caption_text, nextlayer=None, width=None, active=False):
    spec = {"id": name, "text": caption_text, "sp": 2 if active else 1}
    if nextlayer:
        spec["nextlayer"] = nextlayer
    if width:
        spec["width"] = width
    return spec

def virama(mapping):
    base = mapping["GRAVE"][0]
    spec = {"id": unicode_key(base), "text": caption(base), "width": 95}
    others = [v for v in mapping["GRAVE"][1:] if v is not None]
    if others:
        spec["sk"] = [popup(v) for v in others]
    return spec

def bottom(mapping, numeric=False):
    return [
        special("K_NUMERALS", "*ABC*" if numeric else "*123*",
                nextlayer="default" if numeric else "numeric", width=120,
                active=numeric),
        {"id": unicode_key(mapping["COMMA"][0]), "text": caption(mapping["COMMA"][0]),
         "sk": [popup(mapping["COMMA"][1])]},
        virama(mapping),
        {"id": "K_SPACE", "text": "*Sp*", "width": 380, "layer": "default"},
        {"id": unicode_key(mapping["PERIOD"][0]), "text": caption(mapping["PERIOD"][0]),
         "sk": [popup(v) for v in mapping["PERIOD"][1:] if v is not None]},
        special("K_ENTER", "*Enter*", width=115),
    ]

def rows_for(mapping, layer):
    row0 = [keycap(key, mapping, layer, RELATED.get(key, ())) for key in LETTERS[0]]
    row1 = [keycap(key, mapping, layer) for key in LETTERS[1]]
    row2 = [
        special("K_SHIFT", "*Shifted*" if layer else "*Shift*",
                nextlayer="default" if layer else "shift", active=bool(layer),
                width=130),
        *[keycap(key, mapping, layer) for key in LETTERS[2]],
        special("K_BKSP", "*BkSp*", width=130),
    ]
    return [row0, row1, row2, bottom(mapping)]

def numeric_rows(mapping):
    digits = []
    for key in DIGITS:
        values = mapping[key]
        spec = {"id": unicode_key(values[0]), "text": caption(values[0])}
        alternates = []
        for value in values[1:]:
            if value is not None and value != values[0] and value not in alternates:
                alternates.append(value)
        if alternates:
            spec["sk"] = [popup(value) for value in alternates]
        digits.append(spec)
    symbols = [keycap(key, mapping) for key in PUNCTUATION]
    shifted_digits = [
        {"id": unicode_key(mapping[key][1]), "text": caption(mapping[key][1])}
        for key in DIGITS[:9]
    ]
    shifted_digits.append(special("K_BKSP", "*BkSp*", width=130))
    return [digits, symbols, shifted_digits, bottom(mapping, numeric=True)]

def render_data(mapping):
    layers = []
    for name, rows in (
        ("default", rows_for(mapping, 0)),
        ("shift", rows_for(mapping, 1)),
        ("numeric", numeric_rows(mapping)),
    ):
        layers.append({
            "id": name,
            "row": [{"id": i + 1, "key": keys} for i, keys in enumerate(rows)]
        })
    return {
        "phone": {
            "displayUnderlying": False,
            "fontsize": "1em",
            "layer": layers,
        }
    }

def render(mapping):
    return json.dumps(render_data(mapping), ensure_ascii=False, indent=2) + "\n"
