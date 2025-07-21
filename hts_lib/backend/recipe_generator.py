import sys
import numpy as np

from .input.constraints_preparation import prepare_constraints_dict
from .algorithm.constraints import Constraints
from .algorithm.computation import Computation
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
    def solve_with_mcmc(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]] | None:
        """
        Builds the constraint system and runs the MCMC algorithm
        to sample valid combinations when multiple values are unknown.
        """
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
