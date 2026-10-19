"""Test of the quadrant arrangement and the letters with the 1587 number cipher.

On 20 April 1587 Kelley was told to 'join Enoch his Tables', 'give every place his
running number' and 'refer every letter in the Table to his number'; then came 196
numbers whose letters spell a Latin message. If the numbers were made from a given
table and numbering, they hit the message letters far above chance on that table
and not on others.

Hypotheses scored (every one with 1-based running numbers):
  - table-wise numbering, tables in any of the 24 orders, each table row by row
    (13 x 12 = 156 cells), with the letters of a given witness (C1 original or S2
    recensa, or C2);
  - row-wise numbering across the joined table (rows of 24 cells, black cross
    skipped) for each of the 24 placements of the four tables in the quarters.
Score: exact hits, and hits allowing the off-by-one slip RPG 2025 found (number-1).
Control: the same score with the message letters shuffled against the numbers
(10,000 shuffles, seed 20261019) gives the chance level for each hypothesis.
Usage: cipher_test.py OUT_JSON
"""

import itertools
import json
import random
import sys
from pathlib import Path

from gt import QUARTER_ORIGIN, TABLES, norm

D = Path(__file__).resolve().parent.parent / "data"
CELLS = json.load(open(D / "cells.json"))["cells"]
CIPHER = json.load(open(D / "private" / "cipher1587.json"))
SEED = 20261019


def letters(w):
    g = {t: [[""] * 12 for _ in range(13)] for t in TABLES}
    for c in CELLS:
        x = c["read"][w]
        g[c["table"]][c["row"]][c["col"]] = norm(x.split("/")[0]) if x.strip() else "?"
    return g


def tablewise(g, order):
    seq = []
    for t in order:
        for i in range(13):
            seq.extend(g[t][i])
    return seq


def rowwise(g, placement):
    seq = []
    full = [["#"] * 25 for _ in range(27)]
    for q, t in enumerate(placement):
        r0, c0 = QUARTER_ORIGIN[q]
        for i in range(13):
            for j in range(12):
                full[r0 + i][c0 + j] = g[t][i][j]
    for r in range(27):
        if r == 13:
            continue
        for c in range(25):
            if c == 12:
                continue
            seq.append(full[r][c])
    return seq


def score(seq, nums, msg):
    exact = sum(
        1 for n, m in zip(nums, msg, strict=False) if 1 <= n <= len(seq) and seq[n - 1] == m
    )
    near = sum(
        1
        for n, m in zip(nums, msg, strict=False)
        if (1 <= n <= len(seq) and seq[n - 1] == m) or (2 <= n <= len(seq) + 1 and seq[n - 2] == m)
    )
    return exact, near


def main(out):
    nums = [r["num"] for r in CIPHER]
    msg = [norm(r["msg"]) for r in CIPHER]
    rng = random.Random(SEED)
    shuffles = []
    for _ in range(10000):
        m = msg[:]
        rng.shuffle(m)
        shuffles.append(m)
    results = []
    for w in ("C1", "S2", "C2"):
        g = letters(w)
        for order in itertools.permutations(TABLES):
            for kind, seq in (("tablewise", tablewise(g, order)), ("rowwise", rowwise(g, order))):
                e, n = score(seq, nums, msg)
                results.append({"witness": w, "kind": kind, "order": order, "exact": e, "near": n})
    # chance level for the best hypotheses
    results.sort(key=lambda r: -r["near"])
    for r in results[:6] + [
        x
        for x in results
        if x["witness"] == "C1"
        and x["kind"] == "rowwise"
        and x["order"] == ("ORO", "MOR", "OIP", "MPH")
    ]:
        g = letters(r["witness"])
        seq = tablewise(g, r["order"]) if r["kind"] == "tablewise" else rowwise(g, r["order"])
        null = [score(seq, nums, m)[1] for m in shuffles]
        r["null_near_mean"] = sum(null) / len(null)
        r["null_near_max"] = max(null)
        r["p_near"] = (1 + sum(1 for x in null if x >= r["near"])) / (1 + len(null))
    json.dump(results, open(out, "w"), indent=0)
    for r in results[:12]:
        print(
            r["witness"],
            r["kind"],
            "-".join(r["order"]),
            "exact",
            r["exact"],
            "near",
            r["near"],
            "null mean {:.1f} max {} p {}".format(
                r.get("null_near_mean", float("nan")), r.get("null_near_max"), r.get("p_near")
            ),
        )
    base = [
        x
        for x in results
        if x["witness"] == "C1"
        and x["kind"] == "rowwise"
        and x["order"] == ("ORO", "MOR", "OIP", "MPH")
    ][0]
    print("original layout, row-wise, C1:", base["exact"], base["near"], base.get("null_near_mean"))


if __name__ == "__main__":
    main(sys.argv[1])
