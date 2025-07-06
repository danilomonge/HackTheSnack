import numpy as np
from numpy.random import rand, randn
from tqdm.auto import tqdm
from scipy.optimize import linprog


class Computation:
    """
    Class for performing MCMC sampling to estimate values for unknown components under linear constraints.
    """

    @staticmethod
    def _find_initial_point(A, a, B, b, eps):
        """
        Finds a point inside the polytope defined by equality- and inequality
        constrains through linear programming.

        Args:
            A (np.ndarray): Matrix for inequality constraints A @ x <= a.
            a (np.ndarray): Vector for inequality constraints.
            B (np.ndarray): Matrix for equality constraints B @ x = b.
            b (np.ndarray): Vector for equality constraints.
            eps (float, optional): Slack added to shrink the constrain region. Defaults to 1e-6.

        Returns:
            np.ndarray: Feasible starting point x0.
        """

        D = A.shape[1]
        out = linprog(
            np.ones(D), A_ub=A, b_ub=a - eps, A_eq=B, b_eq=b, method="highs-ipm"
        )
        if not out.success:
            print(
                f"⚠️ No feasible solution found for the constraint system with the given eps: {eps}."
            )
            return None

        return out.x

    @staticmethod
    def _svd_projection(B):
        """
        Performs Singular Value Decomposition (SVD) to obtain a stable projection
        onto the null space of a matrix B.

        Args:
            B (np.ndarray): Matrix representing the equality constraints.

        Returns:
             tuple: Two matrices:
            - R (np.ndarray): Basis for the null space of B.
            - S (np.ndarray): Non-zero singular values, normalized.

        """

        # Dimensionality of the space we are sampling in
        _, D = B.shape

        # comuptes a compact Standard Value Decomposition manually to sequre stability
        # B = Q * S * U^T
        # ut forms a basis for the row space of B
        q, s, ut = np.linalg.svd(B, full_matrices=False)

        # projection on to the nullspace of B
        # = I (identity) - ut^T * ut (projection on to the row space)
        Q, S, Ut = np.linalg.svd(np.eye(D) - ut.T @ ut)

        S[S < 1e-12] = 0  # set numerically zero to actually zero
        Q[np.abs(Q) < 1e-26] = 0  # do the same for the directions
        R = Q[:, S != 0]  # only keep directions with nonzero singular value
        S = np.sqrt(S[S != 0])

        return R, S

    @staticmethod
    def _construct_directions(B):
        """
        Constructs a sampling function that generates random unit direction vectors
        while maintaining the equality constraints defined by the matrix B.

        The function first computes the projection onto the null space of B using
        Singular Value Decomposition (SVD) to ensure stability. The resulting
        sampling function returns a random unit vector that lies within the
        constraint-compliant subspace.

        Args:
            B (np.ndarray): Matrix representing the equality constraints.

        Returns:
            function: A sampling function that, when called, returns a random unit
                    direction vector that satisfies the equality constraints.
        """
        R, S = Computation._svd_projection(B)

        def sample():
            """
            Generates a random unit vector from the subspace defined by the given
            projection matrices.

            Args:
            R (np.ndarray): Basis for the null space.
            S (np.ndarray): Non-zero singular values.

            Returns:
            np.ndarray: A random unit direction vector.
            """
            K = R.shape[1]
            u = R @ np.reshape(np.sqrt(S) * randn(K), [K, 1])
            u /= np.linalg.norm(u)
            return u.flatten()

        return sample

    @staticmethod
    def _constrain_reduction(xi, s, A, a):
        """
        Reduces the constraint problem to a single dimension by projecting the
        inequality constraints onto the given direction.

        Args:
        xi (np.ndarray): Current point in the feasible region.
        s (np.ndarray): Direction vector.
        A (np.ndarray): Matrix for inequality constraints.
        a (np.ndarray): Vector for inequality constraints.

        Returns:
        tuple:
            - upper (float): Upper limit for movement along the direction.
            - lower (float): Lower limit for movement along the direction.
            - s (np.ndarray): The original direction vector.
        """

        # take direction s, project the inequality constraints Ax <= a onto it, and sample
        y = (A @ xi) - a  # value of inequality constraints
        z = A @ s  # projected onto the slice

        upper = np.inf
        lower = -np.inf

        # find the *tightest* of all constrains in both directions
        K = len(y)
        for k in range(K):
            if z[k] > 0:
                upper = np.minimum(upper, -y[k] / z[k])
            elif z[k] < 0:
                lower = np.maximum(lower, -y[k] / z[k])

        return xi, upper, lower, s

    @staticmethod
    def _point_construction(xi, upper, lower, s):
        """
        Constructs a new random point within the feasible slice by sampling along
        the specified direction.

        Args:
        upper (float): Upper limit for the movement.
        lower (float): Lower limit for the movement.
        s (np.ndarray): Direction vector.

        Returns:
        np.ndarray: A new valid random point within the slice.

        """
        # sample:
        a = lower + (upper - lower) * np.random.rand()

        return xi + a * s

    @staticmethod
    def _project_and_sample(xi, s, A, a):
        """
        Projects a direction and samples along it while satisfying inequality constraints.

        Args:
            xi (np.ndarray): Current point.
            s (np.ndarray): Direction vector.
            A (np.ndarray): Matrix for inequality constraints.
            a (np.ndarray): Vector for inequality constraints.

        Returns:
            np.ndarray: New valid random point inside the polytope.
        """
        xi, s, A, a = Computation._constrain_reduction(xi, s, A, a)
        return Computation._point_construction(xi, s, A, a)

    @staticmethod
    def _handle_only_one_possible_initial_point(A, a, B, b):
        """
        Tries to find a valid point without adding any slack (eps = 0).
        If it finds one, it checks if it is the only solution by checking the null space of B.
        If there is no freedom to move or movement is extremely small, it returns the initial point.
        If there is freedom to move, it returns None, indicating that sampling might not be reliable.

        Args:
            A (np.ndarray): Matrix for inequality constraints A @ x <= a.
            a (np.ndarray): Vector for inequality constraints.
            B (np.ndarray): Matrix for equality constraints B @ x = b.
            b (np.ndarray): Vector for equality constraints.
        Returns:
            Two identical points if the solution is (almost) unique, otherwise None.
        """

        # Try to find a feasible point without slack, exactly on the boundary
        x0 = Computation._find_initial_point(A, a, B, b, eps=0.0)

        if x0 is None:
            return None

        # Generate a random direction that satisfies the equality constraints
        generate_direction = Computation._construct_directions(B)
        test_direction = generate_direction()

        # Check how far movement is allowed in this direction without violating inequalities
        _, step_limit_forward, step_limit_backward, _ = (
            Computation._constrain_reduction(x0, test_direction, A, a)
        )

        # Check the null space of B to see if there are possible movement directions
        null_space_basis, _ = Computation._svd_projection(B)

        # No valid directions available → the point is unique
        if null_space_basis.shape[1] == 0:
            print(
                "ℹ️ Found a unique point that satisfies all constraints. Returning it."
            )
            return np.tile(
                x0, (2, 1)  # Return the same point twice to allow mean/std calculations
            )

        # Only minimal movement possible → treat it as a unique solution
        if step_limit_forward - step_limit_backward < 1e-6:
            print("ℹ️ Movement directions are very small, returning the initial point.")
            return np.tile(
                x0, (2, 1)  # Return the same point twice to avoid sampling issues
            )

        # Movement is possible → not a unique solution
        print(
            "⚠️ Found an initial point in the boundary, but there are multiple valid solutions."
        )
        print("ℹ️ Returning None to indicate that sampling might not be reliable.")
        return None

    @staticmethod
    def _MCMC(A, a, B, b, num_iter=int(1e7), thinning=int(int(1e5) / 100)):
        """
        Runs the MCMC sampling algorithm under linear constraints.

        Args:
            A (np.ndarray): Matrix for inequality constraints A @ x <= a.
            a (np.ndarray): Vector for inequality constraints.
            B (np.ndarray): Matrix for equality constraints B @ x = b.
            b (np.ndarray): Vector for equality constraints.
            num_iter (int, optional): Total number of MCMC iterations. Defaults to 1e7.
            thinning (int, optional): Subsampling interval. Defaults to 1e5.

        Returns:
            np.ndarray: Sampled feasible points after thinning.
        """

        x0 = Computation._find_initial_point(
            A, a, B, b, eps=1e-6
        )  # adding some slack to ensure we are _within_ the feasible region, not just on the boundary
        # not doing this will cause trouble down the line for the MCMC method, which will get stuck in a corner

        # If that fails, check if there’s one valid solution on the boundary
        # In that case, check if it is the only valid solution (no direction to move in)
        if x0 is None:
            boundary_solution = Computation._handle_only_one_possible_initial_point(
                A, a, B, b
            )
            if boundary_solution is not None:
                return boundary_solution
            print("⚠️ MCMC aborted: No feasible starting point.")
            return None

        # Check if there are any valid directions to move (degrees of freedom) if the initial point with eps=1e-6 is feasible
        null_space_basis, _ = Computation._svd_projection(B)
        if null_space_basis.shape[1] == 0:
            print("ℹ️ No valid directions to move in, returning initial point.")
            return np.tile(
                x0, (2, 1)  # Needed to calculate mean and standard deviation
            )

        sample = Computation._construct_directions(B)

        D = A.shape[1]
        samples = np.zeros(shape=(num_iter, D))
        samples[0, :] = x0
        xi = x0

        for i in tqdm(range(num_iter - 1)):
            xi = Computation._project_and_sample(xi, sample(), A, a)
            samples[i + 1, :] = xi

        return samples[0::thinning, :]

    @staticmethod
    def compute_result(A, a, B, b, num_iter=int(1e5), thinning=int(1e4)):
        """
        Runs the MCMC sampling algorithm and calculates the mean and var for each ingredient.

        Args:
            A (np.ndarray): Matrix for inequality constraints A @ x <= a.
            a (np.ndarray): Vector for inequality constraints.
            B (np.ndarray): Matrix for equality constraints B @ x = b.
            b (np.ndarray): Vector for equality constraints.

        Returns:
            - mean_sample (np.ndarray): Mean of the sample.
            - std_sample (np.ndarray): Standard deviation the sample.
        """
        SAMPLES = Computation._MCMC(A, a, B, b, num_iter, thinning=int(int(1e5) / 100))
        if SAMPLES is None:  # adress None values
            print("⚠️ MCMC aborted: No valid samples.")
            return None, None
        if np.size(A) == 1:  # only one ingredient
            return np.array([100]), np.array([0])

        mean_sample = np.mean(SAMPLES, axis=0) * 100
        std_sample = np.std(SAMPLES, axis=0) * 2 * 100

        mean_sample_r = np.round(mean_sample, 2)
        std_sample_r = np.round(std_sample, 2)

        return mean_sample_r, std_sample_r
