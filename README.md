# MUNIS on mouse MHC: CspC against H2-Kb, H2-Db, Qa-1

Scoring 8-11mers from a *C. difficile* antigen (CspC, discovered to elicit
sterilizing immunity in C57BL/6 mice) for presentation on the three mouse
MHC-I molecules relevant to a B6 immune response: the two classical
alleles **H2-Kb** and **H2-Db**, and the non-classical **Qa-1**.

This is a separate, unrelated project from `HLA-E-Testing` (human
HLA-E / malaria): different tool (MUNIS, not EHLAstic), different species,
different antigen. The two repos share no code; `HLA-E-Testing`'s
discussion of why MUNIS fails on human HLA-E is exactly the reasoning
behind the Qa-1 caveat here (Qa-1 is HLA-E's mouse functional
counterpart).

**Read [`docs/CAVEATS.md`](docs/CAVEATS.md) before trusting the Qa-1
numbers.** H2-Kb/H2-Db are classical alleles MUNIS plausibly trained on
directly. Qa-1 is not in MUNIS's released allele list and is unlikely to
be well represented in its training data at all -- treat those scores as
a shortlist to test, not a result.

## What is here

| Path | What it is |
| --- | --- |
| `antigens/CspC.fasta` | The *C. difficile* antigen. |
| `mhc/H2Kb.fasta`, `mhc/H2Db.fasta` | The classical alleles, as supplied. |
| `mhc/QA1_as_received_INCOMPLETE.fasta` | The Qa-1 FASTA as supplied -- kept for the record. It is missing ~100 N-terminal residues. |
| `mhc/QA1_full_corrected.fasta` | The correct, full Qa-1b sequence (UniProt P06339), used for the actual predictions. |
| `mhc/original_munis_colab_code.txt` | The original Colab cell MUNIS was run from, for reference. |
| `scripts/setup.sh` | Clones MUNIS and builds the environment. Run once. |
| `scripts/patch_munis.py` | The two local patches to MUNIS (checkpoint loading on CPU, and adding Qa-1). |
| `scripts/run_predictions.sh` | Runs the actual scoring. |
| `docs/HOW_TO_RUN.md` | Step-by-step instructions. |
| `docs/CAVEATS.md` | What to trust and what not to, in detail. |
| `results/` | Output lands here. |

## Quick start

```bash
bash scripts/setup.sh
bash scripts/run_predictions.sh
```

See [`docs/HOW_TO_RUN.md`](docs/HOW_TO_RUN.md) for details, and
[`docs/CAVEATS.md`](docs/CAVEATS.md) before acting on any Qa-1 result.

## Why MUNIS, and why this needed two small patches

[MUNIS](https://github.com/jwohlwend/munis) (Wohlwend et al.) predicts
whether a peptide-MHC pair would be detected in mass-spec
immunopeptidomics, using an ESM protein-language-model encoding of the
MHC's sequence plus the candidate peptide -- not a fixed table of trained
alleles. That architecture is exactly why it's possible to point it at
Qa-1, an allele it ships no pseudo-sequence for: the allele name is just
a lookup key into a sequence dictionary (`munis/seqs.py`), and the model
itself conditions on the literal sequence string, not an allele index.

Two patches were needed to make this run at all, both documented in
`scripts/patch_munis.py`:

1. The released checkpoints need `strict=False` and a CPU `map_location`
   to load without a GPU -- taken directly from the authors' own Colab
   notebook (`mhc/original_munis_colab_code.txt`), not something we
   invented.
2. Qa-1b's sequence was added to `munis/seqs.py`, since it isn't in the
   upstream release.
