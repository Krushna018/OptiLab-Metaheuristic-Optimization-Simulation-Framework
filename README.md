# OptiLab — Metaheuristic Optimization & Simulation Framework

<p align="center">
  <b>A reproducible research framework for controlled comparison of stochastic optimization algorithms across continuous and graph-based problems.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Algorithms-4-orange" alt="Algorithms">
  <img src="https://img.shields.io/badge/Problems-20-green" alt="Problems">
  <img src="https://img.shields.io/badge/Experiments-2%2C400-purple" alt="Experiments">
  <img src="https://img.shields.io/badge/Trials-30%20per%20pair-red" alt="Trials">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

---

## Overview

**OptiLab** is a reproducible Python research framework for evaluating and comparing stochastic optimization algorithms under controlled objective-evaluation budgets.

The framework studies four optimization strategies:

* **Genetic Algorithm (GA)**
* **Particle Swarm Optimization (PSO)**
* **Differential Evolution (DE)**
* **Monte Carlo Search**

Rather than evaluating algorithms on a single application, OptiLab provides a **cross-domain experimental environment** containing:

* **12 continuous numerical benchmark functions**
* **8 graph-based resource-allocation and routing problems**
* **20 total optimization problems**
* **30 independent trials per algorithm/problem pair**
* **1,000 objective evaluations per run**
* **2,400 primary optimization runs**

The resulting data can be used to study **convergence, solution quality, runtime, robustness, ranking stability, and statistical differences between algorithms**.

---

## Research Scope

OptiLab is designed around one central question:

> **How do different stochastic optimization strategies behave when they are evaluated under the same computational budget across heterogeneous optimization problems?**

The experimental design emphasizes **fair comparison and reproducibility** rather than relying on a single successful run.

### Experimental configuration

| Component               |                             Configuration |
| ----------------------- | ----------------------------------------: |
| Optimization algorithms |                                         4 |
| Continuous benchmarks   |                                        12 |
| Graph-based problems    |                                         8 |
| Total problems          |                                    **20** |
| Independent trials      |                             **30 / pair** |
| Evaluation budget       |                           **1,000 / run** |
| Primary runs            |                                 **2,400** |
| Main metrics            | Objective, convergence, runtime, variance |
| Statistical analysis    |                  Friedman + Wilcoxon-Holm |

---

## Algorithms

OptiLab implements four fundamentally different search strategies.

| Algorithm                             | Search principle                                                              |
| ------------------------------------- | ----------------------------------------------------------------------------- |
| **Genetic Algorithm (GA)**            | Population-based evolutionary search using selection, crossover, and mutation |
| **Particle Swarm Optimization (PSO)** | Population-based search driven by individual and swarm-level movement         |
| **Differential Evolution (DE)**       | Vector-difference-based evolutionary search with mutation and recombination   |
| **Monte Carlo Search**                | Random sampling of candidate solutions within the search space                |

This diversity allows the framework to compare both **population-based metaheuristics** and a **random-search baseline** under a common evaluation budget.

---

## Benchmark Problems

The framework contains **20 optimization problems** divided into two categories.

### 1. Continuous Numerical Benchmarks

The continuous benchmark suite contains **12 mathematical objective functions** designed to expose different optimization behaviors, such as:

* multimodality
* non-convexity
* variable interaction
* local minima
* rugged search landscapes
* sensitivity to initialization

These problems provide controlled environments for studying algorithmic convergence and solution quality.

### 2. Graph-Based Problems

OptiLab also evaluates optimization behavior on **8 graph-based resource-allocation and routing scenarios**.

Graph instances are generated using **NetworkX** and are constructed as connected networks.

The graph problems introduce additional challenges involving:

* network structure
* routing decisions
* congestion
* resource allocation
* competing objectives
* graph-dependent search spaces

This extends the evaluation beyond conventional mathematical benchmark functions toward more application-oriented optimization settings.

---

## Experimental Methodology

Each algorithm/problem combination is evaluated using the same experimental protocol.

```text
                    ┌─────────────────────┐
                    │   20 Optimization    │
                    │       Problems       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   4 Algorithms       │
                    │ GA / PSO / DE / MC   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  30 Independent      │
                    │      Trials          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ 1,000 Objective      │
                    │ Evaluations / Run    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Raw Run + Convergence│
                    │       Data           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Statistical Analysis │
                    │ & Visualizations      │
                    └─────────────────────┘
```

### Primary experiment

The complete study contains:

```text
20 problems
× 4 algorithms
× 30 independent trials
──────────────────────────
= 2,400 optimization runs
```

Every run is constrained by the same **1,000 objective-evaluation budget**.

This makes computational effort directly comparable across algorithms.

---

## Evaluation Metrics

OptiLab records multiple measures rather than relying solely on the final objective value.

### Solution Quality

Measures the best objective value obtained by an algorithm during a run.

### Convergence

Tracks the **best-so-far objective value** throughout the evaluation budget.

This allows comparison of:

* early-stage progress
* convergence speed
* stagnation
* final solution quality

### Runtime

Execution time is recorded for each optimization run to provide an additional computational-efficiency perspective.

### Variability

Repeated trials allow the framework to quantify how consistently an algorithm performs across different stochastic runs.

### Rankings

Algorithms are ranked independently for each optimization problem and then aggregated to obtain average ranks across the benchmark suite.

---

## Statistical Analysis

Because metaheuristic algorithms are stochastic, a single execution is insufficient to characterize their behavior.

OptiLab therefore uses **30 independent trials** for each algorithm/problem pair.

### Friedman Test

The **Friedman test** is used to examine whether there are statistically detectable differences among algorithms across the repeated problem-level comparisons.

### Pairwise Wilcoxon Tests

Pairwise comparisons are performed using the **Wilcoxon signed-rank test**.

### Holm Correction

Multiple pairwise comparisons are adjusted using **Holm correction** to reduce the risk of false-positive statistical findings.

The resulting analysis includes:

```text
Per-run measurements
        ↓
Problem-level rankings
        ↓
Average algorithm ranks
        ↓
Friedman test
        ↓
Pairwise Wilcoxon tests
        ↓
Holm-adjusted results
```

The framework reports the statistical results rather than relying on conclusions from individual runs.

---

## Reproducibility

Reproducibility is a core design goal of OptiLab.

The framework uses:

* deterministic benchmark definitions
* controlled random seeds
* fixed evaluation budgets
* repeated independent trials
* deterministic graph-instance generation
* raw experimental output
* stored convergence histories

This allows experiments to be rerun and independently inspected.

---

## Project Structure

```text
OptiLab/
│
├── src/
│   └── optilab/
│       ├── core.py
│       │   └── Problem/result abstractions and evaluation-budget tracking
│       │
│       ├── benchmarks.py
│       │   └── 12 continuous benchmark functions
│       │
│       ├── graph_problems.py
│       │   └── 8 graph-based allocation/routing problems
│       │
│       ├── algorithms.py
│       │   └── GA, PSO, DE, and Monte Carlo search
│       │
│       ├── experiments.py
│       │   └── Controlled multi-trial experiment runner
│       │
│       ├── statistics.py
│       │   └── Summary, ranking, Friedman, and Wilcoxon-Holm analysis
│       │
│       └── plotting.py
│           └── Convergence and ranking visualizations
│
├── scripts/
│   ├── run_quick_demo.py
│   └── run_full_study.py
│
├── tests/
│   └── test_suite.py
│
├── docs/
│   └── research_notes.md
│
├── results/
│   └── Generated experiment outputs
│
├── requirements.txt
└── README.md
```

---

## Installation

### Requirements

* Python **3.10+**
* pip
* virtual environment support

### 1. Clone the repository

```bash
git clone https://github.com/Krushna018/OptiLab-Metaheuristic-Optimization-Simulation-Framework.git
cd OptiLab-Metaheuristic-Optimization-Simulation-Framework
```

### 2. Create a virtual environment

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Verify the Implementation

Run the test suite:

```bash
python tests/test_suite.py
```

The tests verify that:

* all **20 optimization problems** produce finite objective values
* algorithm executions remain within the configured evaluation budget
* best-so-far convergence traces are valid
* core optimization components behave as expected

---

## Quick Demo

For a fast end-to-end validation:

```bash
python scripts/run_quick_demo.py
```

The quick experiment executes:

```text
20 problems
× 4 algorithms
× 1 trial
──────────────
= 80 optimization runs
```

This provides a lightweight way to verify the complete experiment pipeline before running the full study.

---

## Full Research Experiment

Run the complete experimental protocol with:

```bash
python scripts/run_full_study.py
```

The default study performs:

```text
20 problems
× 4 algorithms
× 30 trials
────────────────
= 2,400 runs
```

with:

```text
1,000 objective evaluations per run
```

Depending on the machine, the full study may require significantly more time than the quick demo.

---

## Generated Results

The framework stores both raw experimental data and aggregated statistical results.

| File                         | Description                                  |
| ---------------------------- | -------------------------------------------- |
| `runs.csv`                   | Raw results for every optimization run       |
| `convergence_history.csv`    | Best-so-far convergence trajectories         |
| `summary.csv`                | Aggregated performance statistics            |
| `problem_ranks.csv`          | Algorithm rankings for each problem          |
| `average_ranks.csv`          | Average ranks across problems                |
| `friedman.json`              | Friedman test results                        |
| `pairwise_wilcoxon_holm.csv` | Pairwise Wilcoxon tests with Holm correction |

The framework also generates convergence and ranking figures for visual analysis.

---

## Research Workflow

```text
Benchmark Definition
        │
        ▼
Problem Generation
        │
        ▼
Algorithm Execution
        │
        ▼
Fixed Evaluation Budget
        │
        ▼
30 Independent Trials
        │
        ▼
Raw Result Collection
        │
        ├──────────────► Convergence Analysis
        │
        ├──────────────► Runtime Analysis
        │
        ├──────────────► Variance Analysis
        │
        └──────────────► Ranking Analysis
                              │
                              ▼
                    Statistical Testing
                              │
                              ▼
                    Research Outputs
```

---

## Why OptiLab?

Many optimization experiments focus on a single algorithm, a single benchmark, or a single successful execution.

OptiLab instead emphasizes:

**Controlled comparison**
All algorithms operate under a common objective-evaluation budget.

**Cross-domain evaluation**
The benchmark suite combines mathematical functions with graph-based optimization scenarios.

**Stochastic robustness**
Repeated independent trials capture variation between runs.

**Statistical analysis**
Rank-based and non-parametric tests provide a structured way to analyze repeated results.

**Reproducibility**
Seeds, deterministic instances, raw measurements, and convergence histories make the experimental pipeline repeatable.

**Extensibility**
The modular architecture makes it possible to add new algorithms, benchmarks, graph scenarios, metrics, and statistical analyses.

---

## Extending the Framework

OptiLab is structured so that additional research components can be introduced without redesigning the entire pipeline.

Potential extensions include:

* additional metaheuristic algorithms
* multi-objective optimization
* larger graph instances
* dynamic optimization environments
* alternative statistical tests
* hyperparameter sensitivity analysis
* additional convergence metrics
* parallel experiment execution
* real-world optimization datasets

---

## Research-Oriented Design

OptiLab is intended not merely as an implementation of optimization algorithms, but as an **experimental framework for reproducible comparative research**.

The separation between:

```text
Problems
   ↓
Algorithms
   ↓
Experiment Runner
   ↓
Statistics
   ↓
Visualization
```

allows each component to be independently tested, extended, and analyzed.

---



