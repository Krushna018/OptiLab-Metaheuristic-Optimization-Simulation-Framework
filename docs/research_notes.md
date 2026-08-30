# OptiLab Research Design

## Research question
How do population-based metaheuristics and Monte Carlo search differ in convergence speed, robustness, and final solution quality across continuous numerical landscapes and graph-structured optimization tasks when all methods receive the same objective-evaluation budget?

## Algorithms
- Genetic Algorithm (GA)
- Particle Swarm Optimization (PSO)
- Differential Evolution (DE)
- Monte Carlo random search baseline

## Problem suite
The framework defines **20 reproducible optimization problems**:

- **12 continuous benchmarks:** Sphere, Rastrigin, Rosenbrock, Ackley, Griewank, Schwefel, Zakharov, Levy, Alpine1, Styblinski-Tang, Salomon, and Dixon-Price.
- **4 graph resource-allocation instances:** continuous resource allocation over sparse/dense graphs with demand, centrality, scarcity, and neighbor-smoothness terms.
- **4 graph routing instances:** traffic splitting over candidate paths with travel-cost and nonlinear congestion penalties.

The graph suite deliberately introduces structure beyond standard numerical benchmarks while retaining a common bounded-vector search interface.

## Controlled experimental protocol
The default full study uses:
- 20 problems
- 4 algorithms
- 30 independent trials per problem/algorithm configuration
- 1,000 objective evaluations per trial
- deterministic seed generation for complete reproducibility

This produces exactly **2,400 primary optimization runs**. Every algorithm receives the same evaluation budget to avoid misleading comparisons based on different numbers of objective calls.

## Metrics
For each run the framework records:
- final best objective value
- best-so-far convergence trajectory
- objective evaluations
- wall-clock runtime

Across trials it computes:
- mean, median, and standard deviation of final solution quality
- per-problem algorithm rankings
- average ranks across the complete problem suite
- Friedman omnibus test
- pairwise Wilcoxon signed-rank tests with Holm correction

## Interpretation
Because GA, PSO, DE, and Monte Carlo search are stochastic, a single run is not treated as evidence. Thirty independent repetitions quantify variance and robustness. Median outcome and rank-based non-parametric tests are emphasized because optimization-result distributions are often non-normal and heavy-tailed.

## Reproducibility
All graph instances, algorithm seeds, budgets, and benchmark definitions are deterministic. `scripts/run_full_study.py` reconstructs the 2,400-run experiment from scratch and saves raw runs, convergence histories, statistical summaries, significance tests, and figures.
