"""Controls, so that a 'fit' is not an artefact.

1. Shuffled grids: letters permuted within each watchtower of the 1584 table;
   how many governor names still read exactly along their paths?
2. Shuffled names: names moved to other governors' paths (same length);
   how many still read exactly, and what does the model's cost become?
3. Random corrections against the real 1587 changes: do Kelley's 23 changes
   break / fix governor names, or fall on the 16 mismatching names, more or less
   than random changes of the same shape (one row shifted left by one cell with a
   new last letter, plus 11 single-cell changes)?
4. Recovery (known-answer) test: synthetic tables with planted errors in the
   table copy and in the names; can the model tell which side is wrong?
Writes results/controls.json. Seeds from model_config.json.
"""

import json
import random
from pathlib import Path

import model
from gt import TABLES, norm

HERE = Path(__file__).resolve().parent
R = HERE.parent / "results"
CFG = json.load(open(HERE / "model_config.json"))
SEED = CFG["seed"]
NC = CFG["controls"]
GOVS = [g for g in model.GOVS if not g["special"]]
RUNS = json.load(open(R / "model_runs.json"))
T84 = RUNS["default_1584"]["table"]  # 1584 reconstruction (C1 + 3 blanks filled)


def exact_names(table, govs=GOVS):
    n = letters = 0
    for g in govs:
        r = model.read_name(table, g)
        t = "".join(norm(c) for c in g["name"])
        n += r == t
        letters += sum(a == b for a, b in zip(r, t, strict=False))
    return n, letters


def shuffled_grids(rng):
    real = exact_names(T84)
    res = []
    for _ in range(NC["n_shuffled_grids"]):
        tab = {}
        for t in TABLES:
            ids = [f"{t}.{i}.{j}" for i in range(13) for j in range(12)]
            vals = [T84[c] for c in ids]
            rng.shuffle(vals)
            tab.update(dict(zip(ids, vals, strict=False)))
        res.append(exact_names(tab))
    return {
        "real_exact_names": real[0],
        "real_letters": real[1],
        "null_exact_max": max(r[0] for r in res),
        "null_exact_mean": sum(r[0] for r in res) / len(res),
        "null_letters_mean": sum(r[1] for r in res) / len(res),
        "null_letters_max": max(r[1] for r in res),
    }


def shuffled_names(rng):
    real_cost = RUNS["default_1584"]["cost"]
    res, costs = [], []
    for k in range(NC["n_name_shuffles"]):
        names = [g["name"] for g in GOVS]
        rng.shuffle(names)
        govs = [{**g, "name": nm} for g, nm in zip(GOVS, names, strict=False)]
        res.append(exact_names(T84, govs)[0])
        if k < 50:
            specials = [g for g in model.GOVS if g["special"]]
            costs.append(model.solve(CFG["default"]["1584"], govs=govs + specials)["cost"])
    return {
        "real_exact_names": exact_names(T84)[0],
        "null_exact_max": max(res),
        "real_model_cost": real_cost,
        "null_model_cost_min": min(costs),
        "null_model_cost_mean": sum(costs) / len(costs),
        "n_cost_runs": len(costs),
    }


def name_status(table):
    return {g["n"]: model.read_name(table, g) == "".join(norm(c) for c in g["name"]) for g in GOVS}


def random_corrections(rng):
    ro = {c["id"]: norm(c["read"]["RO"]) for c in model.CELLS}
    rr = {c["id"]: norm(c["read"]["RR"]) for c in model.CELLS}
    real_changed = [k for k in ro if ro[k] != rr[k]]
    mismatch16 = {
        p
        for g in GOVS
        for p, L in zip(g["path"], g["name"], strict=False)
        if p in ro and not name_status(ro)[g["n"]]
    }
    st0 = name_status(ro)

    def stats(table, changed):
        st = name_status(table)
        return {
            "broken": sum(1 for n in st if st0[n] and not st[n]),
            "fixed": sum(1 for n in st if not st0[n] and st[n]),
            "on_mismatch_paths": sum(1 for c in changed if c in mismatch16),
        }

    real = stats(rr, real_changed)
    letters = [v for v in ro.values()]
    null = []
    for _ in range(NC["n_random_corrections"]):
        tab = dict(ro)
        changed = set()
        t = rng.choice(TABLES)
        i = rng.randrange(13)
        row = [tab[f"{t}.{i}.{j}"] for j in range(12)]
        new = row[1:] + [rng.choice(letters)]
        for j in range(12):
            if new[j] != row[j]:
                tab[f"{t}.{i}.{j}"] = new[j]
                changed.add(f"{t}.{i}.{j}")
        while len(changed) < len(real_changed):
            c = rng.choice(list(ro))
            if c in changed:
                continue
            a = rng.choice(letters)
            if a != ro[c]:
                tab[c] = a
                changed.add(c)
        null.append(stats(tab, changed))
    out = {"real": real, "n_changed": len(real_changed), "mismatch_path_cells": len(mismatch16)}
    for k in real:
        vals = [x[k] for x in null]
        out[k] = {
            "null_mean": sum(vals) / len(vals),
            "p_low": (1 + sum(1 for v in vals if v <= real[k])) / (1 + len(vals)),
            "p_high": (1 + sum(1 for v in vals if v >= real[k])) / (1 + len(vals)),
        }
    return out


RECOVERY_WEIGHTS = {
    "default_1584": None,
    "names_trusting": {
        "ms84": 1,
        "ms87": 0,
        "s1": 0,
        "gov_letter": 3,
        "gov_name": 3,
        "spoken": 2,
        "inv": 0,
        "cipher": 0,
    },
    "balanced": {
        "ms84": 2,
        "ms87": 0,
        "s1": 0,
        "gov_letter": 1,
        "gov_name": 1,
        "spoken": 2,
        "inv": 0,
        "cipher": 0,
    },
}


def recovery(rng, w=None):
    """Synthetic truth = T84. Plant 10 errors in the table copy (C1) and 10 letter
    errors in names (different governors, cells not shared). The 1587 copies are the
    planted copy with the real 1587 edits; inv = planted copy at the AD cells;
    spoken = truth at the spoken cells. Score: at each planted cell, did the model
    recover the truth? Split by side and by spoken coverage."""
    w = w or CFG["default"]["1584"]
    ro = {c["id"]: norm(c["read"]["RO"]) for c in model.CELLS}
    rr = {c["id"]: norm(c["read"]["RR"]) for c in model.CELLS}
    edits87 = {k: rr[k] for k in ro if ro[k] != rr[k]}
    spoken = set(model.SPOKEN)
    letters = list(T84.values())
    path_of = {}
    for g in GOVS:
        for k, p in enumerate(g["path"]):
            if p in T84:
                path_of[p] = (g["n"], k)
    tally = {
        "table_err": [0, 0],
        "name_err": [0, 0],
        "table_err_spoken": [0, 0],
        "name_err_spoken": [0, 0],
    }
    for _ in range(NC["n_recovery_trials"]):
        cells_t = rng.sample(sorted(path_of), 20)
        t_err, n_err = cells_t[:10], cells_t[10:]
        copy = dict(T84)
        for c in t_err:
            copy[c] = rng.choice([a for a in set(letters) if a != T84[c]])
        names = {g["n"]: list("".join(norm(x) for x in g["name"])) for g in GOVS}
        # synthetic truth names: read from truth
        for g in GOVS:
            names[g["n"]] = list(model.read_name(T84, g))
        for c in n_err:
            n, k = path_of[c]
            names[n][k] = rng.choice([a for a in set(letters) if a != T84[c]])
        cells = []
        for c in model.CELLS:
            cid = c["id"]
            r87 = edits87.get(cid, copy[cid])
            cells.append(
                {
                    "id": cid,
                    "read": {
                        "C1": copy[cid],
                        "S2": r87,
                        "C2": r87,
                        "S1": r87,
                        "AD": copy[cid],
                        "RO": T84[cid],
                    },
                    "AD_forced": c["AD_forced"],
                }
            )
        govs = [{**g, "name": "".join(names[g["n"]])} for g in GOVS]
        res = model.solve(
            w, cells=cells, govs=govs, spoken=[s for s in spoken if s in T84], cipher_uses=[]
        )
        for c in t_err:
            key = "table_err_spoken" if c in spoken else "table_err"
            tally[key][0] += res["table"][c] == T84[c]
            tally[key][1] += 1
        for c in n_err:
            key = "name_err_spoken" if c in spoken else "name_err"
            tally[key][0] += res["table"][c] == T84[c]
            tally[key][1] += 1
    return {
        k: {"recovered": v[0], "n": v[1], "rate": round(v[0] / v[1], 3) if v[1] else None}
        for k, v in tally.items()
    }


def main():
    rng = random.Random(SEED)
    out = {"seed": SEED}
    out["shuffled_grids"] = shuffled_grids(rng)
    print("shuffled grids", out["shuffled_grids"])
    out["shuffled_names"] = shuffled_names(rng)
    print("shuffled names", out["shuffled_names"])
    out["random_corrections"] = random_corrections(rng)
    print("random corrections", out["random_corrections"])
    out["recovery_weights"] = RECOVERY_WEIGHTS
    out["recovery"] = {}
    for name, w in RECOVERY_WEIGHTS.items():
        out["recovery"][name] = recovery(random.Random(SEED + 1), w)
        print("recovery", name, out["recovery"][name])
    json.dump(out, open(R / "controls.json", "w"), indent=1)


if __name__ == "__main__":
    main()
