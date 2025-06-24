import sys

sys.dont_write_bytecode = True

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

import flet as ft
import httpx
import json
from Frontend.src.add_product_table.logic.input_validator import InputValidator
from Frontend.src.add_product_table.logic.data_builder import IngredientDataBuilder
from Frontend.src.create_result_table.result_table_ui import RecipeResultUI
from styles import Styles
from Backend.recipe_generator import RecipeGenerator
from Backend.data_base_manager.recipe_manager import RecipeManager





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
        feedback_text.color = Styles.GREEN_COLOR
        feedback_text.size = Styles.FEEDBACK_FONT_SIZE
        page.update()

        # Extract product name and ingredient dictionary
        product_name = (product_name_field.value or "").strip()
        ingredient_dict = IngredientDataBuilder.build_data_from_rows(ingredient_rows)

        # Store recipe in data base
        RecipeManager.submit_recipe(product_name, ingredient_dict)
        
        # Generate the recipe using the RecipeGenerator from the backend
        result_dict = RecipeGenerator.generate_recipe(ingredient_dict)

        # Display the recipe result
        RecipeResultUI.display_recipe_result(page, result_dict)

