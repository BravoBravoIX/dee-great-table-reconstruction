"""Two checks suggested by Burns & Moore (JWMT 2010, part II):
1. 'the capital letters on the four quadrants of the Great Table are all the first
   [letters of the] names of the Governors (with the exception of eight adverse
   letters)'. If so, the capitals are an independent check of where each sigil
   path starts. Count, per witness, the capitals and how many sit at a path start.
2. The PARAOAN sigil: AZOTH notes the sigil's own cells (on MPH) do not spell
   PARAOAN; Burns & Moore read them as 'Laxdizi'. Read those cells.
Writes results/capitals.json."""

import json
from pathlib import Path

from gt import full_to_cell

HERE = Path(__file__).resolve().parent
D = HERE.parent / "data"
cells = {c["id"]: c for c in json.load(open(D / "cells.json"))["cells"]}
govs = json.load(open(D / "governors.json"))["governors"]
starts = {g["path"][0]: g["n"] for g in govs}
out = {}
for w in ("C1", "S1", "S2", "C2", "RO", "RR"):
    caps = [cid for cid, c in cells.items() if c["read"][w][:1].isupper()]
    at_start = [c for c in caps if c in starts]
    starts_cap = [s for s in starts if s in cells and cells[s]["read"][w][:1].isupper()]
    out[w] = {
        "capitals": len(caps),
        "capitals_at_path_start": len(at_start),
        "path_starts_on_table": sum(1 for s in starts if s in cells),
        "path_starts_capital": len(starts_cap),
        "capitals_not_at_start": sorted(set(caps) - set(at_start)),
    }
    print(
        w,
        {k: v for k, v in out[w].items() if k != "capitals_not_at_start"},
        out[w]["capitals_not_at_start"],
    )
alt = [(7, 21), (8, 20), (9, 20), (9, 19), (10, 19), (10, 18), (9, 18)]  # AZOTH, commented out
ids = []
for r, c in alt:
    t, i, j = full_to_cell(r, c, "recensa")
    ids.append(f"{t}.{i}.{j}")
reading = {w: "".join(cells[x]["read"][w] for x in ids) for w in ("C1", "S2")}
out["paraoan_sigil_cells"] = {"cells": ids, "reading": reading}
print("PARAOAN sigil cells", ids, reading)
json.dump(out, open(HERE.parent / "results" / "capitals.json", "w"), indent=1)
