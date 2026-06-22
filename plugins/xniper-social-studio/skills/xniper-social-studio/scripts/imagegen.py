#!/usr/bin/env python3
"""
Xniper Social Studio — AI background / hero image generation (Gemini).

OPTIONAL. The skill works fully without it (CSS + textures + stock). When the
user wants real generated imagery (hero shots, painterly backgrounds, textures,
product scenes), this script calls Gemini's image model.

Key handling (the skill auto-configures — the user never edits env vars):
  1. env  GEMINI_API_KEY            (checked first)
  2. file ~/.config/xniper-social-studio/gemini.key   (gitignored, local only)
The skill OFFERS image-gen; if the user wants it, they paste their key once and
the skill saves it with `--save-key`. No key → this script exits cleanly and the
caller falls back to CSS/textures/stock.

Get a key: https://aistudio.google.com/apikey   (revocable anytime)

Examples
--------
  python imagegen.py --save-key AIza...                 # store the key once
  python imagegen.py --check                             # is a key + SDK present?
  python imagegen.py "soft dark navy gradient mesh, grain, abstract, premium" \
        --ar 4:5 --out out/bg.png
"""
import argparse
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KEY_FILE = Path.home() / ".config" / "xniper-social-studio" / "gemini.key"
# Image-capable Gemini models, tried in order (first that works wins).
MODELS = ["gemini-2.5-flash-image", "gemini-2.0-flash-preview-image-generation"]


def resolve_key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k and k.strip():
        return k.strip()
    if KEY_FILE.exists():
        v = KEY_FILE.read_text(encoding="utf-8").strip()
        if v:
            return v
    return None


def save_key(key):
    key = key.strip()
    if not key:
        print("ERROR: empty key.", file=sys.stderr)
        return 1
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(key, encoding="utf-8")
    try:
        os.chmod(KEY_FILE, 0o600)  # best effort; no-op semantics on Windows
    except Exception:
        pass
    print(f"OK  key saved to {KEY_FILE}")
    print("    (local + gitignored — never committed. Revoke anytime at "
          "https://aistudio.google.com/apikey)")
    return 0


def have_sdk():
    try:
        import google.genai  # noqa
        return True
    except ImportError:
        return False


def do_check():
    sdk = have_sdk()
    key = resolve_key()
    src = ("env" if (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
           else ("file" if key else "none"))
    print(f"SDK (google-genai): {'present' if sdk else 'MISSING — pip install google-genai'}")
    print(f"API key: {'present (' + src + ')' if key else 'none — run --save-key, or skip image-gen'}")
    return 0 if (sdk and key) else 1


def generate(prompt, ar, out):
    if not have_sdk():
        print("IMAGEGEN-UNAVAILABLE: google-genai not installed. "
              "Run: pip install google-genai  — or skip and use CSS/textures.", file=sys.stderr)
        return 2
    key = resolve_key()
    if not key:
        print("IMAGEGEN-UNAVAILABLE: no API key. Run --save-key <KEY> once, "
              "or skip image-gen and fall back to CSS/textures/stock.", file=sys.stderr)
        return 2

    from google import genai
    from google.genai import types  # noqa
    client = genai.Client(api_key=key)

    full = prompt.strip()
    if ar:
        full += (f". Aspect ratio {ar}, composed for a {ar} social canvas. "
                 "No text, no watermark, no logos.")
    else:
        full += ". No text, no watermark, no logos."

    last_err = None
    for model in MODELS:
        try:
            resp = client.models.generate_content(model=model, contents=full)
        except Exception as e:
            last_err = e
            continue
        img_bytes = _extract_image(resp)
        if img_bytes:
            out = Path(out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(img_bytes)
            print(f"OK  {out}  (model: {model})")
            return 0
        last_err = "no image part in response"
    print(f"IMAGEGEN-FAILED: {last_err}. Falling back to CSS/textures is fine.", file=sys.stderr)
    return 1


def _extract_image(resp):
    try:
        for cand in resp.candidates or []:
            for part in (cand.content.parts or []):
                inline = getattr(part, "inline_data", None)
                if inline and getattr(inline, "data", None):
                    return inline.data
    except Exception:
        pass
    return None


def main():
    ap = argparse.ArgumentParser(description="Gemini image generation (optional)")
    ap.add_argument("prompt", nargs="?", help="image description")
    ap.add_argument("--out", help="output .png")
    ap.add_argument("--ar", help="aspect ratio hint, e.g. 4:5, 1:1, 9:16, 16:9")
    ap.add_argument("--save-key", dest="save", help="store an API key locally and exit")
    ap.add_argument("--check", action="store_true", help="report SDK + key status")
    args = ap.parse_args()

    if args.save:
        return save_key(args.save)
    if args.check:
        return do_check()
    if not args.prompt or not args.out:
        print("ERROR: need a prompt and --out (or use --save-key / --check).", file=sys.stderr)
        return 1
    return generate(args.prompt, args.ar, args.out)


if __name__ == "__main__":
    sys.exit(main())
