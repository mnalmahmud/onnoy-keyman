"""US-QWERTY reference positions and platform-neutral key identifiers.
Hardware codes here are mechanics, not Onnoy character assignments.
"""
ALPHABET = tuple("QWERTYUIOPASDFGHJKLZXCVBNM")
DIGITS = tuple("1234567890")
SYMBOLS = ("GRAVE", "MINUS", "EQUAL", "LBRACKET", "RBRACKET",
           "BACKSLASH", "SEMICOLON", "APOSTROPHE", "COMMA", "PERIOD", "SLASH")
STANDARD = ALPHABET + DIGITS + SYMBOLS + ("SPACE",)
ISO_EXTRA = "ISO_EXTRA"
LAYERS = ("base", "shift", "altgr", "shift_altgr")

XKB = {}
for row, prefix in (("QWERTYUIOP", "AD"), ("ASDFGHJKL", "AC"),
                    ("ZXCVBNM", "AB"), ("1234567890", "AE")):
    XKB.update({key: f"{prefix}{i:02d}" for i, key in enumerate(row, 1)})
XKB.update(dict(zip(SYMBOLS, (
    "TLDE", "AE11", "AE12", "AD11", "AD12", "BKSL",
    "AC10", "AC11", "AB08", "AB09", "AB10"))))
XKB.update(SPACE="SPCE", ISO_EXTRA="LSGT")

WINDOWS = {}
for row, scans in (
    ("1234567890", "02 03 04 05 06 07 08 09 0A 0B"),
    ("QWERTYUIOP", "10 11 12 13 14 15 16 17 18 19"),
    ("ASDFGHJKL", "1E 1F 20 21 22 23 24 25 26"),
    ("ZXCVBNM", "2C 2D 2E 2F 30 31 32")):
    WINDOWS.update({key: (scan, key) for key, scan in zip(row, scans.split())})
WINDOWS.update(dict(zip(SYMBOLS, (
    ("29","OEM_3"), ("0C","OEM_MINUS"), ("0D","OEM_PLUS"),
    ("1A","OEM_4"), ("1B","OEM_6"), ("2B","OEM_5"),
    ("27","OEM_1"), ("28","OEM_7"), ("33","OEM_COMMA"),
    ("34","OEM_PERIOD"), ("35","OEM_2")))))
WINDOWS.update(SPACE=("39", "SPACE"), ISO_EXTRA=("56", "OEM_102"))

MAC = {}
for row, codes in (
    ("ASDFGHJKL", [0,1,2,3,5,4,38,40,37]),
    ("QWERTYUIOP", [12,13,14,15,17,16,32,34,31,35]),
    ("ZXCVBNM", [6,7,8,9,11,45,46]),
    ("1234567890", [18,19,20,21,23,22,26,28,25,29])):
    MAC.update(dict(zip(row, codes)))
MAC.update(dict(zip(SYMBOLS, (50,27,24,33,30,42,41,39,43,47,44))))
MAC.update(SPACE=49, ISO_EXTRA=10)

KEYMAN = {key: "K_" + key for key in ALPHABET + DIGITS}
KEYMAN.update(dict(zip(SYMBOLS, (
    "K_BKQUOTE", "K_HYPHEN", "K_EQUAL", "K_LBRKT", "K_RBRKT",
    "K_BKSLASH", "K_COLON", "K_QUOTE", "K_COMMA", "K_PERIOD",
    "K_SLASH"))))
KEYMAN.update(SPACE="K_SPACE", ISO_EXTRA="K_oE2")

BROWSER = {key: "Key" + key for key in ALPHABET}
BROWSER.update({key: "Digit" + key for key in DIGITS})
BROWSER.update(dict(zip(SYMBOLS, (
    "Backquote", "Minus", "Equal", "BracketLeft", "BracketRight",
    "Backslash", "Semicolon", "Quote", "Comma", "Period", "Slash"))))
BROWSER.update(SPACE="Space", ISO_EXTRA="IntlBackslash")
assert all(set(mapping)==set(STANDARD)|{ISO_EXTRA} for mapping in (XKB, WINDOWS, MAC, KEYMAN, BROWSER))
