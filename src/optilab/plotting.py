from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_average_ranks(ranks_csv: str | Path, output: str | Path):
    df = pd.read_csv(ranks_csv).sort_values("rank")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(df["algorithm"], df["rank"])
    ax.invert_yaxis()
    ax.set_xlabel("Average rank (lower is better)")
    ax.set_title("Algorithm ranking across benchmark problems")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_convergence(history_csv: str | Path, problem: str, output: str | Path, points: int = 100):
    hist = pd.read_csv(history_csv)
    hist = hist[hist["problem"] == problem]
    if hist.empty:
        raise ValueError(f"No history found for problem {problem}")
    max_eval = int(hist["evaluation"].max())
    grid = np.unique(np.linspace(1, max_eval, points).astype(int))
    fig, ax = plt.subplots(figsize=(7, 4))
    for alg, sub in hist.groupby("algorithm"):
        curves = []
        for _, trial in sub.groupby("trial"):
            trial = trial.sort_values("evaluation")
            vals = np.interp(grid, trial["evaluation"], trial["best_value"])
            curves.append(vals)
        median_curve = np.median(np.vstack(curves), axis=0)
        ax.plot(grid, median_curve, label=alg)
    ax.set_xlabel("Objective evaluations")
    ax.set_ylabel("Best-so-far objective")
    ax.set_title(f"Median convergence: {problem}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)
