"""Generate Windows KLC source directly; no imported US .klc template."""
from ..hardware import WINDOWS, STANDARD, ISO_EXTRA
from ..reference import ordinary_ascii

CTRL_SPECIAL = {
    "LBRACKET": "001b", "RBRACKET": "001d", "BACKSLASH": "001c",
    "ISO_EXTRA": "001c", "SPACE": "0020",
}
def hex_units(value):
    raw = value.encode("utf-16-le")
    return [int.from_bytes(raw[j:j+2], "little") for j in range(0,len(raw),2)]
def code(value):
    if value is None:
        return "-1"
    units = hex_units(value)
    return "%%" if len(units)>1 else f"{units[0]:04x}"
def render(mapping):
    lines = [
        'KBD\tonnoy\t"Onnoy"',
        'COPYRIGHT\t"Copyright (c) Onnoy contributors"',
        'COMPANY\t"Onnoy"',
        'LOCALENAME\t"bn-BD"',
        'LOCALEID\t"00000845"',
        'VERSION\t1.0',
        '',
        'SHIFTSTATE', '0\t// Base', '1\t// Shift',
        '2\t// Ctrl', '6\t// AltGr', '7\t// Shift+AltGr',
        '', 'LAYOUT', '//SC VK_ Cap 0 1 2 6 7'
    ]
    ligatures = []
    for key in STANDARD+(ISO_EXTRA,):
        if key not in mapping: continue
        sc,vk=WINDOWS[key]
        vals=mapping[key]
        ctrl=CTRL_SPECIAL.get(key,"-1")
        fields=[code(vals[0]),code(vals[1]),ctrl,code(vals[2]),code(vals[3])]
        lines.append(f'{sc}\t{vk}\t0\t'+"\t".join(fields)+f'\t// {key}')
        for idx,value in enumerate(vals):
            if value is not None and len(hex_units(value))>1:
                ligatures.append(f'{vk}\t{(0,1,3,4)[idx]}\t'+
                                 " ".join(f'{unit:04x}' for unit in hex_units(value)))
    if ligatures:
        lines.extend(['', 'LIGATURE', '//VK_ Mod# Char0 Char1 Char2 Char3', *ligatures])
    lines += ['', 'KEYNAME', '01\tEsc', '0e\tBackspace', '0f\tTab',
              '1c\tEnter', '1d\tCtrl', '2a\tShift', '36\t"Right Shift"',
              '38\tAlt', '39\tSpace', '3a\t"Caps Lock"',
              'KEYNAME_EXT', '1c\t"Num Enter"', '1d\t"Right Ctrl"',
              '35\t"Num /"', '38\t"Right Alt"', '5b\t"Left Windows"',
              '5c\t"Right Windows"', '5d\tApplication',
              'DESCRIPTIONS', '0845\tBengali (Onnoy)',
              'LANGUAGENAMES', '0845\tBangla (Bangladesh)', 'ENDKBD', '']
    return "\r\n".join(lines)
