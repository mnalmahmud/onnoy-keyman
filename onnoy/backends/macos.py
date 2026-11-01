"""Build self-contained native macOS .keylayout, including shortcut maps."""
import xml.etree.ElementTree as ET
from ..hardware import MAC, STANDARD, ISO_EXTRA
from ..reference import ordinary_ascii

def render(mapping):
    root = ET.Element("keyboard", {
        "group": "126", "id": "-15231", "name": "Onnoy", "maxout": "2"})
    layouts=ET.SubElement(root,"layouts")
    ET.SubElement(layouts,"layout",{"first":"0","last":"17","modifiers":"OnnoyModifiers","mapSet":"OnnoyMap"})
    mods=ET.SubElement(root,"modifierMap",{"id":"OnnoyModifiers","defaultIndex":"0"})
    selectors = [
        [""],["anyShift"],["anyOption"],["anyShift anyOption"],
        ["command anyShift? anyOption? anyControl?"],
        ["anyControl command? anyShift? anyOption?"],
    ]
    for idx, options in enumerate(selectors):
        entry=ET.SubElement(mods,"keyMapSelect",{"mapIndex":str(idx)})
        for option in options:
            ET.SubElement(entry,"modifier",{"keys":option+" caps?" if option else "caps?"})
    maps=ET.SubElement(root,"keyMapSet",{"id":"OnnoyMap"})
    # The shortcut maps deliberately emit plain ASCII on Command/Control keys,
    # leaving native application shortcuts available instead of typing Bengali.
    for layer in range(6):
        element=ET.SubElement(maps,"keyMap",{"index":str(layer)})
        for key in STANDARD+(ISO_EXTRA,):
            if key==ISO_EXTRA and key not in mapping:
                continue
            if layer>=4:
                value=ordinary_ascii(key)
            else:
                value=mapping.get(key,(None,)*4)[layer]
            attrs={"code":str(MAC[key]),"output":value or ""}
            ET.SubElement(element,"key",attrs)
    ET.indent(root,space="  ")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">\n'
            +ET.tostring(root,encoding="unicode")+"\n")
