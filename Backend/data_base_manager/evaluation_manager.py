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
        
        return response

    @staticmethod
    def build_results_payload( 
        product_id, 
        ingredient_ids: list[int],
        recipe_ids: list[int],
        result_dict: dict[str, dict[str, float]]  
    ) -> dict:
        """
        Builds an arrangement for the POST evaluation service with static top-level product info and dynamic result list.

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

        return {
            "idProduct": product_id,
            "idIngredient": ingredient_ids[0],
            "idRecipe": recipe_ids[0],
            "ingredientMeanPercentage": 5.55,
            "ingredientStdPercentage": 3.03,
            "evaluationDate": "2025-06-13",
            "resultList": result_list
        }
    
    @staticmethod
    def find_evaluation(product_id):
        """
        Searches for an evaluation by id in the data base and returns the information of every ingredient-value.

        Args:
            product_id (int)

        Returns:
            dict[int, dict[str, float]]: A dictionary with structure:
                {
                    ingredient_id: {
                        'mean': float,
                        'variation': float
                    },
                    ...
                }
        """
        response = httpx.get(f"http://localhost:8087/user-management/evaluation/detail?id={product_id}")

        return response


    @staticmethod
    def evaluation_translation(results_json: dict) -> dict[int, dict[str, float]]:
        """
        Parses a result JSON and returns a dictionary mapping ingredient IDs to their mean and std percentages.

        Args:
            results_json (dict): The JSON object containing resultList.

        Returns:
            dict[int, dict[str, float]]: A dictionary with structure:
                {
                    ingredient_id: {
                        'mean': float,
                        'variation': float
                    },
                    ...
                }
        """
        ingredient_dict = {}

        for result in results_json.get("resultList", []):
            ingredient_id = result.get("ingredientId")
            mean = result.get("ingredientMeanPercentage")
            std = result.get("ingredientStdPercentage")

            if ingredient_id is not None:
                ingredient_dict[ingredient_id] = {
                    "mean": mean,
                    "variation": std,
                }

        return ingredient_dict