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
        product_id (int): Product ID
        ingredient_ids (list[int]): List of ingredient IDs matching the result_dict order.
        recipe_ids (list[int]): List of recipe IDs, one per ingredient.
        result_dict (dict[str, dict[str, float]]): Dict with ingredient names as keys and their stats.
        
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
        Builds a JSON arrangement for the POST evaluation service.
        Args:
            product_id (int): Product ID
        ingredient_ids (list[int]): List of ingredient IDs matching the result_dict order.
        recipe_ids (list[int]): List of recipe IDs, one per ingredient.
        result_dict (dict[str, dict[str, float]]): Dict with ingredient names as keys and their stats.
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
            "ingredientMeanPercentage": 0.5,
            "ingredientStdPercentage": 0.2,
            "resultList": result_list
        }

    @staticmethod
    def find_evaluation_list(product_id):
        """
        Searches for all evaluations related to one product ID. 
        Args:
            product_id (int)
        """
        response = httpx.get(f"http://localhost:8087/user-management/evaluation/list?page=1&size=10&orderBy&orderType&idProduct={product_id}")

        return response


    @staticmethod
    def find_evaluation_detail(product_id):
        """
        Searches for the details of an evaluation by id and returns the information for every ingredient-value.
        Args:
            product_id (int)
        """
        response = httpx.get(f"http://localhost:8087/user-management/evaluation/detail?id={product_id}")

        return response

    @staticmethod
    def find_evaluation_product_ingredient(product_id, ingredient_id):
        """
        Searches for a product or ingredient by ID and returns all related result-items
        Args:
            product_id (int)
            
        """
        #transformt product_id and ingredient_id if they are not searched
        if product_id == 0:
            product_id = ""

        if ingredient_id == 0:
            ingredient_id = ""

        response = httpx.get(f"http://localhost:8087/user-management/evaluation/listResult?page=1&size=50&orderBy&orderType&idProduct={product_id}&idIngredient={ingredient_id}")

        return response