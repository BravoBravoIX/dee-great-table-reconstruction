"""Parse the 1587 number cipher (Sloane 3191 / Cotton App. XLVI pt 2, 20 April 1587;
Klein lib. XIX pp. 27-30) from Rinasce Piu Gloriosa 2025, Appendix A (pdftotext
-layout output). Each row: given number, letter at that number on the Recensa (per
RPG), corrected number (blank = same, '?' = unclear), message letter.
Usage: parse_cipher.py PAPER_TXT OUT_JSON
"""

import json
import re
import sys


def main(txt, out):
    lines = open(txt, encoding="utf-8").read().split("\n")
    start = next(k for k, ln in enumerate(lines) if "Cipher solution" in ln)
    rows = []
    for ln in lines[start:]:
        s = ln.strip()
        m = re.match(r"^(\d+)\s+([a-zA-Z])\s+(?:(\??\d*|\?)\s+)?([a-zA-Z])$", s)
        if not m:
            m2 = re.match(r"^(\d+)\s+([a-zA-Z])\s+(\?\d*)\s+([a-zA-Z])$", s)
            if not m2:
                continue
            m = m2
        num, given, corr, msg = m.group(1), m.group(2), m.group(3), m.group(4)
        corr_n = None
        unclear = False
        if corr:
            if corr.startswith("?"):
                unclear = True
            else:
                corr_n = int(corr)
        rows.append(
            {
                "num": int(num),
                "rpg_letter_at_num": given,
                "corrected": corr_n,
                "unclear": unclear,
                "msg": msg,
            }
        )
    json.dump(rows, open(out, "w"), indent=0)
    print(len(rows), "cipher numbers;", "message:", "".join(r["msg"] for r in rows))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
