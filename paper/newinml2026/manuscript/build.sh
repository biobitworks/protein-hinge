#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
mkdir -p build
cp neurips_2026.sty build/
cp main.tex references.bib build/
# NeurIPS explicitly requires deletion of the checklist instruction block while
# retaining the checklist heading/questions/answers/guidelines. Preserve the
# source template verbatim, but strip only the marked instruction block in the
# submission build copy.
awk '
  /%%% BEGIN INSTRUCTIONS %%%/ { skip=1; next }
  /%%% END INSTRUCTIONS %%%/   { skip=0; next }
  !skip { print }
' checklist.tex > build/checklist.tex
cp -r sections build/
cd build

# Fixed epoch for byte-identical PDF rebuilds (2026-08-29T00:00:00Z).
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1756425600}"

if command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode main.tex
  bibtex main || true
  pdflatex -interaction=nonstopmode main.tex
  pdflatex -interaction=nonstopmode main.tex
else
  docker run --rm -v "$ROOT/build:/work" -w /work texlive/texlive:latest \
    sh -c 'pdflatex -interaction=nonstopmode main.tex && (bibtex main || true) && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex'
fi

mv -f main.pdf ../main_smoke.pdf
echo "Wrote main_smoke.pdf"
