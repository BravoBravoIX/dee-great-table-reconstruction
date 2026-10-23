# The Enochian Great Table, 1584 against 1587: a reconstruction with controls

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23470963.svg)](https://doi.org/10.5281/zenodo.23470963)

A study of how John Dee's and Edward Kelley's "Great Table" was made, copied and
changed. It weighs every surviving witness to each letter of the table, tests what
each kind of evidence can and cannot decide, and checks every result against
controls (shuffled or random data treated in exactly the same way).

This is a study of a text and its copies. It is not a decipherment, and it does not
claim to prove which letters the table "really" had. Where the evidence is short of
proof, it says "the evidence weighs toward".

October 2026. CPU only; the whole analysis reruns in a few minutes.

**Archived on Zenodo** with its paper, code, data and results: [doi:10.5281/zenodo.23470963](https://doi.org/10.5281/zenodo.23470963) (this DOI always opens the latest version; see How to cite at the end).

**The paper:** [`paper/great-table.pdf`](paper/great-table.pdf) (working paper, 6 pages: abstract,
method, results, discussion and references; built from `paper/great-table.typ` by
`paper/build.sh`). The README below covers the same ground in more detail.

## In short

| Question | Answer | How firm |
|---|---|---|
| On which arrangement of the four quarters was the 1587 number cipher built? | The reformed one, ORO MPH / MOR OIP, numbered row by row across the joined table | Settled: 190 of 196 numbers hit, against at most 48 in 10,000 shuffles |
| Are the cipher's well-known "off-by-one" slips scattered errors? | No. They form **one offset block, numbers 121 to 414**; outside it the numbers are exact | 8 switches between exact and slip, against 63 or more in every one of 10,000 shuffles |
| Which letters, 1584 or 1587, are best supported at the 26 disputed cells? | The **1584 letters**, at all 26, at the default weights; 24 keep it under nearly every weighting tried | Best-supported, not proved; the u/y cell of Aydropt is a tie |
| Do Kelley's 1587 changes look like corrections toward the governors' names? | No. They behave like random edits of the same shape, **except the one that fixes Aydropt** | p ≈ 0.45 (names broken), p ≈ 0.27 (names touched), p ≈ 0.012 (Aydropt fixed) |
| The 16 governors whose names do not read on the 1584 table: is the table wrong or the name? | **Undecided.** With only two witnesses, no method can tell from these documents | Shown by a known-answer test; two cells lean to the table |
| Does the rebuilt table really carry the names? | Yes. With each name hidden in turn, the table rebuilt without it predicts **71 of 87** names exactly; shuffled tables predict **0** | 0 in 1,000 shuffles; at most 4 with names moved to other paths |

## 1. The problem

**The table.** On 25 June 1584, in Cracow, Dee recorded four "Watchtowers", each a
grid of 13 rows by 12 columns of letters. They are named ORO, MOR, OIP and MPH after
the first letters of their middle rows. Joined by a "Black Cross" of 20 letters they
make one table of 27 rows by 25 columns. Dee joined them in the order ORO MOR / OIP MPH.
The diary copy is British Library, Cotton Appendix XLVI, part 1.

**The names.** A month earlier (21–23 May 1584) the angel Nalvage had dictated,
letter by letter, the names of 91 "governors" (the Parts of the Earth). Each name has
a sigil. Laid on the table, a sigil traces the seven cells that spell the name. On
the 1584 table, 16 of these names do not read exactly: 23 letters disagree.

**The reform.** On 20 April 1587 Kelley brought a "reformed" table (Sloane 3191 ff.
55v–56r, "Thus reformed by Raphael"; also in Cotton Appendix XLVI, part 2). It moves
three Watchtowers into the order ORO MPH / MOR OIP and changes 23 letters, twelve of
them by shifting one row of MOR one cell to the left. In the same month Dee recorded a
message enciphered as 196 running numbers on that table.

**The questions**, made checkable:
1. On which arrangement and numbering was the 1587 cipher built, and what do its
   slips say?
2. At each cell, which letter is best supported once every witness is weighed
   together: the manuscript copies, the names read along their sigils, names the
   angels spoke aloud in 1584, Dee's later working names, and the cipher?
3. How firm is each decision, and which disputes can the documents decide at all?

## 2. Sources

Each cell has nine witnesses. None of the third-party transcriptions or images is
included here (see Licensing); `scripts/fetch_sources.sh` downloads them from where
their owners publish them, and the code rebuilds the data from them.

| Id | Witness | Date | Read from |
|---|---|---|---|
| C1 | Cotton App. XLVI pt 1 (the 1584 diary) | 1584 | Vovina Archives cell renderings, by a glyph reader (our code) plus a check by Claude |
| S1 | Sloane 3191 "tabula originalis" (Dee's later copy) | after 1587 | same |
| S2 | Sloane 3191 "tabula recensa" | 1587 | same |
| C2 | Cotton App. XLVI pt 2, recensa | 1587 | same |
| RO, RR, RT | Rinasce Più Gloriosa (2025), figs 3, 4 and 8 (original, reformed, and their own "True Great Table"; after Klein 2020) | | the PDF's text layer |
| AR, AD | AZOTH (1993), *Enochian Tools*: the Recensa, and a "derived" table refitted to the names in Dee's Book of Supplications | | parsed from AZOTH's `extract.c` |

Other evidence:
- **The 91 names**, in diary order, checked against the OCR of Casaubon's 1659 print
  of the diaries (archive.org `truefaithfulrela00deej`, public domain): 67 match
  exactly; 24 are garbled by the OCR but consistent where legible; one letter stays
  open (Pristac/Pristag). Report: `results/tfr_name_check.txt`.
- **The sigil paths**, from AZOTH (1993), who retraced them from Denning & Phillips.
  They were checked three independent ways:
  - they reproduce the 2025 paper's 16 mismatching names exactly, and all 112 cells
    of those paths are the cells shaded in its fig. 2 (`results/check_paths.txt`);
  - 87 of the 88 path starts on the table are capital letters, as Burns & Moore
    (2010) said the capitals mark (`results/capitals.json`);
  - the 91 sigils tile the table almost exactly: 615 cells used once, one used twice
    (ORO 1.9, the L of both Lexarph and Lauacon), and eight unused, seven of which are
    the PARAOAN sigil itself, reading "Laxdixi" (1584) or "Laxdizi" (1587), as Burns &
    Moore reported (`results/coverage.json`).
- **Names spoken by the angels in 1584**: the bold letters of the 2025 paper's fig. 6,
  plus the R of PARAOAN.
- **The 1587 cipher**: 196 numbers and their message letters, from the 2025 paper's
  Appendix A (after Klein's edition).

The witnesses agree closely: only 26 of 624 cells are disputed. Of these, 23 are the
1587 changes the 2025 paper lists, and three are slips found only in Sloane 3191, each
outvoted by the other copies (OIP 9.2 l/b, OIP 11.8 z, MPH 11.11 p). The Cotton 1584
OIP leaves three cells empty (OIP 0.11, 1.10, 1.11); the other copies fill them, in
agreement with the name Vavaamp. Sloane 3191's "originalis" already carries the 1587
letters and the shifted row, so it is a copy made after the reform.

Cells are written `TABLE row.col`, rows 0–12 (row 6 is the middle row), columns 0–11.
Letters are compared case-folded with u = v.

**How AI was used.** The four manuscript witnesses were read from the Vovina Archives' typeset
renderings by our own glyph reader (nearest-neighbour code, `code/ocr_vovina.py`); the other
witnesses come from the 2025 paper's text layer and AZOTH's source code. Claude checked the cells
where the glyph reader disagreed with its seed or was unsure against the renderings; its 14
readings are recorded in `data/vovina_eyecheck.json`. An AI coding assistant (Claude Code) was used. Every step reruns without any AI service.

## 3. Method

**The model** (`code/model.py`, OR-Tools CP-SAT). The unknown is the letter of each of
the 624 cells. The model chooses the table that minimises the weighted disagreements
with every channel at once: the manuscript copies; each governor's name read along its
sigil; the spoken names; the Book of Supplications names; and, for the 1587 target,
the cipher. A name either reads exactly, or is "garbled" at a fixed cost plus a cost
per wrong letter, which ties together the seven cells of one name.

**Weights** were written down before any run (`code/model_config.json`). Default for
the 1584 target: 1584 copy 3, each 1587 copy 0.5, name letter 1 plus garbled name 1,
spoken name 2, Book of Supplications 0.5. The model was then rerun under 1,296
weightings, to show which decisions hold whatever one believes about the sources.
A cell's **margin** is the extra cost of forcing its runner-up letter.

**Held-out prediction.** Each governor's name is hidden in turn, the table is rebuilt
without it, and the name is read back off the rebuilt table.

**The cipher.** All 24 placements of the four quarters are scored, with running numbers
row by row and table by table, on three witnesses. Chance is set by 10,000 shuffles of
the message against the numbers. The slip pattern is tested against random placement
of the same number of slips.

**Controls** (`code/controls.py`, seed 20261019):
- shuffled grids, and names moved onto other sigil paths;
- 10,000 random corrections shaped like Kelley's (one row shift plus 11 single changes);
- a known-answer test: synthetic tables with 10 planted copy errors and 10 planted name
  errors, 200 trials, under three weightings, to see which kind of error the method
  can find.

## 4. Results, with controls

### The arrangement and the cipher's slips

| Hypothesis | Numbers that hit (exact or one below) | Chance (shuffled message) |
|---|---|---|
| 1587 arrangement, row-wise, 1587 letters (S2) | 190 / 196 (105 exact) | mean 26.6, max 48 |
| same, 1584 letters (C1) | 187 / 196 | mean 26.5, max 47 |
| 1584 arrangement, row-wise | 80 / 196 | mean 23.7, max 42 |
| best table-by-table numbering | 36 / 196 | |

In number order the slips form one block: exact up to 119, one below from 123 to 414
(with two isolated exact hits, at 151 and 228), exact again from 416, with a single
stray slip at 466. That is 8 switches between "exact" and "slip"; if the same slips
were scattered at random there would be about 90 (never fewer than 63 in 10,000
trials). So these are not 89 separate careless readings but one counting offset over
one stretch of the table.

Inside the exact stretch, MOR row 7 is read with the shifted (1587) letters at numbers
490–491; the 1584 row would need a "one above" slip, which happens nowhere else. The
cipher also reads 't' at ORO 7.0 and 'p' at OIP 11.3. So the cipher was worked on the
reformed table with the shifted row, which corrects the 2025 paper's view that the row
shift was not needed for the cipher. Six numbers stay unexplained (two of them the
2025 paper already marks unclear). Files: `results/cipher_test.json`,
`results/cipher_cells.json`, `results/cipher_slips.json`.

### Names on each table (87 governors; the three Black-Cross names and PARAOAN left out)

| Table | Names that do not read exactly | Letters |
|---|---|---|
| 1584, as in the 2025 paper (RO) | 16 | 23 |
| 1584, Cotton (C1; three empty cells) | 17 | 26 |
| 1587 (RR, C2) | 27 | 41 |
| AZOTH "derived" (Book of Supplications) | 15 | 20 |
| 2025 "True Great Table" (RT) | 15 | 22 |

### Does the reconstruction carry real information?

With each name hidden in turn, the rebuilt 1584 table predicts **71 of the 87** names
exactly (586 of 609 letters). Shuffled grids give **0** names in 1,000 tries (letters:
mean 51, max 74). Moving the names onto other paths gives at most 4, and the model's
cost rises from 77 to at least 648. (Counting all 91 names, 75 of 91.)

### Kelley's 1587 changes against random changes of the same shape

| | Real 1587 changes | Random changes (mean) | p |
|---|---|---|---|
| names broken | 12 | 12.7 | ≈ 0.45 |
| changed cells on the 16 mismatching names | 6 | 4.2 | ≈ 0.27 |
| names fixed | 1 (Aydropt) | 0.01 | ≈ 0.012 |

The old view that the Recensa was Kelley "fixing" the names (Wilson 2012) does not
hold up as a whole: the changes break and touch names at the random rate. The one
sign of a name-aware change is the u→y that fixes Aydropt.

### The 26 disputed cells

Every one takes the 1584 letter at the default weights. Of the 26, 24 keep it in at
least 1,116 of the 1,296 weightings (23 in at least 1,269; MPH 10.5 in 1,116), with
margins of 2 to 6 cost units. The two exceptions:
- **ORO 0.7 u/y** (Aydropt / Audropt) is an exact tie at the default weights, and the
  sweep leans to the 1587 'y' (858 of 1,296). This fits the diary's "both names be
  true".
- **MOR 7.4** splits n / m / c (666 / 531 / 99), because it is also the cell of
  Orcamir's m/n conflict.

Per-cell detail: `results/disputed_cells.csv`. The full rebuilt tables (1584 and 1587
targets) and the sweep tallies: `results/model_runs.json`.

### The 16 name conflicts: what the documents cannot decide

Known-answer test (planted errors, 200 trials; how often the true letter came back):

| Weighting | Planted copy errors | Planted name errors | Where a spoken name covers the cell (copy / name) |
|---|---|---|---|
| default (trust the copy) | 0 % | 100 % | 3 % / 100 % |
| trust the names | 100 % | 0 % | 100 % / 0 % |
| balanced | 0 % (ties) | 100 % | 100 % / 100 % |

With only a table letter and a name letter, the "reconstruction" just returns the
prior: whichever source one trusts more wins. Only a third witness decides, and then
only if it is not outweighed. At 21 of the 23 conflicting letters there is no third
witness. At the other two, ORO 4.6 (Tahando, m/n) and ORO 6.9 (Chirspa, z/s), names
the angels spoke in 1584 side with the table letter.

## 5. Verdict

- **Arrangement:** a unique answer. The cipher was made on ORO MPH / MOR OIP, numbered
  row by row, with one offset block (121–414). No other placement comes close.
- **Letters at the 26 disputed cells:** the evidence weighs toward the 1584 (Cotton)
  letters, as the 2025 paper proposed. ORO 0.7 (u/y) stays undecided. Kelley's changes
  look like copying changes, not corrections, apart from Aydropt; the shifted MOR row,
  't' at ORO 7.0 and 'p' at OIP 11.3 are the letters he actually worked the cipher on.
- **The 16 governor-name conflicts:** undecided by these documents. The model makes
  the dependence on one's trust in each source explicit instead of hiding it in a
  choice. Two (Tahando, Chirspa) lean toward the table letter.

## 6. What is new, and what earlier work did

Much of the ground here was broken by others, and this study stands on their work:

- **Dee himself** made the first rectification: the Sloane 3191 copy with reformed
  letters, and Liber Scientiae, where in some squares he wrote both the table letter
  and the name letter.
- **The Golden Dawn** answered the governor dilemma with multi-lettered squares in its
  Recensa (Hulse, as reported by Burns & Moore).
- **AZOTH, *Enochian Tools* 1.2 (1993)**, a C program that extracts every name from
  either table, a "derived" table refitted to the Book of Supplications names, and a
  comparison of 31 names across Turner, James and Crowley. This is the earliest
  computational work on the problem we found, and **its sigil coordinates are used
  here**.
- **Teresa Burns & J. Alan Moore** (*Journal of the Western Mystery Tradition*,
  2010, parts I–III): a rectified table, PARAOAN as a "blind" whose sigil reads
  Laxdizi, and the capitals as the first letters of the governors' names, all of which
  this study confirms by count.
- **Other rectifications and readings:** Stenwick, *Mastering the Great Table* (2013;
  probability testing that favoured the Recensa); Wilson (2012; Kelley "fixed" the
  names); Klein (2020; Kelley's errors, and the edition our cipher data comes through);
  Leitch (2014; the reform served the cipher); DuQuette (2008; the Recensa, but the
  originals where the angels used them).
- **Frater Rinasce Più Gloriosa, "Reconstructing the True Great Table"** (enochian.blog,
  12 December 2025): a careful manual comparison listing the 16 name mismatches and the
  23 changes, the cipher solution in Appendix A, and a proposed "True Great Table"
  (the 1587 arrangement with the 1584 letters, keeping u→y, leaving c/t open). Our
  letter verdict agrees with theirs.
- **Vovina Archives**: clear renderings of the four manuscript tables, from which the
  manuscript witnesses here were read, and an essay on the arrangement.

What this study adds, as far as our search found (GitHub and the web, October 2026,
including the previous 60 days; see Open checks):
1. A cell-level, machine-readable comparison of four manuscript witnesses and five
   secondary ones, with every disputed cell listed (26), including three slips found
   only in Sloane 3191 and the three empty Cotton OIP cells.
2. One formal model of every extraction channel, with weights declared in advance, a
   1,296-weighting robustness sweep, a firmness margin per cell, and held-out
   prediction against shuffled controls.
3. A known-answer test that separates what the documents can decide (the arrangement,
   the 26 copy disputes) from what they cannot (21 of the 23 name conflicts).
4. The cipher's slips shown to be **one contiguous offset (121–414)** rather than
   scattered errors, and with that the cipher fixing the shifted MOR row, 't' at ORO
   7.0 and 'p' at OIP 11.3 as the letters the cipher was worked on.
5. A significance test of the claim that the Recensa fixed the names: it does not,
   except for Aydropt.

## 7. Open checks

These could firm up or change the results, and need sources we could not read:
1. **Klein's edition, lib. XIX p. 28 (pp. 27–30)**: Dee's margin note on the
   off-by-one numbers. Did he already see the block, and do its edges (120/121 and
   414/415) match anything he wrote? If so, the block finding is his, not ours.
2. **Print-only books**, not read: Klein (2020), Stenwick (2013), Hulse, Leitch (2014),
   Wilson (2012), and Jones, *The Evolution of the Tablets* (the online copy refused
   access). Any of them may already contain points listed above as new.
3. **Liber Scientiae** (Sloane 3191): Dee's own spellings and multi-letter squares for
   the 16 names. A later Dee witness, not an independent one.
4. **The diary's pronunciation notes** (e.g. Virochi "ki", Nociabi "ci") as a third
   witness for some name letters.
5. **Capitals in Cotton**, where the glyph reader was least sure of case.
6. **The manuscripts themselves.** The manuscript witnesses were read from Vovina's
   renderings, not from images of the manuscripts; a check against the British
   Library images would remove that step.

## 8. How to reproduce

Needs Linux or macOS with `python3`, [`uv`](https://docs.astral.sh/uv/) (which fetches
pdfplumber, Pillow, NumPy and OR-Tools on the fly), `pdftotext` (poppler) and `curl`.

```
scripts/fetch_sources.sh sources/downloads    # about 6 MB; checks SHA-256 sums
code/run_all.sh sources/downloads             # a few minutes on one CPU
git diff --stat results/                      # should be empty apart from the run record
```

`fetch_sources.sh` checks each download against `sources/SHA256SUMS`, the copies the
published results were made from (downloaded 19 October 2026). If a source has changed
since, the script warns and the results may differ. From these copies the pipeline
rebuilds every data file and result byte for byte, except the run record at the top
of `results/model_runs.json` (Python version, commit, time taken).

Rebuilt data that copies the sources (the nine-witness cell table, the sigil paths, the
spoken cells, the full cipher table) lands in `data/` and `data/private/`, which git
ignores, so a rebuild never republishes it by accident.

Main files: `code/model.py` (the model), `code/run_model.py` (default runs, margins,
sweep, held-out names), `code/controls.py` (controls and the known-answer test),
`code/cipher_test.py`, `code/cipher_cells.py`, `code/cipher_slips.py` (the cipher),
`code/ocr_vovina.py` (the glyph reader), `code/build_data.py` (the witness table).

## Licensing

- **Code** (`code/`, `scripts/`): MIT, see `LICENSE`.
- **Our data and results** (`data/`, `results/`): CC BY-NC-SA 4.0
  (https://creativecommons.org/licenses/by-nc-sa/4.0/). They are our own work, but the
  manuscript readings rest in part on the Vovina Archives renderings, which are
  CC BY-NC-SA 4.0, so we keep the same terms for everything derived from them.
  - `data/vovina_eyecheck.json` is our check of cells in the Vovina Archives
    renderings, made by Claude ("Vovina archives" by vovina, CC BY-NC-SA 4.0,
    https://vovina-archives.statichost.eu/docs/license/), under the same licence.
  - `data/name_sources.json` is our notes on each governor's name, citing Casaubon
    (1659), AZOTH (1993), Turner, James, Crowley and the 2025 paper.
  - `code/names_seed.py` lists the 91 names as dictated in 1584 (public domain).

**Left out, and why:**
- **The 2025 paper's PDF, figures, tables and Appendix A** (© Enochian Corner): not
  redistributed. The fetch script downloads the PDF from enochian.blog; the code reads
  the grids and the cipher table from it locally. The published `results/cipher_cells.json`
  leaves out the message letters so that Appendix A is not reproduced.
- **The Vovina Archives images** (CC BY-NC-SA 4.0): not redistributed; fetched from the
  Vovina site. Our cell-by-cell transcription made from them (`data/cells.json`) is
  rebuilt locally rather than published, because it also carries the 2025 paper's and
  AZOTH's grids.
- **AZOTH's *Enochian Tools*** (1993): it states no licence, so neither the source nor
  its tables and sigil coordinates are included; the fetch script downloads
  `extract.c` from the Lysator archive.
- **Casaubon (1659) OCR**: public domain, but large; fetched from archive.org.
- **Peterson's editions** (esotericarchives.com, copyright): not used for the data and
  not included.
- No manuscript images are included.

## References

- John Dee, diaries: British Library Cotton Appendix XLVI; Sloane MS 3191.
- Meric Casaubon, *A True & Faithful Relation* (London, 1659); OCR at
  https://archive.org/details/truefaithfulrela00deej
- AZOTH, *Enochian Tools* 1.2 (30 August 1993),
  https://anna.lysator.liu.se/pub/magick/Enochian/Enochian_pgm/
- Teresa Burns and J. Alan Moore, "John Dee and Edward Kelley's Great Table",
  *Journal of the Western Mystery Tradition* (2010), http://www.jwmt.org/v2n19/john.html
- Frater Rinasce Più Gloriosa, "Reconstructing the True Great Table", enochian.blog,
  12 December 2025, https://enochian.blog/posts/reconstructing-the-true-great-table/
- Vovina Archives, Tabula Originalis and Tabula Recensa,
  https://vovina-archives.statichost.eu/docs/tabula-recensa-1/
- Klein (2020); Stenwick (2013); Wilson (2012); Leitch (2014); DuQuette (2008); Denning
  & Phillips, *Mysteria Magica*; Turner, *Elizabethan Magic* (1989); G. James,
  *Enochian Evocation* (1984); Crowley, *Liber Chanokh*.

## How to cite

Burford, B. (2026). A computational reconstruction of John Dee's Great Table (1584 and 1587). Zenodo. https://doi.org/10.5281/zenodo.23470963 (this DOI always points to the latest version; each release has its own version DOI on Zenodo).
