"""How the 91 sigil paths cover the table: cells used 0, 1, 2+ times; cells shared
between governors; black-cross cells used. Writes results/coverage.json."""

import collections
import json
from pathlib import Path

D = Path(__file__).resolve().parent.parent
govs = json.load(open(D / "data" / "governors.json"))["governors"]
use = collections.defaultdict(list)
for g in govs:
    for k, p in enumerate(g["path"]):
        use[p].append((g["n"], k))
cells = [f"{t}.{i}.{j}" for t in ("ORO", "MOR", "OIP", "MPH") for i in range(13) for j in range(12)]
hist = collections.Counter(len(use.get(c, [])) for c in cells)
shared = {c: v for c, v in use.items() if len(v) > 1}
bx = [c for c in use if c.startswith("BX")]
unused = [c for c in cells if c not in use]
out = {
    "positions": sum(len(g["path"]) for g in govs),
    "cell_use_histogram": dict(hist),
    "shared": shared,
    "blackcross_cells_used": sorted(bx),
    "unused_cells": unused,
}
json.dump(out, open(D / "results" / "coverage.json", "w"), indent=1)
print("positions", out["positions"], "histogram", dict(hist), "black-cross cells", len(bx))
print("shared cells:", shared)
print("unused:", unused)
