#!/usr/bin/env python3
"""
Xniper Social Studio — render HTML → exact-size PNG (Playwright, retina-crisp).

Examples
--------
  python render.py out/post.html --size 1080x1350 --out out/post.png
  python render.py out/ --batch --out out/exports/        # whole folder
  python render.py out/slide-1080x1350.html               # size read from filename

Renders at deviceScaleFactor 2 by default, hides scrollbars, and waits for web
fonts + images to load before capture. If the Chromium browser binary is missing
it is installed automatically (Playwright itself must already be pip-installed).
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SIZE_RE = re.compile(r"(\d{3,5})x(\d{3,5})")


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa
        return sync_playwright
    except ImportError:
        print("ERROR: Playwright is not installed. Run once:\n"
              "    pip install playwright\n"
              "    python -m playwright install chromium", file=sys.stderr)
        sys.exit(1)


def launch(sync_playwright):
    """Launch Chromium, auto-installing the browser binary on first failure."""
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.launch()
        return pw, browser
    except Exception as e:
        msg = str(e).lower()
        if "executable doesn" in msg or "install" in msg or "not found" in msg:
            print("Chromium not found — installing it once (python -m playwright install chromium)...")
            pw.stop()
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            pw = sync_playwright().start()
            return pw, pw.chromium.launch()
        pw.stop()
        raise


def size_for(path, override):
    if override:
        m = SIZE_RE.fullmatch(override.lower()) or SIZE_RE.search(override.lower())
        if m:
            return int(m.group(1)), int(m.group(2))
    m = SIZE_RE.search(path.name)
    if m:
        return int(m.group(1)), int(m.group(2))
    print(f"WARN: no size for {path.name}; defaulting 1080x1350. Pass --size WxH.", file=sys.stderr)
    return 1080, 1350


def shoot(browser, html_path, out_path, w, h, scale):
    page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
    page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
    try:
        page.evaluate("document.fonts && document.fonts.ready")
        page.wait_for_function("document.fonts ? document.fonts.status === 'loaded' : true", timeout=8000)
    except Exception:
        pass
    page.wait_for_timeout(600)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out_path), type="png", clip={"x": 0, "y": 0, "width": w, "height": h})
    page.close()
    print(f"OK  {out_path}  ({w}x{h} @{scale}x)")


def main():
    ap = argparse.ArgumentParser(description="Render HTML → PNG")
    ap.add_argument("input", help="an .html file OR a folder (with --batch)")
    ap.add_argument("--out", help="output .png (single) or output folder (batch)")
    ap.add_argument("--size", help="WxH, e.g. 1080x1350 (else parsed from filename)")
    ap.add_argument("--batch", action="store_true", help="render every .html in the input folder")
    ap.add_argument("--scale", type=int, default=2, help="device scale factor (default 2)")
    args = ap.parse_args()

    inp = Path(args.input)
    sync_playwright = ensure_playwright()

    if args.batch or inp.is_dir():
        files = sorted(inp.glob("*.html"))
        if not files:
            print(f"ERROR: no .html files in {inp}", file=sys.stderr)
            sys.exit(1)
        out_dir = Path(args.out) if args.out else inp / "exports"
        pw, browser = launch(sync_playwright)
        try:
            for f in files:
                w, h = size_for(f, args.size)
                shoot(browser, f, out_dir / (f.stem + ".png"), w, h, args.scale)
        finally:
            browser.close(); pw.stop()
    else:
        if not inp.exists():
            print(f"ERROR: file not found: {inp}", file=sys.stderr)
            sys.exit(1)
        w, h = size_for(inp, args.size)
        out_path = Path(args.out) if args.out else inp.with_suffix(".png")
        pw, browser = launch(sync_playwright)
        try:
            shoot(browser, inp, out_path, w, h, args.scale)
        finally:
            browser.close(); pw.stop()


if __name__ == "__main__":
    main()
