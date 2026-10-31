# Changelog

## Unreleased

### Move avagraha to AltGr+H
- Move Bengali avagraha ঽ (U+09BD) from AltGr+A to AltGr+H; AltGr+A is now unassigned.
- Leave Base/Shift A and H unchanged and update the native layout and browser regression tests.

### Swap Shift+S and X outputs
- Shift+S now produces ষ and plain X produces শ; plain S remains স and Shift+X remains nukta (়).
- Update generated-platform layout assertions, reference typing examples and browser preview tests.

### Platform US base references instead of hard-coded defaults
- Replace the Python `US_BASE`/`US_SHIFT` tables with pinned exported native US reference files.
- Generate macOS `.keylayout` with `baseMapSet`/`baseIndex` for inherited keys, native Option punctuation, and Command/Control shortcut layers.
- Generate Windows `.klc` by patching the exported US MSKLC layout; preserve Ctrl key behavior, ISO key rows, and key labels.
- Leave `layout/onnoy.json` override-only and retain Linux `us(basic)` inheritance.


### Inherit ordinary US keyboard keys
- Remove unchanged Space, Minus, Backslash, Comma and Backtick from canonical Onnoy overrides.
- Linux XKB inherits them through `us(basic)`; macOS and Windows emit required native mappings from US default data in the generator.
- Browser preview and benchmark inherit defaults rather than copying them into Onnoy JSON.


### Group joiners on the apostrophe key
- Assign U+200D to AltGr+apostrophe and U+200C to Shift+AltGr+apostrophe.
- Restore the backtick and tilde key to normal punctuation without custom AltGr outputs.
- Keep Base apostrophe and Shift+apostrophe as ordinary quotes; no other layout changes.
- Update Linux XKB, Windows KLC and macOS keylayout generation checks, website smoke tests, documentation and typing examples.


### Unshifted virama and reserved joiner shortcuts
- Assign the physical slash key to virama (্), retaining question mark on Shift+/ and moving ASCII slash to AltGr+/.
- Remove the former Shift+F virama assignment entirely; Base F remains ফ.
- Move ZWJ and ZWNJ from AltGr+Z to AltGr+backtick and Shift+AltGr+backtick, preserving ordinary backtick and tilde.
- Keep Base Z=য, Shift+Z=ঙ; AltGr Z layers are unassigned.
- Extend all native platform generators and website keymap to support four-layer punctuation, update tests and documentation.


### Native-first redesign, independent of Keyman
- Treat Onnoy as an operating-system-native Bengali Unicode layout rather than a Keyman product.
- Remove Keyman project files, compiled packages, runtime and compiler requirements.
- Generate Linux XKB symbols, macOS .keylayout, and Windows .klc directly from the canonical layout.
- Replace KeymanWeb with an optional standalone JavaScript typing preview for the project website.
- Publish explicit native installation guides and platform-specific CI jobs. Windows DLL and installer builds still require MSKLC on Windows and real-device verification.
- Proposed public repository rename: `onnoy` (requires separate GitHub settings and Pages migration).


### Reposition independent অ and AU length mark
- Swap Shift+V and Shift+B: Shift+V now emits অ (U+0985), Shift+B emits ৗ (U+09D7).
- Retain unshifted V=ভ and B=ব, plus all other consonant and vowel assignments.
- Update Keyman/native/mobile generators through the canonical JSON, layout tests, browser tests, and documentation.


### Move joiners off Space
- Move ZWJ to AltGr+Z and ZWNJ to Shift+AltGr+Z; keep Z=য and Shift+Z=ঙ.
- Restore Space as ordinary space on every keyboard layer, avoiding OS-level Space shortcut conflicts.
- Mobile joiners are available via long-press Z, not Space.
- Bump compiled keyboard and package version to 1.1; native layouts, tests and documentation are regenerated.
- Platform-specific AltGr+Z collisions still require end-user verification.


### Restore Bengali Ra and consolidate Ri/virama/nukta
- Base R now emits Bengali র (U+09B0), and Shift+R emits Assamese ৰ (U+09F0); Assamese ৱ remains AltGr+W.
- Assign the dependent/independent Ri pair to physical equals: Base `=` → ৃ and Shift+`=` → ঋ, preserving ASCII `=`/`+` on the corresponding AltGr layers.
- Keep phonetic Base F = ফ, move virama to Shift+F; Base X = ষ, Shift+X = nukta, AltGr+X = 𑷰.
- Preserve V = ভ/ৗ and B = ব/অ, including the existing vowel and punctuation arrangements.
- Include the equals key in native generators and website keyboard; on touch, expose the Ri pair via long-press R.
- Restore direct standard-Unicode Bengali র, superseding the previous compatibility limitation.

### Direct NFC O/AU vowels
- Split O family: O = ো/ও and physical semicolon key = ৌ/ঔ. These emit U+09CB and U+09CC directly without a separate input method or Unicode normalization step.
- Move ASCII semicolon and colon to AltGr+; and Shift+AltGr+; respectively, retaining their physical location.
- Update the native Keyman/XKB/Windows/macOS generators, touch key rows, browser layout, tests and documentation.


### Proposed vowel and consonant redistribution
- Promote ী/ঈ to Y, ৈ/ঐ to [ and ূ/ঊ to ]; retain original brackets and braces on their respective AltGr layers.
- Move virama/nukta/𑷰 to Shift+X/X/AltGr+X, ফ to F, ষ to Shift+F, ঞ to Shift+P, য to Z, ঙ to Shift+Z, ং to Shift+L, ভ to V, অ to Shift+B, and ৗ to Shift+V.
- Drop direct ক্ষ, ্য, ড়, ঢ়, য়, ো, and ৌ shortcuts in favor of normal Unicode sequences.
- **Historical note, superseded by the restoration above:** this version temporarily removed direct Bengali র, which was not canonically replaceable with ব + nukta.
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
