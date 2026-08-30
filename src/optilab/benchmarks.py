from __future__ import annotations

import numpy as np
from .core import Problem


def _problem(name, dim, low, high, fn, description):
    return Problem(
        name=name,
        dimension=dim,
        lower=np.full(dim, low, dtype=float),
        upper=np.full(dim, high, dtype=float),
        objective=fn,
        family="continuous",
        description=description,
    )


def sphere(x):
    return np.sum(x**2)


def rastrigin(x):
    n = len(x)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))


def rosenbrock(x):
    return np.sum(100 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2)


def ackley(x):
    n = len(x)
    return -20 * np.exp(-0.2 * np.sqrt(np.sum(x**2) / n)) - np.exp(np.sum(np.cos(2*np.pi*x)) / n) + 20 + np.e


def griewank(x):
    i = np.arange(1, len(x) + 1)
    return np.sum(x**2) / 4000 - np.prod(np.cos(x / np.sqrt(i))) + 1


def schwefel(x):
    n = len(x)
    return 418.9829 * n - np.sum(x * np.sin(np.sqrt(np.abs(x))))


def zakharov(x):
    i = np.arange(1, len(x) + 1)
    s = np.sum(0.5 * i * x)
    return np.sum(x**2) + s**2 + s**4


def levy(x):
    w = 1 + (x - 1) / 4
    t1 = np.sin(np.pi * w[0]) ** 2
    t2 = np.sum((w[:-1] - 1) ** 2 * (1 + 10 * np.sin(np.pi * w[:-1] + 1) ** 2))
    t3 = (w[-1] - 1) ** 2 * (1 + np.sin(2 * np.pi * w[-1]) ** 2)
    return t1 + t2 + t3


def alpine1(x):
    return np.sum(np.abs(x * np.sin(x) + 0.1 * x))


def styblinski_tang(x):
    return 0.5 * np.sum(x**4 - 16*x**2 + 5*x)


def salomon(x):
    r = np.sqrt(np.sum(x**2))
    return 1 - np.cos(2*np.pi*r) + 0.1*r


def dixon_price(x):
    total = (x[0] - 1) ** 2
    for i in range(1, len(x)):
        total += (i + 1) * (2*x[i]**2 - x[i-1])**2
    return total


def build_continuous_suite(dim: int = 8) -> list[Problem]:
    """Twelve standard continuous benchmark functions."""
    return [
        _problem("Sphere", dim, -5.12, 5.12, sphere, "Unimodal convex baseline."),
        _problem("Rastrigin", dim, -5.12, 5.12, rastrigin, "Highly multimodal separable landscape."),
        _problem("Rosenbrock", dim, -3.0, 3.0, rosenbrock, "Narrow curved valley with strong variable interaction."),
        _problem("Ackley", dim, -32.768, 32.768, ackley, "Multimodal landscape with nearly flat outer region."),
        _problem("Griewank", dim, -100.0, 100.0, griewank, "Many regularly distributed local minima."),
        _problem("Schwefel", dim, -500.0, 500.0, schwefel, "Deceptive multimodal benchmark with distant optimum."),
        _problem("Zakharov", dim, -5.0, 10.0, zakharov, "Smooth non-separable polynomial landscape."),
        _problem("Levy", dim, -10.0, 10.0, levy, "Multimodal benchmark with sinusoidal structure."),
        _problem("Alpine1", dim, -10.0, 10.0, alpine1, "Non-smooth multimodal benchmark."),
        _problem("StyblinskiTang", dim, -5.0, 5.0, styblinski_tang, "Multimodal quartic benchmark."),
        _problem("Salomon", dim, -100.0, 100.0, salomon, "Radially oscillatory benchmark."),
        _problem("DixonPrice", dim, -10.0, 10.0, dixon_price, "Non-separable valley benchmark."),
    ]
