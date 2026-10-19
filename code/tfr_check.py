"""Check each governor name against the OCR of Casaubon's 1659 True & Faithful
Relation (archive.org truefaithfulrela00deej, public domain), pages with the
91 names delivered by Nalvage on 21-23 May 1584.

For each name, report the best fuzzy-matching token (letters only, spaces in
spelled-out forms removed) inside the OCR line range, and its line.
Usage: tfr_check.py OCR_TXT NAMES_JSON
"""

import difflib
import json
import re
import sys

LO, HI = 20340, 21420  # OCR lines spanning TFR pp. 113-160 name deliveries


def main(ocr, names_path):
    lines = open(ocr, encoding="utf-8", errors="replace").read().split("\n")[LO:HI]
    cands = []
    for k, ln in enumerate(lines):
        # spelled-out capitals ("T A S T O X O") -> join
        caps = re.sub(r"(?<=[A-Z])[ .,]+(?=[A-Z])", "", ln)
        for tok in re.findall(r"[A-Za-z]{4,}", caps) + re.findall(r"[A-Za-z]{4,}", ln):
            cands.append((tok.lower().replace("v", "u"), LO + k + 1, ln.strip()))
    names = json.load(open(names_path))
    out = {}
    for g in names:
        n = g["name"].lower().replace("v", "u")
        best = max(cands, key=lambda c: difflib.SequenceMatcher(None, n, c[0]).ratio())
        r = difflib.SequenceMatcher(None, n, best[0]).ratio()
        out[g["n"]] = {"name": g["name"], "ocr": best[0], "ratio": round(r, 2), "line": best[1]}
        print(f"{g['n']:3d} {g['name']:9s} {best[0]:12s} {r:.2f} L{best[1]}  {best[2][:60]}")
    return out


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
