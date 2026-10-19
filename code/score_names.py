"""Read every governor's name along its sigil path on each witness table and
count mismatches with the diary name (case-folded, u = v).
Usage: score_names.py [WITNESS ...]   (prints a summary; --list W prints mismatches)
"""

import json
import sys
from pathlib import Path

from gt import norm

D = Path(__file__).resolve().parent.parent / "data"
CELLS = {x["id"]: x for x in json.load(open(D / "cells.json"))["cells"]}
GOVS = json.load(open(D / "governors.json"))["governors"]
BX = json.load(open(D / "blackcross.json"))


def read_path(path, getter):
    return "".join(getter(p) for p in path)


def witness_getter(w, bx_w="RO"):
    def get(p):
        if p.startswith("BX"):
            _, r, c = p.split(".")
            return BX[bx_w][f"{r},{c}"]
        return CELLS[p]["read"][w] or "_"

    return get


def grid_getter(grid, bx_w="RO"):
    """grid: {cell_id: letter}"""

    def get(p):
        if p.startswith("BX"):
            _, r, c = p.split(".")
            return BX[bx_w][f"{r},{c}"]
        return grid[p]

    return get


def mismatches(getter, govs=GOVS, skip_special=True):
    out = []
    for g in govs:
        if skip_special and g["special"]:
            continue
        r = read_path(g["path"], getter)
        diffs = [
            k for k, (a, b) in enumerate(zip(r, g["name"], strict=False)) if norm(a) != norm(b)
        ]
        if diffs or len(r) != len(g["name"]):
            out.append((g["n"], g["name"], r, diffs))
    return out


def main(argv):
    ws = ["C1", "RO", "S1", "S2", "C2", "RR", "AR", "AD", "RT"]
    if argv and argv[0] == "--list":
        for m in mismatches(witness_getter(argv[1])):
            print(m)
        return
    for w in ws:
        mm = mismatches(witness_getter(w))
        letters = sum(len(m[3]) for m in mm)
        print(f"{w}: {len(mm)} of 87 governors mismatch, {letters} letters")


if __name__ == "__main__":
    main(sys.argv[1:])
