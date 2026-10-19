"""Cells of names the angels spoke explicitly in the 1584 actions, as marked (bold)
by Rinasce Piu Gloriosa 2025 fig. 6 (recensa layout). Lists them by table and
checks which disputed cells and which governor-mismatch cells they touch.
Writes data/spoken_cells.json (cell ids only)."""

import json
from pathlib import Path

from gt import full_to_cell, norm

D = Path(__file__).resolve().parent.parent / "data"
figs = json.load(open(D / "private" / "rpg2025_figs.json"))
cells = {x["id"]: x for x in json.load(open(D / "cells.json"))["cells"]}
govs = json.load(open(D / "governors.json"))["governors"]

bold = []
for rc in figs["fig6"]["bold"]:
    r, c = map(int, rc.split(","))
    cell = full_to_cell(r, c, "recensa")
    bold.append(f"{cell[0]}.{cell[1]}.{cell[2]}" if cell else f"BX.{r}.{c}")
by_table = {}
for b in bold:
    by_table.setdefault(b.split(".")[0], []).append(b)
for t, v in by_table.items():
    print(
        t,
        len(v),
        " ".join(
            f"{x.split('.', 1)[1]}={cells[x]['read']['RR'] if x in cells else '?'}" for x in v
        ),
    )
print("disputed cells among spoken:", [b for b in bold if b in cells and cells[b]["disputed"]])
mm_cells = set()
for g in govs:
    for k, p in enumerate(g["path"]):
        if p in cells and norm(cells[p]["read"]["RO"]) != norm(g["name"][k]):
            mm_cells.add(p)
print("governor-mismatch cells (1584 table):", len(mm_cells))
print("mismatch cells that are also spoken:", sorted(mm_cells & set(bold)))
json.dump(
    {
        "source": "RPG 2025 fig. 6 bold letters (names explicitly spoken by the angels)",
        "cells": bold,
        "mismatch_cells_1584": sorted(mm_cells),
    },
    open(D / "spoken_cells.json", "w"),
    indent=0,
)
