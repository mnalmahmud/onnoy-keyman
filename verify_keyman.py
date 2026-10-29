#!/usr/bin/env python3
from pathlib import Path
import re
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
src=(root/'source/onnoy.kmn').read_text(encoding='utf-8')
pattern=re.compile(r'^\+ \[(?:(SHIFT) )?(?:(RALT) )?K_([A-Z0-9]+)\] > (nul|U\+[0-9A-F]{4,6})$',re.M)
found={}
for shift,ralt,key,result in pattern.findall(src):
  token=(key, int(bool(shift))+2*int(bool(ralt)))
  assert token not in found, f'duplicate key {token}'
  found[token]=result
assert len(found)==144, f'Expected 144 alphabet+digit rules, got {len(found)}'
for key,level,value in [('V',0,'U+0985'),('V',1,'U+09F1'),('F',0,'U+09CD'),('F',1,'U+09BC'),('R',2,'U+098B'),('R',3,'U+09F0'),('X',0,'U+09B7'),('W',2,'U+09DC'),('W',3,'U+09DD'),('I',1,'U+0987')]:
  assert found[key,level]==value, (key,level)
for key,level,value in [('PERIOD',0,'U+0964'),('PERIOD',2,'U+002E')]:
  assert re.search(r'^\+ \['+('RALT ' if level==2 else '')+r'K_'+key+r'\] > '+value+r'$',src,re.M),key
ET.parse(root/'source/onnoy.kps')
print('Onnoy Keyman source checks passed.')
