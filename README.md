# OptiLab: Metaheuristic Optimization & Simulation Framework

OptiLab is a reproducible Python research project for comparing four stochastic optimization strategies—**Genetic Algorithms (GA), Particle Swarm Optimization (PSO), Differential Evolution (DE), and Monte Carlo search**—under fixed objective-evaluation budgets.

It is intentionally broader than a single application: the framework evaluates algorithms on **12 continuous numerical benchmarks and 8 graph-based resource-allocation/routing problems**, making it suitable for studying convergence behavior, robustness, and cross-domain performance trade-offs.

## Research claims supported by the project

- **20 optimization problems:** 12 continuous + 8 graph-based.
- **Four optimization methods:** GA, PSO, DE, Monte Carlo search.
- **Controlled experimental design:** default full study uses 30 independent trials for every problem/algorithm pair with equal evaluation budgets.
- **2,400 main runs:** `20 problems × 4 algorithms × 30 trials`.
- **Graph scenarios:** resource allocation and routing/congestion simulation using NetworkX-generated connected graphs.
- **Evaluation:** best objective, convergence trajectory, runtime, variance, per-problem ranks, average ranks, Friedman test, and pairwise Wilcoxon tests with Holm correction.
- **Reproducibility:** deterministic benchmark instances and seeds; raw run data and convergence histories are saved to CSV.

## Resume-aligned project summary

**OptiLab: Metaheuristic Optimization & Simulation Framework**  
*Python, Metaheuristics, Monte Carlo, NetworkX*

- Investigated the convergence and robustness of **Genetic Algorithms, Particle Swarm Optimization, Differential Evolution, and Monte Carlo search** across **20 continuous and graph-based optimization problems**, using fixed evaluation budgets and 30 independent trials per configuration to enable controlled comparison of stochastic behavior.
- Developed a modular experimentation framework in **Python** with configurable population sizes, mutation/crossover strategies, particle dynamics, stopping criteria, and graph constraints; implemented reproducible simulation pipelines for resource-allocation, routing, and numerical optimization scenarios.
- Conducted **2,400 primary optimization runs** in the default full study and evaluated solution quality, convergence rate, runtime, and variance using statistical summaries and non-parametric significance testing; generated convergence profiles and algorithm rankings to identify performance trade-offs across problem classes.

> The full 2,400-run result files are generated when `scripts/run_full_study.py` is executed. Do not claim completed-run results until that script has actually been run successfully on the target machine.

## Project layout

```text
OptiLab/
├── src/optilab/
│   ├── core.py             # Problem/result abstractions and fixed-budget tracking
│   ├── benchmarks.py       # 12 continuous benchmark functions
│   ├── graph_problems.py   # 8 graph allocation/routing instances
│   ├── algorithms.py       # GA, PSO, DE, Monte Carlo
│   ├── experiments.py      # Controlled multi-trial experiment runner
│   ├── statistics.py       # Summary + Friedman/Wilcoxon-Holm analyses
│   └── plotting.py         # Convergence and ranking figures
├── scripts/
│   ├── run_quick_demo.py
│   └── run_full_study.py
├── tests/
│   └── test_suite.py
├── docs/
│   └── research_notes.md
└── results/
```

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\\Scripts\\activate       # Windows
pip install -r requirements.txt
```

## Verify the implementation

```bash
python tests/test_suite.py
```

The test checks that all 20 problems evaluate to finite values and that each algorithm respects a fixed objective-evaluation budget while maintaining a valid best-so-far convergence trace.

## Quick demo

```bash
python scripts/run_quick_demo.py
```

This executes 80 short runs (20 problems × 4 algorithms × 1 trial) so the complete pipeline can be verified quickly.

## Full research experiment

```bash
python scripts/run_full_study.py
```

Default protocol:

```text
20 problems
× 4 algorithms
× 30 independent trials
= 2,400 primary optimization runs
```

Each run receives an objective-evaluation budget of 1,000 evaluations.

Outputs include:
- `runs.csv`
- `convergence_history.csv`
- `summary.csv`
- `problem_ranks.csv`
- `average_ranks.csv`
- `friedman.json`
- `pairwise_wilcoxon_holm.csv`
- convergence and rank plots

## Why non-parametric statistics?

Metaheuristic outcomes are stochastic and often non-normal. The framework therefore uses repeated trials and rank-based/non-parametric analyses rather than drawing conclusions from one run or assuming Gaussian result distributions.

## Academic integrity / resume use

The codebase supports the design and evaluation claims above, but anyone listing this work should run the experiments, inspect the outputs, understand the algorithms, and be able to explain the experimental choices. In particular, the phrase “conducted 2,400 runs” should only be used after the full experiment has actually completed.
