# Onnoy (অন্বয়)

Onnoy is a fixed, Unicode keyboard layout for Bengali script. The character mapping is stored in [`layout/onnoy.json`](layout/onnoy.json). Native desktop layouts and the KeymanWeb keyboard are generated from that same file.

[Try typing online](https://mnalmahmud.github.io/onnoy-keyman/) · [Source mapping](layout/onnoy.json) · [CI builds](https://github.com/mnalmahmud/onnoy-keyman/actions)

## Install

**Linux (XKB):** Copy the generated `dist/linux/symbols/onnoy` to your user or system XKB symbols directory, and configure the `onnoy(basic)` variant using your desktop's XKB integration. Desktop settings menus may require a separate layout registration. Installing system-wide XKB files requires appropriate permissions.

**macOS:** Copy `dist/macos/Onnoy.keylayout` to `~/Library/Keyboard Layouts/`, log out and back in if it does not appear, then enable Onnoy in **System Settings → Keyboard → Input Sources**. This is a native layout; Keyman is not required.

**Windows:** `dist/windows/onnoy.klc` is source for Microsoft Keyboard Layout Creator (MSKLC), **not** an installer. It must be compiled into a Windows keyboard DLL and installer before general Windows deployment. The Windows installer is **not yet available**. Don't treat the `.klc` as a downloadable, ready-to-install keyboard.

**Web:** The [GitHub Pages test](https://mnalmahmud.github.io/onnoy-keyman/) uses KeymanWeb with the compiled `onnoy.js` keyboard. Keyman is needed for the browser implementation only, not for native macOS and Linux layouts.

### Keyboard behavior

The 26 letters use their physical US-QWERTY positions and four layers: Base, Shift, AltGr, AltGr+Shift. Use the [canonical layout definition](layout/onnoy.json) for all assignments. Q carries ড/ঢ/ড়/ঢ় and W carries ট/ঠ, keeping each consonant family together while placing the more frequent ট/ঠ on W. In particular, the vowel groups are E (ে এ ৈ ঐ), I (ি ই ী ঈ), U (ু উ ূ ঊ) and O (ো ও ৌ ঔ). F produces virama (্); Shift+F produces nukta (়). The number row yields Bengali digits; AltGr gives ASCII digits. Shift+4 gives ৳ and AltGr+Shift+4 gives $. The period key yields । (base), > (Shift), and . (AltGr).

On macOS, **Option** corresponds to the third layer; on Linux and Windows, **Right Alt (AltGr)** usually supplies it. Some host shortcuts and modifier handling differ by OS.

## Build and test

Requirements: Python 3. The KeymanWeb build additionally needs Node.js and Keyman Developer CLI 18.

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
npm install -g @keymanapp/kmc@18
bash scripts/build.sh
python3 scripts/verify_build.py
```

The generator writes:
- `dist/linux/symbols/onnoy` — Linux XKB
- `dist/macos/Onnoy.keylayout` — macOS native XML keyboard
- `dist/windows/onnoy.klc` — Windows native layout source, needs MSKLC compilation
- `source/onnoy.kmn` — Keyman source for the web keyboard

CI compiles the XKB layout, checks the macOS XML, and compiles the Keyman keyboard. Windows native DLL building is not implemented in CI yet. No Windows binary should be advertised until that work is completed and verified.

## Development

Edit **only** `layout/onnoy.json` when changing key assignments, then run the generator and update tests/documentation. Do not make independent edits to platform layouts. Keep OS-specific packaging separate from the shared mapping.

## License

MIT. Copyright © 2026 Muhtasham Nawr al-Mahmud. See [LICENSE](LICENSE).
