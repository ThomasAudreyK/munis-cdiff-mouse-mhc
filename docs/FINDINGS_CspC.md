# CspC vs H2-Kb / H2-Db / Qa-1: results

Full protein (557aa), every 8-11mer scored with flanking sequence context
(`--use_flanks`), against all three alleles. Raw scores:
`results/CspC_munis_predictions.csv` (6,582 peptide-allele rows).
Cross-allele pivot: `results/CspC_munis_cross_allele_summary.csv`.

**Read [`CAVEATS.md`](CAVEATS.md) first.** H2-Kb/H2-Db scores are a
reasonable shortlist. Qa-1 scores are extrapolation (Qa-1 is not in
MUNIS's training-relevant allele set) -- a hypothesis generator, not a
validated prediction.

## The headline finding: peptides that score high on all three molecules

Ranked by the *minimum* score across H2-Kb, H2-Db, and Qa-1b (i.e.
peptides that are not just a high score on one allele dragging the
average up):

| Peptide | Position (1-indexed) | H2-Db | H2-Kb | Qa-1b | min |
| --- | --- | --- | --- | --- | --- |
| IYLPNKNLI | 399 | 0.994 | 0.996 | 0.937 | 0.937 |
| FTQVLKTYL | 514 | 0.996 | 0.985 | 0.837 | 0.837 |
| AAITYVTNI | 223 | 0.993 | 0.996 | 0.818 | 0.818 |
| KNTIQQIANTL | 547 | 0.980 | 0.981 | 0.808 | 0.808 |
| TQVLKTYL | 515 | 0.861 | 0.935 | 0.711 | 0.711 |
| EIYTYPNV | 530 | 0.984 | 0.997 | 0.675 | 0.675 |
| NTIQQIANTL | 548 | 0.972 | 0.904 | 0.670 | 0.670 |

These cluster into essentially three regions of CspC, not seven
independent epitopes (the overlapping windows are the same underlying
stretch tiled at different lengths):

- **~position 399-407** (`IYLPNKNLI`) -- the single strongest hit, and
  the top-ranked candidate on every allele including Qa-1.
- **~position 511-538** (`FTQVLKTYL` / `TQVLKTYL` / `SLFTQVLKTYL` /
  `LSLFTQVLK` / `EIYTYPNV`) -- a broader stretch with several overlapping
  high-scoring windows, suggesting the whole region is a good antigen
  processing target, not just one 9mer.
- **~position 547-557** (`KNTIQQIANTL` / `NTIQQIANTL` / `TIQQIANTL`) --
  right at the protein's C-terminus.
- Plus one clean singleton: `AAITYVTNI` at position 223.

Practically: if your replacements in lab are designing synthetic
peptides or minigenes to chase the mechanism, these three regions (not
necessarily the single best 9mer from each) are where I'd start -- an
overlapping-peptide pool spanning roughly 395-410, 508-540, and 545-557
would cover all of the above with margin for register shifts.

## Per-allele top 15

See the console output of `scripts/summarize_results.py`, or:

```bash
.venv/bin/python scripts/summarize_results.py results/CspC_munis_predictions.csv
```

## What this does not tell you

- No claim about actual processing/TAP transport/proteasomal cleavage
  efficiency beyond what the flanking-residue model implicitly captures.
- No claim about immunogenicity -- MHC presentation is necessary, not
  sufficient, for a T cell response.
- Qa-1 numbers specifically should be read as "worth testing," full stop
  -- see `CAVEATS.md`.
