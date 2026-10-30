# Changelog

## Unreleased

### Direct NFC O/AU vowels
- Split O family: O = ো/ও and physical semicolon key = ৌ/ঔ. These emit U+09CB and U+09CC directly without a separate input method or Unicode normalization step.
- Move ASCII semicolon and colon to AltGr+; and Shift+AltGr+; respectively, retaining their physical location.
- Update the native Keyman/XKB/Windows/macOS generators, touch key rows, browser layout, tests and documentation.


### Proposed vowel and consonant redistribution
- Promote ী/ঈ to Y, ৈ/ঐ to [ and ূ/ঊ to ]; retain original brackets and braces on their respective AltGr layers.
- Move virama/nukta/𑷰 to Shift+X/X/AltGr+X, ফ to F, ষ to Shift+F, ঞ to Shift+P, য to Z, ঙ to Shift+Z, ং to Shift+L, ভ to V, অ to Shift+B, and ৗ to Shift+V.
- Drop direct ক্ষ, ্য, ড়, ঢ়, য়, ো, and ৌ shortcuts in favor of normal Unicode sequences.
- **Compatibility warning:** direct Bengali র is deliberately removed without an equivalent Unicode decomposition or a custom conversion rule. The layout cannot type U+09B0 at present; Assamese ৰ and ৱ remain distinct and available.
- Update web keymap, touch keyboard, tests, and documentation; bracket and brace symbols move to AltGr layers.


### Unicode 18 character
- Assign AltGr+F to U+11DF0 Bengali Combining Anusvara Above.
- Generate UTF-16 surrogate pairs for supplementary Unicode characters in native Windows KLC ligatures.


### Multilingual AU length mark
- Move ৗ (`U+09D7`) from AltGr+V to Shift+V, retaining Base V = অ.
- Leave AltGr+V unassigned; keep the rest of the Assamese Wa relocation unchanged.


### Assamese Wa placement
- Move Assamese ৱ (`U+09F1`) from Shift+V to AltGr+W.
- Leave Shift+V unassigned; retain V = অ, AltGr+V = ৗ and W = ট, Shift+W = ঠ.


### Joiner shortcuts
- Move ZWJ to AltGr+Space and ZWNJ to Shift+AltGr+Space across Keyman, native layouts, and mobile touch.
- Leave AltGr+Z and Shift+AltGr+Z unassigned, preserving normal Space and Shift+Space.


### Design D
- Swap Y Base/Shift: Y = য়, Shift+Y = য, while keeping AltGr+Y = ্য and Shift+AltGr+Y unassigned.
- Keep the change consistent across generated Keyman, native layouts and mobile touch layers.

### Design C and packaging
- Apply Design C: Z = ং, Shift+Z = ঙ, Shift+M = ঁ, AltGr+N = ঞ, AltGr+M unassigned.
- Correct the web playground's বাংলা example to B · A · Z · L · A.
- Generate a mobile Keyman touch layout (four alphabetic layers, long-press alternatives and numeric layer).
- Provide OS-specific native packaging scripts for Linux, macOS, and Windows (MSKLC required).


### Keyboard layout
- Swap Z Base/Shift: Z = ঙ, Shift+Z = ঞ.
- Put ZWJ (`U+200D`) on AltGr+Z and ZWNJ (`U+200C`) on Shift+AltGr+Z.
- Swap entire Q/W families: Q = ড/ঢ/ড়/ঢ়, W = ট/ঠ.
- Add Shift+X = ক্ষ and AltGr+Y = য-ফলা with explicit Unicode sequences.
- Remove AltGr+G = জ্ঞ; leave AltGr+G unassigned while researching an অ্যা shortcut.
- Keep R = র/ৃ/ঋ/ৰ unchanged.

### Platform support
- Generate one shared mapping for Keyman, Linux XKB/XCompose, macOS `.keylayout`, and Windows MSKLC `.klc`.
- Generate native Linux Compose rules for multi-code-point shortcuts without requiring Keyman.
- Generate Windows ligature entries; native Windows compilation and installation are still unverified.

### Maintenance
- Restore interactive browser playground and add responsive styling.
- Add layout, compiled-artifact and browser tests; fix generated Windows tab delimiters.
- Consolidate verification and release documentation, removing unused project scaffolding.
