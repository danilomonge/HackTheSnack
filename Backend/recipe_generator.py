import sys

sys.dont_write_bytecode = True

import numpy as np

from Backend.Input.validation import validate
from Backend.Input.constraints_preparation import prepare_constraints_dict
from Backend.constraints import build_inequality_constraints, build_equality_constraints
from Backend.computation import MCMC


class RecipeGenerator:
    """
    Generates a complete recipe suggestion from a partially defined ingredient dictionary.

    The process includes:
    - Validating input values
    - Preparing equality and inequality constraints
    - Running MCMC sampling under those constraints
    - Returning computed ingredient percentages and their estimated variation
    """

    @staticmethod
    def generate_recipe(
        ingredient_dict: dict[str, float | None],
    ) -> dict[str, dict[str, float]] | None:
        """
        Orchestrates the recipe generation process.

        Args:
            ingredient_dict (dict[str, float | None]):
                Dictionary of ingredient names with fixed percentages or None.

        Returns:
            dict[str, dict[str, float]]: Keys are ingredient names. Each value is a dict with:
                - "value": the computed percentage
                - "variation": the estimated variation (std deviation)
            None: If validation fails or computation errors occur.
        """
        if not RecipeGenerator._validate_input(ingredient_dict):
            return None

        # Special case: only one ingredient → assign 100%
        if len(ingredient_dict) == 1:
            ingredient_name = next(iter(ingredient_dict))
            return {ingredient_name: {"value": 100.0, "variation": 0.0}}

        try:
            samples = RecipeGenerator._compute_feasible_samples(ingredient_dict)
        except Exception as e:
            print(f"❌ MCMC computation failed: {e}")
            return None

        if samples is None:
            return None

        return RecipeGenerator._build_output_dict(ingredient_dict, samples)

    # ------------------ Helper Functions ------------------

    @staticmethod
    def _validate_input(ingredient_dict: dict[str, float | None]) -> bool:
        """
        Checks if input values are valid:
        - All fixed values must be > 0
        - Total sum must not exceed 100

        Returns:
            bool: True if valid, else False.
        """
        if not validate(ingredient_dict):
            print(
                "❌ Invalid input: All fixed values must be > 0 and total must not exceed 100%."
            )
            return False
        return True

    @staticmethod
    def _compute_feasible_samples(
        ingredient_dict: dict[str, float | None],
    ) -> np.ndarray | None:
        """
        Prepares constraints and runs the MCMC algorithm.

        Returns:
            np.ndarray | None: Array of sampled ingredient combinations, or None if infeasible.
        """
        num_ingredients = len(ingredient_dict)
        fixed_values = prepare_constraints_dict(ingredient_dict)

        A, a = build_inequality_constraints(num_ingredients)
        B, b = build_equality_constraints(fixed_values, num_ingredients)

        samples = MCMC(A, a, B, b, num_iter=int(1e5), thinning=int(1e4))

        if samples is None:
            print("⚠️ Recipe generation skipped due to infeasible constraint setup.")
            return None

        return samples

    @staticmethod
    def _build_output_dict(
        ingredient_dict: dict[str, float | None], samples: np.ndarray
    ) -> dict[str, dict[str, float]]:
        """
        Builds the final result dictionary from MCMC samples.

        Returns:
            dict: Ingredient name → { "value": %, "variation": ±% }
        """
        final_sample = samples[-1]
        std_deviation = samples.std(axis=0)
        ingredient_names = list(ingredient_dict.keys())

        result_dict = {
            name: {"value": round(percent * 100, 4), "variation": round(std * 100, 4)}
            for name, percent, std in zip(ingredient_names, final_sample, std_deviation)
        }

        return result_dict
