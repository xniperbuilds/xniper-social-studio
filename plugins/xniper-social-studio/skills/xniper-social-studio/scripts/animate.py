#!/usr/bin/env python3
"""
Xniper Social Studio — animate: a CSS-animated HTML page → GIF / MP4 / WebM.

For Reels covers, story motion, kinetic type, stat count-ups, gradient drift and
seamless loops. The page is built with normal CSS @keyframes; this scrubs those
animations frame-by-frame **deterministically** (via the Web Animations API —
each frame sets `animation.currentTime`, so output is reproducible, not a
real-time capture) and assembles the frames.

Output:
  - GIF  always (Pillow) — needs no extra tools.
  - MP4 / WebM only if `ffmpeg` is on PATH (auto-detected; otherwise skipped with
    a note — GIF still ships).

Examples
--------
  python animate.py out/cover.html --size 1080x1920 --duration 3 --fps 24 --out out/cover.gif
  python animate.py out/cover.html --size 1080x1350 --duration 2.5 --mp4 --webm --out out/cover.gif
  python animate.py out/cover.html --duration 4 --fps 30 --scale 1 --out out/loop.gif
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SIZE_RE = re.compile(r"(\d{2,5})x(\d{2,5})")

SCRUB_PAUSE = "document.getAnimations().forEach(a => a.pause());"
# set every running animation (and the document timeline) to time t ms
SCRUB_SET = "(t) => { document.getAnimations().forEach(a => { try { a.currentTime = t; } catch(e){} }); }"


def size_for(path, override):
    for src in (override, path.name):
        if src:
            m = SIZE_RE.search(src.lower())
            if m:
                return int(m.group(1)), int(m.group(2))
    print(f"WARN: no size for {path.name}; defaulting 1080x1350.", file=sys.stderr)
    return 1080, 1350


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        print("ERROR: Playwright not installed. Run: pip install playwright\n"
              "       python -m playwright install chromium", file=sys.stderr)
        sys.exit(1)


def capture_frames(html, w, h, scale, duration, fps, tmp):
    """Render `total` deterministic frames to PNGs in tmp; return their paths."""
    sync_playwright = ensure_playwright()
    total = max(1, round(duration * fps))
    step_ms = (duration * 1000.0) / total
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.launch()
    except Exception:
        pw.stop()
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        pw = sync_playwright().start()
        browser = pw.chromium.launch()
    paths = []
    try:
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
        page.goto(html.resolve().as_uri(), wait_until="domcontentloaded", timeout=30000)
        try:
            page.evaluate("async () => { if (document.fonts) await document.fonts.ready; }")
        except Exception:
            pass
        page.wait_for_timeout(300)
        n_anim = page.evaluate("document.getAnimations().length")
        if not n_anim:
            print("WARN: no CSS animations found on the page — output will be static. "
                  "Add @keyframes animations to the HTML.", file=sys.stderr)
        page.evaluate(SCRUB_PAUSE)
        for i in range(total):
            page.evaluate(SCRUB_SET, i * step_ms)
            page.wait_for_timeout(16)  # let the scrubbed frame paint
            fp = tmp / f"frame_{i:04d}.png"
            page.screenshot(path=str(fp), type="png",
                            clip={"x": 0, "y": 0, "width": w, "height": h})
            paths.append(fp)
        page.close()
    finally:
        browser.close(); pw.stop()
    return paths, fps


def build_gif(frames, fps, out):
    from PIL import Image
    imgs = [Image.open(f).convert("RGB") for f in frames]
    # quantize for a smaller, cleaner GIF palette
    imgs = [im.convert("P", palette=Image.ADAPTIVE, colors=256) for im in imgs]
    out.parent.mkdir(parents=True, exist_ok=True)
    imgs[0].save(out, save_all=True, append_images=imgs[1:],
                 duration=round(1000 / fps), loop=0, optimize=True, disposal=2)
    mb = out.stat().st_size / 1_048_576
    print(f"OK  {out}  (GIF, {len(frames)} frames @ {fps}fps, {mb:.2f} MB)")
    if mb > 15:
        print("    NOTE: large GIF — drop --fps or --scale, or shorten --duration, "
              "or export MP4 (smaller) with --mp4.", file=sys.stderr)


def build_video(frames_dir, fps, out, vcodec, pix=None):
    ff = shutil.which("ffmpeg")
    if not ff:
        print(f"SKIP {out.suffix[1:].upper()}: ffmpeg not on PATH. Install ffmpeg to enable "
              f"MP4/WebM (GIF already exported). https://ffmpeg.org/download.html", file=sys.stderr)
        return False
    cmd = [ff, "-y", "-framerate", str(fps), "-i", str(frames_dir / "frame_%04d.png"),
           "-c:v", vcodec]
    if pix:
        cmd += ["-pix_fmt", pix]
    cmd += ["-movflags", "+faststart"] if out.suffix == ".mp4" else []
    cmd.append(str(out))
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR {out.suffix[1:].upper()}: ffmpeg failed: "
              f"{e.stderr.decode('utf-8', 'ignore')[-300:]}", file=sys.stderr)
        return False
    mb = out.stat().st_size / 1_048_576
    print(f"OK  {out}  ({out.suffix[1:].upper()}, {mb:.2f} MB)")
    return True


def main():
    ap = argparse.ArgumentParser(description="CSS-animated HTML → GIF / MP4 / WebM")
    ap.add_argument("input", help="an .html file with CSS @keyframes animations")
    ap.add_argument("--out", help="output .gif (MP4/WebM derive their names from it)")
    ap.add_argument("--size", help="WxH (else parsed from filename)")
    ap.add_argument("--duration", type=float, default=3.0, help="seconds (default 3)")
    ap.add_argument("--fps", type=int, default=24, help="frames/sec (default 24)")
    ap.add_argument("--scale", type=int, default=1, help="device scale (1 keeps GIFs light)")
    ap.add_argument("--mp4", action="store_true", help="also export MP4 (needs ffmpeg)")
    ap.add_argument("--webm", action="store_true", help="also export WebM (needs ffmpeg)")
    args = ap.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"ERROR: file not found: {inp}", file=sys.stderr); return 1
    w, h = size_for(inp, args.size)
    out_gif = Path(args.out) if args.out else inp.with_suffix(".gif")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        frames, fps = capture_frames(inp, w, h, args.scale, args.duration, args.fps, tmp)
        try:
            build_gif(frames, fps, out_gif)
        except ImportError:
            print("ERROR: Pillow not installed. Run: pip install pillow", file=sys.stderr)
            return 1
        if args.mp4:
            build_video(tmp, fps, out_gif.with_suffix(".mp4"), "libx264", pix="yuv420p")
        if args.webm:
            build_video(tmp, fps, out_gif.with_suffix(".webm"), "libvpx-vp9")
    return 0


if __name__ == "__main__":
    sys.exit(main())
