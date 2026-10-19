"""Split the RPG 2025 figure-3 (original) and figure-4 (recensa) grids into watchtowers."""

import json
import sys

from gt import split

figs = json.load(open(sys.argv[1]))
orig = [[c or " " for c in row] for row in figs["fig3"]["cells"]]
rec = [[c or " " for c in row] for row in figs["fig4"]["cells"]]
json.dump(split(orig, "original"), open(sys.argv[2], "w"), indent=1)
json.dump(split(rec, "recensa"), open(sys.argv[3], "w"), indent=1)
print(json.load(open(sys.argv[2]))["MOR"][7])
