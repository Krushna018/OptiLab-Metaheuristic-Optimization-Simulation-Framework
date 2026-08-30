from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from optilab.experiments import run_study
from optilab.statistics import build_statistical_report


def main():
    out = ROOT / "results" / "quick_demo"
    # One trial per configuration and a smaller budget for a fast correctness/demo run.
    df = run_study(out, trials=1, budget=160)
    build_statistical_report(df, str(out))
    print(df.groupby("algorithm")["best_value"].median())
    print(f"Quick demo complete: {len(df)} runs written to {out}")


if __name__ == "__main__":
    main()
