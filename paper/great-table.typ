// Working paper for the dee-great-table-reconstruction repository. Build: paper/build.sh
#set document(title: "The Enochian Great Table, 1584 against 1587: a reconstruction with controls", author: "Brett Burford")
#set page(paper: "a4", margin: (x: 2.3cm, y: 2.4cm), numbering: "1")
#set text(font: ("Libertinus Serif", "New Computer Modern"), size: 10.5pt, lang: "en", region: "au")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: set block(above: 1.3em, below: 0.7em)
#show link: set text(fill: rgb("#1a4f8b"))
#set table(stroke: 0.4pt + luma(150), inset: 5pt)
#show table: set text(size: 9.2pt)
#show table: set par(justify: false)

#align(center)[
  #text(size: 16pt, weight: "bold")[The Enochian Great Table, 1584 against 1587: \ a reconstruction with controls]
  #v(0.5em)
  #text(size: 11pt)[Brett Burford]
  #v(0.2em)
  #text(size: 9pt)[ORCID #link("https://orcid.org/0009-0003-6599-8297")[0009-0003-6599-8297] · Independent researcher, Australia]
  #v(0.2em)
  #text(size: 9pt)[Working paper, version 1.1.1, 21 October 2026 (version 1.1, 19 October 2026) · not peer reviewed]
  #v(0.2em)
  #text(size: 9pt)[Code, data and results: #link("https://github.com/BravoBravoIX/dee-great-table-reconstruction")[github.com/BravoBravoIX/dee-great-table-reconstruction], #link("https://doi.org/10.5281/zenodo.23470963")[doi:10.5281/zenodo.23470963]]
]

#v(0.8em)
#block(inset: (x: 1.2cm))[
  #text(weight: "bold")[Abstract.] John Dee's and Edward Kelley's "Great Table" of 1584, four lettered Watchtowers joined by a Black Cross, survives in a 1584 form and in a "reformed" form of 1587 that rearranges the quarters and changes 23 letters. Which letters the table should carry has been argued over by practitioners and historians, most recently in a careful manual comparison published in December 2025. This paper weighs every surviving witness to each of the 624 cells at once (four manuscript witnesses read from published renderings, five secondary ones, the 91 governors' names read along their sigils, names the angels spoke aloud, Dee's later working names and the 1587 number cipher) in one constraint model with weights declared in advance, and checks every result against controls. The 1587 cipher was built on the reformed arrangement, numbered row by row (190 of 196 numbers hit, against at most 48 in 10,000 shuffles). Its well-known off-by-one slips are not scattered errors but one offset block over numbers 121–414 (8 switches between exact and slip, against at least 63 in every shuffle), which shows the cipher was worked on the reformed table with the shifted row of MOR. At all 26 disputed cells the evidence weighs toward the 1584 letters; with each name hidden in turn the rebuilt table predicts 71 of 87 names, against none for shuffled tables. Kelley's 1587 changes behave like random edits of the same shape, except the one that fixes the name Aydropt. A known-answer test shows that the 16 conflicts between the table and the governors' names cannot be decided from these documents.
]

= Introduction

On 25 June 1584, in Cracow, Dee recorded four "Watchtowers", each a grid of 13 rows by 12 columns of letters. They are named ORO, MOR, OIP and MPH after the first letters of their middle rows. Joined by a "Black Cross" of 20 letters they make one table of 27 rows by 25 columns. Dee joined them in the order ORO MOR / OIP MPH; the diary copy is British Library, Cotton Appendix XLVI, part 1.

A month earlier (21–23 May 1584) the angel Nalvage had dictated, letter by letter, the names of 91 "governors" (the Parts of the Earth), each with a sigil. Laid on the table, a sigil traces the seven cells that spell the name. On the 1584 table, 16 of these names do not read exactly: 23 letters disagree.

On 20 April 1587 Kelley brought a "reformed" table (Sloane MS 3191 ff. 55v–56r, "Thus reformed by Raphael"; also in Cotton Appendix XLVI, part 2). It moves three Watchtowers into the order ORO MPH / MOR OIP and changes 23 letters, twelve of them by shifting one row of MOR one cell to the left. In the same month Dee recorded a message enciphered as 196 running numbers on that table.

This paper asks three questions, each made checkable. On which arrangement and numbering was the 1587 cipher built, and what do its slips say? At each cell, which letter is best supported once every witness is weighed together? And how firm is each decision: which disputes can the documents decide at all?

= Earlier work

- *Dee himself* made the first rectification: the Sloane 3191 copy with reformed letters, and _Liber Scientiae_, where in some squares he wrote both the table letter and the name letter.
- *The Golden Dawn* answered the governor dilemma with multi-lettered squares in its Recensa (Hulse, as reported by Burns and Moore).
- *AZOTH*, _Enochian Tools_ 1.2 (1993): a C program that extracts every name from either table, a "derived" table refitted to the names in Dee's Book of Supplications, and a comparison of 31 names across Turner, James and Crowley. This is the earliest computational work on the problem we found, and its sigil coordinates are used here.
- *Burns and Moore* (2010): a rectified table, PARAOAN as a "blind" whose sigil reads Laxdizi, and the capitals as the first letters of the governors' names, all of which this study confirms by count.
- *Other rectifications and readings*: Stenwick (2013; probability testing that favoured the Recensa); Wilson (2012; Kelley "fixed" the names); Klein (2020; Kelley's errors, and the edition our cipher data comes through); Leitch (2014; the reform served the cipher); DuQuette (2008).
- *Frater Rinasce Più Gloriosa* (2025): a careful manual comparison listing the 16 name mismatches and the 23 changes, the cipher solution, and a proposed "True Great Table" (the 1587 arrangement with the 1584 letters, keeping u → y, leaving c/t open). Our letter verdict agrees with theirs.
- *The Vovina Archives*: clear renderings of the four manuscript tables, from which the manuscript witnesses here were read.

= Sources

Each cell has nine witnesses (Table 1). No third-party transcription or image is redistributed; a script fetches each from where its owner publishes it, checks its SHA-256 sum, and the code rebuilds the data locally.

#figure(
  table(
    columns: (auto, 1fr, auto, 1fr),
    align: left,
    table.header([*Id*], [*Witness*], [*Date*], [*Read from*]),
    [C1], [Cotton App. XLVI pt 1 (the 1584 diary)], [1584], [Vovina Archives cell renderings, by a glyph reader (our code) plus a check by Claude],
    [S1], [Sloane 3191 "tabula originalis" (Dee's later copy)], [after 1587], [same],
    [S2], [Sloane 3191 "tabula recensa"], [1587], [same],
    [C2], [Cotton App. XLVI pt 2, recensa], [1587], [same],
    [RO, RR, RT], [Rinasce Più Gloriosa (2025), figs 3, 4 and 8 (original, reformed, and their "True Great Table"; after Klein 2020)], [], [the PDF's text layer],
    [AR, AD], [AZOTH (1993): the Recensa, and a table refitted to the Book of Supplications names], [], [parsed from AZOTH's `extract.c`],
  ),
  caption: [The nine witnesses to each cell.],
)

The 91 names, in diary order, were checked against the OCR of Casaubon's 1659 print of the diaries (public domain): 67 match exactly, 24 are garbled by the OCR but consistent where legible, and one letter stays open (Pristac/Pristag). The sigil paths come from AZOTH, who retraced them from Denning and Phillips, and were checked three independent ways: they reproduce the 2025 paper's 16 mismatching names exactly, with all 112 cells of those paths shaded in its fig. 2; 87 of the 88 path starts on the table are capital letters, as Burns and Moore said the capitals mark; and the 91 sigils tile the table almost exactly (615 cells used once, one used twice, eight unused, seven of which are the PARAOAN sigil itself). Names spoken by the angels in 1584 are taken from the 2025 paper's fig. 6, and the 1587 cipher (196 numbers and their message letters) from its Appendix A, after Klein's edition.

The witnesses agree closely: only 26 of 624 cells are disputed. Of these, 23 are the 1587 changes and three are slips found only in Sloane 3191, each outvoted by the other copies. Sloane 3191's "originalis" already carries the 1587 letters and the shifted row, so it is a copy made after the reform. Cells are written `TABLE row.col`, rows 0–12 (row 6 is the middle row), columns 0–11; letters are compared case-folded with u = v.

= Method

*The model* (OR-Tools CP-SAT). The unknown is the letter of each of the 624 cells. The model chooses the table that minimises the weighted disagreements with every channel at once: the manuscript copies; each governor's name read along its sigil; the spoken names; the Book of Supplications names; and, for the 1587 target, the cipher. A name either reads exactly or is "garbled", at a fixed cost plus a cost per wrong letter, which ties the seven cells of one name together.

*Weights* were written down before any run. Default for the 1584 target: 1584 copy 3, each 1587 copy 0.5, name letter 1 plus garbled name 1, spoken name 2, Book of Supplications 0.5. The model was then rerun under 1,296 weightings, to show which decisions hold whatever one believes about the sources. A cell's _margin_ is the extra cost of forcing its runner-up letter.

*Held-out prediction.* Each governor's name is hidden in turn, the table is rebuilt without it, and the name is read back off the rebuilt table.

*The cipher.* All 24 placements of the four quarters are scored, with running numbers row by row and table by table, on three witnesses. Chance is set by 10,000 shuffles of the message against the numbers. The slip pattern is tested against random placement of the same number of slips.

*Controls* (seed 20261019): shuffled grids, and names moved onto other sigil paths; 10,000 random corrections shaped like Kelley's (one row shift plus 11 single changes); and a known-answer test, in which synthetic tables carry 10 planted copy errors and 10 planted name errors (200 trials, three weightings), to see which kind of error the method can find.

= Results

== The arrangement and the cipher's slips

#figure(
  table(
    columns: (1.8fr, 1fr, 1fr),
    align: (left, center, center),
    table.header([*Hypothesis*], [*Numbers that hit (exact or one below)*], [*Shuffled message*]),
    [1587 arrangement, row by row, 1587 letters (S2)], [190 / 196 (105 exact)], [mean 26.6, max 48],
    [same, 1584 letters (C1)], [187 / 196], [mean 26.5, max 47],
    [1584 arrangement, row by row], [80 / 196], [mean 23.7, max 42],
    [best table-by-table numbering], [36 / 196], [],
  ),
  caption: [Which arrangement the 1587 cipher was built on (`results/cipher_test.json`).],
)

In number order the slips form one block: exact up to 119, one below from 123 to 414 (with two isolated exact hits, at 151 and 228), exact again from 416, with a single stray slip at 466. That is 8 switches between "exact" and "slip"; if the same slips were scattered at random there would be about 90, and never fewer than 63 in 10,000 trials. These are not 89 separate careless readings but one counting offset over one stretch of the table.

Inside the exact stretch, MOR row 7 is read with the shifted (1587) letters at numbers 490–491; the 1584 row would need a "one above" slip, which happens nowhere else. The cipher also reads _t_ at ORO 7.0 and _p_ at OIP 11.3. So the cipher was worked on the reformed table with the shifted row, which corrects the 2025 paper's view that the row shift was not needed for the cipher. Six numbers stay unexplained, two of which the 2025 paper already marks unclear.

== Names on each table

Of the 87 governors (the three Black-Cross names and PARAOAN left out), 16 names (23 letters) do not read exactly on the 1584 table as given in the 2025 paper; 17 (26 letters) on Cotton, which leaves three cells empty; 27 (41 letters) on the 1587 table; 15 (20 letters) on AZOTH's derived table; and 15 (22 letters) on the 2025 "True Great Table".

== Does the reconstruction carry real information?

With each name hidden in turn, the rebuilt 1584 table predicts 71 of the 87 names exactly (586 of 609 letters). Shuffled grids give no names in 1,000 tries (letters: mean 51, max 74). Moving the names onto other paths gives at most 4, and the model's cost rises from 77 to at least 648.

== Kelley's 1587 changes against random changes of the same shape

#figure(
  table(
    columns: (2fr, 1fr, 1fr, auto),
    align: (left, center, center, center),
    table.header([], [*Real 1587 changes*], [*Random changes, mean*], [*p*]),
    [names broken], [12], [12.7], [≈ 0.45],
    [changed cells on the 16 mismatching names], [6], [4.2], [≈ 0.27],
    [names fixed], [1 (Aydropt)], [0.01], [≈ 0.012],
  ),
  caption: [The 23 changes of 1587 against 10,000 random changes of the same shape (`results/controls.json`).],
)

The view that the Recensa was Kelley "fixing" the names (Wilson 2012) does not hold up as a whole: the changes break and touch names at the random rate. The one sign of a name-aware change is the u → y that fixes Aydropt.

== The 26 disputed cells

Every one takes the 1584 letter at the default weights. Of the 26, 24 keep it in at least 1,116 of the 1,296 weightings (23 in at least 1,269; MPH 10.5 in 1,116), with margins of 2 to 6 cost units. The two exceptions: ORO 0.7 (u/y; Aydropt or Audropt) is an exact tie at the default weights, and the sweep leans to the 1587 _y_ (858 of 1,296), which fits the diary's "both names be true"; and MOR 7.4 splits n / m / c (666 / 531 / 99), because it is also the cell of Orcamir's m/n conflict. Per-cell detail is in `results/disputed_cells.csv`.

== The 16 name conflicts: what the documents cannot decide

#figure(
  table(
    columns: (1.4fr, 1fr, 1fr, 1.4fr),
    align: (left, center, center, center),
    table.header([*Weighting*], [*Planted copy errors recovered*], [*Planted name errors recovered*], [*Where a spoken name covers the cell (copy / name)*]),
    [default (trust the copy)], [0 %], [100 %], [3 % / 100 %],
    [trust the names], [100 %], [0 %], [100 % / 0 %],
    [balanced], [0 % (ties)], [100 %], [100 % / 100 %],
  ),
  caption: [Known-answer test: synthetic tables with planted errors, 200 trials (`results/controls.json`).],
)

With only a table letter and a name letter, the "reconstruction" returns the prior: whichever source one trusts more wins. Only a third witness decides, and then only if it is not outweighed. At 21 of the 23 conflicting letters there is no third witness. At the other two, ORO 4.6 (Tahando, m/n) and ORO 6.9 (Chirspa, z/s), names the angels spoke in 1584 side with the table letter.

= Discussion

*What the evidence weighs toward.* The arrangement has a unique answer: the cipher was made on ORO MPH / MOR OIP, numbered row by row, with one offset block (121–414), and no other placement comes close. At the 26 disputed cells the evidence weighs toward the 1584 (Cotton) letters, as the 2025 paper proposed; ORO 0.7 (u/y) stays undecided. Kelley's changes look like copying changes, not corrections, apart from Aydropt; the shifted MOR row, _t_ at ORO 7.0 and _p_ at OIP 11.3 are the letters he actually worked the cipher on. The 16 governor-name conflicts are undecided by these documents; the model makes the dependence on one's trust in each source explicit instead of hiding it in a choice. Two (Tahando, Chirspa) lean toward the table letter.

*What is new*, as far as a search of GitHub and the web in October 2026 found:
+ a cell-level, machine-readable comparison of four manuscript witnesses and five secondary ones, with every disputed cell listed, including three slips found only in Sloane 3191 and the three empty Cotton OIP cells;
+ one formal model of every extraction channel, with weights declared in advance, a 1,296-weighting robustness sweep, a firmness margin per cell, and held-out prediction against shuffled controls;
+ a known-answer test that separates what the documents can decide (the arrangement, the 26 copy disputes) from what they cannot (21 of the 23 name conflicts);
+ the cipher's slips shown to be one contiguous offset (121–414) rather than scattered errors, and with that the cipher fixing the shifted MOR row, _t_ at ORO 7.0 and _p_ at OIP 11.3 as the letters it was worked on;
+ a significance test of the claim that the Recensa fixed the names: it does not, except for Aydropt.

*Limits and open checks.*
+ The manuscript witnesses were read from the Vovina Archives renderings, not from images of the manuscripts; a check against the British Library images would remove that step.
+ Dee's margin note on the off-by-one numbers (Klein's edition, lib. XIX p. 28) was not read. If he already saw the block and its edges, the block finding is his, not ours.
+ Several print-only books were not read: Klein (2020), Stenwick (2013), Hulse, Leitch (2014), Wilson (2012), and Jones, _The Evolution of the Tablets_. Any of them may already contain points listed above as new.
+ _Liber Scientiae_ (Sloane 3191) and the diary's pronunciation notes could serve as further witnesses for some name letters; they were not used.
+ The best-supported letters are best-supported under declared weights, not proved; the sweep shows how much each depends on them.

= Data and code availability

Code (MIT) and our data and results (CC BY-NC-SA 4.0, because the manuscript readings rest in part on the Vovina Archives renderings, which carry that licence) are at #link("https://github.com/BravoBravoIX/dee-great-table-reconstruction")[github.com/BravoBravoIX/dee-great-table-reconstruction] and archived at #link("https://doi.org/10.5281/zenodo.23470963")[doi:10.5281/zenodo.23470963]. Third-party texts and images are not redistributed; the fetch script downloads them and checks their SHA-256 sums, and the pipeline rebuilds every data file and result byte for byte except the run record. This paper is released under CC BY-NC-SA 4.0.

= How AI was used

The four manuscript witnesses were read from the Vovina Archives' typeset renderings by our own glyph reader (nearest-neighbour code); the other witnesses come from the 2025 paper's text layer and AZOTH's source code. Claude checked the cells where the glyph reader disagreed with its seed or was unsure against the renderings; its 14 readings are recorded as data. An AI coding assistant (Claude Code) was used. Every step reruns without any AI service.

= Acknowledgements

This study stands on the work of AZOTH, Teresa Burns and J. Alan Moore, Frater Rinasce Più Gloriosa and the Vovina Archives, and on the editions of Casaubon and Klein. The author is responsible for any errors.

= References

#set par(hanging-indent: 1.2em, justify: false)
#set text(size: 9.5pt)

AZOTH (1993). _Enochian Tools_ 1.2. #link("https://anna.lysator.liu.se/pub/magick/Enochian/Enochian_pgm/")[anna.lysator.liu.se/pub/magick/Enochian/Enochian_pgm].

British Library, Cotton Appendix XLVI; Sloane MS 3191.

Burns, T. and Moore, J. A. (2010). John Dee and Edward Kelley's Great Table. _Journal of the Western Mystery Tradition_. #link("http://www.jwmt.org/v2n19/john.html")[jwmt.org/v2n19/john.html].

Casaubon, M. (1659). _A True & Faithful Relation of What Passed for Many Yeers between Dr. John Dee … and Some Spirits_. London. #link("https://archive.org/details/truefaithfulrela00deej")[archive.org/details/truefaithfulrela00deej].

Crowley, A. _Liber Chanokh_.

Denning, M. and Phillips, O. _Mysteria Magica_.

DuQuette, L. M. (2008). _Enochian Vision Magick_.

Frater Rinasce Più Gloriosa (2025). Reconstructing the True Great Table. enochian.blog, 12 December 2025. #link("https://enochian.blog/posts/reconstructing-the-true-great-table/")[enochian.blog/posts/reconstructing-the-true-great-table].

James, G. (1984). _Enochian Evocation of Dr John Dee_.

Klein (2020). Edition of Dee's spiritual diaries, through which the 2025 paper's cipher data come.

Leitch, A. (2014).

Stenwick, J. (2013). _Mastering the Great Table_.

Turner, R. (1989). _Elizabethan Magic_.

Vovina Archives. Tabula Originalis and Tabula Recensa. #link("https://vovina-archives.statichost.eu/docs/tabula-recensa-1/")[vovina-archives.statichost.eu/docs/tabula-recensa-1].

Wilson (2012).
