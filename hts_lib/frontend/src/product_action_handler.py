import flet as ft

from backend.data_base_manager.evaluation_manager import EvaluationManager
from backend.data_base_manager.product_manager import ProductManager
from backend.data_base_manager.recipe_manager import RecipeManager
from backend.translation import Translation
from frontend.src.add_product_table.logic.data_filler import DataFiller
from frontend.src.styles import Styles


class ProductActionHandler:
    """
    Database actions of the recipe generator page: search, autofill and save.
    Every method reports its outcome in the page's feedback text.
    """

    @staticmethod
    def _set_feedback(feedback_text: ft.Text, message: str, color: str) -> None:
        feedback_text.value = message
        feedback_text.color = color
        feedback_text.size = Styles.FEEDBACK_FONT_SIZE
        feedback_text.text_align = ft.TextAlign.CENTER

    @staticmethod
    def handle_product_search(product_name_field: ft.TextField, feedback_text: ft.Text, page: ft.Page):
        """
        Looks the entered product up and reports whether it exists.
        """
        found = ProductActionHandler.check_if_product_exists(product_name_field, feedback_text, page)
        if found:
            ProductActionHandler._set_feedback(feedback_text, "✅ Product found.", Styles.GREEN_COLOR)
            page.update()

    @staticmethod
    def check_if_product_exists(product_name_field: ft.TextField, feedback_text: ft.Text, page: ft.Page):
        """
        Returns True if a product with the entered name exists, False if not,
        and None when no name was entered or the database could not be reached
        (the reason is written to ``feedback_text``).
        """
        product_name = (product_name_field.value or "").strip()
        if not product_name:
            ProductActionHandler._set_feedback(
                feedback_text, "⚠️ Please enter a product name to search.", Styles.RED_COLOR
            )
            page.update()
            return None

        try:
            response = ProductManager.find_product(product_name)
        except Exception as ex:
            ProductActionHandler._set_feedback(
                feedback_text, ProductActionHandler.get_user_friendly_error_message(ex), Styles.RED_COLOR
            )
            page.update()
            return None

        if response.status_code == 200:
            feedback_text.value = ""
            page.update()
            return True

        if response.status_code == 404:
            ProductActionHandler._set_feedback(
                feedback_text,
                "❌ Product not found. Enter its ingredients and press Submit Product to analyze it.",
                Styles.RED_COLOR,
            )
        else:
            ProductActionHandler._set_feedback(
                feedback_text, f"❌ Search failed (HTTP {response.status_code}). Please try again.", Styles.RED_COLOR
            )
        page.update()
        return False

    @staticmethod
    def handle_search_and_fill(
        product_name_field: ft.TextField,
        feedback_text: ft.Text,
        page: ft.Page,
        ingredient_manager,
        store_values_callback,
    ) -> bool:
        """
        Loads a stored product and fills the ingredient table with its
        ingredients (in label order). Percentages are left empty for the user.

        Returns:
            bool: True if the table was filled.
        """
        try:
            response = ProductManager.find_product(product_name_field.value or "")
            if response.status_code != 200:
                ProductActionHandler._set_feedback(feedback_text, "❌ Product not found.", Styles.RED_COLOR)
                page.update()
                return False

            id_product = response.json()["data"]["id"]
            recipe_json = RecipeManager.find_product_ingredient_list(id_product).json()
            recipe_dict, ingredient_ids = Translation.product_table_filter(recipe_json)

            if not recipe_dict:
                ProductActionHandler._set_feedback(
                    feedback_text, "ℹ️ This product has no saved ingredients yet.", Styles.TEXT_COLOR
                )
                page.update()
                return False

            store_values_callback(id_product, ingredient_ids, [], None)
            DataFiller.fill_rows_from_data(recipe_dict, ingredient_manager)
            ProductActionHandler._set_feedback(
                feedback_text,
                f"✅ Loaded {len(recipe_dict)} ingredient(s). Add the known percentages and press Submit Product.",
                Styles.GREEN_COLOR,
            )
            page.update()
            return True
        except Exception as ex:
            ProductActionHandler._set_feedback(
                feedback_text, ProductActionHandler.get_user_friendly_error_message(ex), Styles.RED_COLOR
            )
            page.update()
            return False

    @staticmethod
    def handle_save_new_recipe(product_name_field, result_dict, store_values_callback) -> tuple[bool, str]:
        """
        Saves the generated recipe: product, ingredients, their associations and
        a new evaluation with the estimated percentages.

        Returns:
            (success, message) — the message is meant for the user.
        """
        product_name = (product_name_field.value or "").strip()
        if not product_name:
            return False, "⚠️ Please enter a product name before saving."
        if not result_dict:
            return False, "⚠️ Generate a recipe with Submit Product before saving."

        try:
            product_id, ingredient_ids, recipe_ids = RecipeManager.submit_recipe(product_name, result_dict)
            response = EvaluationManager.create_evaluation(product_id, ingredient_ids, recipe_ids, result_dict)
            if response.status_code != 201:
                return False, f"❌ The recipe could not be saved (HTTP {response.status_code}). Please try again."
            store_values_callback(
                product_id=product_id,
                ingredient_ids=ingredient_ids,
                recipe_ids=recipe_ids,
                result_dict=result_dict,
            )
            return True, f"✅ Recipe for “{product_name}” saved. You can find it in My Recipes."
        except Exception as ex:
            return False, ProductActionHandler.get_user_friendly_error_message(ex)

    @staticmethod
    def get_user_friendly_error_message(ex: Exception) -> str:
        """
        Turns a technical exception into a message the user understands.
        """
        error_message = str(ex).lower()
        if any(
            word in error_message
            for word in ("connection", "timeout", "timed out", "temporarily unavailable", "network", "failed to fetch")
        ):
            return (
                "⚠️ The database service is offline or still starting up.\n"
                "Please try again in a moment."
            )
        return "⚠️ Something went wrong while contacting the database. Please try again."
