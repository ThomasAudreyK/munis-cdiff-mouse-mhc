"""Summarize a MUNIS predictions CSV: top hits per MHC allele.

Usage: python scripts/summarize_results.py results/CspC_munis_predictions.csv
"""
import sys
import pandas as pd

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python summarize_results.py <predictions csv>")
    path = sys.argv[1]
    df = pd.read_csv(path)

    for mhc, group in df.groupby("mhc"):
        top = group.sort_values("score", ascending=False).head(15)
        print(f"\n=== Top 15 for {mhc} (n={len(group)} peptides scored) ===")
        print(top[["pep", "score"]].to_string(index=False))

if __name__ == "__main__":
    main()
