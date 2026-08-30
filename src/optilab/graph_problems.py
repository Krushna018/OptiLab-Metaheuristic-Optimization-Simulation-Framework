from __future__ import annotations

import numpy as np
import networkx as nx
from .core import Problem


def _connected_graph(n: int, p: float, seed: int) -> nx.Graph:
    rng = np.random.default_rng(seed)
    for offset in range(100):
        g = nx.erdos_renyi_graph(n, p, seed=seed + offset)
        if nx.is_connected(g):
            break
    else:
        g = nx.path_graph(n)
    for u, v in g.edges:
        g[u][v]["base_cost"] = float(rng.uniform(1.0, 8.0))
        g[u][v]["capacity"] = float(rng.uniform(1.0, 4.0))
    return g


def node_allocation_problem(name: str, n: int, p: float, seed: int, budget: float = 10.0) -> Problem:
    """Allocate a continuous resource budget over graph nodes.

    Benefits depend on node demand and centrality; smoothness penalizes allocations
    that differ strongly across adjacent nodes. The objective is minimized.
    """
    g = _connected_graph(n, p, seed)
    rng = np.random.default_rng(seed + 10_000)
    demand = rng.uniform(0.5, 2.0, size=n)
    centrality = nx.betweenness_centrality(g, normalized=True)
    importance = demand * np.array([1.0 + centrality[i] for i in range(n)])
    edges = list(g.edges)

    def objective(raw: np.ndarray) -> float:
        weights = np.clip(raw, 0.0, 1.0)
        if weights.sum() <= 1e-12:
            alloc = np.full(n, budget / n)
        else:
            alloc = budget * weights / weights.sum()
        benefit = np.sum(importance * np.log1p(alloc))
        smoothness = np.mean([(alloc[u] - alloc[v])**2 for u, v in edges]) if edges else 0.0
        scarcity = np.sum(np.maximum(0.0, demand - alloc / (budget/n + 1e-9))**2)
        return float(-benefit + 0.08 * smoothness + 0.15 * scarcity)

    return Problem(
        name=name,
        dimension=n,
        lower=np.zeros(n),
        upper=np.ones(n),
        objective=objective,
        family="graph-resource-allocation",
        description=f"Continuous resource allocation over a connected {n}-node graph.",
    )


def routing_split_problem(name: str, n: int, p: float, seed: int, k_paths: int = 6) -> Problem:
    """Optimize traffic splitting across candidate source-destination paths.

    Decision variables are real-valued logits converted to a probability simplex.
    Objective combines travel cost and nonlinear congestion penalties on shared edges.
    """
    g = _connected_graph(n, p, seed)
    source, target = 0, n - 1
    # Ensure a useful set of candidate simple paths.
    paths = []
    try:
        gen = nx.shortest_simple_paths(g, source, target, weight="base_cost")
        for _ in range(k_paths):
            paths.append(next(gen))
    except (nx.NetworkXNoPath, StopIteration):
        paths = [nx.shortest_path(g, source, target, weight="base_cost")]
    while len(paths) < k_paths:
        paths.append(paths[-1])

    path_edges = []
    path_costs = []
    for path in paths:
        edges = [tuple(sorted((path[i], path[i+1]))) for i in range(len(path)-1)]
        path_edges.append(edges)
        path_costs.append(sum(g[u][v]["base_cost"] for u, v in edges))

    capacities = {tuple(sorted((u, v))): g[u][v]["capacity"] for u, v in g.edges}
    demand = 8.0

    def objective(logits: np.ndarray) -> float:
        z = logits - np.max(logits)
        frac = np.exp(z)
        frac = frac / frac.sum()
        edge_load = {e: 0.0 for e in capacities}
        for f, edges in zip(frac, path_edges):
            for e in edges:
                edge_load[e] += demand * f
        congestion = 0.0
        for e, load in edge_load.items():
            cap = capacities[e]
            ratio = load / cap
            congestion += ratio**2 + 2.0 * max(0.0, ratio - 1.0)**2
        travel = float(np.dot(frac, np.asarray(path_costs)))
        concentration = float(np.sum(frac**2))
        return travel + 3.0 * congestion + 0.5 * concentration

    return Problem(
        name=name,
        dimension=k_paths,
        lower=np.full(k_paths, -5.0),
        upper=np.full(k_paths, 5.0),
        objective=objective,
        family="graph-routing",
        description=f"Traffic-splitting optimization over {k_paths} candidate paths in a {n}-node graph.",
    )


def build_graph_suite() -> list[Problem]:
    """Eight reproducible graph-based problem instances: four allocation + four routing."""
    return [
        node_allocation_problem("GraphAlloc-Sparse-12", 12, 0.22, 101),
        node_allocation_problem("GraphAlloc-Dense-12", 12, 0.45, 102),
        node_allocation_problem("GraphAlloc-Sparse-20", 20, 0.16, 103),
        node_allocation_problem("GraphAlloc-Dense-20", 20, 0.32, 104),
        routing_split_problem("Routing-Sparse-14", 14, 0.22, 201),
        routing_split_problem("Routing-Dense-14", 14, 0.42, 202),
        routing_split_problem("Routing-Sparse-22", 22, 0.15, 203),
        routing_split_problem("Routing-Dense-22", 22, 0.30, 204),
    ]
