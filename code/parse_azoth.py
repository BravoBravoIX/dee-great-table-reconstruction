"""Parse AZOTH's Enochian Tools 1.2 (extract.c, 30 Aug 1993; Lysator archive
https://anna.lysator.liu.se/pub/magick/Enochian/Enochian_pgm/) for:
  - the governors' sigil coordinates (cgov1..cgov91), given on the Tabula Recensa
    in full-table (row, col) form, taken by AZOTH from the sigils in Denning &
    Phillips, Mysteria Magica, proofed against Crowley, Turner and James;
  - every other extraction rule (names of God, seniors, kings, angels ...);
  - the tables rtable (Recensa), otable (Recensa rearranged), dtable (AZOTH's
    'derived' table: Recensa retro-fitted to the names in Dee's Book of
    Supplications and Invocations, via Turner's Elizabethan Magic).
Writes JSON. Usage: parse_azoth.py EXTRACT_C OUT_JSON
"""

import json
import re
import sys


def main(src, out):
    t = open(src, encoding="latin-1").read()
    tables = {}
    for name in ("rtable", "otable", "dtable", "xdtable"):
        m = re.search(r"static char \*" + name + r"\[\] = \{[^\n]*\n(.*?)\};", t, re.S)
        tables[name] = re.findall(r'"([^"]*)"', m.group(1))
        assert len(tables[name]) == 27 and all(len(r) == 25 for r in tables[name]), name
    coords = {}
    for m in re.finditer(r"^COORD\s+(\w+)\[\]\s*=\s*\{([^}]*)\};", t, re.M):
        nums = [int(x) for x in re.findall(r"-?\d+", m.group(2).replace("END", ""))]
        coords[m.group(1)] = [(nums[k], nums[k + 1]) for k in range(0, len(nums), 2)]
    origins = {}
    for m in re.finditer(r"^ORIG\s+(\w+)\[\]\s*=\s*\{([^}]*)\};", t, re.M):
        origins[m.group(1)] = [x.strip() for x in m.group(2).split(",")]
    rules = {}
    for m in re.finditer(r"^RULE\s+(\w+)\s*=\s*\{(\w+),\s*(\w+),\s*(\w+)\};", t, re.M):
        rules[m.group(1)] = {"coord": m.group(2), "label": m.group(3), "origin": m.group(4)}
    json.dump(
        {"tables": tables, "coords": coords, "origins": origins, "rules": rules},
        open(out, "w"),
        indent=1,
    )
    gov = [k for k in coords if k.startswith("cgov")]
    print(len(gov), "governor coord sets;", len(rules), "rules")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
