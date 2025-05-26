import flet as ft
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from Frontend.src.add_product_table.logic.input_validator import InputValidator
from Frontend.src.add_product_table.logic.data_builder import IngredientDataBuilder
from Frontend.src.create_result_table.result_table_ui import RecipeResultUI


class ProductSubmitHandler:
    """
    Handles the submit action for the product ingredient table.

    Responsibilities:
    - Validates user input (product name and ingredients)
    - Builds a dictionary from the ingredient rows using IngredientDataBuilder
    - Provides visual feedback through the Flet UI
    - Triggers recipe generation and display
    """

    @staticmethod
    def handle_submit(
        product_name_field: ft.TextField,
        ingredient_rows: list[ft.Container],
        feedback_text: ft.Text,
        page: ft.Page,
    ) -> tuple[str, dict[str, float | None]] | None:
        """
        Validates the input and returns the product data if valid.

        Args:
            product_name_field (ft.TextField): Field with the product name.
            ingredient_rows (list[ft.Container]): UI rows with ingredients.
            feedback_text (ft.Text): UI text for validation messages.
            page (ft.Page): The current Flet page instance.

        Returns:
            tuple | None: (product name, ingredient dict) if valid, else None
        """
        # Validate all fields using InputValidator
        if not InputValidator.validate_all_inputs(
            product_name_field,
            ingredient_rows,
            feedback_text,
            page,
        ):
            return None

        # If valid, update UI feedback
        feedback_text.value = "✅ Product is valid. Recipe generated!"
        feedback_text.color = "green"
        page.update()

        # Extract product name and ingredient dictionary
        product_name = (product_name_field.value or "").strip()
        ingredient_dict = IngredientDataBuilder.build_data_from_rows(ingredient_rows)

        # Generate and display the recipe result
        RecipeResultUI.generate_and_display_recipe(page, ingredient_dict)

        return product_name, ingredient_dict
