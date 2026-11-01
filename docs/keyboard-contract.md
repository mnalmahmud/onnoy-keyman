# Onnoy keyboard contract

Onnoy is a fixed, positional US-QWERTY-based Bengali/Assamese keyboard.
ANSI and ISO hardware share the same Bengali assignments. AZERTY and QWERTZ
profiles are out of scope. Native XKB, Windows KLC/DLL, macOS .keylayout, and
Keyman are independent delivery mechanisms for the same layout.

## Canonical source and resolution

`layout/onnoy.json` contains **only intentional Unicode overrides**, keyed by
short logical names and `base`, `shift`, `altgr`, `shift_altgr` fields.
No `null` values and no separate passthrough map. Missing alphabetic levels
produce no text. Missing digit/punctuation levels inherit the plain-US
reference Base/Shift outputs; unspecified higher levels emit no text. Space
is U+0020 on every character layer. Control and navigation keys are outside
the character map.

The reference is a fixed US-QWERTY *output convention*, not the user's current
national layout or a platform-default Option/dead-key action. In particular,
macOS Option symbols are **not** automatically inherited. All resolved levels
are explicit before passing to a backend.

## Input semantics

- Emit the **exact Unicode scalar** designated by the mapping, with no
  transliteration, normalization, implicit composition, or dead keys.
- ZWJ U+200D and ZWNJ U+200C are distinct invisible characters.
- Duplicate U+09DF on Shift+Z and AltGr+Y is intentional.
- Caps Lock does not change selected Bengali Base/Shift symbols.
- Ctrl and Command shortcuts are retained through native platform handling.
  Right Alt / AltGr may conflict with application-defined shortcuts; verify
  actual applications rather than promising universal interception.
- A missing ISO extra key on ANSI does not affect the shared character map.
  On ISO, ISO_EXTRA produces backslash / vertical bar on Base / Shift.
- On macOS ISO, test and account for the physical code 10/50 distinction
  between the extra position and the grave position (virama).

## Release verification

Generated-source checks, native compilation, and real-device installation
tests are separate levels of evidence. Windows KLC is only source until a
verified keyboard DLL/installer is built. macOS unsigned packages are not
signed or notarized. Linux XKB symbol compilation does not imply automatic
Wayland desktop registration.
