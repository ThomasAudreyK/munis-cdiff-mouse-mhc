#!/usr/bin/env bash
# One-time setup: clones MUNIS, applies the two local patches (see
# scripts/patch_munis.py), and installs a Python 3.11 virtualenv with
# everything it needs. Re-running is safe (idempotent).
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -d munis ]; then
    git clone https://github.com/jwohlwend/munis
fi

python3 scripts/patch_munis.py munis

if [ ! -d .venv ]; then
    uv venv --python 3.11 .venv
fi

uv pip install --python .venv/bin/python "torch==2.3.1" --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv/bin/python \
    "pytorch-lightning==2.0.2" "torchmetrics==1.4.0" "fair-esm==2.0.0" \
    "scikit-learn" "numpy==1.26.4" "scipy==1.11.3" "pandas==2.2.2" \
    "biopython==1.84" "wandb==0.18.2" "setuptools<81"

echo "Setup complete. Run scripts/run_predictions.sh next."
