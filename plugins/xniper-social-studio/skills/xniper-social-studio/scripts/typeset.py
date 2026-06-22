#!/usr/bin/env python3
"""
Xniper Social Studio — typeset: turn raw copy into typographically-correct text.

Straight quotes, hyphens-as-dashes and three-dots are the small tells that make
type look amateur. This fixes them: curly quotes, real apostrophes, en/em dashes,
a true ellipsis, and (optionally) a no-break space before the last word so
headlines never end on a one-word widow line.

Pure standard library. Reads --text or stdin; prints the fixed string.

Examples
--------
  python typeset.py --text "\"Don't\" wait -- play now... it's free"
  echo "10 tips - swipe to see them all" | python typeset.py --nbsp
  python typeset.py --text "Beat 50 levels" --nbsp     # widow-proof a headline
"""
import argparse
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NBSP = " "


def smart_quotes(s):
    # apostrophes inside words: it's, don't, '90s
    s = re.sub(r"(\w)'(\w)", "’".join(("\\1", "\\2")), s)
    s = re.sub(r"'(\d0s)", "’\\1", s)            # '90s
    # opening vs closing singles
    s = re.sub(r"(^|[\s(\[{<—–\"])'", "\\1‘", s)
    s = s.replace("'", "’")
    # opening vs closing doubles
    s = re.sub(r'(^|[\s(\[{<—–])"', "\\1“", s)
    s = s.replace('"', "”")
    return s


def dashes(s):
    s = re.sub(r"(\d)\s*-\s*(\d)", "\\1–\\2", s)   # 10–20 en dash for ranges
    s = s.replace(" -- ", " — ")          # spaced em dash
    s = re.sub(r"\s--\s?|\s?--\s", " — ", s)
    s = re.sub(r"(\w)\s-\s(\w)", "\\1 — \\2", s)  # word - word → em
    return s


def ellipsis(s):
    return re.sub(r"\.\.\.+", "…", s)


def widow_guard(s):
    """Bind the last two words of each line with a no-break space."""
    out = []
    for line in s.split("\n"):
        parts = line.rstrip().split(" ")
        if len(parts) >= 2:
            line = " ".join(parts[:-1]) + NBSP + parts[-1]
        out.append(line)
    return "\n".join(out)


def typeset(s, nbsp=False):
    s = smart_quotes(s)
    s = dashes(s)
    s = ellipsis(s)
    s = re.sub(r"[ \t]{2,}", " ", s)            # collapse runs of spaces
    if nbsp:
        s = widow_guard(s)
    return s


def main():
    ap = argparse.ArgumentParser(description="Fix copy typography (curly quotes, dashes, ellipsis, widows)")
    ap.add_argument("--text", help="text to fix (else reads stdin)")
    ap.add_argument("--nbsp", action="store_true", help="bind last two words per line to prevent widows")
    args = ap.parse_args()
    src = args.text if args.text is not None else sys.stdin.read()
    sys.stdout.write(typeset(src.rstrip("\n"), args.nbsp))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
