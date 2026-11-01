"""Plain-US character fallback for *symbol and digit* positions.

This tiny reference is not a copied platform keyboard, and is never edited to
accommodate Onnoy changes. AltGr symbol fallbacks are deliberately empty.
"""
from .hardware import DIGITS, SYMBOLS

PAIRS = {
    "GRAVE": ("`", "~"), "MINUS": ("-", "_"), "EQUAL": ("=", "+"),
    "LBRACKET": ("[", "{"), "RBRACKET": ("]", "}"),
    "BACKSLASH": ("\\", "|"), "SEMICOLON": (";", ":"),
    "APOSTROPHE": ("'", '"'), "COMMA": (",", "<"),
    "PERIOD": (".", ">"), "SLASH": ("/", "?"),
    "ISO_EXTRA": ("\\", "|")
}
SHIFT_DIGITS = ")!@#$%^&*("
for digit in DIGITS:
    PAIRS[digit] = (digit, SHIFT_DIGITS[int(digit)])

def ordinary_ascii(key, shifted=False):
    if len(key) == 1 and key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return key if shifted else key.lower()
    if key == "SPACE":
        return " "
    return PAIRS[key][int(shifted)]

assert set(SYMBOLS) <= set(PAIRS)
