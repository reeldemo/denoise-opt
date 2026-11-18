#!/usr/bin/env python3
"""Write review-safe copies of the three raster figures that carry identifying text in their pixels.

Run from the repository root after the figures in ../../figures changed:
    python3 submission/tmlr/anonymize_figures.py

make_tmlr.py copies the files in anon_figures/ over the same-named figures in the double-blind variant only.
The text is painted over with the background colour and re-set in the same font (DejaVu Sans, as in the
matplotlib originals); nothing else in the images changes. Needs Pillow.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / "anon_figures"
OUT.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def fit_font(old_text, target_w):
    size = 10
    for s in range(10, 80):
        f = ImageFont.truetype(FONT, s)
        if f.getlength(old_text) >= target_w:
            return ImageFont.truetype(FONT, s - 1 if f.getlength(old_text) > target_w * 1.01 else s)
        size = s
    return ImageFont.truetype(FONT, size)


def horizontal(src, box, old, new):
    """box = (x0, y0, x1, y1) of the old text line; the new text is centred on the same centre."""
    im = Image.open(ROOT / "figures" / src).convert("RGB")
    x0, y0, x1, y1 = box
    bg = im.getpixel((max(x0 - 6, 0), y0))
    d = ImageDraw.Draw(im)
    d.rectangle((x0 - 4, y0 - 4, x1 + 4, y1 + 4), fill=bg)
    f = fit_font(old, x1 - x0)
    w = f.getlength(new)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.text((cx - w / 2, cy), new, font=f, fill=(0, 0, 0), anchor="lm")
    im.save(OUT / src, optimize=True)


def vertical(src, box, old, new):
    """Vertical label read bottom-to-top (matplotlib ylabel)."""
    im = Image.open(ROOT / "figures" / src).convert("RGB")
    x0, y0, x1, y1 = box
    bg = im.getpixel((2, 2))
    pad = 4
    d = ImageDraw.Draw(im)
    d.rectangle((x0 - pad, y0 - pad, x1 + pad, y1 + pad), fill=bg)
    f = fit_font(old, y1 - y0)
    w = int(f.getlength(new)) + 8
    h = (x1 - x0) + 2 * pad
    tile = Image.new("RGB", (w, h), bg)
    ImageDraw.Draw(tile).text((w / 2, h / 2), new, font=f, fill=(0, 0, 0), anchor="mm")
    tile = tile.rotate(90, expand=True)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    im.paste(tile, (cx - tile.width // 2, cy - tile.height // 2))
    im.save(OUT / src, optimize=True)


horizontal("fig_hear_samples_panel.png", (100, 10, 1976, 49),
           "Audible wrap-seam demos (fixed A4 playback) \u2014 downloadable WAVs under reelsynth/brand/artifacts/meta_approach_compare/hear_samples/",
           "Audible wrap-seam demos (fixed A4 playback)")
horizontal("fig_vibrato_spectrogram.png", (457, 41, 2146, 79),
           "DenoiseOpt under slow vibrato playback | holdout seed=20260719, tile=46, |wrap|=2.283 | search seed=1902771841",
           "HybridSeam under slow vibrato playback | holdout seed=20260719, tile=46, |wrap|=2.283 | search seed=1902771841")
vertical("fig_wt_diversity_gallery.png", (13, 141, 46, 342), "ReelSynth export", "synthesizer export")
print("wrote", sorted(p.name for p in OUT.iterdir()))
