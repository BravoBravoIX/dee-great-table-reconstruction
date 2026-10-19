"""Where do the cipher's off-by-one slips fall? For every cipher number, whether
the message letter sits at n (exact) or n-1 (slip) on the recensa (S2 letters),
by full-table row and quarter. A slip confined to whole regions would point to a
numbering that counted an extra cell; scattered slips point to careless reading.
Writes results/cipher_slips.json."""

import json
from pathlib import Path

from cipher_cells import CELLS, CIPHER, numbering
from gt import norm

R = Path(__file__).resolve().parent.parent / "results"
num = numbering()
rows = []
for k, c in enumerate(CIPHER):
    m, n = norm(c["msg"]), c["num"]

    def at(x):
        cid = num.get(x)
        return norm(CELLS[cid]["read"]["S2"].split("/")[0]) if cid else None

    kind = "exact" if at(n) == m else "slip-1" if at(n - 1) == m else "other"
    cid = num.get(n)
    rows.append({"k": k, "n": n, "cell": cid, "kind": kind, "both": at(n) == m and at(n - 1) == m})
by_row = {}
for r in rows:
    if not r["cell"]:
        continue
    t, i, _j = r["cell"].split(".")
    key = f"{t}.{int(i):02d}"
    by_row.setdefault(key, {"exact": 0, "slip-1": 0, "other": 0})[r["kind"]] += 1
# runs: is the slip state autocorrelated in message order?
seq = [r["kind"] for r in rows if r["kind"] != "other"]
changes = sum(1 for a, b in zip(seq, seq[1:], strict=False) if a != b)
p_slip = seq.count("slip-1") / len(seq)
exp_changes = 2 * p_slip * (1 - p_slip) * (len(seq) - 1)
out = {
    "by_row": dict(sorted(by_row.items())),
    "changes_in_message_order": changes,
    "expected_changes_if_independent": round(exp_changes, 1),
    "rows": rows,
}
json.dump(out, open(R / "cipher_slips.json", "w"), indent=0)
for k, v in sorted(by_row.items()):
    print(k, v)
print("state changes along message:", changes, "expected if independent:", round(exp_changes, 1))
# in number order, ignoring numbers where n and n-1 carry the same letter
clear = sorted((r["n"], r["kind"]) for r in rows if not r["both"] and r["kind"] != "other")
blocks = []
for n, kind in clear:
    if blocks and blocks[-1][0] == kind:
        blocks[-1][2] = n
        blocks[-1][3] += 1
    else:
        blocks.append([kind, n, n, 1])
print("blocks in number order (kind, first n, last n, count):")
for b in blocks:
    print("  ", b)
out["blocks_in_number_order"] = blocks
# control: if slips were independent of position, how many exact/slip changes in
# number order? (shuffle the kinds over the numbers, 10,000 times, seed 20261019)
import random  # noqa: E402

kinds = [k for _n, k in clear]
obs_changes = sum(1 for a, b in zip(kinds, kinds[1:], strict=False) if a != b)
rng = random.Random(20261019)
null = []
for _ in range(10000):
    s = kinds[:]
    rng.shuffle(s)
    null.append(sum(1 for a, b in zip(s, s[1:], strict=False) if a != b))
p = (1 + sum(1 for x in null if x <= obs_changes)) / (1 + len(null))
out["number_order_changes"] = {
    "observed": obs_changes,
    "null_mean": sum(null) / len(null),
    "null_min": min(null),
    "p": p,
}
print(
    "changes in number order:",
    obs_changes,
    "null mean",
    sum(null) / len(null),
    "min",
    min(null),
    "p",
    p,
)
json.dump(out, open(R / "cipher_slips.json", "w"), indent=0)
