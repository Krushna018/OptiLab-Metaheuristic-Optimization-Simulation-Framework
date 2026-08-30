from __future__ import annotations

import time
import numpy as np
from .core import Problem, BudgetedObjective, OptimizationResult


def _result(name, problem, seed, tracked, start):
    best_x = tracked.best_x if tracked.best_x is not None else np.zeros(problem.dimension)
    return OptimizationResult(
        algorithm=name,
        problem=problem.name,
        seed=seed,
        best_value=tracked.best_value,
        best_x=best_x,
        evaluations=tracked.evaluations,
        history_evals=tracked.history_evals,
        history_best=tracked.history_best,
        runtime_seconds=time.perf_counter() - start,
    )


def monte_carlo_search(problem: Problem, budget: int, seed: int, **kwargs) -> OptimizationResult:
    start = time.perf_counter()
    rng = np.random.default_rng(seed)
    obj = BudgetedObjective(problem, budget)
    while obj.remaining > 0:
        obj(problem.sample(rng, 1)[0])
    return _result("MonteCarlo", problem, seed, obj, start)


def genetic_algorithm(
    problem: Problem,
    budget: int,
    seed: int,
    population_size: int = 30,
    crossover_rate: float = 0.9,
    mutation_rate: float | None = None,
    mutation_scale: float = 0.08,
    tournament_size: int = 3,
    elitism: int = 2,
    **kwargs,
) -> OptimizationResult:
    start = time.perf_counter()
    rng = np.random.default_rng(seed)
    obj = BudgetedObjective(problem, budget)
    mutation_rate = mutation_rate or (1.0 / problem.dimension)
    pop_n = min(population_size, budget)
    pop = problem.sample(rng, pop_n)
    scores = np.array([obj(ind) for ind in pop])

    def tournament():
        idx = rng.integers(0, len(pop), size=tournament_size)
        return pop[idx[np.argmin(scores[idx])]].copy()

    while obj.remaining > 0:
        elite_idx = np.argsort(scores)[:min(elitism, len(pop))]
        new_pop = [pop[i].copy() for i in elite_idx]
        while len(new_pop) < pop_n and obj.remaining > 0:
            p1, p2 = tournament(), tournament()
            child = p1.copy()
            if rng.random() < crossover_rate:
                alpha = rng.random(problem.dimension)
                child = alpha * p1 + (1 - alpha) * p2
            mask = rng.random(problem.dimension) < mutation_rate
            span = problem.upper - problem.lower
            child[mask] += rng.normal(0.0, mutation_scale, size=mask.sum()) * span[mask]
            child = problem.clip(child)
            new_pop.append(child)
        # Evaluate only new generation under remaining budget.
        pop = np.asarray(new_pop[:pop_n])
        scores_list = []
        for ind in pop:
            if obj.remaining <= 0:
                break
            scores_list.append(obj(ind))
        if len(scores_list) < len(pop):
            pop = pop[:len(scores_list)]
        scores = np.asarray(scores_list)
        if len(pop) == 0:
            break
    return _result("GA", problem, seed, obj, start)


def particle_swarm(
    problem: Problem,
    budget: int,
    seed: int,
    swarm_size: int = 30,
    inertia: float = 0.72,
    cognitive: float = 1.49,
    social: float = 1.49,
    **kwargs,
) -> OptimizationResult:
    start = time.perf_counter()
    rng = np.random.default_rng(seed)
    obj = BudgetedObjective(problem, budget)
    n = min(swarm_size, budget)
    pos = problem.sample(rng, n)
    span = problem.upper - problem.lower
    vel = rng.uniform(-0.1, 0.1, size=pos.shape) * span
    scores = np.array([obj(x) for x in pos])
    pbest = pos.copy()
    pbest_scores = scores.copy()
    g_idx = int(np.argmin(scores))
    gbest = pos[g_idx].copy()
    gbest_score = scores[g_idx]

    while obj.remaining > 0:
        r1 = rng.random(pos.shape)
        r2 = rng.random(pos.shape)
        vel = inertia * vel + cognitive * r1 * (pbest - pos) + social * r2 * (gbest - pos)
        pos = problem.clip(pos + vel)
        for i in range(n):
            if obj.remaining <= 0:
                break
            s = obj(pos[i])
            if s < pbest_scores[i]:
                pbest_scores[i] = s
                pbest[i] = pos[i].copy()
                if s < gbest_score:
                    gbest_score = s
                    gbest = pos[i].copy()
    return _result("PSO", problem, seed, obj, start)


def differential_evolution(
    problem: Problem,
    budget: int,
    seed: int,
    population_size: int = 30,
    differential_weight: float = 0.7,
    crossover_rate: float = 0.9,
    **kwargs,
) -> OptimizationResult:
    start = time.perf_counter()
    rng = np.random.default_rng(seed)
    obj = BudgetedObjective(problem, budget)
    n = max(4, min(population_size, budget))
    pop = problem.sample(rng, n)
    scores = np.array([obj(x) for x in pop])

    while obj.remaining > 0:
        for i in range(n):
            if obj.remaining <= 0:
                break
            pool = [j for j in range(n) if j != i]
            a, b, c = rng.choice(pool, size=3, replace=False)
            mutant = pop[a] + differential_weight * (pop[b] - pop[c])
            mutant = problem.clip(mutant)
            mask = rng.random(problem.dimension) < crossover_rate
            mask[rng.integers(problem.dimension)] = True
            trial = np.where(mask, mutant, pop[i])
            trial_score = obj(trial)
            if trial_score <= scores[i]:
                pop[i] = trial
                scores[i] = trial_score
    return _result("DE", problem, seed, obj, start)
