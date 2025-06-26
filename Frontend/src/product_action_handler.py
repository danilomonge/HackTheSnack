import sys

sys.dont_write_bytecode = True

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

import flet as ft
from Backend.data_base_manager.product_manager import ProductManager
from Backend.data_base_manager.recipe_manager  import RecipeManager
from Frontend.src.add_product_table.logic.data_filler import DataFiller
from Backend.translation import Translation
from Frontend.src.add_product_table.logic.input_validator import InputValidator
from Frontend.src.add_product_table.logic.data_builder import IngredientDataBuilder
from styles import Styles



class ProductActionHandler:
    """
    Handles frontend actions after recieving information data.

    """
    @staticmethod
    def handle_product_search(
        product_name_field: ft.TextField,
        feedback_text: ft.Text,
        page: ft.Page,
    ):
        """
        Handles the product search operation based on user input.

        This method retrieves the product name from the input field, 
        sends a request to the backend to find the product, and updates 
        the UI with the appropriate feedback message based on the result.

        Args:
            product_name_field (ft.TextField): Field with the product name.
            feedback_text (ft.Text): UI text for validation messages.
            page (ft.Page): The current Flet page instance.

        Returns:
            tuple | None: (product name, ingredient dict) if valid, else None
        """
        
        try:
            product_name = product_name_field.value
            if not product_name:
                feedback_text.value = "⚠️ Please enter a product name to search."
                page.update()
                return
            
            response = ProductManager.find_product(product_name)
            
            if response.status_code == 200:
                feedback_text.value = "✅ Product found."
                feedback_text.color = Styles.GREEN_COLOR
                feedback_text.size = Styles.FEEDBACK_FONT_SIZE
            elif response.status_code == 404:
                feedback_text.value = "❌ Product not found."
                feedback_text.color = Styles.RED_COLOR
                feedback_text.size = Styles.FEEDBACK_FONT_SIZE
            else:
                feedback_text.value = f"❌ Error {response.status_code}: {response.text}"
                feedback_text.color = Styles.RED_COLOR
                feedback_text.size = Styles.FEEDBACK_FONT_SIZE
        except Exception as ex:
            feedback_text.value = f"⚠️ Exception: {ex}"

        page.update()

    @staticmethod
    def check_if_product_exists(
        product_name_field: ft.TextField,
        feedback_text: ft.Text,
        page: ft.Page,):
        """
        Searches for a product by name in the database and returns a boolean statement

        Args:
        product_name (str): The name of the product to search for.

        Returns:
        boolean: True if the product exists and false if it does not 
        """
        try:
            product_name = product_name_field.value
            if not product_name:
                feedback_text.value = "⚠️ Please enter a product name to search."
                page.update()
                return
        
            response = ProductManager.find_product(product_name)

            if response.status_code == 200:
                #feedback_text.value = "✅ Product found."
                page.update()
                return True
            else:
                feedback_text.value = "❌ Product not found."
                page.update()
                return False
        except Exception as ex:
            feedback_text.value = f"⚠️ Exception: {ex}"

        page.update()

    


    @staticmethod
    def handle_create_product(product_name_field: ft.TextField, 
                       feedback_text: ft.Text, 
                       page: ft.Page,):
        """
        Sends a POST request to create a product in the database and updates the feedback text.

        Args:
            product_name (ft.TextField): The input field containing the product name.
            feedback_text (ft.Text): A text element to display the result status.
        """
        try:
            product_name = product_name_field.value
            if not product_name:
                feedback_text.value = "⚠️ Please enter a product name to create."
                page.update()
                return
            
            response = ProductManager.create_product(product_name)

            if response.status_code == 201:

                feedback_text.value = "✅ Product created successfully!"
                feedback_text.color = Styles.GREEN_COLOR
                feedback_text.size = Styles.FEEDBACK_FONT_SIZE
            else:
                feedback_text.value = f"❌ Error {response.status_code}: {response.text}"
                feedback_text.color = Styles.RED_COLOR
                feedback_text.size = Styles.FEEDBACK_FONT_SIZE
        except Exception as ex:
            feedback_text.value = f"⚠️ Exception: {ex}"

        page.update()

    @staticmethod
    def handle_search_and_fill(product_name_field: ft.TextField, 
                          feedback_text: ft.Text,
                          page: ft.Page,
                          ingredient_manager):
        """
        Sends a GET request to search a product in the database. If the product exist sends a request
        to get all their related ingredients and fills the product table automatically.

        Args:
            product_name (ft.TextField): The input field containing the product name.
            feedback_text (ft.Text): A text element to display the result status.
        """
        try:
            product_name = product_name_field.value
            
            response = ProductManager.find_product(product_name)

            if response.status_code == 200:
                product_data = response.json()
                id_product = product_data['data']['id']

                data = RecipeManager.find_product_ingredient_list(id_product)
                recipe_json = data.json()
                recipe_dict = Translation.product_table_filter(recipe_json)
                DataFiller.fill_rows_from_data(recipe_dict, ingredient_manager)
            
        except Exception as ex:
            feedback_text.value = f"⚠️ Exception: {ex}"
        
        page.update()
    

