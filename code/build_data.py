"""Build the study's machine-readable data from the private source extractions.

Inputs (data/private/, not committed: third-party transcriptions):
  rpg2025_figs.json  RPG 2025 figures (extract_rpg_pdf.py)
  vovina_ocr.json    Vovina images read cell by cell (ocr_vovina.py)
  azoth.json         AZOTH 1993 tables, sigil coordinates and rules (parse_azoth.py)
  names_seed.json    91 governor names, diary order (names_seed.py)
Inputs (committed): data/vovina_eyecheck.json, data/name_sources.json
Outputs:
  data/cells.json      every watchtower cell with each witness's reading
  data/governors.json  91 governors: diary name, variants, sigil cells
  data/blackcross.json black-cross cells per witness
"""

import json
import sys
from pathlib import Path

from gt import TABLES, full_to_cell, norm, split

D = Path(__file__).resolve().parent.parent / "data"
P = D / "private"

WITNESSES = {
    # id: (description, date, kind)
    "C1": (
        "Cotton App. XLVI pt 1 (Dee's diary, tables of 25 June 1584), via Vovina Archives image",
        "1584",
        "manuscript",
    ),
    "S1": (
        "Sloane 3191 'tabula originalis' (Dee's later fair copy), via Vovina Archives image",
        "after 1587",
        "manuscript",
    ),
    "S2": (
        "Sloane 3191 ff. 55v-56r 'tabula recensa' ('20 Aprilis 1587. Thus reformed by "
        "Raphael'), via Vovina Archives image",
        "1587",
        "manuscript",
    ),
    "C2": ("Cotton App. XLVI pt 2 recensa, via Vovina Archives image", "1587", "manuscript"),
    "RO": (
        "Rinasce Piu Gloriosa 2025, fig. 3 (Original Table, after Klein 2020)",
        "1584",
        "secondary",
    ),
    "RR": (
        "Rinasce Piu Gloriosa 2025, fig. 4 (Tabula Recensa, after Klein 2020)",
        "1587",
        "secondary",
    ),
    "RT": (
        "Rinasce Piu Gloriosa 2025, fig. 8 (their reconstructed 'True Great Table')",
        "2025",
        "reconstruction",
    ),
    "AR": ("AZOTH 1993 Enochian Tools, Tabula Recensa (rtable)", "1587", "secondary"),
    "AD": (
        "AZOTH 1993 'derived' table: Recensa retro-fitted to the names in Dee's Book of "
        "Supplications and Invocations (Turner 1989)",
        "c. 1587-",
        "reconstruction",
    ),
}


def main():
    figs = json.load(open(P / "rpg2025_figs.json"))
    ocr = json.load(open(P / "vovina_ocr.json"))
    eye = json.load(open(D / "vovina_eyecheck.json"))
    az = json.load(open(P / "azoth.json"))

    grids = {}
    vmap = {"C1": "cotton", "S1": "3191", "S2": "3191-recensa", "C2": "cotton-recensa"}
    for wid, v in vmap.items():
        grids[wid] = {}
        for t in TABLES:
            g = [list(row) for row in ocr[f"{t}/{v}"]["grid"]]
            for rc, val in eye.get(f"{t}/{v}", {}).items():
                r, c = map(int, rc.split(","))
                g[r][c] = val
            grids[wid][t] = g
    full = {
        k: [[c or " " for c in row] for row in figs[f]["cells"]]
        for k, f in (("RO", "fig3"), ("RR", "fig4"), ("RT", "fig8"))
    }
    grids["RO"] = {t: [list(r) for r in g] for t, g in split(full["RO"], "original").items()}
    grids["RR"] = {t: [list(r) for r in g] for t, g in split(full["RR"], "recensa").items()}
    grids["RT"] = {t: [list(r) for r in g] for t, g in split(full["RT"], "recensa").items()}
    grids["AR"] = {
        t: [list(r) for r in g] for t, g in split(az["tables"]["rtable"], "recensa").items()
    }
    grids["AD"] = {
        t: [list(r) for r in g] for t, g in split(az["tables"]["dtable"], "original").items()
    }
    xd = split(az["tables"]["xdtable"], "original")

    cells = []
    for t in TABLES:
        for i in range(13):
            for j in range(12):
                rd = {w: grids[w][t][i][j] for w in grids}
                vals = {
                    norm(x)
                    for w, x in rd.items()
                    if x.strip() and "/" not in x and w not in ("RT", "AD")
                }
                cells.append(
                    {
                        "id": f"{t}.{i}.{j}",
                        "table": t,
                        "row": i,
                        "col": j,
                        "read": rd,
                        "AD_forced": xd[t][i][j].isupper(),
                        "disputed": len(vals) > 1,
                    }
                )
    # black cross (full-table coords; same frame in both layouts)
    bx = {}
    for w, tab in (
        ("RO", full["RO"]),
        ("RR", full["RR"]),
        ("AR", az["tables"]["rtable"]),
        ("AO", az["tables"]["otable"]),
    ):
        bx[w] = {f"{r},12": tab[r][12] for r in range(27)}
        bx[w].update({f"13,{c}": tab[13][c] for c in range(25)})

    # governors
    names = json.load(open(P / "names_seed.json"))
    srcs = json.load(open(D / "name_sources.json"))
    govs = []
    for g in names:
        n = g["n"]
        coords = az["coords"][f"cgov{n}"]
        path = []
        for r, c in coords:
            cell = full_to_cell(r, c, "recensa")
            path.append(f"{cell[0]}.{cell[1]}.{cell[2]}" if cell else f"BX.{r}.{c}")
        s = srcs.get(str(n), {})
        govs.append(
            {
                **g,
                "name": s.get("diary", g["name"]),
                "path": path,
                "variants": s.get("variants", {}),
                "notes": s.get("notes", ""),
                "special": n in (28, 29, 30, 65),
            }
        )
    meta = {
        "witnesses": WITNESSES,
        "coords": "table.row.col; row 0-12 (row 6 = linea spiritus sancti), col 0-11",
        "letter_identity": "case-folded, u = v",
        "licence": "Private research data. Readings come from third-party transcriptions "
        "(Vovina Archives CC BY-NC-SA 4.0; Rinasce Piu Gloriosa 2025; AZOTH 1993). "
        "Do not publish without checking terms.",
    }
    json.dump({"meta": meta, "cells": cells}, open(D / "cells.json", "w"), indent=0)
    json.dump(
        {
            "meta": {
                "source": "names: Casaubon 1659 (TFR) pp. 140-158 as checked; paths: "
                "AZOTH 1993 cgov1-91 (sigils after Denning & Phillips), mapped from "
                "the recensa layout"
            },
            "governors": govs,
        },
        open(D / "governors.json", "w"),
        indent=1,
    )
    json.dump(bx, open(D / "blackcross.json", "w"), indent=0)
    nd = sum(c["disputed"] for c in cells)
    print(len(cells), "cells;", nd, "disputed among witnesses (excl. RT, AD)")


if __name__ == "__main__":
    sys.exit(main())
