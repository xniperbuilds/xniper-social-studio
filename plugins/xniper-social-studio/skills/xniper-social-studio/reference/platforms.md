# Platform Sizes & Safe Zones

Always design at the exact pixel size. Never "close enough" — platforms crop and
compress, and off-spec art looks amateur instantly.

## Full size table

| Platform | Format | Size (px) | Aspect | Notes |
|---|---|---|---|---|
| Instagram | Portrait post / carousel | **1080×1350** | 4:5 | Best default — most feed real estate |
| Instagram | Square post | 1080×1080 | 1:1 | Classic; safe for grid uniformity |
| Instagram | Story / Reel cover | 1080×1920 | 9:16 | Heavy UI overlay — see safe zones |
| Instagram | Landscape | 1080×566 | 1.91:1 | Rarely optimal |
| Facebook | Feed post | 1200×630 | 1.91:1 | Also the OG/link-share size |
| Facebook | Story | 1080×1920 | 9:16 | |
| X / Twitter | Single image | 1600×900 | 16:9 | In-feed shows ~16:9 |
| X / Twitter | Portrait | 1080×1350 | 4:5 | Allowed, more height |
| LinkedIn | Feed post | 1200×1500 | 4:5 | Portrait performs best |
| LinkedIn | Link card | 1200×627 | 1.91:1 | |
| Pinterest | Standard pin | 1000×1500 | 2:3 | Vertical is mandatory |
| Pinterest | Long pin | 1000×2100 | ~1:2.1 | |
| YouTube | Thumbnail | 1280×720 | 16:9 | < 2MB, readable tiny |
| YouTube | Community post | 1080×1080 | 1:1 | |
| TikTok | Cover / image | 1080×1920 | 9:16 | |
| Threads | Post | 1080×1080 | 1:1 | Also accepts 4:5 |

## Safe zones

Keep all critical content (headline, logo, CTA) inside the **central ~80%**.
Outer margin = breathing room + crop insurance.

### Default margins (per 1080px width)
- Outer padding: **64–96px** all sides minimum.
- Generous is premium. Cramped-to-the-edge is cheap.

### Instagram / TikTok Story (1080×1920) — UI overlay zones
The platform paints UI over your art. Keep text/logo clear of:
- **Top ~250px** — profile pic, username, close button.
- **Bottom ~320px** — caption, like/share/comment rail, "Send message" bar.
- **Right ~120px** — action buttons on Reels.
- → Safe creative band ≈ **y:250 to y:1600**, slightly left of center.

### Instagram carousel (1080×1350)
- Bottom ~80px can be grazed by the dots indicator on some clients — keep CTAs a touch higher.

### YouTube thumbnail (1280×720)
- Bottom-right ~ **180×60px** gets the duration stamp — keep faces/text out of it.
- Must read at **120px wide** (sidebar). Test by shrinking. Big face + ≤4 words wins.

## Output quality
- Render at **deviceScaleFactor 2** (so 1080×1350 → 2160×2700 actual pixels), then the platform downscales for crispness.
- Keep PNGs reasonable; if a platform caps file size (YouTube < 2MB), compress.
