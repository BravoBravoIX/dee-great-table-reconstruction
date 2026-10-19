"""Constraint model of the Great Table (CP-SAT, OR-Tools).

Unknown: the letter T[c] of each of the 624 watchtower cells of the table being
reconstructed (target '1584' = the table as delivered and meant in June 1584;
target '1587' = the Tabula Recensa as meant in April 1587). Black-cross letters are
taken as given (all witnesses agree; see data/blackcross.json, rebuilt by build_data.py).

Evidence channels (each an observation 'cell c has letter L' with a weight):
  ms84    Cotton App. XLVI pt 1 (C1), the 1584 diary copy
  ms87    Sloane 3191 recensa (S2) and Cotton App. XLVI pt 2 recensa (C2), each
  s1      Sloane 3191 'originalis' (S1), Dee's later copy (contains reformed letters)
  gov     the 91 governors' names, delivered 21-23 May 1584, read along their sigil
          paths: a letter that disagrees with T costs gov_letter; a governor with any
          disagreeing letter also costs gov_name once (a name is either faithfully
          transmitted or garbled; this couples the cells of one name)
  spoken  names the angels spoke in the 1584 actions (RPG 2025 fig. 6, bold), plus
          the R of PARAOAN (MOR 7.0)
  inv     Dee's Book of Supplications names (AZOTH's derived table), at the cells
          where they differ from the Recensa
  cipher  the 1587 number cipher's letters at the cells it reads (cipher_cells.py)
Readings printed as two letters ('l/b') split their weight between the two.

The objective is the weighted sum of disagreements; the solution is the table (and
the set of names judged garbled) that minimises it. All weights are declared in
model_config.json before the runs; a sweep over a grid of weights shows which cell
decisions hold under every weighting and which depend on the weighting.
"""

import json
from pathlib import Path

from gt import norm
from ortools.sat.python import cp_model

D = Path(__file__).resolve().parent.parent / "data"
CELLS = json.load(open(D / "cells.json"))["cells"]
CELL_IDS = [c["id"] for c in CELLS]
BYID = {c["id"]: c for c in CELLS}
GOVS = json.load(open(D / "governors.json"))["governors"]
BX = json.load(open(D / "blackcross.json"))["RO"]
SPOKEN = json.load(open(D / "spoken_cells.json"))["cells"]
CIPHER_USES = json.load(open(D / "private" / "cipher_cells_full.json"))["uses"]
SCALE = 4  # weights are multiples of 0.25


def observations(w, cells=None, spoken=None, cipher_uses=None):
    """List of (cell, letter, weight, channel). cells/spoken/cipher_uses default to
    the real data; the controls pass synthetic ones."""
    cells = CELLS if cells is None else cells
    spoken = SPOKEN if spoken is None else spoken
    cipher_uses = CIPHER_USES if cipher_uses is None else cipher_uses
    byid = {c["id"]: c for c in cells}
    obs = []

    def add(cid, reading, weight, ch):
        if weight <= 0 or not reading or not reading.strip():
            return
        alts = [norm(x) for x in reading.split("/") if x.strip()]
        for a in alts:
            obs.append((cid, a, weight / len(alts), ch))

    for c in cells:
        add(c["id"], c["read"]["C1"], w["ms84"], "ms84")
        add(c["id"], c["read"]["S2"], w["ms87"], "ms87")
        add(c["id"], c["read"]["C2"], w["ms87"], "ms87")
        add(c["id"], c["read"]["S1"], w["s1"], "s1")
        if c["AD_forced"]:
            add(c["id"], c["read"]["AD"], w["inv"], "inv")
    for cid in spoken:
        if cid in byid:
            # the letter the angels spoke is the 1584 letter at that cell (RPG marks
            # letters of the 1584 names on the recensa figure; recensa letter differs
            # only at the two disputed cells, where the 1584 form was spoken)
            add(cid, byid[cid]["read"]["RO"], w["spoken"], "spoken")
    if "MOR.7.0" in byid and spoken is SPOKEN:
        add("MOR.7.0", "R", w["spoken"], "spoken")  # PARAOAN (spoken repeatedly)
    for u in cipher_uses:
        add(u["cell"], u["msg"], w["cipher"], "cipher")
    return obs


def solve(
    w,
    drop_govs=(),
    force=None,
    time_limit=20.0,
    seed=0,
    cells=None,
    govs=None,
    spoken=None,
    cipher_uses=None,
):
    """Return dict with table, cost, garbled governors, changed cells."""
    obs = observations(w, cells, spoken, cipher_uses)
    m = cp_model.CpModel()
    dom = {cid: set() for cid in CELL_IDS}
    for cid, a, _wt, _ch in obs:
        dom[cid].add(a)
    govs = [g for g in (GOVS if govs is None else govs) if g["n"] not in drop_govs]
    for g in govs:
        for p, L in zip(g["path"], g["name"], strict=False):
            if p in dom:
                dom[p].add(norm(L))
    if force:
        for cid, a in force.items():
            dom[cid].add(a)
    x = {}
    for cid in CELL_IDS:
        d = sorted(dom[cid]) or ["?"]
        for a in d:
            x[(cid, a)] = m.NewBoolVar(f"x_{cid}_{a}")
        m.AddExactlyOne(x[(cid, a)] for a in d)
    if force:
        for cid, a in force.items():
            m.Add(x[(cid, a)] == 1)
    cost = []
    for cid, a, wt, _ch in obs:
        cost.append(int(round(wt * SCALE)) * (1 - x[(cid, a)]))
    z = {}
    for g in govs:
        z[g["n"]] = zg = m.NewBoolVar(f"z_{g['n']}")
        cost.append(int(round(w["gov_name"] * SCALE)) * zg)
        for p, L in zip(g["path"], g["name"], strict=False):
            L = norm(L)
            if p.startswith("BX"):
                _, r, c = p.split(".")
                if norm(BX[f"{r},{c}"]) != L:
                    m.Add(zg == 1)
                    cost.append(int(round(w["gov_letter"] * SCALE)))
                continue
            m.Add(x[(p, L)] + zg >= 1)
            cost.append(int(round(w["gov_letter"] * SCALE)) * (1 - x[(p, L)]))
    m.Minimize(sum(cost))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = 1
    s.parameters.random_seed = seed
    st = s.Solve(m)
    assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE), st
    table = {cid: next(a for a in sorted(dom[cid]) if s.Value(x[(cid, a)])) for cid in CELL_IDS}
    garbled = sorted(n for n, v in z.items() if s.Value(v))
    return {
        "table": table,
        "cost": s.ObjectiveValue() / SCALE,
        "optimal": st == cp_model.OPTIMAL,
        "garbled": garbled,
        "domains": {k: sorted(v) for k, v in dom.items()},
    }


def read_name(table, g):
    out = ""
    for p in g["path"]:
        if p.startswith("BX"):
            _, r, c = p.split(".")
            out += norm(BX[f"{r},{c}"])
        else:
            out += table[p]
    return out
