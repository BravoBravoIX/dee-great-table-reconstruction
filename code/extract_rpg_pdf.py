"""Extract the cell grids from Frater Rinasce Piu Gloriosa (2025), "Reconstructing
the True Great Table" (enochian.blog PDF), figures 1-4, 6-8.

Research use only. The PDF is not redistributed; this script reads a local copy
and writes cell letters plus cell shading/outline flags to a private JSON file
(data/private/, git-ignored). Run with the PDF path and an output path.

Each figure is a 27 x 25 grid (13 rows + black-cross row + 13 rows; 12 columns +
black-cross column + 12 columns). Each cell is a 13 x 13 pt box.
"""

import json
import sys

import pdfplumber

FIG_PAGES = {  # figure number -> 0-based page index (from pdftotext page markers)
    1: 1,
    2: 6,
    3: 7,
    4: 8,
    6: 11,
    7: 15,
    8: 16,
}


def main(pdf_path, out_path):
    pdf = pdfplumber.open(pdf_path)
    out = {}
    for fig, pn in FIG_PAGES.items():
        page = pdf.pages[pn]
        chars = [c for c in page.chars if c["text"].strip() and "FreeSerif" in c["fontname"]]
        rects = [r for r in page.rects if 12 <= r["width"] <= 15 and 12 <= r["height"] <= 15]
        # Grid lines: take the pitch from the black-cross rects (filled black).
        top = min((c["top"] + c["bottom"]) / 2 for c in chars)
        left = min(c["x0"] + c["width"] / 2 for c in chars)
        bottom = max((c["top"] + c["bottom"]) / 2 for c in chars)
        right = max(c["x0"] + c["width"] / 2 for c in chars)
        py = (bottom - top) / 26
        px = (right - left) / 24
        cells = [["" for _ in range(25)] for _ in range(27)]
        bold = []
        for c in chars:
            x = c["x0"] + c["width"] / 2
            y = (c["top"] + c["bottom"]) / 2
            r = round((y - top) / py)
            k = round((x - left) / px)
            if not (0 <= r < 27 and 0 <= k < 25):
                continue
            cells[r][k] += c["text"]
            if "Bold" in c["fontname"]:
                bold.append(f"{r},{k}")
        fills = {}
        strokes = {}
        for rc in rects:
            x = rc["x0"] + rc["width"] / 2
            y = rc["top"] + rc["height"] / 2
            r = round((y - top) / py)
            k = round((x - left) / px)
            if not (0 <= r < 27 and 0 <= k < 25):
                continue
            col = rc.get("non_stroking_color")
            if rc.get("fill"):
                fills[f"{r},{k}"] = str(col)
            if rc.get("stroke"):
                strokes[f"{r},{k}"] = rc.get("linewidth")
        # outlined cells may be drawn as lines/curves instead of rects
        lines = [ln for ln in page.lines if ln.get("linewidth", 0) > 0.6]
        out[f"fig{fig}"] = {
            "page": pn + 1,
            "pitch": [py, px],
            "cells": cells,
            "bold": bold,
            "fills": fills,
            "strokes": strokes,
            "n_thick_lines": len(lines),
            "line_widths": sorted({round(ln.get("linewidth", 0), 2) for ln in page.lines}),
        }
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    for k, v in out.items():
        bad = sum(1 for row in v["cells"] for c in row if len(c) > 1)
        empty = sum(1 for row in v["cells"] for c in row if not c)
        print(
            k,
            "page",
            v["page"],
            "multi",
            bad,
            "empty",
            empty,
            "fills",
            len(v["fills"]),
            "strokes",
            len(v["strokes"]),
            "lines",
            v["n_thick_lines"],
            v["line_widths"],
        )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
