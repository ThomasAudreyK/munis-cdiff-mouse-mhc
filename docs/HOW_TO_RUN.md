# How to run this

Written for someone new to the command line.

## 1. Set up (once)

```bash
bash scripts/setup.sh
```

This clones the published MUNIS tool, applies two small local patches
(see `scripts/patch_munis.py` and `docs/CAVEATS.md`), and builds a Python
environment with everything it needs. Takes a few minutes, mostly
downloading PyTorch.

## 2. Run predictions

```bash
bash scripts/run_predictions.sh
```

With no arguments, this scores every 8-11mer in `antigens/CspC.fasta`
against `H2-Kb`, `H2-Db`, and `Qa-1b`, using flanking sequence context
(since the input is a whole protein, not synthetic peptides). It writes
`results/CspC_munis_predictions.csv`. Expect roughly 15-20 minutes on
CPU; the first run also downloads MUNIS's ~30MB ESM-2 language model
weights.

To score a different antigen or allele list:

```bash
bash scripts/run_predictions.sh antigens/your_antigen.fasta H2-Kb,H2-Db,Qa-1b results/your_run
```

## 3. Read the output

The output CSV has columns `prot, pep, left, right, mhc, score`.
`score` is MUNIS's predicted probability of mass-spec detection
(0 to 1, averaged across its 5-model ensemble), higher = more likely to
be a natural ligand of that MHC.

**Read `docs/CAVEATS.md` before acting on the Qa-1 scores specifically.**
H2-Kb and H2-Db are classical alleles MUNIS was plausibly trained on
directly. Qa-1 is not in MUNIS's released allele list at all -- we added
its sequence so the model runs, but there is good reason to think MUNIS's
training data contains no Qa-1 ligands, for the same reason human HLA-E
predictors struggle (documented in the sibling `HLA-E-Testing` project).
Treat Qa-1 hits as peptides worth testing at the bench, not as validated
predictions.

## If you get stuck

Paste the error back along with the command you ran.
