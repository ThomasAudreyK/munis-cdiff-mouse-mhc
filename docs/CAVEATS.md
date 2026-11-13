# What to trust here, and what not to

## H2-Kb and H2-Db: reasonably trustworthy

MUNIS ships pseudo-sequences for `H2-Kb` and `H2-Db` already (checked
against your FASTAs in `mhc/H2Kb.fasta` and `mhc/H2Db.fasta` -- they match
exactly once the signal peptide is removed). These are classical MHC
class Ia alleles. They are two of the most heavily profiled mouse alleles
in mass-spec immunopeptidomics, which is what MUNIS is trained on, so
there is a real chance the model has seen ligands from these exact
molecules during training. Treat the scores as a genuine shortlist worth
testing, not a guess.

## Qa-1: a real caveat, not a technicality

Qa-1 (gene `H2-T23`) is **not** in MUNIS's built-in allele list. We added
it (`scripts/patch_munis.py`), which makes the model *runnable* on Qa-1,
but does not make it *validated* for Qa-1. Two separate problems:

1. **The FASTA you sent for Qa-1 was incomplete.** `QA1.fasta` (now kept
   as `mhc/QA1_as_received_INCOMPLETE.fasta` for the record) starts at
   `MLGYYNQS...`, which is missing roughly the first 100 residues of the
   mature chain -- the signal peptide and most of the alpha-1 domain, i.e.
   half the peptide-binding groove. We pulled the correct, full mature
   sequence from UniProt **P06339** (reviewed, Swiss-Prot, protein-level
   evidence, gene `H2-T23`) -- see `mhc/QA1_full_corrected.fasta` -- and
   used that instead. Your fragment is a verbatim substring of it, so this
   looks like a copy/trim error somewhere upstream, not a different
   molecule.

2. **MUNIS was almost certainly never trained on Qa-1 ligands at all.**
   Reading `munis/model.py`: the model doesn't use a fixed per-allele
   embedding lookup table -- the MHC's identity is conveyed entirely by
   feeding its literal protein sequence through an ESM protein language
   model, alongside the peptide. That's *why* it's technically possible to
   point it at an allele it never trained on. But Qa-1 is a non-classical,
   highly restrictive MHC-Ib molecule (it is the mouse functional
   counterpart of human HLA-E -- same biology, same problem). Standard
   mass-spec immunopeptidomics datasets, which is what MUNIS trains on,
   are dominated by classical class Ia alleles and essentially never
   include Qa-1 ligands in any volume. This is exactly the failure mode
   your other project (`HLA-E-Testing`) already documents for MUNIS on
   human HLA-E, for the same underlying reason.

**Bottom line:** treat Qa-1 scores from this pipeline as a hypothesis
generator, not a prediction. A high MUNIS score against Qa-1 is a peptide
worth testing at the bench (e.g. by stabilization assay or tetramer), not
evidence of presentation on its own. If this matters enough to publish
on, the only way to get a real Qa-1 predictor is measured binding data
(peptide-MHC stabilization, mono-allelic mass spec, or a Qa-1
tetramer/immunopeptidomics dataset) -- the same lesson as
`docs/USING_YOUR_OWN_DATA.md` in `HLA-E-Testing`.

## Other things worth knowing

- **`--use_flanks` was turned on.** The antigen FASTA is a whole protein
  (557aa), not a list of synthetic peptides, so we used MUNIS's
  flanking-residue mode, which is what the authors' own Colab notebook
  recommends for exactly this case (it lets the model see 5 residues of
  real sequence context on each side of the candidate peptide, rather than
  the placeholder `GGGGG`).
- **Peptide length window 8-11.** Covers the common range for classical
  MHC-I ligands. Kb is classically associated with 8mers, Db with 9mers;
  we scored both alleles across the full 8-11 range rather than
  pre-committing to one length.
- **This is a re-implementation detail, not a MUNIS bug:** the released
  checkpoints need `strict=False` and an explicit CPU `map_location` to
  load without a GPU -- this is the same patch the authors' own Colab
  notebook applies, not something we invented.
