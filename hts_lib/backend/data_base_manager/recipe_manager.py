import httpx
import json

from backend.data_base_manager.db_config import get_user_management_url
from backend.data_base_manager.ingredient_manager import IngredientManager
from backend.data_base_manager.product_manager import ProductManager

_TIMEOUT = 45.0


class RecipeManager:
    """
    Handles API interactions for product-ingredient associations (recipes).
    """

    @staticmethod
    def _base_url() -> str:
        return f"{get_user_management_url()}/recipe"

    @staticmethod
    def submit_recipe(product_name: str, ingredient_dict: dict[str, float]) -> tuple[int, list[int], list[int]]:
        """
        Creates and associates a product with a series of ingredients.

        Args:
        product_name (str):     The name of the product.
        ingredient_dict (dict):  The ingredient dictionary with percentage values.

        Returns:
        product_id (int): Product database ID
        id_ingredients (list[int]): List of ingredient IDs
        recipe_ids (list[int]): List of recipe (product-ingredient association) IDs
        """
        id_ingredients = IngredientManager.create_ingredient_list(ingredient_dict)

        product_response = ProductManager.create_product(product_name)

        if product_response.status_code == 201:
            product_data = product_response.json()
            id_product = product_data['data']
        else:
            product_data = ProductManager.find_product_id(product_name)
            id_product = product_data['id']

        recipe_ids = RecipeManager.associate_ingredients_to_product(id_product, id_ingredients)

        return id_product, id_ingredients, recipe_ids

    @staticmethod
    def associate_product_ingredient(idProduct, idIngredient):
        """
        Sends a POST request to associate an ingredient with a product.

        Args:
        idProduct (int):     The product ID.
        idIngredient (int):  The ingredient ID.

        Returns:
        httpx.Response
        """
        data = {
                "idProduct": idProduct,
                "idIngredient": idIngredient,
                "fechaRegistro": "2025-06-05",
            }

        response = httpx.post(
                RecipeManager._base_url(),
                headers={"Content-Type": "application/json"},
                content=json.dumps(data),
                timeout=_TIMEOUT,
            )

        return response

    @staticmethod
    def associate_ingredients_to_product(idProduct: int, ingredient_ids: list[int]) -> list[int]:
        """
        Associates all ingredient IDs to a given product ID via the API.

        Args:
            idProduct (int): The product ID to associate with.
            ingredient_ids (list[int]): List of ingredient IDs to associate.

        Returns:
            recipe_ids (list[int]): List of recipe IDs
        """
        recipe_ids = []

        for id_ingredient in ingredient_ids:
            response = RecipeManager.associate_product_ingredient(idProduct, id_ingredient)

            if response.status_code == 201:
                recipe_data = response.json()
                recipe_ids.append(recipe_data['data'])
                print(f"Associated ingredient {id_ingredient} with product {idProduct}")

            elif response.status_code == 400:
                recipe_search_response = RecipeManager.find_detail_product_ingredient(idProduct, id_ingredient)
                recipe_data = recipe_search_response.json()
                recipe_ids.append(recipe_data['data']['idRecipe'])

            else:
                print(f"Error: {response.status_code} while associating ingredient {id_ingredient}")

        return recipe_ids

    @staticmethod
    def delete_product_ingredient(idProduct, idIngredient):
        """
        Deletes the association between a product and an ingredient.

        Returns:
        httpx.Response
        """
        response = httpx.delete(
            f"{RecipeManager._base_url()}/deleteByProduct/?idProduct={idProduct}&idIngredient={idIngredient}",
            timeout=_TIMEOUT,
        )
        return response

    @staticmethod
    def find_product_ingredient_list(idProduct):
        """
        Searches for the ingredients related to a product.

        Returns:
        httpx.Response
        """
        response = httpx.get(
            f"{RecipeManager._base_url()}/list?page=1&size=10&orderBy&orderType&id={idProduct}",
            timeout=_TIMEOUT,
        )
        return response

    @staticmethod
    def find_detail_product_ingredient(idProduct, idIngredient):
        """
        Gets the details of a specific product-ingredient association.

        Returns:
        httpx.Response
        """
        response = httpx.get(
            f"{RecipeManager._base_url()}/detailRecipeByProduct?idProduct={idProduct}&idIngredient={idIngredient}",
            timeout=_TIMEOUT,
        )
        return response
