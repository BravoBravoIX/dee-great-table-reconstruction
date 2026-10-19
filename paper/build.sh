#!/bin/sh
# Builds paper/great-table.pdf from the Typst source (needs uv; fetches the typst package).
cd "$(dirname "$0")" && uv run --no-project --with typst==0.15.0 python -c "import typst; typst.compile('great-table.typ', output='great-table.pdf')"
