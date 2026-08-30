from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from optilab.experiments import run_study
from optilab.statistics import build_statistical_report
from optilab.plotting import plot_average_ranks, plot_convergence


def main():
    out = ROOT / "results" / "full_study"
    print("Running 20 problems x 4 algorithms x 30 independent trials = 2,400 main runs")
    df = run_study(out, trials=30, budget=1000)
    build_statistical_report(df, str(out))
    plot_average_ranks(out / "average_ranks.csv", out / "average_ranks.png")
    plot_convergence(out / "convergence_history.csv", "Rastrigin", out / "rastrigin_convergence.png")
    print(f"Finished {len(df)} runs. Results written to {out}")


if __name__ == "__main__":
    main()
