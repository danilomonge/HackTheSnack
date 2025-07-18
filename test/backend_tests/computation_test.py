import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hts_lib.backend.algorithm.computation import Computation

#Definition of standard constraints for 3 ingredients 
D = 3
A = np.zeros((D + D - 1, D))
A[0:D, 0:D] = -np.eye(D)
for i in range(D - 1):
    A[D + i, i + 1] = 1
    A[D + i, i] = -1
a = np.array([0, 0, 0, 0, 0])
B = np.array([[1, 1, 1], [0, 0, 1]])
b = np.array([1, 0.2])
num_iter = 100
thinning = 10


def test_find_initial_point():
    """
    Tests find_initial_point generates a valid point 

    """

    x0 = Computation._find_initial_point(A, a, B, b, eps=1e-6)

    assert np.allclose(np.sum(x0), 1)  # Sum = 1                        # type: ignore[arg-type]
    assert np.all(x0 > 0)              # Ingredients > 0                # type: ignore[arg-type]
    assert np.all(A @ x0 - a < 0)      # Test for inequalities          # type: ignore[arg-type]
    assert np.allclose(B @ x0 - b, 0)  # Test for equalities


def test_constraint_reduction_bounds():
    """
    Test constraint_reduction generates valid bounds

    """
    xi = np.array([0.5, 0.5])
    s = np.array([1, -1])
    A = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    a = np.array([1, 1, 0, 0])
    point, upper, lower, d = Computation._constrain_reduction(xi, s, A, a)

    assert np.isfinite(lower) and np.isfinite(
        upper
    ), f"lower bound {lower} and upper bound {upper}"  # constraints exist
    assert ~np.isclose(upper, lower)                   # slice has finite length


def test_project_and_sample():
    """
    Test project_and_sample generates a valid point

    """
    xi = np.array([0.3, 0.3, 0.4])
    s = np.array([1, 0, -1])

    new_point = Computation._project_and_sample(xi, s, A, a)

    assert new_point.shape == xi.shape               # dimension congruency 
    assert np.all(new_point >= 0)                    # positive coordinates
    assert np.all(np.isclose(np.sum(new_point), 1))  # sum = 1


def test_MCMC():
    """
    Test that the MCMC returns a sample with correct dimensions and form

    """
    samples = Computation._MCMC(A, a, B, b, num_iter=num_iter, thinning=thinning)

    assert samples.shape[0] == num_iter // thinning         # correct thinning                   # type: ignore[arg-type]                   
    assert samples.shape[1] == A.shape[1]                   # dimensions for one sample          # type: ignore[arg-type]
    assert np.all(np.isclose(np.sum(samples, axis=1), 1))   # sum = 1                            # type: ignore[arg-type]


S = int(1e5)


def test_compute_result():
    """
    Test that result values are real numbers and satisfy the recipe form (ingredients sum up to 100%)

    """

    mean, std = Computation.compute_result(A, a, B, b)

    assert np.all(np.isfinite(mean, std))        # values exist                   # type: ignore[arg-type]
    assert not np.all(np.isnan(mean, std))       # values are not NAN             # type: ignore[arg-type]
    assert np.all(mean > 0) and np.all(std >= 0) # values are positive            # type: ignore[arg-type]
    assert np.all(np.isclose(np.sum(mean), 100))   # mean sum = 1                 # type: ignore[arg-type]


def test_compute_result_for_one_ingredient():
    """
    Test the algorithm for one ingredient

    """
    A = np.array([[-1]])
    a = np.array([0])
    B = np.array([[1]])
    b = np.array([1])

    mean, std = Computation.compute_result(A, a, B, b)


    assert mean == np.array([100])
    assert std == np.array([0])



