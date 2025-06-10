import flet as ft
import httpx
import json
from DataBase.product_manager import ProductManager
from add_product_table.logic.input_validator import InputValidator
from add_product_table.logic.data_builder import IngredientDataBuilder


class ProductActionHandler:
    """
    Handles the search and create actions of the products.

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
                product_data = response.json()
                id_product = product_data['data']['id']
                feedback_text.value = "✅ Product found."
            elif response.status_code == 404:
                feedback_text.value = "❌ Product not found."
            else:
                feedback_text.value = f"❌ Error {response.status_code}: {response.text}"
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
            else:
                feedback_text.value = f"❌ Error {response.status_code}: {response.text}"
        except Exception as ex:
            feedback_text.value = f"⚠️ Exception: {ex}"

        page.update()

