import httpx

from backend.data_base_manager import api_client


class IngredientManager:
    """
    API calls for ingredients (``/ingredient`` endpoints of HackTheSnackDB,
    an alias of ``/substance``). Names are stored upper-case by the API.
    """

    @staticmethod
    def create_ingredient(ingredient_name: str) -> httpx.Response:
        """
        Creates an ingredient. Returns 201 with ``{"data": id}`` on success.
        """
        name = (ingredient_name or "").strip()
        return api_client.post("/ingredient", {"name": name, "description": name})

    @staticmethod
    def find_ingredient(ingredient_name: str) -> httpx.Response:
        """
        Looks an ingredient up by its exact name (case-insensitive).
        Returns 200 with the ingredient in ``data`` or 404.
        """
        return api_client.get(
            "/ingredient/detail",
            params={"name": (ingredient_name or "").upper().strip()},
        )

    @staticmethod
    def find_ingredient_list(ingredient_name: str = "") -> httpx.Response:
        """
        Lists ingredients whose name contains ``ingredient_name`` (all if empty).
        """
        return api_client.get(
            "/ingredient/list",
            params={"page": 1, "size": 500, "name": ingredient_name or ""},
        )

    @staticmethod
    def get_or_create_ingredient(ingredient_name: str) -> int:
        """
        Returns the id of an ingredient, creating it first if it does not exist.

        Raises:
            Exception: if the ingredient can neither be found nor created.
        """
        response = IngredientManager.find_ingredient(ingredient_name)
        if response.status_code == 200:
            data = api_client.json_data(response)
            if isinstance(data, dict) and data.get("id") is not None:
                return data["id"]

        create_response = IngredientManager.create_ingredient(ingredient_name)
        if create_response.status_code == 201:
            new_id = api_client.json_data(create_response)
            if new_id is not None:
                return new_id

        raise Exception(f"Failed to create ingredient: {ingredient_name}")

    @staticmethod
    def create_ingredient_list(ingredient_dict: dict) -> list[int]:
        """
        Finds or creates every ingredient of ``ingredient_dict`` (keys are names).

        Returns:
            list[int]: ingredient ids in the same order as the dictionary keys.
        """
        return [IngredientManager.get_or_create_ingredient(name) for name in ingredient_dict]
