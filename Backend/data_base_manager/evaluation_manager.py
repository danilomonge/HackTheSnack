import httpx
import json

class EvaluationManager:
    """
    Handles API interactions for evaluation-related actions.

    Attributes:
        page (ft.Page): The Flet page object for UI updates.
        
    """
    @staticmethod
    def create_evaluation(product_id, 
        ingredient_ids: list[int],
        recipe_ids: list[int],
        result_dict: dict[str, dict[str, float]]):
        """
        Sends a POST request to create an evaluation in the database.

        Args:
        result_dict (dict[str, dict[str, float]]): Dict with ingredient names as keys and their stats.
        recipe_ids (list[int]): List of recipe IDs, one per ingredient.
        ingredient_ids (list[int]): List of ingredient IDs matching the result_dict order.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data
        """
        
        data = EvaluationManager.build_results_payload(product_id, ingredient_ids, recipe_ids, result_dict)
        
        response = httpx.post(
                "http://localhost:8087/user-management/evaluation",
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )
        
        print(json.dumps(data))
        return response

    @staticmethod
    def build_results_payload( 
        product_id, 
        ingredient_ids: list[int],
        recipe_ids: list[int],
        result_dict: dict[str, dict[str, float]]  
    ) -> dict:
        """
        Builds a full result payload with static top-level product info and dynamic result list.

        Args:
            result_dict (dict[str, dict[str, float]]): Dict with ingredient names as keys and their stats.
            recipe_ids (list[int]): List of recipe IDs, one per ingredient.
            ingredient_ids (list[int]): List of ingredient IDs matching the result_dict order.

        Returns:
            dict: Payload with overall stats and a resultList of per-recipe stats.
        """
        if not (len(recipe_ids) == len(ingredient_ids) == len(result_dict)):
            raise ValueError("recipe_ids, ingredient_ids, and result_dict must all be the same length.")

        result_list = []
        for recipe_id, ingredient_id, (ingredient, stats) in zip(recipe_ids, ingredient_ids, result_dict.items()):
            result_entry = {
                "recipeId": recipe_id,
                "ingredientId": ingredient_id,
                "ingredientMeanPercentage": stats.get("mean", 0.0),
                "ingredientStdPercentage": stats.get("variation", 0.0),
            }
            result_list.append(result_entry)

        # Static + example values for demonstration (you can parameterize these later)
        return {
            "idProduct": 1, #to be updated to specify product
            "idIngredient": 1,
            "idRecipe": 1,
            "ingredientMeanPercentage": 5.55,
            "ingredientStdPercentage": 3.03,
            "evaluationDate": "2025-06-13",
            "resultList": result_list
        }