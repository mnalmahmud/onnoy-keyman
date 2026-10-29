#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile, is_zipfile
root=Path(__file__).resolve().parents[1]
for name in ('onnoy.kmp','onnoy.kmx','onnoy.js'):
 p=root/'build'/name
 assert p.exists() and p.stat().st_size>100, f'Missing {name}'
assert is_zipfile(root/'build/onnoy.kmp')
with ZipFile(root/'build/onnoy.kmp') as z:
 assert any(p.lower().endswith('onnoy.kmx') for p in z.namelist())
assert 'onnoy.js' in (root/'.github/workflows/build.yml').read_text()
print('Compiled outputs verified')
