"""The browser build has no SciPy, so the MCMC starting point is found with NumPy.

These tests compare the NumPy solver (``Computation._feasible_point``) with
SciPy's ``linprog`` on constraint systems built exactly like the app builds
them, and check that a full estimation works without SciPy.
"""

import numpy as np
import pytest
from scipy.optimize import linprog

from backend.algorithm.computation import Computation
from backend.algorithm.constraints import Constraints
from backend.input.constraints_preparation import prepare_constraints_dict
from backend.recipe_generator import RecipeGenerator


def _system(fixed: dict[int, float], n: int):
    A, a = Constraints.build_inequality_constraints(n)
    B, b = Constraints.build_equality_constraints(fixed, n)
    return A, a, B, b


def _random_recipes(count: int, seed: int = 7):
    """Label-ordered recipes with some percentages known (as fractions), incl. edge cases."""
    rng = np.random.default_rng(seed)
    systems = []
    for _ in range(count):
        n = int(rng.integers(2, 13))
        shares = np.sort(rng.dirichlet(np.ones(n)))[::-1]
        known = rng.random(n) < rng.uniform(0.0, 0.7)
        if known.all():
            known[int(rng.integers(0, n))] = False
        fixed = {i: float(np.round(shares[i], 4)) for i in range(n) if known[i]}
        if rng.random() < 0.15 and fixed:  # break the label order -> usually infeasible
            i = next(iter(fixed))
            fixed[i] = float(rng.uniform(0.0, 0.05))
        if rng.random() < 0.1 and fixed:  # known shares that add up to more than 100 %
            i = next(iter(fixed))
            fixed[i] = 0.99
        systems.append((fixed, n))
    # hand-picked edge cases: equal neighbours, a value at the boundary, a unique solution
    systems += [({0: 0.5, 1: 0.5}, 3), ({1: 0.3, 2: 0.3}, 4), ({0: 0.25, 1: 0.25, 2: 0.25}, 4), ({}, 2), ({2: 0.4}, 3)]
    return systems


@pytest.mark.parametrize("eps", [1e-3, 1e-8, 0.0])
def test_numpy_solver_agrees_with_linprog(eps):
    disagreements = []
    for fixed, n in _random_recipes(250):
        A, a, B, b = _system(fixed, n)
        reference = linprog(np.ones(n), A_ub=A, b_ub=a - eps, A_eq=B, b_eq=b, method="highs-ipm")
        x = Computation._feasible_point(A, a - eps, B, b)

        if (x is not None) != reference.success:
            disagreements.append((fixed, n, reference.success))
            continue
        if x is not None:
            assert np.allclose(B @ x, b, atol=1e-9)
            assert np.all(A @ x <= a - eps + 1e-7)

    assert not disagreements, disagreements[:5]


def test_solver_returns_a_central_point():
    # x = (x0, x1, 0.2) with x0 >= x1 >= 0.2 and x0 + x1 = 0.8: the centre is far from both bounds.
    A, a, B, b = _system({2: 0.2}, 3)
    x = Computation._feasible_point(A, a - 1e-3, B, b)
    slack = a - A @ x
    assert slack.min() > 1e-3  # strictly inside, not on a vertex


def test_estimation_works_without_scipy(monkeypatch):
    monkeypatch.setattr(Computation, "_load_linprog", staticmethod(lambda: None))
    np.random.seed(0)

    result = RecipeGenerator.generate_recipe({"PEANUTS": None, "SUGAR": None, "SALT": 0.015})

    assert result is not None
    peanuts, sugar, salt = result["PEANUTS"], result["SUGAR"], result["SALT"]
    assert salt == {"mean": 1.5, "variation": 0.0}
    assert peanuts["mean"] >= sugar["mean"] >= 1.5
    assert abs(peanuts["mean"] + sugar["mean"] + salt["mean"] - 100) < 0.05
    # A real sample, not the deterministic fallback (which reports no variation).
    assert peanuts["variation"] > 5 and sugar["variation"] > 5


def test_estimation_without_scipy_matches_scipy(monkeypatch):
    recipe = {"A": None, "B": 0.2, "C": None, "D": None, "E": 0.05, "F": None, "G": None, "H": 0.01}
    np.random.seed(1)
    with_scipy = RecipeGenerator.generate_recipe(recipe)

    monkeypatch.setattr(Computation, "_load_linprog", staticmethod(lambda: None))
    np.random.seed(1)
    without_scipy = RecipeGenerator.generate_recipe(recipe)

    for name in recipe:
        # Same constraints, different starting point: estimates agree within sampling noise.
        assert abs(with_scipy[name]["mean"] - without_scipy[name]["mean"]) < 4.0, name


def test_infeasible_input_is_reported_without_scipy(monkeypatch):
    monkeypatch.setattr(Computation, "_load_linprog", staticmethod(lambda: None))
    fixed = prepare_constraints_dict({"A": None, "B": 0.6, "C": 0.7})  # 60 % then 70 %: not in label order
    A, a, B, b = _system(fixed, 3)
    assert Computation._find_initial_point(A, a, B, b, eps=0.0) is None
