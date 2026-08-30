from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from optilab.experiments import all_problems
from optilab.algorithms import genetic_algorithm, particle_swarm, differential_evolution, monte_carlo_search


def test_problem_suite():
    problems = all_problems()
    assert len(problems) == 20
    assert sum(p.family == "continuous" for p in problems) == 12
    assert sum(p.family.startswith("graph-") for p in problems) == 8
    for p in problems:
        x = (p.lower + p.upper) / 2
        value = p.evaluate(x)
        assert np.isfinite(value), p.name


def test_algorithms_fixed_budget():
    p = all_problems()[0]
    for i, alg in enumerate((genetic_algorithm, particle_swarm, differential_evolution, monte_carlo_search)):
        result = alg(p, budget=120, seed=100+i, population_size=20, swarm_size=20)
        assert result.evaluations == 120
        assert np.isfinite(result.best_value)
        assert len(result.history_evals) == 120
        assert len(result.history_best) == 120
        # best-so-far sequence must be monotonically non-increasing.
        assert np.all(np.diff(result.history_best) <= 1e-12)


if __name__ == "__main__":
    test_problem_suite()
    test_algorithms_fixed_budget()
    print("All OptiLab tests passed.")
