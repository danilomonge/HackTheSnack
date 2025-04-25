import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker
from numpy.random import rand, randn
from tqdm.auto import tqdm

from scipy.optimize import linprog


def find_initial_point(A, a, B, b):
    D = A.shape[1]
    eps = 1e-6 # adding some slack to ensure we are _within_ the feasible region, not just on the boundary
    # not doing this will cause trouble down the line for the MCMC method, which will get stuck in a corner
    out = linprog(np.ones(D), A_ub=A, b_ub=a - eps, A_eq=B, b_eq=b, method="highs-ipm")
    return out.x

import scipy
print(scipy.__version__)
print(np.__version__)

x0 = find_initial_point(A, a, B, b)

# check your implementation:
print(f"Test for inequalities: {np.all(A @ x0 - a < 0)}")
print(f"Test for equalities: {np.allclose(B @ x0 - b,0)}")

x0.sum()
x0

def construct_directions(B):
    """
    The main challenge here is to ensure the equality constraints remain satisfied
    Naïvely using random.multivariatenormal or similar typically adds a "nugget",
    a minimal amount of "noise" to the covariance's diagonal, which messes up the
    equality constaraints. We solve this by actually computing the SVD manually, and
    then setting all directions that have nearly zero singular values to an actual zero.
    """

    _, D = B.shape
    q, s, ut = np.linalg.svd(
        B, full_matrices=False
    )  # the "full_matrices=False" matters, otherwise the next line is garbage
    Q, S, Ut = np.linalg.svd(np.eye(D) - ut.T @ ut)
    S[S < 1e-12] = 0  # set numerically zero to actually zero
    Q[np.abs(Q) < 1e-12] = 0  # do the same for the directions
    R = Q[:, S != 0]  # only keep directions with nonzero singular value
    S = np.sqrt(S[S != 0])

    K = R.shape[1]

    # now define the sampling function, as per usual for multivariate Gaussians:
    def sample():
        u = R @ np.reshape(np.sqrt(S) * randn(K), [K, 1])
        u /= np.linalg.norm(u)
        return u.flatten()

    return sample

def project_and_sample(xi, s, A, a):
    # take direction d, project the inequality constraints Ax <= a onto it, and sample
    y = (A @ xi) - a  # value of inequality constraints
    z = A @ s  # projected onto the slice

    # find the *tightest* of all constraints in both directions (i.e. towards xi + d and xi - d).
    K = len(y)
    upper = np.inf
    lower = -np.inf
    for k in range(K):
        if z[k] > 0:
            upper = np.minimum(upper, -y[k] / z[k])
        elif z[k] < 0:
            lower = np.maximum(lower, -y[k] / z[k])

    # sanity checks:
    assert np.isfinite(lower) and np.isfinite(
        upper
    ), f"lower bound {lower} and upper bound {upper}"  # constraints exist
    assert ~np.isclose(upper, lower)  # slice has finite length

    # sample:
    a = lower + (upper - lower) * np.random.rand()

    return xi + a * s

def MCMC(A, a, B, b, num_iter=int(1e7), thinning=int(1e5)):

    print("finding initial point.")
    eps = 1e-6
    out = linprog(np.ones(D), A_ub=A, b_ub=a - eps, A_eq=B, b_eq=b)
    x0 = out.x.flatten()

    print("precomputing space of search directions")
    sample = construct_directions(B)

    print("starting MCMC loop")
    samples = np.zeros(shape=(num_iter, D))
    samples[0, :] = x0
    xi = x0
    for i in tqdm(range(num_iter - 1)):
        xi = project_and_sample(xi, sample(), A, a)
        samples[i + 1, :] = xi

    return samples[0::thinning, :]



S = int(1e5)
SAMPLES = MCMC(A, a, B, b, num_iter=S, thinning=int(S / 100))


def acf(x, length=50):
    return np.array([1] + [np.corrcoef(x[:-i], x[i:])[0, 1] for i in range(1, length)])

