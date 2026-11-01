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
           "store(&layoutfile) 'onnoy.keyman-touch-layout'",
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

def package_source():
    """Generate a minimal installable Keyman package definition."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<Package>
  <System>
    <KeymanDeveloperVersion>18.0.254.0</KeymanDeveloperVersion>
    <FileVersion>7.0</FileVersion>
  </System>
  <Options>
    <FollowKeyboardVersion/>
  </Options>
  <StartMenu>
    <Folder></Folder>
    <Items/>
  </StartMenu>
  <Info>
    <Version URL=""></Version>
    <Name URL="">Onnoy</Name>
    <Copyright URL="">Onnoy contributors</Copyright>
    <Author URL="">Onnoy contributors</Author>
    <Description URL="">Fixed Unicode Bengali and Assamese keyboard, US-QWERTY positions.</Description>
  </Info>
  <Files>
    <File><Name>onnoy.kmx</Name><Description>Onnoy desktop keyboard</Description><CopyLocation>0</CopyLocation><FileType>.kmx</FileType></File>
    <File><Name>onnoy.js</Name><Description>Onnoy browser keyboard</Description><CopyLocation>0</CopyLocation><FileType>.js</FileType></File>
  </Files>
  <Keyboards>
    <Keyboard>
      <ID>onnoy</ID>
      <Languages><Language ID="bn">Bangla</Language><Language ID="as">Assamese</Language></Languages>
    </Keyboard>
  </Keyboards>
  <Strings/>
</Package>
"""
