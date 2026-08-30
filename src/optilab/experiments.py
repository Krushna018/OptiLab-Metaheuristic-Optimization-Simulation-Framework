from __future__ import annotations

from pathlib import Path
import json
import pandas as pd

from .benchmarks import build_continuous_suite
from .graph_problems import build_graph_suite
from .algorithms import genetic_algorithm, particle_swarm, differential_evolution, monte_carlo_search

ALGORITHMS = {
    "GA": genetic_algorithm,
    "PSO": particle_swarm,
    "DE": differential_evolution,
    "MonteCarlo": monte_carlo_search,
}


def all_problems():
    problems = build_continuous_suite() + build_graph_suite()
    assert len(problems) == 20
    return problems


def run_study(
    output_dir: str | Path = "results/full_study",
    trials: int = 30,
    budget: int = 1000,
    base_seed: int = 2027,
    algorithms: tuple[str, ...] = ("GA", "PSO", "DE", "MonteCarlo"),
) -> pd.DataFrame:
    """Run the controlled 20 x 4 x 30 = 2,400-run main study by default."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    histories = []
    problems = all_problems()

    for p_idx, problem in enumerate(problems):
        for a_idx, alg_name in enumerate(algorithms):
            alg = ALGORITHMS[alg_name]
            for trial in range(trials):
                seed = base_seed + p_idx * 10_000 + a_idx * 1_000 + trial
                result = alg(problem, budget=budget, seed=seed)
                rows.append({
                    "problem": problem.name,
                    "family": problem.family,
                    "algorithm": alg_name,
                    "trial": trial + 1,
                    "seed": seed,
                    "budget": budget,
                    "evaluations": result.evaluations,
                    "best_value": result.best_value,
                    "runtime_seconds": result.runtime_seconds,
                })
                histories.extend({
                    "problem": problem.name,
                    "algorithm": alg_name,
                    "trial": trial + 1,
                    "evaluation": e,
                    "best_value": v,
                } for e, v in zip(result.history_evals, result.history_best))

    df = pd.DataFrame(rows)
    hist_df = pd.DataFrame(histories)
    df.to_csv(output_dir / "runs.csv", index=False)
    hist_df.to_csv(output_dir / "convergence_history.csv", index=False)
    metadata = {
        "problems": len(problems),
        "algorithms": list(algorithms),
        "trials_per_configuration": trials,
        "evaluation_budget": budget,
        "total_main_runs": len(df),
        "continuous_problems": 12,
        "graph_based_problems": 8,
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    return df
