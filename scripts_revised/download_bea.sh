#!/usr/bin/env bash
# Download BEA public bulk data (NO API key required). Run once.
#   bash scripts_revised/download_bea.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/bea_raw
UA="Mozilla/5.0"

echo "Downloading NIPA annual (all tables, ~12 MB)..."
curl -fSL --http1.1 -A "$UA" -o data/bea_raw/NipaDataA.txt \
  "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt"

echo "Downloading GDP-by-Industry (~2.4 MB)..."
curl -fSL --http1.1 -A "$UA" -o data/bea_raw/GDPbyInd.zip \
  "https://apps.bea.gov/industry/Release/ZIP/GDPbyInd.zip"

echo "Unzipping GDP-by-Industry..."
mkdir -p data/bea_raw/gdpind
unzip -o data/bea_raw/GDPbyInd.zip -d data/bea_raw/gdpind >/dev/null

echo "Done. Now run:  Rscript scripts_revised/extended_analysis.R"
