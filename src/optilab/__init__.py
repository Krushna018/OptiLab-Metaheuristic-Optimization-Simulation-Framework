"""OptiLab research framework."""

from .benchmarks import build_continuous_suite
from .graph_problems import build_graph_suite
from .algorithms import genetic_algorithm, particle_swarm, differential_evolution, monte_carlo_search
from .experiments import run_study

__all__ = [
    "build_continuous_suite",
    "build_graph_suite",
    "genetic_algorithm",
    "particle_swarm",
    "differential_evolution",
    "monte_carlo_search",
    "run_study",
]
