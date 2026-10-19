"""Write results/disputed_cells.csv: the 26 cells where the witnesses disagree, each
witness's reading, the model's choice at the default 1584 weights, its firmness
margin, and how often each letter wins over the 1,296-weighting sweep.
Needs data/cells.json (build_data.py) and results/model_runs.json (run_model.py).
Usage: disputed_table.py
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cells = json.load(open(ROOT / "data" / "cells.json"))["cells"]
runs = json.load(open(ROOT / "results" / "model_runs.json"))
d, sweep = runs["default_1584"], runs["sweep_1584"]
W = ["C1", "S1", "S2", "C2", "RO", "RR", "AR"]
with open(ROOT / "results" / "disputed_cells.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["cell", *W, "chosen_1584", "margin", "sweep_wins"])
    for c in cells:
        if not c["disputed"]:
            continue
        cid = c["id"]
        tally = sweep["cell_choices"].get(cid, {})
        w.writerow(
            [
                cid,
                *[c["read"][x] for x in W],
                d["table"][cid],
                d["margins"].get(cid, {}).get("margin"),
                " ".join(f"{k}:{v}" for k, v in sorted(tally.items(), key=lambda kv: -kv[1])),
            ]
        )
print("wrote", ROOT / "results" / "disputed_cells.csv")
