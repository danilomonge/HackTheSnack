import httpx
import json

class EvaluationManager:
    """
    Handles API interactions for evaluation-related actions.

    Attributes:
        page (ft.Page): The Flet page object for UI updates.
        
    """
    @staticmethod
    def create_evaluation(recipe_ids ,result_dict):
        """
        Sends a POST request to create an evaluation in the database.

        Args:
        recipe_ids (list[int]): List of recipe IDs.
        result_dict (dict[str, dict[str, float]]): Dictionary with ingredient names as keys,
        each containing 'mean' and 'variation'.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data
        """
        
        data = EvaluationManager.build_results_payload(recipe_ids ,result_dict)
        
        response = httpx.post(
                "http://localhost:8087/user-management/evaluation",
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )
        
        return response

    @staticmethod
    def build_results_payload(recipe_ids: list[int], result_dict) -> dict:
        """
        Builds a JSON-compatible payload that matches recipe IDs with ingredient stats.

        Args:
            recipe_ids (list[int]): List of recipe IDs.
            result_dict (dict[str, dict[str, float]]): Dictionary with ingredient names as keys,
            each containing 'mean' and 'variation'.

        Returns:
            dict: A dictionary with a key 'resultsList' containing the structured list of data.
        """
        # Ensure keys and recipe_ids align
        if len(recipe_ids) != len(result_dict):
            raise ValueError("The number of recipe IDs must match the number of ingredients in result_dict.")

        results_list = []
        for recipe_id, (ingredient, stats) in zip(recipe_ids, result_dict.items()):
            result_entry = {
                "idRecipe": recipe_id,
                "ingredientMeanPercentage": stats.get("mean", 0.0),
                "ingredientVarPercentage": stats.get("variation", 0.0),
            }
            results_list.append(result_entry)


        return {"resultsList": results_list}