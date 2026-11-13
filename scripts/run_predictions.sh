#!/usr/bin/env bash
# Scores every 8-11mer in antigens/CspC.fasta against H2-Kb, H2-Db, and
# Qa-1b. Takes ~15-20 minutes on CPU for a ~550aa protein.
#
# Usage: scripts/run_predictions.sh [fasta file] [mhc list] [outdir]
set -euo pipefail
cd "$(dirname "$0")/.."

FASTA="${1:-antigens/CspC.fasta}"
MHC="${2:-H2-Kb,H2-Db,Qa-1b}"
OUTDIR="${3:-results}"

mkdir -p "$OUTDIR" cache

.venv/bin/python munis/predict.py \
    --fasta "$FASTA" \
    --mhc "$MHC" \
    --min_len 8 --max_len 11 \
    --use_flanks \
    --device cpu \
    --batch_size 64 \
    --cache cache \
    --outdir "$OUTDIR"
