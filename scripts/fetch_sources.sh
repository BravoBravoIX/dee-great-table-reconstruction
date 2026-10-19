#!/usr/bin/env bash
# Download the public sources this study is built from, into SOURCE_DIR, and check
# them against the SHA-256 sums of the copies used for the published results.
# None of these files is redistributed here; each stays under its own terms.
# Usage: scripts/fetch_sources.sh SOURCE_DIR
set -euo pipefail
SUMS="$(cd "$(dirname "$0")/.." && pwd)/sources/SHA256SUMS"
OUT="$1"
mkdir -p "$OUT"/eblog "$OUT"/lysator "$OUT"/vovimg "$OUT"/tfr1659
get() { [ -s "$2" ] || curl -fsSL --retry 3 -o "$2" "$1"; }

# Frater Rinasce Piu Gloriosa, "Reconstructing the True Great Table" (enochian.blog, 12 Dec 2025)
get https://enochian.blog/pdfs/reconstructing-the-true-great-table.pdf "$OUT/eblog/paper.pdf"
# AZOTH, Enochian Tools 1.2 (30 Aug 1993), Lysator archive
get https://anna.lysator.liu.se/pub/magick/Enochian/Enochian_pgm/extract.c "$OUT/lysator/extract.c"
# Casaubon, A True & Faithful Relation (1659), archive.org OCR (public domain)
get https://archive.org/download/truefaithfulrela00deej/truefaithfulrela00deej_djvu.txt "$OUT/tfr1659/tfr_djvu.txt"
# Vovina Archives watchtower renderings (CC BY-NC-SA 4.0)
for stem in oroibAhaozpi MOrdialhCtGa oiPteaapDoce mpharslgaiol; do
  for v in cotton 3191 3191-recensa cotton-recensa; do
    get "https://vovina-archives.statichost.eu/images/91-parts-of-the-earth/${stem}-${v}-labeled.png" \
      "$OUT/vovimg/${stem}-${v}-labeled.png"
  done
done

cd "$OUT"
if sha256sum --quiet -c "$SUMS"; then
  echo "all sources match the copies used for the published results"
else
  echo "WARNING: a source differs from the copy used for the published results." >&2
  echo "The rebuild may still run, but results can differ (see README, How to reproduce)." >&2
fi
