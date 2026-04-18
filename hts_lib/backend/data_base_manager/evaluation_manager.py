import httpx
import json

from backend.data_base_manager.db_config import get_user_management_url


class EvaluationManager:
    """
    Handles API interactions for evaluation-related actions.
    """

    @staticmethod
    def _base_url() -> str:
        return f"{get_user_management_url()}/evaluation"

    @staticmethod
    def create_evaluation(product_id,
        ingredient_ids: list[int],
        recipe_ids: list[int],
        result_dict: dict[str, dict[str, float]]):
        """
        Sends a POST request to create an evaluation in the database.

        Args:
        product_id (int): Product ID
        ingredient_ids (list[int]): List of ingredient IDs matching the result_dict order.
        recipe_ids (list[int]): List of recipe IDs, one per ingredient.
        result_dict (dict[str, dict[str, float]]): Dict with ingredient names as keys and their stats.

        Returns:
        httpx.Response
        """
        data = EvaluationManager.build_results_payload(
            product_id, ingredient_ids, recipe_ids, result_dict
        )

        response = httpx.post(
                EvaluationManager._base_url(),
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )

        return response

    @staticmethod
    def build_results_payload(
        product_id,
        ingredient_ids: list[int],
        recipe_ids: list[int],
        result_dict: dict[str, dict[str, float]]
    ) -> dict:
        """
        Builds the JSON payload for the POST evaluation service.
        """
        if not (len(recipe_ids) == len(ingredient_ids) == len(result_dict)):
            raise ValueError(
                "recipe_ids, ingredient_ids, and result_dict must all be the same length."
            )

        result_list = []
        for recipe_id, ingredient_id, (ingredient, stats) in zip(
            recipe_ids, ingredient_ids, result_dict.items()
        ):
            result_entry = {
                "recipeId": recipe_id,
                "ingredientId": ingredient_id,
                "ingredientMeanPercentage": stats.get("mean", 0.0),
                "ingredientStdPercentage": stats.get("variation", 0.0),
            }
            result_list.append(result_entry)

        return {
            "idProduct": product_id,
            "idIngredient": ingredient_ids[0],
            "idRecipe": recipe_ids[0],
            "ingredientMeanPercentage": 0.5,
            "ingredientStdPercentage": 0.2,
            "resultList": result_list
        }

    @staticmethod
    def find_evaluation_list(product_id):
        """
        Searches for all evaluations related to one product ID.
        """
        response = httpx.get(
            f"{EvaluationManager._base_url()}/list?page=1&size=10&orderBy&orderType&idProduct={product_id}"
        )
        return response

    @staticmethod
    def find_evaluation_detail(product_id):
        """
        Searches for the details of an evaluation by id.
        """
        response = httpx.get(
            f"{EvaluationManager._base_url()}/detail?id={product_id}"
        )
        return response

    @staticmethod
    def find_evaluation_product_ingredient(product_id, ingredient_id):
        """
        Searches all evaluations related to a product and ingredient ID.
        """
        if product_id == 0:
            product_id = ""
        if ingredient_id == 0:
            ingredient_id = ""

        response = httpx.get(
            f"{EvaluationManager._base_url()}/listResult?page=1&size=50&orderBy&orderType"
            f"&idProduct={product_id}&idIngredient={ingredient_id}"
        )
        return response
