"""Emit Keyman desktop/web .kmn from the same resolved mapping.

The KMN is generated, never hand-maintained as a parallel keyboard.
"""
from ..hardware import KEYMAN, STANDARD, ISO_EXTRA

def render(mapping):
    lines=["c Generated from layout/onnoy.json; do not edit.",
           "store(&VERSION) '15.0'",
           "store(&NAME) 'Onnoy'",
           "store(&KEYBOARDVERSION) '1.0'",
           "store(&TARGETS) 'any'",
           "begin Unicode > use(main)", "",
           "group(main) using keys"]
    modifiers=("","SHIFT ","RALT ","SHIFT RALT ")
    for key in STANDARD+(ISO_EXTRA,):
        if key not in mapping:
            continue
        for i,output in enumerate(mapping[key]):
            # All four chords get explicit rules, including nul for unused
            # levels, so Keyman cannot leak an underlying Latin character.
            result=("U+%04X"%ord(output)) if output else "nul"
            lines.append(f'+ [{modifiers[i]}{KEYMAN[key]}] > {result}')
    return "\ufeff"+"\n".join(lines)+"\n"
