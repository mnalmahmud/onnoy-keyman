# Changelog

## Unreleased

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
