# Vowel-placement research (experimental)

## What we are investigating

Onnoy's E/I/U/O families currently group dependent vowel signs and independent vowels on the same key, with several assigned to AltGr or Shift+AltGr. User feedback questions the accessibility and learnability of these shortcuts. We are free to separate families but aim for local repairs rather than redesigning the entire mapping. Use A–Z wherever possible and preserve everyday punctuation and digits.

| Key | Base | Shift | AltGr | Shift+AltGr |
|---|---|---|---|---|
| E | ে | এ | ৈ | ঐ |
| I | ি | ই | ী | ঈ |
| U | ু | উ | ূ | ঊ |
| O | ো | ও | ৌ | ঔ |

51 of 52 Base/Shift alphabetic positions are already occupied. Promoting several AltGr outputs means demoting other characters, so every proposal must enumerate and score its displacements. A good fix must not silently make virama, conjuncts, common consonants or Assamese orthography harder.

Compare with [Probhāt](https://www.mediawiki.org/wiki/Help:Extension:UniversalLanguageSelector/Input_methods/bn-probhat), which places some vowel families across keys rather than using four layers of one key. This is a design reference, not a prescription.

## Corpus candidates, NOT measured data

- Bengali and Assamese: [IndicCorp](https://indicnlp.ai4bharat.org/corpora/) and [IndicCorp v2](https://huggingface.co/datasets/ai4bharat/IndicCorpV2) (language-script configurations ben_Beng and asm_Beng). Inspect releases, licensing, text provenance and genres before use; web/news text alone is not balanced.
- Bengali: [Bangla NLP Corpus](https://huggingface.co/datasets/irfanhossainsust/bangla-nlp-corpus). Audit its source mix and deduplication.
- Bishnupriya Manipuri: source explicitly labeled Bengali-script Bishnupriya text and seek native-speaker review. Do not use Meitei corpora as substitutes.
- Bengali-script Kokborok: consult authorized Bengali-script primers, e.g. [Tripura primer catalog](https://adivaani.tribal.gov.in/resources/primers/tripura-primers). Do not count Latin-script text or unchecked OCR as Bengali-script writing.

No audited language corpora have been analyzed yet. Earlier ad hoc samples are NOT evidence for the key mapping.

## Repeatable evaluation

Obtain licensed UTF-8 text, one document or sentence per line, then run:

    python3 scripts/evaluate_vowels.py --corpus bn=/data/bn.txt.gz --corpus as=/data/as.txt.xz --output build/vowels.json

Compare a separate experimental layout without changing the canonical mapping:

    python3 scripts/evaluate_vowels.py --candidate /tmp/candidate.json --corpus bn=/data/bn.txt.gz --corpus as=/data/as.txt.xz --output build/comparison.json

The evaluator handles plain text, gzip, bz2, xz and JSONL with the --jsonl-field option; NFD normalization handles Unicode-equivalent spellings. It reports mapped events by layer, per-vowel counts and unmapped characters separately per language. It is a modifier-use *proxy*, not a human ergonomics or typing-speed measurement.

Record corpus version, license, source genres, sampling protocol and script validity. Do not combine language counts into a global weighted statistic without explicit rationale. Use a representative sample and ensure no leakage between tuning and evaluation.

## Decision checklist

- Fix vowel accessibility locally without forced grouping.
- Identify every character moved or demoted and its potential frequency/ergonomic penalty by language.
- Retain essential Bengali, Assamese, Kokborok and Bishnupriya orthographic coverage.
- Evaluate actual words with conjuncts, combining signs and independent vowels.
- Test key discoverability, reliability and comfort with new users and experienced Probhāt/Onnoy typists.
- Keep live main mapping unchanged until validated evidence supports a specific change.

**Status:** corpus discovery and evaluation tooling only; no alternative mapping approved yet.
