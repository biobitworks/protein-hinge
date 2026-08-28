#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
mkdir -p build
cp neurips_2026.sty build/
cp main.tex references.bib checklist.tex build/
cp -r sections build/
cd build

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
