# product_creator.py

import httpx
import json
import flet as ft


class ProductManager:
    """
    Handles API interactions for product-related actions.

    Attributes:
        page (ft.Page): The Flet page object for UI updates.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the ProductCreator with a reference to the Flet page.

        Args:
            page (ft.Page): The active Flet page instance.
        """
        self.page = page

    def create_product(self, product_name: ft.TextField, result_text: ft.Text):
        """
        Sends a POST request to create a product in the database.

        Args:
            product_name (ft.TextField): The input field containing the product name.
            result_text (ft.Text): A text element to display the result status.
        """
        try:
            data = {
                "name": product_name.value,
                "descripcion": "delicious",      # Default description; can be extended later
                "idBrand": 1,           # Default brand ID
                "idCategory": 1,        # Default category ID
                "idSubCategory": 1      # Default subcategory ID
            }
            response = httpx.post(
                "http://localhost:8087/user-management/product",
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )

            if response.status_code == 201:
                result_text.value = "✅ Product created successfully!"
                product_name.value = ""
            else:
                result_text.value = f"❌ Error {response.status_code}: {response.text}"
        except Exception as ex:
            result_text.value = f"⚠️ Exception: {ex}"

        self.page.update()

    def find_product(self, product_name: ft.TextField, result_text: ft.Text):
        """
        Searches for a product by name and autofills the description if found.

        Args:
        product_name (ft.TextField): The input field with the product name.
        descripcion_field (ft.TextField): The field to fill with the product's description.
        result_text (ft.Text): A text field to show status messages.
        """
        try:
            name = product_name.value
            if not name:
                result_text.value = "⚠️ Please enter a product name to search."
                self.page.update()
                return

            response = httpx.get(f"http://localhost:8087/user-management/product/detail?name={name}")

            if response.status_code == 200:
                product_data = response.json()
                id_product = product_data['data']['id']
                result_text.value = "✅ Product found."
            elif response.status_code == 404:
                result_text.value = "❌ Product not found."
            else:
                result_text.value = f"❌ Error {response.status_code}: {response.text}"
        except Exception as ex:
            result_text.value = f"⚠️ Exception: {ex}"

        self.page.update()

