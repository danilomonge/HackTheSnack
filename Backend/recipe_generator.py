import sys

sys.dont_write_bytecode = True

import numpy as np

from Backend.Input.validation import validate
from Backend.Input.constraints_preparation import prepare_constraints_dict
from Backend.constraints import build_inequality_constraints, build_equality_constraints
from Backend.computation import compute_result


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
        - If only one ingredient: assign 100%
        - If one ingredient is missing: compute it directly
        - Otherwise: run MCMC to generate valid percentage combinations
        """
        if not RecipeGenerator.validate_input(ingredient_input):
            return None

        if RecipeGenerator.has_only_one_ingredient(ingredient_input):
            return RecipeGenerator.solve_single_ingredient_case(ingredient_input)

        if RecipeGenerator.has_exactly_one_missing(ingredient_input):
            return RecipeGenerator.solve_one_missing_directly(ingredient_input)

        return RecipeGenerator.solve_with_mcmc(ingredient_input)

    @staticmethod
    def validate_input(ingredient_input: dict[str, float | None]) -> bool:
        """
        Validates the input by checking:
        - All fixed values must be > 0
        - Total of all fixed values must not exceed 100%
        """
        if not validate(ingredient_input):
            print("❌ Invalid input: fixed values must be > 0 and total ≤ 100%.")
            return False
        return True

    @staticmethod
    def has_only_one_ingredient(ingredient_input: dict[str, float | None]) -> bool:
        """
        Returns True if the input contains only one ingredient.
        """
        return len(ingredient_input) == 1

    @staticmethod
    def solve_single_ingredient_case(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]]:
        """
        If there's just one ingredient, its percentage is 100% with no variation.
        """
        name = next(iter(ingredient_input))
        return {name: {"value": 100.0, "variation": 0.0}}

    @staticmethod
    def has_exactly_one_missing(ingredient_input: dict[str, float | None]) -> bool:
        """
        Returns True if exactly one ingredient is missing (value is None).
        """
        return sum(1 for v in ingredient_input.values() if v is None) == 1

    @staticmethod
    def solve_one_missing_directly(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]] | None:
        """
        Calculates the missing value by subtracting the known total from 1.
        Useful when only one ingredient is unknown.
        """
        known = {k: v for k, v in ingredient_input.items() if v is not None}
        unknown = [k for k in ingredient_input if ingredient_input[k] is None]

        known_total = sum(known.values())
        missing_value = 1.0 - known_total

        if missing_value < 0:
            print("❌ Error: known percentages exceed 100%.")
            return None

        result = {
            name: {"value": round(val * 100, 4), "variation": 0.0}
            for name, val in known.items()
        }
        result[unknown[0]] = {"value": round(missing_value * 100, 4), "variation": 0.0}

        print("ℹ️ Only one missing value. Calculated directly.")
        return result

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

        A, a = build_inequality_constraints(num_ingredients)
        B, b = build_equality_constraints(fixed_values, num_ingredients)

        mean_result, std_dev_result = compute_result(A, a, B, b, num_iter=int(1e5), thinning=int(1e4))

        if mean_result is None or std_dev_result is None:
            print("⚠️ MCMC failed or returned no valid samples.")
            return None

        return RecipeGenerator.build_output_dict(ingredient_input, mean_result, std_dev_result)

    @staticmethod
    def build_output_dict(
        ingredient_input: dict[str, float | None], means: np.ndarray, stds: np.ndarray
    ) -> dict[str, dict[str, float]]:
        """
        Formats the output by taking the last sample and calculating the variation
        (standard deviation) for each ingredient.
        """
        ingredient_names = list(ingredient_input.keys())

        #result = dict[means, stds]
        #output = dict[ingredient_names, result]

        return {
            name: {"mean": val , "variation": std }
            for name, val, std in zip(ingredient_names, means, stds)
        }
