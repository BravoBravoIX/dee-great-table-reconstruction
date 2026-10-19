"""Glyph reader for the Vovina Archives watchtower images.

The Vovina images (CC BY-NC-SA 4.0, https://vovina-archives.statichost.eu) are clean
typeset 12 x 13 grids, 100 px per cell. Each cell glyph is cut out, cropped to its
ink bounding box, resized to 20 x 20, and described with that bitmap plus the box
size and position (which separates o/O, c/C, s/S, v/V, z/Z, p/P). Cells are labelled
by nearest neighbour against the four Cotton App. XLVI (pt 1) images, labelled with
a seed transcription of the original table (Rinasce Piu Gloriosa 2025, figure 3,
read from the PDF). Leave-one-out on the labelled cells shows where the seed and
the image disagree. Every cell where the reader disagrees with the seed or is
unsure is listed for a check by eye; the eye check is recorded in
data/vovina_eyecheck.json and applied by build_cells.py.

Usage: ocr_vovina.py IMAGE_DIR SEED_JSON OUT_JSON
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

TABLES = {
    "ORO": "oroibAhaozpi",
    "MOR": "MOrdialhCtGa",
    "OIP": "oiPteaapDoce",
    "MPH": "mpharslgaiol",
}
VARIANTS = ["cotton", "3191", "3191-recensa", "cotton-recensa"]
PITCH, ORIGIN, MARGIN = 100, 50, 6
N = 20


def features(path):
    rgb = np.asarray(Image.open(path).convert("RGB")).astype(int)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    red = (r > 150) & (g < 90) & (b < 90)
    ink = ((r + g + b) / 3 < 140) | red
    out = {}
    for i in range(13):
        for j in range(12):
            y0 = ORIGIN + PITCH * i + MARGIN
            x0 = ORIGIN + PITCH * j + MARGIN
            c = ink[y0 : y0 + PITCH - 2 * MARGIN, x0 : x0 + PITCH - 2 * MARGIN]
            ys, xs = np.nonzero(c)
            if len(ys) == 0:
                out[(i, j)] = (np.zeros(N * N + 4), False, 0)
                continue
            box = c[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
            im = Image.fromarray((box * 255).astype(np.uint8)).resize((N, N), Image.BILINEAR)
            v = np.asarray(im, dtype=float).ravel() / 255.0
            geo = np.array([box.shape[0], box.shape[1], ys.min(), xs.min()], dtype=float) / 4.0
            nred = int(red[y0 : y0 + PITCH - 2 * MARGIN, x0 : x0 + PITCH - 2 * MARGIN].sum())
            out[(i, j)] = (np.concatenate([v, geo]), nred > 30, int(c.sum()))
    return out


def main(img_dir, seed_path, out_path):
    seed = json.load(open(seed_path))
    img_dir = Path(img_dir)
    feats = {
        (t, v): features(img_dir / f"{stem}-{v}-labeled.png")
        for t, stem in TABLES.items()
        for v in VARIANTS
    }
    lab_x, lab_y, lab_id = [], [], []
    for t in TABLES:
        for (i, j), (f, _red, _ink) in feats[(t, "cotton")].items():
            lab_x.append(f)
            lab_y.append(seed[t][i][j])
            lab_id.append((t, i, j))
    lab_x = np.array(lab_x)
    out = {}
    for (t, v), cells in feats.items():
        grid, info = [], []
        for i in range(13):
            row = []
            for j in range(12):
                f, red, ink = cells[(i, j)]
                d = np.sqrt(((lab_x - f) ** 2).sum(1))
                if v == "cotton":  # leave one out
                    d[lab_id.index((t, i, j))] = np.inf
                order = np.argsort(d)
                best = lab_y[order[0]]
                d1 = float(d[order[0]])
                other = next(k for k in order if lab_y[k] != best)
                d2 = float(d[other])
                row.append(best)
                info.append(
                    {
                        "r": i,
                        "c": j,
                        "best": best,
                        "d1": round(d1, 2),
                        "alt": lab_y[other],
                        "d2": round(d2, 2),
                        "ratio": round(d1 / max(d2, 1e-9), 3),
                        "red": red,
                        "ink": ink,
                        "seed": seed[t][i][j],
                    }
                )
            grid.append("".join(row))
        out[f"{t}/{v}"] = {"grid": grid, "cells": info}
        nd = sum(1 for x in info if x["best"] != x["seed"])
        unsure = sum(1 for x in info if x["ratio"] > 0.6)
        print(f"{t:3s} {v:15s} differs from seed {nd:3d}  unsure {unsure:3d}")
    json.dump(out, open(out_path, "w"), indent=0)


if __name__ == "__main__":
    main(*sys.argv[1:4])
