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

## Mobile touch arrangement

Keyman Android/iOS uses a separate **generated** phone interface, not the
US-QWERTY desktop hardware representation. The touch placement code contains
only logical Onnoy key IDs and layer navigation. Bengali and Assamese output
scalars come entirely from `layout/onnoy.json` via the resolver.

- The default three alphabetic rows are QWERTYUIOP / ASDFGHJKL / ZXCVBNM.
- The shifted layer exposes the mapped Shift variants.
- Every alphabetic key has long-press alternatives from its nonempty mapping
  layers, including Assamese letters, nukta, ZWJ and ZWNJ.
- Vowel signs on LBRACKET/RBRACKET and the SEMICOLON mapping are also
  accessible through relevant vowel/consonant long-presses and the
  numeric/symbol layer.
- A dedicated virama key is always visible next to space.
- A numeric page exposes Bengali digits, punctuation, AltGr alternatives,
  ASCII digits, and currency/symbol variants by long-press.
- Backspace, Enter, Space, Shift and numeric-page switching are engine keys,
  not separately defined Unicode character overrides.
- Combining marks use dotted-circle labels for clarity; the dotted circle is
  **not** inserted into the text. ZWJ and ZWNJ have readable labels.

No context-sensitive rules, normalization, autocorrect, transliteration,
or alternative authoritative Unicode map is introduced by touch support.

## Release verification

Generated-source checks, native compilation, and real-device installation
tests are separate levels of evidence. Windows KLC is only source until a
verified keyboard DLL/installer is built. macOS unsigned packages are not
signed or notarized. Linux XKB symbol compilation does not imply automatic
Wayland desktop registration.
