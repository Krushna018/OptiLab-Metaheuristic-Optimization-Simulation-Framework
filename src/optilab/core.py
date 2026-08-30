from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np

Array = np.ndarray


@dataclass(frozen=True)
class Problem:
    name: str
    dimension: int
    lower: Array
    upper: Array
    objective: Callable[[Array], float]
    family: str
    description: str

    def sample(self, rng: np.random.Generator, n: int = 1) -> Array:
        return rng.uniform(self.lower, self.upper, size=(n, self.dimension))

    def clip(self, x: Array) -> Array:
        return np.clip(x, self.lower, self.upper)

    def evaluate(self, x: Array) -> float:
        return float(self.objective(np.asarray(x, dtype=float)))


@dataclass
class OptimizationResult:
    algorithm: str
    problem: str
    seed: int
    best_value: float
    best_x: Array
    evaluations: int
    history_evals: list[int]
    history_best: list[float]
    runtime_seconds: float


class BudgetedObjective:
    """Tracks calls and best-so-far values under a fixed objective-evaluation budget."""

    def __init__(self, problem: Problem, budget: int):
        self.problem = problem
        self.budget = int(budget)
        self.evaluations = 0
        self.best_value = float("inf")
        self.best_x: Array | None = None
        self.history_evals: list[int] = []
        self.history_best: list[float] = []

    @property
    def remaining(self) -> int:
        return self.budget - self.evaluations

    def __call__(self, x: Array) -> float:
        if self.evaluations >= self.budget:
            raise RuntimeError("Evaluation budget exhausted")
        value = self.problem.evaluate(x)
        self.evaluations += 1
        if value < self.best_value:
            self.best_value = value
            self.best_x = np.asarray(x, dtype=float).copy()
        self.history_evals.append(self.evaluations)
        self.history_best.append(self.best_value)
        return value
