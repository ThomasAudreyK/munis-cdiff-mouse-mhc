"""Apply two local patches to a freshly cloned jwohlwend/munis checkout.

Run once, right after cloning, before installing dependencies:

    python scripts/patch_munis.py munis/

Patch 1 (from the authors' own Colab notebook): the released checkpoints
were saved with extra keys (the LM's contact/lm heads) that the inference
model no longer has, and were saved on GPU. load_from_checkpoint needs
strict=False and an explicit CPU map_location to load on a machine with no
GPU.

Patch 2 (ours, not from upstream): adds the C57BL/6 Qa-1b allele (gene
H2-T23) to munis/seqs.py. MUNIS ships pseudo-sequences for H2-Kb and H2-Db
already, but not for Qa-1 -- a non-classical MHC-Ib molecule, so this is
unlikely to be in its mass-spec training data at all. See docs/CAVEATS.md
before trusting predictions against it. Source sequence: UniProt P06339
(reviewed, Swiss-Prot), mature chain with the signal peptide removed,
verified 2026-11-13.
"""
import sys
from pathlib import Path

QA1_BLOCK = '''    # Qa-1b (gene H2-T23), the C57BL/6 (H2^b) non-classical MHC class Ib allele.
    # Not in the upstream MUNIS release; added locally. Mature chain (signal
    # peptide removed) from UniProt P06339 (reviewed, protein-level evidence),
    # confirmed against NCBI/MGI as the H2-T23 gene product. MUNIS's training
    # set (mass-spec immunopeptidomics) almost certainly contains no Qa-1
    # ligands, since it is a rare, highly restrictive non-classical molecule --
    # see docs/CAVEATS.md before trusting these scores.
    "Qa-1b": "HSLRYFTTAVSRPGLGEPRFIIVGYVDDTQFVRFDSDAENPRMEPRARWIEQEGPEYWERETWKARDMGRNFRVNLRTLLGYYNQSNDESHTLQWMYGCDVGPDGRLLRGYCQEAYDGQDYISLNEDLRSWTANDIASQISKHKSEAVDEAHQQRAYLQGPCVEWLHRYLRLGNETLQRSDPPKAHVTHHPRSEDEVTLRCWALGFYPADITLTWQLNGEELTQDMELVETRPAGDGTFQKWAAVVVPLGKEQYYTCHVYHEGLPEPLTLRWEPPPSTVSNMVIIAVLVVLGAVIILGAVVAFVMKRRRHIGVKGCYAHVLGSKSFQTSDWPQKA",
    "H2-T23": "HSLRYFTTAVSRPGLGEPRFIIVGYVDDTQFVRFDSDAENPRMEPRARWIEQEGPEYWERETWKARDMGRNFRVNLRTLLGYYNQSNDESHTLQWMYGCDVGPDGRLLRGYCQEAYDGQDYISLNEDLRSWTANDIASQISKHKSEAVDEAHQQRAYLQGPCVEWLHRYLRLGNETLQRSDPPKAHVTHHPRSEDEVTLRCWALGFYPADITLTWQLNGEELTQDMELVETRPAGDGTFQKWAAVVVPLGKEQYYTCHVYHEGLPEPLTLRWEPPPSTVSNMVIIAVLVVLGAVIILGAVVAFVMKRRRHIGVKGCYAHVLGSKSFQTSDWPQKA",
'''


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python patch_munis.py <path to cloned munis repo>")
    root = Path(sys.argv[1])
    model_py = root / "munis" / "model.py"
    seqs_py = root / "munis" / "seqs.py"

    # Patch 1: checkpoint loading
    text = model_py.read_text()
    old = "MunisModel.load_from_checkpoint(checkpoint)"
    new = 'MunisModel.load_from_checkpoint(checkpoint, strict=False, map_location="cpu")'
    if old in text:
        model_py.write_text(text.replace(old, new))
        print(f"Patched {model_py}")
    elif new in text:
        print(f"Already patched: {model_py}")
    else:
        sys.exit(f"Could not find expected checkpoint-loading line in {model_py}")

    # Patch 2: add Qa-1b
    text = seqs_py.read_text()
    if '"Qa-1b"' in text:
        print(f"Already patched: {seqs_py}")
        return
    marker = '    "HLA-A01:01":'
    if marker not in text:
        sys.exit(f"Could not find insertion point in {seqs_py}")
    seqs_py.write_text(text.replace(marker, QA1_BLOCK + marker, 1))
    print(f"Patched {seqs_py}")


if __name__ == "__main__":
    main()
