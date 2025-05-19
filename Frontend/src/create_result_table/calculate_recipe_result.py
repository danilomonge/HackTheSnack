import flet as ft
from Backend.recipe_generator import RecipeGenerator


class RecipeResultCalculator:
    """
    Handles recipe generation using the RecipeGenerator.
    """

    def __init__(self):
        self.result = None

    def calculate_recipe(self, ingredients: dict[str, float | None]) -> bool:
        """
        Calls the recipe generator and stores the result.

        Args:
            ingredients (dict): Ingredient name and optional percentage.

        Returns:
            bool: True if generation was successful, else False.
        """
        self.result = RecipeGenerator.generate_recipe(ingredients)
        return self.result is not None

    def get_recipe_result(self) -> dict[str, dict[str, float]] | None:
        """
        Returns the stored recipe result.

        Returns:
            dict or None: Recipe result dictionary or None if not available.
        """
        return self.result
