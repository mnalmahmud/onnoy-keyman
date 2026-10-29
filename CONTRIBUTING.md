# Contributing to Onnoy

## Source-tree guide

| Path | Purpose |
| --- | --- |
| `layout/onnoy.json` | **Only source of key assignments** |
| `scripts/generate.py` | Generates Keyman source and native Linux, macOS and Windows layouts |
| `scripts/build.sh` | Reproducible generation checks and Keyman build |
| `source/onnoy.kps`, `source/welcome.htm` | Keyman distribution package source |
| `web/` | Browser playground |
| `tests/` | Layout, build-artifact and browser verification |
| `.github/workflows/build.yml` | CI builds, release assets and Pages deployment |

All `dist/`, `build/`, `site/`, and `source/onnoy.kmn` content is generated. Do not hand-edit generated layouts. The last file is generated even though it is under `source/`.

## Editing a key

Explain the old and proposed assignments, modifier layers, and any Unicode sequence changes. Edit `layout/onnoy.json` only, then run:

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
python3 -m unittest discover -s tests -p 'test_layout.py'
```

The generator handles single-code-point outputs and approved multi-code-point sequences. Native Linux uses generated XKB plus Compose rules; validate the actual keystrokes on the target desktop. Windows ligature entries need MSKLC compilation. Update tests and the changelog if you change behavior.

Bug reports should include OS, desktop/application, physical keys and modifiers, expected Unicode code points, actual code points, and whether the bug occurs in a native layout or KeymanWeb.

## Release checklist

- [ ] Run the generator's `--check` mode and all CI tests.
- [ ] Compile XKB with `xkbcomp` and test XKB+XCompose shortcuts in real Linux apps on X11 and Wayland.
- [ ] Validate macOS XML and test the installed native input source.
- [ ] Compile Windows `.klc` with MSKLC; test its ligature shortcuts and installer before publishing a native Windows download.
- [ ] Check physical typing, AltGr, all Unicode sequences, and the browser playground.
- [ ] Check downloadable CI artifacts, GitHub Pages, metadata, license and changelog.
- [ ] Only tag a release for platforms that have been verified. Do not call a `.klc` an installer.

License: [MIT](LICENSE).
