import httpx
import json

from backend.data_base_manager.db_config import get_user_management_url


class IngredientManager:
    """
    Handles API interactions for ingredient-related actions.
    Maps to the /ingredient endpoints on FakeTheSnackDB
    (which are aliases of the /substance endpoints).
    """

    @staticmethod
    def _base_url() -> str:
        return f"{get_user_management_url()}/ingredient"

    @staticmethod
    def create_ingredient(ingredient_name):
        """
        Sends a POST request to create an ingredient in the database.

        Args:
        ingredient_name (str): The name of the ingredient to create.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
        """
        data = {
                "name": ingredient_name,
                "description": ingredient_name,
            }

        response = httpx.post(
                IngredientManager._base_url(),
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )

        return response

    @staticmethod
    def find_ingredient(ingredient_name):
        """
        Searches for an ingredient by name in the database.

        Args:
        ingredient_name (str): The name of the ingredient to search for.

        Returns:
        httpx.Response
        """
        response = httpx.get(
            f"{IngredientManager._base_url()}/detail?name={ingredient_name}"
        )
        return response

    @staticmethod
    def find_ingredient_list(ingredient_name):
        """
        Searches for multiple ingredients by name in the database.

        Args:
        ingredient_name (str): The name of the ingredient to search for.

        Returns:
        httpx.Response
        """
        response = httpx.get(
            f"{IngredientManager._base_url()}/list?page=1&size=500&name={ingredient_name}"
        )
        return response

    @staticmethod
    def create_ingredient_list(ingredient_dict: dict) -> list[int]:
        """
        Takes a dictionary of ingredients and searches or creates them in the backend.

        Args:
            ingredient_dict (dict[str, int]): Dictionary mapping ingredient names to their IDs.

        Returns:
            list[int]: List of ingredient IDs.
        """
        ingredient_ids = []

        for name in ingredient_dict.keys():
            response = IngredientManager.find_ingredient(name)

            if response.status_code == 200 and response.json().get("success"):
                data = response.json().get("data")
                if data:
                    ingredient_ids.append(data["id"])
                    continue

            create_response = IngredientManager.create_ingredient(name)
            if create_response.status_code == 201 and create_response.json().get("success"):
                id_ingredient = create_response.json().get("data")
                ingredient_ids.append(id_ingredient)
                continue
            else:
                raise Exception(f"Failed to create ingredient: {name}")

        return ingredient_ids
