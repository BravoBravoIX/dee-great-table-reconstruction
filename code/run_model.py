"""Run the constraint model: default solutions (1584 and 1587 targets), per-cell
margins, the weight sweep, and leave-one-governor-out prediction.
Writes results/model_runs.json. Usage: run_model.py [--quick]
"""

import itertools
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import model
from gt import norm

HERE = Path(__file__).resolve().parent
R = HERE.parent / "results"
CFG = json.load(open(HERE / "model_config.json"))


def interesting_cells():
    s = set(c["id"] for c in model.CELLS if c["disputed"] or not c["read"]["C1"].strip())
    for g in model.GOVS:
        for p, L in zip(g["path"], g["name"], strict=False):
            if p in model.BYID and norm(model.BYID[p]["read"]["C1"] or "?") != norm(L):
                s.add(p)
    return sorted(s)


def margins(w, base, cells):
    out = {}
    for cid in cells:
        alts = [a for a in base["domains"][cid] if a != base["table"][cid]]
        res = {}
        for a in alts:
            r = model.solve(w, force={cid: a})
            res[a] = round(r["cost"] - base["cost"], 2)
        out[cid] = {
            "chosen": base["table"][cid],
            "cost_of_alternatives": res,
            "margin": min(res.values()) if res else None,
        }
    return out


def main(quick=False):
    t0 = time.time()
    out = {
        "run": {
            "python": platform.python_version(),
            "seed": CFG["seed"],
            "commit": subprocess.run(
                ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=HERE
            ).stdout.strip(),
        }
    }
    cells = interesting_cells()
    out["interesting_cells"] = cells
    for target in ("1584", "1587"):
        w = CFG["default"][target]
        base = model.solve(w)
        c1 = {
            c["id"]: norm(c["read"]["C1"]) if c["read"]["C1"].strip() else "_" for c in model.CELLS
        }
        s2 = {c["id"]: norm(c["read"]["S2"].split("/")[0]) for c in model.CELLS}
        names = {g["n"]: model.read_name(base["table"], g) for g in model.GOVS}
        out[f"default_{target}"] = {
            "weights": w,
            "cost": base["cost"],
            "optimal": base["optimal"],
            "garbled_governors": base["garbled"],
            "changed_vs_C1": {k: [c1[k], v] for k, v in base["table"].items() if c1[k] != v},
            "changed_vs_S2": {k: [s2[k], v] for k, v in base["table"].items() if s2[k] != v},
            "names": {
                n: [g["name"], names[g["n"]]]
                for g in model.GOVS
                for n in [g["n"]]
                if norm(g["name"]) != names[g["n"]]
            },
            "table": base["table"],
            "margins": margins(w, base, cells),
        }
        print(target, "cost", base["cost"], "garbled", base["garbled"])
    # sweep
    grid = CFG["sweep_1584"]
    keys = list(grid)
    combos = list(itertools.product(*[grid[k] for k in keys]))
    if quick:
        combos = combos[::40]
    tally = {cid: {} for cid in cells}
    ngarb = {}
    for vals in combos:
        w = dict(zip(keys, vals, strict=False))
        r = model.solve(w)
        for cid in cells:
            a = r["table"][cid]
            tally[cid][a] = tally[cid].get(a, 0) + 1
        for n in r["garbled"]:
            ngarb[n] = ngarb.get(n, 0) + 1
    out["sweep_1584"] = {
        "n_weightings": len(combos),
        "cell_choices": tally,
        "garbled_frequency": ngarb,
    }
    print("sweep done", len(combos))
    # leave-one-governor-out prediction, default 1584 weights
    w = CFG["default"]["1584"]
    loo = []
    for g in model.GOVS:
        r = model.solve(w, drop_govs=(g["n"],))
        pred = model.read_name(r["table"], g)
        tru = "".join(norm(ch) for ch in g["name"])
        loo.append(
            {
                "n": g["n"],
                "name": g["name"],
                "pred": pred,
                "exact": pred == tru,
                "letters_right": sum(a == b for a, b in zip(pred, tru, strict=False)),
                "len": len(tru),
            }
        )
    out["loo_1584"] = {
        "exact": sum(x["exact"] for x in loo),
        "n": len(loo),
        "letters_right": sum(x["letters_right"] for x in loo),
        "letters": sum(x["len"] for x in loo),
        "detail": loo,
    }
    print("LOO exact", out["loo_1584"]["exact"], "/", len(loo))
    out["run"]["elapsed_s"] = round(time.time() - t0, 1)
    json.dump(out, open(R / "model_runs.json", "w"), indent=1)


if __name__ == "__main__":
    main("--quick" in sys.argv)
