"""List the reader's disagreements with the seed (and unsure cells) per image,
and optionally build a contact sheet of those cells for a check against the image.
Usage: ocr_review.py OCR_JSON [IMAGE_DIR SHEET_DIR]
"""

import json
import sys
from pathlib import Path

from gt import norm

TABLES = {
    "ORO": "oroibAhaozpi",
    "MOR": "MOrdialhCtGa",
    "OIP": "oiPteaapDoce",
    "MPH": "mpharslgaiol",
}


def main(ocr_path, img_dir=None, sheet_dir=None):
    d = json.load(open(ocr_path))
    flagged = []
    for key, v in d.items():
        cells = [
            c
            for c in v["cells"]
            if norm(c["best"]) != norm(c["seed"])
            or (c["ratio"] > 0.6 and norm(c["alt"]) != norm(c["best"]))
        ]
        s = " ".join(
            f"{c['r']},{c['c']}:{c['seed']}>{c['best']}{'?' if c['ratio'] > 0.6 else ''}"
            for c in cells
        )
        print(key, s)
        flagged += [(key, c) for c in cells]
    if img_dir:
        from PIL import Image, ImageDraw

        Path(sheet_dir).mkdir(parents=True, exist_ok=True)
        per = 48
        for start in range(0, len(flagged), per):
            chunk = flagged[start : start + per]
            sheet = Image.new("RGB", (8 * 130, ((len(chunk) + 7) // 8) * 150), "white")
            dr = ImageDraw.Draw(sheet)
            for k, (key, c) in enumerate(chunk):
                t, v = key.split("/")
                im = Image.open(Path(img_dir) / f"{TABLES[t]}-{v}-labeled.png").convert("RGB")
                x0, y0 = 50 + 100 * c["c"], 50 + 100 * c["r"]
                crop = im.crop((x0, y0, x0 + 100, y0 + 100))
                X, Y = (k % 8) * 130, (k // 8) * 150
                sheet.paste(crop, (X + 15, Y + 5))
                dr.text((X + 5, Y + 110), f"#{start + k} {t} {v[:9]}", fill="black")
                dr.text(
                    (X + 5, Y + 125), f"{c['r']},{c['c']} s={c['seed']} o={c['best']}", fill="blue"
                )
            sheet.save(Path(sheet_dir) / f"sheet_{start // per:02d}.png")
        print(len(flagged), "flagged cells in", (len(flagged) + per - 1) // per, "sheets")


if __name__ == "__main__":
    main(*sys.argv[1:])
