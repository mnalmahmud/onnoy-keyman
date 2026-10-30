# Contributing to Onnoy

Onnoy is a native cross-platform Bengali keyboard layout. No external runtime is needed once a platform-native layout is installed.

## Canonical files

- `layout/onnoy.json`: single source of key assignments
- `scripts/generate.py`: native Linux, macOS and Windows emitters
- `scripts/build.sh`: generation and regression tests
- `scripts/package-*.sh` and `.ps1`: platform packaging workflows
- `tests/`: codepoint and artifact regression checks
- `web/`: optional browser-only illustration; not a system input engine

All `dist/`, `site/` and `build/` files are generated; do not hand-edit them.

## Local check

```sh
bash scripts/build.sh
python3 scripts/benchmark.py --corpus tests/data/demo-bengali.txt
```

Make changes only in `layout/onnoy.json`, then update tests, rationale and changelog. Source verification is not a replacement for real-device testing.

## Native release checklist

- Linux: XKB compiles; test X11, GNOME Wayland, KDE Wayland, app shortcuts, installation and removal.
- macOS: build package on macOS; test .keylayout, Option, input source registration, signing and Gatekeeper.
- Windows: compile .klc with MSKLC; test native installer, Unicode scalar output, AltGr/Ctrl+Alt, and remove/upgrade.
- Verify Bengali shaping, NFC/NFD, and ZWJ/ZWNJ across several editors.
- Publish real package hashes and clearly state if any platform is source-only.

Bug reports should include platform, physical keyboard, actual keys, expected versus actual Unicode code points, and software/application version.
