# Onnoy architectural migration

The canonical source is `layout/onnoy.json`, a sparse key-centric JSON map.
`onnoy.model.resolve()` applies the plain-US reference and produces explicit
four-layer outputs for ANSI or ISO. Generated data goes to `dist/` and must
never be hand-edited.

The active generators no longer read `layout/platform-bases/`. Historical
copies of Windows and macOS US layouts may be retained temporarily for
comparison, but are not active inputs. Run `python3 scripts/build.py validate`,
`generate`, `check`, then `test` to exercise the core contract.

Each backend has its own responsibility:
- `onnoy/backends/linux.py`: native XKB keys and LevelThree behavior.
- `onnoy/backends/windows.py`: scan/VK, Ctrl layer and UTF-16/KLC.
- `onnoy/backends/macos.py`: XML keyMaps, Option layers and Command/Ctrl maps.
- `onnoy/backends/keyman.py`: positional Keyman rules and unused-level suppression.
- `onnoy/backends/web.py`: visualizer data; typing uses compiled KeymanWeb.

Native packaging and installation remain separate verification gates. Native
Windows DLL installation is not automated yet. macOS ISO keycode behavior
requires real ANSI/ISO hardware verification. XKB compilation alone does not
imply correct X11/Wayland desktop registration.

The website requires an externally loaded KeymanWeb engine. The GitHub Pages
build must stage a compiled `onnoy.js` alongside generated `layout.json`.

## Keyman mobile

`onnoy/backends/touch.py` produces `dist/keyman/onnoy.keyman-touch-layout`
from the same resolved Unicode outputs. The `&layoutfile` KMN store embeds it
in the compiled JS keyboard; the installable `.kmp` includes the JS and
`.kmx`. No duplicate mobile character JSON is edited by hand.
Touch-layout coverage checks are in `tests/test_touch.py`; physical Android/iOS
installation and usability tests remain separate release gates.
