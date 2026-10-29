# Changelog

## Unreleased

- Add approved conjunct shortcuts: Shift+X = ক্ষ, AltGr+G = জ্ঞ, AltGr+Y = য-ফলা.
- Add native Linux XKB + XCompose generation for multi-codepoint strings; other platform generators gain string support.
- Swap the complete Q and W families: Q = ড/ঢ/ড়/ঢ়, W = ট/ঠ (AltGr positions on W remain unassigned).

- Defined `layout/onnoy.json` as the authoritative keyboard mapping.
- Added generation of Linux XKB symbols, macOS `.keylayout`, Windows `.klc` source and Keyman `.kmn` source.
- Kept KeymanWeb as the browser test implementation.
- Added native-source checks to CI. Windows DLL and installer builds remain outstanding.
