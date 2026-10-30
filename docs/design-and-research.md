# Design and benchmark methodology

Onnoy is a fixed Unicode keyboard intended to address specific limitations of Probhat and KaGaPa. The canonical mapping is layout/onnoy.json.

## Why these key positions exist
- F emits ফ; Shift+F is intentionally unassigned. The physical slash key emits virama (্) unshifted, following Probhat; AltGr+/ restores literal /. This reduces modifier use in conjuncts at the cost of easy slash punctuation.
- Y emits ী; O emits ো; [ emits ৈ; ] emits ূ; ; emits ৌ. Frequent dependent vowel signs avoid modifiers, trading off vowel-family regularity and ASCII punctuation.
- Assamese letters and Bengali Unicode decompositions are intentional. Bengali র is direct. O and ; emit precomposed NFC signs.

## Virama research and experiments
Current base / is virama. Historical Shift+F is retained only as a benchmark scenario; it is **not** an alternative key in the active layout. AltGr+` and Shift+AltGr+` emit ZWJ and ZWNJ; base ` and Shift+` preserve ASCII backtick and tilde. Test OS/application shortcut interception for the new combinations. The generator remains native and does not use a context-sensitive input method.

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
