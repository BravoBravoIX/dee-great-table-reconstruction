"""Which cells does the 1587 cipher read (recensa layout, row-wise running numbers,
1-based), and what does it say about the disputed cells?

For each cipher number n, the intended cell is n (exact) or n-1 (the off-by-one
slip). We take the cell whose letter (in any witness) equals the message letter;
when neither does, the number is listed as a miss. Output: per disputed cell the
message letters read there, i.e. the cipher's vote for that cell's letter in 1587.
Usage: cipher_cells.py OUT_JSON

The full output (with the message letter of every number, taken from the 2025
paper's Appendix A) goes to data/private/cipher_cells_full.json, which model.py
reads. OUT_JSON, the published copy, leaves out the message letters and the
witness letters of the misses, so that the paper's table is not republished.
"""

import json
import sys
from pathlib import Path

from gt import LAYOUTS, QUARTER_ORIGIN, norm

D = Path(__file__).resolve().parent.parent / "data"
CELLS = {x["id"]: x for x in json.load(open(D / "cells.json"))["cells"]}
CIPHER = json.load(open(D / "private" / "cipher1587.json"))
W = ["C1", "S1", "S2", "C2"]


def numbering(layout="recensa"):
    full = [[None] * 25 for _ in range(27)]
    for q, t in enumerate(LAYOUTS[layout]):
        r0, c0 = QUARTER_ORIGIN[q]
        for i in range(13):
            for j in range(12):
                full[r0 + i][c0 + j] = f"{t}.{i}.{j}"
    seq = [full[r][c] for r in range(27) for c in range(25) if r != 13 and c != 12]
    return {k + 1: cid for k, cid in enumerate(seq)}


def main(out):
    num = numbering()
    uses, misses = [], []
    for k, row in enumerate(CIPHER):
        m = norm(row["msg"])
        hit = None
        for n, kind in ((row["num"], "exact"), (row["num"] - 1, "minus1")):
            cid = num.get(n)
            if cid is None:
                continue
            vals = {
                w: norm(CELLS[cid]["read"][w].split("/")[0])
                for w in W
                if CELLS[cid]["read"][w].strip()
            }
            if m in vals.values():
                hit = {
                    "k": k,
                    "num": row["num"],
                    "cell": cid,
                    "kind": kind,
                    "msg": m,
                    "agree": sorted(w for w, v in vals.items() if v == m),
                    "disagree": sorted(w for w, v in vals.items() if v != m),
                }
                break
        if hit:
            uses.append(hit)
        else:
            misses.append(
                {
                    "k": k,
                    "num": row["num"],
                    "msg": m,
                    "cell_n": num.get(row["num"]),
                    "cell_n-1": num.get(row["num"] - 1),
                    "letters": {
                        c: {w: CELLS[c]["read"][w] for w in W}
                        for c in (num.get(row["num"]), num.get(row["num"] - 1))
                        if c
                    },
                }
            )
    disputed = [u for u in uses if CELLS[u["cell"]]["disputed"]]

    # direction of the slips: how often does n, n-1, n+1 carry the message letter
    # (recensa letters, S2), and what happens to MOR row 7 with the 1584 letters (C1)?
    def at(n, w):
        cid = num.get(n)
        return (
            norm(CELLS[cid]["read"][w].split("/")[0])
            if cid and CELLS[cid]["read"][w].strip()
            else None
        )

    offs = {}
    for w in ("S2", "C1"):
        cnt = {"n": 0, "n-1 only": 0, "n+1 only": 0, "n-2/n+2 only": 0}
        for row in CIPHER:
            m, n = norm(row["msg"]), row["num"]
            if at(n, w) == m:
                cnt["n"] += 1
            elif at(n - 1, w) == m:
                cnt["n-1 only"] += 1
            elif at(n + 1, w) == m:
                cnt["n+1 only"] += 1
            elif m in (at(n - 2, w), at(n + 2, w)):
                cnt["n-2/n+2 only"] += 1
        offs[w] = cnt
    print("offsets:", offs)
    full = {"uses": uses, "misses": misses, "disputed_uses": disputed, "offsets": offs}
    json.dump(full, open(D / "private" / "cipher_cells_full.json", "w"), indent=1)

    def public(rows):
        return [{k: v for k, v in r.items() if k not in ("msg", "letters")} for r in rows]

    json.dump(
        {
            "note": "Published copy: message letters left out (see the README, Licensing).",
            "uses": public(uses),
            "misses": public(misses),
            "disputed_uses": public(disputed),
            "offsets": offs,
        },
        open(out, "w"),
        indent=1,
    )
    print("hits", len(uses), "misses", len(misses))
    for u in disputed:
        print("disputed cell used:", u)
    for m in misses:
        print("miss:", m)


if __name__ == "__main__":
    main(sys.argv[1])
