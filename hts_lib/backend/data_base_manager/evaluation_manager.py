import httpx

from backend.data_base_manager import api_client


class EvaluationManager:
    """
    API calls for evaluations (saved recipe estimations, ``/evaluation`` endpoints).
    """

    @staticmethod
    def create_evaluation(
        product_id: int,
        ingredient_ids: list[int],
        recipe_ids: list[int],
        result_dict: dict[str, dict[str, float]],
    ) -> httpx.Response:
        """
        Saves one recipe estimation for a product.

        Args:
            product_id: product id.
            ingredient_ids: ingredient ids, in the same order as ``result_dict``.
            recipe_ids: recipe (association) ids, in the same order as ``result_dict``.
            result_dict: ``{ingredient_name: {"mean": float, "variation": float}}``.

        Returns:
            httpx.Response: 201 with ``{"data": evaluation_id}`` on success.
        """
        data = EvaluationManager.build_results_payload(product_id, ingredient_ids, recipe_ids, result_dict)
        return api_client.post("/evaluation", data)

    @staticmethod
    def build_results_payload(
        product_id: int,
        ingredient_ids: list[int],
        recipe_ids: list[int],
        result_dict: dict[str, dict[str, float]],
    ) -> dict:
        """
        Builds the JSON body of ``POST /evaluation``.

        Raises:
            ValueError: if the lists and the result dictionary differ in length or are empty.
        """
        if not (len(recipe_ids) == len(ingredient_ids) == len(result_dict)):
            raise ValueError("recipe_ids, ingredient_ids, and result_dict must all be the same length.")
        if not result_dict:
            raise ValueError("result_dict must contain at least one ingredient.")

        result_list = []
        for recipe_id, ingredient_id, (_, stats) in zip(recipe_ids, ingredient_ids, result_dict.items()):
            result_list.append({
                "recipeId": recipe_id,
                "ingredientId": ingredient_id,
                "ingredientMeanPercentage": float(stats.get("mean", 0.0) or 0.0),
                "ingredientStdPercentage": float(stats.get("variation", 0.0) or 0.0),
            })

        first = result_list[0]
        return {
            "idProduct": product_id,
            "idIngredient": first["ingredientId"],
            "idRecipe": first["recipeId"],
            "ingredientMeanPercentage": first["ingredientMeanPercentage"],
            "ingredientStdPercentage": first["ingredientStdPercentage"],
            "resultList": result_list,
        }

    @staticmethod
    def find_evaluation_list(product_id: int) -> httpx.Response:
        """
        Lists the evaluations of a product.
        """
        return api_client.get("/evaluation/list", params={"idProduct": product_id})

    @staticmethod
    def find_evaluation_detail(evaluation_id: int) -> httpx.Response:
        """
        Gets one evaluation, including its ``resultList``.
        """
        return api_client.get("/evaluation/detail", params={"id": evaluation_id})

    @staticmethod
    def find_evaluation_product_ingredient(product_id, ingredient_id) -> httpx.Response:
        """
        Lists saved result lines filtered by product and/or ingredient.
        Pass 0 (or None) to leave a filter out.
        """
        return api_client.get(
            "/evaluation/listResult",
            params={
                "idProduct": product_id or "",
                "idIngredient": ingredient_id or "",
            },
        )
