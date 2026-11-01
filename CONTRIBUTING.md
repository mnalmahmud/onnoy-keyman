# Contributing to Onnoy

The keyboard layout is defined once in `layout/onnoy.json`.
It is a sparse map of key IDs to named modifier outputs.
**Do not** put Bengali character assignments into platform backends,
reference punctuation tables, website scripts, or generated output files.

## Developer checks

```bash
python3 scripts/build.py validate
python3 scripts/build.py generate
python3 scripts/build.py check
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/benchmark.py --corpus tests/data/demo-bengali.txt
```

For Keyman compilation, additionally run `npm install` and
`npm run build:keyman`. The website depends on compiled KeymanWeb keyboard
assets. Native keyboard users do not need Node.js or Keyman.

## Release testing

- Linux: XKB compilation, real X11/Wayland registration, keyboard selection
  and uninstallation; verify ISO <LSGT> backslash/pipe.
- macOS: real `.keylayout` and package installation, Command/Control shortcuts,
  Right Option, ANSI and ISO code 10/50 behavior.
- Windows: compile KLC with MSKLC into native DLL/setup, validate Ctrl/AltGr
  shortcuts, supplementary Unicode, installation and removal.
- Keyman: compiler and package validation, physical keyboard typing and web
  integration across browsers.

Report precise key chords, Unicode code points, operating-system and
keyboard type for bugs. GitHub Actions source generation and compiler checks
are **not** substitutes for real-device testing.

## Mobile checks

The mobile touch layout is generated in `onnoy/backends/touch.py` from the
resolved canonical characters, never edited as a separate keyboard map.
`tests/test_touch.py` checks its complete Unicode coverage, and
`tests/check_mobile_package.py` checks the compiled KMP archive for the
mobile keyboard and Keyman metadata. Physical Android/iOS tests are required
before claiming full mobile-device compatibility.
