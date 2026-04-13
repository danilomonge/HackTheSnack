import numpy as np

from .input.constraints_preparation import prepare_constraints_dict
from .algorithm.constraints import Constraints
from .algorithm_skipper import AlgorithmSkipper


class RecipeGenerator:
    """
    Class for generating a complete recipe from partially defined ingredient percentages.

    It checks the input, handles simple cases directly,
    and uses MCMC when more than one value is missing.
    """

    @staticmethod
    def generate_recipe(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]] | None:
        """
        Main function that decides how to process the ingredient data:
        - If the input matches a skip condition (e.g., only one ingredient, or sum is already 100%),
        it uses AlgorithmSkipper to return the result directly and skip all algorithm process.
        - Otherwise, it runs the complete algorithm to generate the recipes.
        """

        # Tries to skip the algorithm if possible (with the help of AlgorithmSkipper)
        skipped_result = AlgorithmSkipper.skip_algorithm(ingredient_input)
        if skipped_result is not None:
            return skipped_result

        # Otherwise, runs the full algorithm
        return RecipeGenerator.solve_with_mcmc(ingredient_input)

    @staticmethod
    def solve_with_fallback(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]] | None:
        """
        Builds a deterministic, order-preserving approximation when SciPy-backed
        sampling is unavailable in the web runtime.
        """
        items = list(ingredient_input.items())
        values = [value for _, value in items]
        missing_indexes = [index for index, value in enumerate(values) if value is None]

        if not missing_indexes:
            return AlgorithmSkipper.solve_total_is_100_percent_ingredient_case(ingredient_input)

        fixed_total = sum(value for value in values if value is not None)
        remaining = 1.0 - fixed_total
        if remaining < -1e-9:
            return None

        lower_bounds = []
        upper_bounds = []

        for index in missing_indexes:
            lower_bound = 0.0
            for next_index in range(index + 1, len(values)):
                next_value = values[next_index]
                if next_value is not None:
                    lower_bound = next_value
                    break

            upper_bound = 1.0
            for previous_index in range(index - 1, -1, -1):
                previous_value = values[previous_index]
                if previous_value is not None:
                    upper_bound = previous_value
                    break

            lower_bounds.append(lower_bound)
            upper_bounds.append(upper_bound)

        lower_total = sum(lower_bounds)
        if lower_total - remaining > 1e-9:
            return None

        assigned = lower_bounds[:]
        capacities = [
            max(0.0, upper_bound - lower_bound)
            for lower_bound, upper_bound in zip(lower_bounds, upper_bounds)
        ]
        extra = max(0.0, remaining - lower_total)
        weights = [len(missing_indexes) - offset for offset in range(len(missing_indexes))]

        while extra > 1e-9:
            active = [
                idx for idx, capacity in enumerate(capacities)
                if capacity > 1e-9
            ]
            if not active:
                break

            weight_sum = sum(weights[idx] for idx in active)
            progressed = False

            for idx in active:
                share = extra * (weights[idx] / weight_sum)
                delta = min(share, capacities[idx])
                if delta > 0:
                    assigned[idx] += delta
                    capacities[idx] -= delta
                    extra -= delta
                    progressed = True

            if not progressed:
                break

        if extra > 1e-6:
            return None

        completed_values = values[:]
        for missing_index, assigned_value in zip(missing_indexes, assigned):
            completed_values[missing_index] = assigned_value

        result = {}
        for (name, _), completed_value in zip(items, completed_values):
            assert completed_value is not None
            result[name] = {
                "mean": round(completed_value * 100, 4),
                "variation": 0.0,
            }

        return result

    @staticmethod
    def solve_with_mcmc(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]] | None:
        """
        Builds the constraint system and runs the MCMC algorithm
        to sample valid combinations when multiple values are unknown.
        """
        try:
            from .algorithm.computation import Computation
            num_ingredients = len(ingredient_input)
            fixed_values = prepare_constraints_dict(ingredient_input)

            A, a = Constraints.build_inequality_constraints(num_ingredients)
            B, b = Constraints.build_equality_constraints(fixed_values, num_ingredients)

            mean_result, std_dev_result = Computation.compute_result(
                A, a, B, b, num_iter=int(5e4), thinning=int(1e3)
            )

            if mean_result is None or std_dev_result is None:
                print("⚠️ MCMC failed or returned no valid samples.")
                return None

            return RecipeGenerator.build_output_dict(
                ingredient_input, mean_result, std_dev_result
            )
        except Exception as ex:
            print(f"⚠️ Sampling backend is unavailable in this runtime ({ex}). Using deterministic fallback.")
            return RecipeGenerator.solve_with_fallback(ingredient_input)

    @staticmethod
    def build_output_dict(
        ingredient_input: dict[str, float | None], means: np.ndarray, stds: np.ndarray
    ) -> dict[str, dict[str, float]]:
        """
        Formats the output by taking the mean of the samples and calculating the variation
        (standard deviation) for each ingredient.
        """
        ingredient_names = list(ingredient_input.keys())

        return {
            name: {"mean": val, "variation": std}
            for name, val, std in zip(ingredient_names, means, stds)
        }
