"""Shared helpers for the Great Table study.

Coordinates: a watchtower cell is (table, row, col) with table in ORO, MOR, OIP, MPH,
row 0..12, col 0..11 (row 6 is the linea spiritus sancti; cols 5 and 6 the linea
patris et filii). The full table is 27 x 25: two rows of watchtowers with the black
cross between them (row 13 and column 12).

Layouts (which watchtower sits in which quarter: TL, TR, BL, BR):
  original (Cotton App. XLVI, 1584, as Dee joined them): ORO MOR / OIP MPH
  recensa (Sloane 3191 ff. 55v-56r, 20 April 1587):      ORO MPH / MOR OIP
"""

TABLES = ("ORO", "MOR", "OIP", "MPH")
LAYOUTS = {
    "original": ("ORO", "MOR", "OIP", "MPH"),
    "recensa": ("ORO", "MPH", "MOR", "OIP"),
}
QUARTER_ORIGIN = {0: (0, 0), 1: (0, 13), 2: (14, 0), 3: (14, 13)}


def split(full, layout):
    """27 x 25 grid (list of lists or strings) -> {table: [13 strings of 12]}."""
    out = {}
    for q, t in enumerate(LAYOUTS[layout] if isinstance(layout, str) else layout):
        r0, c0 = QUARTER_ORIGIN[q]
        out[t] = ["".join(full[r0 + i][c0 + j] for j in range(12)) for i in range(13)]
    return out


def full_to_cell(r, c, layout):
    """Full-table (row, col) -> (table, row, col) or None for the black cross."""
    if r == 13 or c == 12:
        return None
    q = (0 if r < 13 else 2) + (0 if c < 12 else 1)
    r0, c0 = QUARTER_ORIGIN[q]
    t = (LAYOUTS[layout] if isinstance(layout, str) else layout)[q]
    return (t, r - r0, c - c0)


def cell_to_full(t, i, j, layout):
    lay = LAYOUTS[layout] if isinstance(layout, str) else layout
    q = lay.index(t)
    r0, c0 = QUARTER_ORIGIN[q]
    return (r0 + i, c0 + j)


def norm(ch):
    """Letter identity used for comparisons: case-folded, u = v (Dee uses them
    interchangeably; so does the angelic alphabet)."""
    ch = ch.lower()
    return "u" if ch == "v" else ch
