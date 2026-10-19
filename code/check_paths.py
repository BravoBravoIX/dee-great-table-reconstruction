"""Cross-check AZOTH's sigil paths against an independent source: the cells shaded
in Rinasce Piu Gloriosa 2025 fig. 2 (the 16 governors whose names differ from the
original table, shaded on the original layout).
Usage: check_paths.py
"""

import json
from pathlib import Path

from gt import cell_to_full

D = Path(__file__).resolve().parent.parent / "data"
figs = json.load(open(D / "private" / "rpg2025_figs.json"))
govs = {g["n"]: g for g in json.load(open(D / "governors.json"))["governors"]}
RPG16 = [6, 8, 10, 11, 19, 40, 43, 50, 56, 61, 67, 70, 78, 83, 88, 91]

fills = figs["fig2"]["fills"]
shaded = {k for k, v in fills.items() if v not in ("(0.0,)",)}
ours = set()
for n in RPG16:
    for p in govs[n]["path"]:
        t, i, j = p.split(".")
        r, c = cell_to_full(t, int(i), int(j), "original")
        ours.add(f"{r},{c}")
print("cells on our 16 paths:", len(ours), " shaded in fig. 2:", len(shaded))
print("ours not shaded:", sorted(ours - shaded))
print("shaded not ours:", sorted(shaded - ours))
