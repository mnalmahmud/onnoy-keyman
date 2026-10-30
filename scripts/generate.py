#!/usr/bin/env python3
"""Generate KeymanWeb, Linux XKB, macOS keylayout, and Windows KLC sources.
The sole character mapping lives in layout/onnoy.json.
"""
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORDER = "QWERTYUIOP[]ASDFGHJKLZXCVBNM1234567890."
KEY_ORDER = tuple(ORDER) + ("SPACE",)
XKB = dict(zip("QWERTYUIOP", "AD01 AD02 AD03 AD04 AD05 AD06 AD07 AD08 AD09 AD10".split()))
XKB.update(dict(zip("ASDFGHJKL", "AC01 AC02 AC03 AC04 AC05 AC06 AC07 AC08 AC09".split())))
XKB.update(dict(zip("ZXCVBNM", "AB01 AB02 AB03 AB04 AB05 AB06 AB07".split())))
XKB.update(dict(zip("1234567890", "AE01 AE02 AE03 AE04 AE05 AE06 AE07 AE08 AE09 AE10".split())))
XKB["["] = "AD11"
XKB["]"] = "AD12"
XKB["."] = "AB09"
XKB["SPACE"] = "SPCE"
SCAN = dict(zip("1234567890", "02 03 04 05 06 07 08 09 0A 0B".split()))
SCAN.update(dict(zip("QWERTYUIOP", "10 11 12 13 14 15 16 17 18 19".split())))
SCAN.update(dict(zip("ASDFGHJKL", "1E 1F 20 21 22 23 24 25 26".split())))
SCAN.update(dict(zip("ZXCVBNM", "2C 2D 2E 2F 30 31 32".split())))
SCAN["["] = "1A"
SCAN["]"] = "1B"
SCAN["."] = "34"
SCAN["SPACE"] = "39"
MAC = dict(zip("ASDFGHJKL", [0,1,2,3,5,4,38,40,37]))
MAC.update(dict(zip("QWERTYUIOP", [12,13,14,15,17,16,32,34,31,35])))
MAC.update(dict(zip("ZXCVBNM", [6,7,8,9,11,45,46])))
MAC.update(dict(zip("1234567890", [18,19,20,21,23,22,26,28,25,29])))
MAC["["] = 33
MAC["]"] = 30
MAC["."] = 47
MAC["SPACE"] = 49
PUNCT = [
 ("29","OEM_3",50,"" + chr(96),"~"),
 ("0C","OEM_MINUS",27,"-","_"),("0D","OEM_PLUS",24,"=","+"),
 ("2B","OEM_5",42,"\\","|"),("27","OEM_1",41,";",":"),
 ("28","OEM_7",39,"'",'"'),("33","OEM_COMMA",43,",","<"),
 ("35","OEM_2",44,"/","?"),
]
def mapping():
    data=json.loads((ROOT/"layout/onnoy.json").read_text(encoding="utf-8"))
    assert data["layers"]==["base","shift","altgr","shift_altgr"]
    m=data["keys"]
    assert set(m)==set(KEY_ORDER)
    assert all(isinstance(v,list) and len(v)==4 and
               all(x is None or isinstance(x,str) and 1<=len(x)<=4 for x in v)
               for v in m.values())
    assert m["X"][:3]==["়","্","𑷰"] and m["."][:3]==["।",">","."]
    assert m["["]==["ৈ","ঐ","[","{"] and m["]"]==["ূ","ঊ","]","}"]
    assert m["4"][1]=="৳" and m["4"][3]=="$"
    assert m["SPACE"][:2]==[" "," "]
    return m

def keyman(m):
    s=["c Onnoy (অন্বয়) — generated from layout/onnoy.json; do not edit directly.",
       "store(&VERSION) '16.0'", "store(&NAME) 'Onnoy (অন্বয়)'",
       "store(&KEYBOARDVERSION) '1.0'", "store(&TARGETS) 'any'",
       "store(&layoutfile) 'onnoy.keyman-touch-layout'",
       "", "begin Unicode > use(main)", "", "group(main) using keys"]
    for k in KEY_ORDER:
        name={".": "PERIOD", "[": "LBRKT", "]": "RBRKT"}.get(k, k)
        s.append("")
        for modifier,output in zip(("","SHIFT ","RALT ","SHIFT RALT "),m[k]):
            symbol="nul" if output is None else " ".join("U+%04X"%ord(ch) for ch in output)
            s.append("+ [%sK_%s] > %s"%(modifier,name,symbol))
    for value in sorted({v for values in m.values() for v in values if v and len(v)>1}):
        ident = "T_SEQ_" + "_".join("%04X" % ord(c) for c in value)
        output = " ".join("U+%04X" % ord(c) for c in value)
        s.append("+ [%s] > %s" % (ident, output))
    return "\n".join(s)+"\n"


def touch(m):
    """Generate a compact phone/tablet layout from the canonical four layers.

    U_ virtual keys emit their Unicode string directly on touch devices; this
    avoids relying on desktop AltGr modifier emulation on phones.
    """
    alpha_rows = ("QWERTYUIOP", "ASDFGHJKL[]", "ZXCVBNM")
    layer_names = ("default", "shift", "altgr", "shift_altgr")

    def direct(value):
        return ("U_" if len(value) == 1 else "T_SEQ_") + "_".join("%04X" % ord(c) for c in value)

    def label(value):
        return {"\u200d": "ZWJ", "\u200c": "ZWNJ"}.get(value, value)

    def letter(key, index):
        value = m[key][index]
        if value is None:
            return {"id": "T_EMPTY_%s_%d" % (key, index), "text": "", "sp": 9}
        item = {"id": direct(value), "text": label(value)}
        if index == 0:
            subkeys = [{"id": direct(other), "text": label(other)}
                       for other in m[key][1:] if other and other != value]
            if subkeys:
                item["sk"] = subkeys
        return item

    def frame(index):
        states = (
            ("shift", "altgr"), ("default", "shift_altgr"),
            ("shift_altgr", "default"), ("altgr", "shift"))
        shift_target, altgr_target = states[index]
        if index in (0, 1):
            space_key = {"id": "K_SPACE", "text": "*Sp*", "width": 270}
            if index == 0:
                space_key["sk"] = [{"id": direct(value), "text": label(value)}
                                   for value in m["SPACE"][2:]]
        else:
            space_key = {"id": direct(m["SPACE"][index]),
                         "text": label(m["SPACE"][index]), "width": 270}
        return [
            {"id": "K_SHIFT", "text": "*Shifted*" if index in (1, 3)
             else "*Shift*", "sp": 2 if index in (1, 3) else 1,
             "nextlayer": shift_target, "width": 115},
            {"id": "K_ALTGR", "text": "AltGr", "sp": 2 if index in (2, 3)
             else 1, "nextlayer": altgr_target, "width": 115},
            {"id": "K_NUMERALS", "text": "*123*", "sp": 1,
             "nextlayer": "numeric", "width": 100},
            space_key,
            letter(".", index),
            {"id": "K_BKSP", "text": "*BkSp*", "sp": 1, "width": 115},
            {"id": "K_ENTER", "text": "*Enter*", "sp": 1, "width": 115},
        ]

    layers = []
    for index, name in enumerate(layer_names):
        rows = [{"id": rownum + 1, "key": [letter(k, index) for k in row]}
                for rownum, row in enumerate(alpha_rows)]
        rows.append({"id": 4, "key": frame(index)})
        layers.append({"id": name, "row": rows})

    digits = []
    for key in "1234567890":
        digits.append({"id": direct(m[key][0]), "text": m[key][0],
                       "sk": [{"id": direct(m[key][2]), "text": m[key][2]}]})
    symbols = ["৳", "।", ".", ",", "?", "!", ":", ";", "-", "/", "(", ")"]
    numeric_rows = [
        {"id": 1, "key": digits},
        {"id": 2, "key": [{"id": direct(v), "text": v} for v in symbols]},
        {"id": 3, "key": [
            {"id": "K_NUMERALS", "text": "*abc*", "sp": 1,
             "nextlayer": "default", "width": 130},
            {"id": "K_SPACE", "text": "*Sp*", "width": 350},
            {"id": "K_BKSP", "text": "*BkSp*", "sp": 1, "width": 130},
            {"id": "K_ENTER", "text": "*Enter*", "sp": 1, "width": 130},
        ]},
    ]
    layers.append({"id": "numeric", "row": numeric_rows})
    return json.dumps({"phone": {"displayUnderlying": False,
                                  "layer": layers}}, ensure_ascii=False,
                      indent=2) + "\n"

def linux(m):
    # Single-key XCompose rules translate F13-F15 into Unicode strings on
    # Linux applications that use libxkbcommon or Xlib Compose processing.
    # This avoids a Keyman dependency, but individual toolkit support varies.
    special = {(k,i): v for k in ORDER for i,v in enumerate(m[k]) if v and len(v)>1}
    triggers = {slot: "F%d"%(13+n) for n,slot in enumerate(special)}
    s=["// Generated from layout/onnoy.json",
       'default partial alphanumeric_keys',
       'xkb_symbols "basic" {',
       '    include "us(basic)"',
       '    name[Group1] = "Bengali (Onnoy)";',
       '    include "level3(ralt_switch)"']
    for k in KEY_ORDER:
        vals=", ".join("VoidSymbol" if v is None else ("space" if v==" " else (triggers[(k,i)] if len(v)>1 else "U%04X"%ord(v))) for i,v in enumerate(m[k]))
        s.append('    key <%s> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ %s ] }; // %s'%(XKB[k],vals,k))
    return "\n".join(s+["};",""])

def linux_compose(m):
    """Single-keysym Compose sequences permit UTF-8 string output."""
    special = [(k,i,v) for k in ORDER for i,v in enumerate(m[k]) if v and len(v)>1]
    result = ['# Onnoy generated XCompose additions; include in ~/.XCompose',
              '# This file intentionally contains only Onnoy-specific rules.']
    for n,(k,i,value) in enumerate(special):
        result.append('<F%d> : "%s" # %s layer %d'%(13+n,value,k,i))
    return "\n".join(result)+"\n"

def utf16_units(value):
    raw = value.encode("utf-16-le")
    return [int.from_bytes(raw[i:i+2], "little") for i in range(0, len(raw), 2)]

def windows(m):
    s=['KBD\tonnoy\t"Onnoy"','',
       'COPYRIGHT "(c) 2026 Muhtasham Nawr al-Mahmud"',
       'COMPANY "Muhtasham Nawr al-Mahmud"','LOCALENAME "bn-BD"',
       'LOCALEID "00000845"','VERSION 1.0','',
       'SHIFTSTATE','0\t// Base','1\t// Shift','2\t// Ctrl',
       '6\t// AltGr','7\t// Shift+AltGr','',
       'LAYOUT','//SC VK_ Cap 0 1 2 6 7']
    code=lambda x: '-1' if x is None else ('%%' if len(utf16_units(x))>1 else '%04x'%ord(x))
    ligatures=[]
    for k in KEY_ORDER:
        vals=m[k]
        cols=" ".join(code(x) for x in (vals[0],vals[1]," " if k=="SPACE" else None,vals[2],vals[3]))
        vk={".": "OEM_PERIOD", "[": "OEM_4", "]": "OEM_6"}.get(k, k)
        s.append("%s\t%s\t0\t%s\t// %s"%(SCAN[k],vk,cols,k))
        for shift_index,value in enumerate((vals[0],vals[1],None,vals[2],vals[3])):
            if value is not None and len(utf16_units(value))>1:
                ligatures.append("%s\t%d\t%s"%(vk,shift_index," ".join("%04x"%unit for unit in utf16_units(value))))
    for scan,vk,mac,base,shift in PUNCT:
        s.append("%s\t%s\t0\t%s %s %s -1 -1"%(scan,vk,code(base),code(shift),"0020" if vk=="SPACE" else "-1"))
    if ligatures:
        s+=['','LIGATURE','//VK_ Mod# Char0 Char1 Char2 Char3']
        s+=ligatures
    s+=['','KEYNAME','01\tEsc','0e\tBackspace','0f\tTab','1c\tEnter',
        '1d\tCtrl','2a\tShift','36\t"Right Shift"','38\tAlt',
        '39\tSpace','3a\t"Caps Lock"','KEYNAME_EXT',
        '38\t"Right Alt"','1d\t"Right Ctrl"',
        'DESCRIPTIONS','0845\tBengali (Onnoy)',
        'LANGUAGENAMES','0845\tBangla (Bangladesh)','ENDKBD','']
    return "\r\n".join(s)

def macos(m):
    root=ET.Element("keyboard",{"group":"126","id":"-15231","name":"Onnoy","maxout":str(max(len(v) for values in m.values() for v in values if v is not None))})
    layouts=ET.SubElement(root,"layouts")
    ET.SubElement(layouts,"layout",{"first":"0","last":"17","modifiers":"OnnoyModifiers","mapSet":"OnnoyMap"})
    mods=ET.SubElement(root,"modifierMap",{"id":"OnnoyModifiers","defaultIndex":"0"})
    conditions=[["","caps"],["anyShift caps?"],["anyOption caps?"],["anyShift anyOption caps?"],
                ["command anyShift? caps? anyOption? anyControl?"],
                ["anyControl command? anyShift? caps? anyOption?"]]
    for i,names in enumerate(conditions):
        node=ET.SubElement(mods,"keyMapSelect",{"mapIndex":str(i)})
        for name in names: ET.SubElement(node,"modifier",{"keys":name})
    maps=ET.SubElement(root,"keyMapSet",{"id":"OnnoyMap"})
    for index in range(6):
        node=ET.SubElement(maps,"keyMap",{"index":str(index)})
        for k in KEY_ORDER:
            v=m[k][index] if index<4 else (" " if k=="SPACE" else (k.lower() if k.isalpha() else k))
            ET.SubElement(node,"key",{"code":str(MAC[k]),"output":v or ""})
        for scan,vk,code,base,shift in PUNCT:
            ET.SubElement(node,"key",{"code":str(code),"output":shift if index in (1,3) else base})
    ET.indent(root,space="  ")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">\n'
            +ET.tostring(root,encoding="unicode")+"\n")

def main():
    m=mapping()
    outputs={
      "source/onnoy.kmn":keyman(m),
      "source/onnoy.keyman-touch-layout":touch(m),
      "dist/linux/symbols/onnoy":linux(m),
      "dist/linux/Onnoy.XCompose":linux_compose(m),
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
