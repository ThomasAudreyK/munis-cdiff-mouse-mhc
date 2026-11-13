"""Pivot a MUNIS predictions CSV to one row per peptide, one column per
allele, and flag peptides that score well across all alleles scored --
plausible universal/cross-presented candidates.

Usage: python scripts/cross_allele_summary.py results/CspC_munis_predictions.csv antigens/CspC.fasta
"""
import sys
import pandas as pd
from Bio import SeqIO


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python cross_allele_summary.py <predictions csv> <antigen fasta>")
    pred_path, fasta_path = sys.argv[1], sys.argv[2]

    df = pd.read_csv(pred_path)
    pivot = df.pivot_table(index="pep", columns="mhc", values="score").reset_index()

    allele_cols = [c for c in pivot.columns if c != "pep"]
    pivot["min_score"] = pivot[allele_cols].min(axis=1)
    pivot["mean_score"] = pivot[allele_cols].mean(axis=1)

    # Position within the antigen (first occurrence; note in the header if ambiguous)
    protein = str(next(SeqIO.parse(fasta_path, "fasta")).seq)
    positions = []
    for pep in pivot["pep"]:
        idx = protein.find(pep)
        positions.append(idx + 1 if idx >= 0 else -1)  # 1-indexed
    pivot["antigen_pos_1indexed"] = positions

    pivot = pivot.sort_values("min_score", ascending=False)

    out_path = pred_path.replace("_predictions.csv", "_cross_allele_summary.csv")
    pivot.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")

    print("\n=== Top 15 by min score across all alleles (candidates presented by all three) ===")
    print(pivot.head(15)[["pep", "antigen_pos_1indexed"] + allele_cols + ["min_score"]].to_string(index=False))


if __name__ == "__main__":
    main()
