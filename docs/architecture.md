# Native-first design

## Mission

Onnoy is **one fixed Unicode Bengali keyboard layout implemented using each operating system's native keyboard APIs**. Its goal is cross-platform typing without installation of a third-party keyboard runtime.

### Canonical source

`layout/onnoy.json` contains only Onnoy-specific overrides. Unchanged US keys (including Space, Minus, Equals and Backtick) do not appear in the canonical mapping. The generator reads pinned platform-specific US source references from `layout/platform-bases/` rather than maintaining `US_BASE` or `US_SHIFT` Python tables. Linux XKB inherits `us(basic)` directly. macOS uses the native `.keylayout` `baseMapSet`/`baseIndex` mechanism between embedded keymaps. Windows patches a checked-in exported US MSKLC `.klc` and preserves its scan codes and Ctrl layer. `scripts/generate.py` emits:
- Linux: `dist/linux/symbols/onnoy` (XKB)
- macOS: `dist/macos/Onnoy.keylayout` (Apple input source)
- Windows: `dist/windows/onnoy.klc` (MSKLC source for a keyboard DLL)

The Linux generator rejects multi-codepoint mappings rather than silently promising support that XKB cannot provide. The current layout outputs one Unicode scalar per chord. Native apps handle Unicode text shaping and grapheme rendering; the layout does not synthesize ligatures or run a phonetic conversion engine.

### What is *not* a runtime dependency

Keyman, IBus, Fcitx, a browser extension, a background keyboard helper, and JavaScript are not needed for the OS-native desktop layouts.

The website includes an optional client-side **demonstration** that maps `KeyboardEvent.code` to Unicode in one textarea. It is not an input method or an OS-global keyboard; OS-level shortcuts may still override it.

### Packaging truth table

| Platform | Native layout? | User-installable file already verified? | Build requirement |
| --- | --- | --- | --- |
| Linux | Yes, XKB symbols | Not yet universal; desktop registration varies | Python 3 for generator, XKB environment |
| macOS | Yes, .keylayout | Unsigned .pkg generated on macOS; device test pending | Apple pkgbuild for package |
| Windows | Yes, native .klc *source* | **No**, DLL/installer build and device test pending | MSKLC on Windows |
| Browser | Demo only | Web page, no installation | No dependency beyond a browser |

### Release blockers

A release labeled “ready to install” must include reproducible installers and actual native typing tests on the target platforms. A compiled XML, KLC, or XKB file is not proof of a functioning system installation.

### Renaming the repository

The recommended GitHub repository name is **`onnoy`**, not `onnoy-keyman`. The name `onnoy-layout` is another neutral option. A repository rename requires GitHub administrative settings and should happen separately after updating Pages and links. GitHub may redirect repository URLs, but a GitHub Pages project URL generally requires deliberate reconfiguration and redirects.

Keep the branding `Onnoy (অন্বয়)` in platform descriptions. Remove vendor names from non-vendor build paths.
