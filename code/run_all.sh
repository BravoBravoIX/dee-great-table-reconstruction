#!/usr/bin/env bash
# Rebuild every data file and result from the public sources.
# Usage: code/run_all.sh SOURCE_DIR
#   SOURCE_DIR is the folder filled by scripts/fetch_sources.sh:
#     eblog/paper.pdf       the 2025 paper (its text layer is made here with pdftotext -layout)
#     lysator/extract.c     AZOTH, Enochian Tools 1.2 (1993)
#     vovimg/*.png          the 16 Vovina Archives watchtower renderings
#     tfr1659/tfr_djvu.txt  archive.org OCR of Casaubon 1659
# Needs: python3, uv (fetches pdfplumber, pillow, numpy, ortools), pdftotext (poppler).
# Third-party extractions go to data/private/ (git-ignored, never published).
set -euo pipefail
SRC="$(cd "$1" && pwd)"
cd "$(dirname "$0")"
mkdir -p ../data/private ../results
UVR="uv run --no-project"
[ -s "$SRC/eblog/paper.txt" ] || pdftotext -layout "$SRC/eblog/paper.pdf" "$SRC/eblog/paper.txt"
$UVR --with pdfplumber python extract_rpg_pdf.py "$SRC/eblog/paper.pdf" ../data/private/rpg2025_figs.json
python3 make_seed.py ../data/private/rpg2025_figs.json ../data/private/rpg_orig_split.json ../data/private/rpg_rec_split.json
nice -n 19 $UVR --with pillow --with numpy python ocr_vovina.py "$SRC/vovimg" ../data/private/rpg_orig_split.json ../data/private/vovina_ocr.json
python3 parse_azoth.py "$SRC/lysator/extract.c" ../data/private/azoth.json
python3 names_seed.py ../data/private/names_seed.json
python3 tfr_check.py "$SRC/tfr1659/tfr_djvu.txt" ../data/private/names_seed.json > ../results/tfr_name_check.txt
python3 parse_cipher.py "$SRC/eblog/paper.txt" ../data/private/cipher1587.json
python3 build_data.py
python3 spoken.py
python3 coverage.py
python3 capitals.py
python3 score_names.py | tee ../results/score_names.txt
python3 check_paths.py | tee ../results/check_paths.txt
python3 cipher_test.py ../results/cipher_test.json
python3 cipher_cells.py ../results/cipher_cells.json
python3 cipher_slips.py
nice -n 19 $UVR --with ortools python run_model.py
nice -n 19 $UVR --with ortools python controls.py
echo "done. Compare with the published results: git diff --stat results/"
