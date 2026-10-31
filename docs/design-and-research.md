# Design and benchmark methodology

Onnoy is a fixed Unicode keyboard intended to address specific limitations of Probhat and KaGaPa. The canonical mapping is layout/onnoy.json.

## Why these key positions exist
- T gives ট/ঠ in English-sound-oriented grouping; F gives ত/থ. D now gives ড/ঢ, which is a closer articulatory match to English alveolar /d/ in Bangladeshi Standard Bengali than dental দ. Q gives দ/ধ as the displaced consonant pair. This is a phonetic-priority decision, not a Romanization convention; pronunciations vary by dialect. P gives প/ফ and B gives ব/ভ so everyday consonants avoid distant AltGr chords.
- Y gives ী/ঈ, O gives ো/ও, W gives ূ/ঊ, [ gives ৈ/ঐ, and ] gives ৌ/ঔ. Frequent dependent vowel signs remain on Base, with corresponding independent vowels on Shift.
- R holds র/ড়, with AltGr+R unassigned; X holds শ/ঢ়, a Shift+X placement also found in Probhat, Baishakhi, and Bornona. Z holds য on Base with Shift+Z unassigned. Y holds ী/ঈ/য় on Base/Shift/AltGr, combining an /i/-related vowel pair with the /j/-related glide on one physical key, with no duplicate য়. AltGr+Y is potentially a one-hand right-thumb/right-index chord on standard keyboards, pending real-device ergonomic validation. M gives ম/ঙ/ঁ and N gives ন/ণ/ঞ, with nasal extensions on the right-hand AltGr side.
- Semicolon gives ৃ/ঋ with literal punctuation on AltGr. Equals and plus inherit native US behavior. Comma preserves its base and Shift punctuation while AltGr+comma is nukta (়) and Shift+AltGr+comma is U+11DF0.
- The period key remains unchanged: danda on Base, greater-than on Shift, ASCII period on AltGr. This intentional placement has not been redesigned.
- Assamese ৱ remains AltGr+W. Assamese ৰ and avagraha ঽ were removed from direct key assignments.
- Direct encoded ড়, ঢ় and য় are included even though Unicode normalization may decompose their encodings. Direct precomposed ো and ৌ are retained because native applications do not reliably compose them from separate keystrokes.

## Virama research and experiments
Current base / is virama. Historical Shift+F is retained only as a benchmark scenario; it is **not** an alternative key in the active layout. AltGr+apostrophe and Shift+AltGr+apostrophe emit U+200D and U+200C. Base apostrophe and Shift+apostrophe preserve ASCII quotes; backtick and tilde return to ordinary punctuation with no special AltGr assignments. Test OS/application shortcut interception of apostrophe combinations on real devices. The generator remains native and does not use a context-sensitive input method.

Run the mechanical experiment using:
python3 scripts/benchmark.py --corpus path/to/licensed-bengali-corpus.txt

The script reads installed Linux XKB symbol definitions (Probhat and KaGaPa) from /usr/share/X11/xkb/symbols/in by default. Use --xkb to supply a different XKB revision. Reports show coverage, physical chords, modifier workload, and approximate same-finger, hand-alternation and travel measures. Normalization uses NFD when comparing output. The demo corpus is NOT representative. Do not compare scores across layouts with different coverage. Try multiple --shift-weight and --altgr-weight choices.

Research supports studying conjuncts carefully rather than assuming that all Bengali words contain one. Different genres have different cluster frequency. Corpus measurements should be published with source, license, size, genre breakdown and normalization. Do not infer actual typing speed from the model alone.

## Human study
Recruit novice and experienced Probhat, KaGaPa and Onnoy typists. Counterbalance layout order, offer practice, repeat sessions and use fixed hardware. Record words per minute, uncorrected/corrected errors, backspaces, modifier events, task time, and comfort/fatigue ratings. Include literary, news, casual and technical texts; keep a holdout corpus. No personal text should be recorded.

## Native verification
- Linux: real X11 and Wayland application tests for XKB, Compose and AltGr.
- Windows: compile KLC with MSKLC; test actual installed layout, Right Alt, Unicode output and supplementary codepoints.
- macOS: install keylayout; test Option and Command combinations, applications and codepoints.
- Keyman desktop/mobile: test genuine devices, touch layers, long-press, joins, backspace and output.
- Track platform, application, version, key sequence, actual vs expected Unicode and font support.

These are verification protocols, not claims that platform or human testing has happened.
