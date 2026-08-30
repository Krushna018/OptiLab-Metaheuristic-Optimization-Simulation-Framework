from __future__ import annotations

from itertools import combinations
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon


def summarize_runs(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["problem", "family", "algorithm"], as_index=False)
          .agg(
              mean_best=("best_value", "mean"),
              median_best=("best_value", "median"),
              std_best=("best_value", "std"),
              mean_runtime=("runtime_seconds", "mean"),
          )
    )


def per_problem_ranks(df: pd.DataFrame) -> pd.DataFrame:
    med = df.groupby(["problem", "algorithm"], as_index=False)["best_value"].median()
    med["rank"] = med.groupby("problem")["best_value"].rank(method="average", ascending=True)
    return med


def friedman_test(df: pd.DataFrame) -> dict:
    med = df.groupby(["problem", "algorithm"], as_index=False)["best_value"].median()
    pivot = med.pivot(index="problem", columns="algorithm", values="best_value").dropna()
    arrays = [pivot[c].to_numpy() for c in pivot.columns]
    stat, p = friedmanchisquare(*arrays)
    return {"statistic": float(stat), "p_value": float(p), "algorithms": list(pivot.columns), "n_problems": int(len(pivot))}


def pairwise_wilcoxon_holm(df: pd.DataFrame) -> pd.DataFrame:
    """Pairwise Wilcoxon tests on per-problem median outcomes with Holm correction."""
    med = df.groupby(["problem", "algorithm"], as_index=False)["best_value"].median()
    pivot = med.pivot(index="problem", columns="algorithm", values="best_value").dropna()
    rows = []
    for a, b in combinations(pivot.columns, 2):
        try:
            stat, p = wilcoxon(pivot[a], pivot[b], zero_method="wilcox", alternative="two-sided")
        except ValueError:
            stat, p = 0.0, 1.0
        rows.append({"algorithm_a": a, "algorithm_b": b, "statistic": float(stat), "p_raw": float(p)})
    out = pd.DataFrame(rows).sort_values("p_raw").reset_index(drop=True)
    m = len(out)
    adjusted = np.empty(m)
    running_max = 0.0
    for i, p in enumerate(out["p_raw"].to_numpy()):
        corrected = min(1.0, (m - i) * p)
        running_max = max(running_max, corrected)
        adjusted[i] = running_max
    out["p_holm"] = adjusted
    out["significant_0_05"] = out["p_holm"] < 0.05
    return out


def build_statistical_report(df: pd.DataFrame, output_dir: str) -> None:
    from pathlib import Path
    import json
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    summarize_runs(df).to_csv(out / "summary.csv", index=False)
    ranks = per_problem_ranks(df)
    ranks.to_csv(out / "problem_ranks.csv", index=False)
    ranks.groupby("algorithm", as_index=False)["rank"].mean().sort_values("rank").to_csv(out / "average_ranks.csv", index=False)
    pairwise_wilcoxon_holm(df).to_csv(out / "pairwise_wilcoxon_holm.csv", index=False)
    (out / "friedman.json").write_text(json.dumps(friedman_test(df), indent=2))
