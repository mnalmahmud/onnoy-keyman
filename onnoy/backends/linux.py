"""Generate native Linux XKB symbols from a fully resolved Onnoy layout."""
from ..hardware import XKB, STANDARD, ISO_EXTRA

def render(mapping):
    lines = [
        "// Generated from layout/onnoy.json. Do not edit.",
        "default partial alphanumeric_keys",
        'xkb_symbols "basic" {',
        '    include "us(basic)"',
        '    include "level3(ralt_switch)"',
        '    name[Group1] = "Bengali (Onnoy)";'
    ]
    for key in STANDARD + (ISO_EXTRA,):
        if key not in mapping:
            continue
        values = mapping[key]
        symbols = ", ".join("VoidSymbol" if value is None else
                            ("space" if value == " " else f"U{ord(value):04X}") for value in values)
        lines.append(f'    key <{XKB[key]}> {{ type[Group1]="FOUR_LEVEL", symbols[Group1]=[ {symbols} ] }}; // {key}')
    return "\n".join(lines + ["};", ""])
