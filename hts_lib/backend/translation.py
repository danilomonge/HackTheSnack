from backend.data_base_manager.product_manager import ProductManager
from backend.data_base_manager.ingredient_manager import IngredientManager

class Translation:
    """
    Filters data to be processed in Backend and Frontend
    """ 

    @staticmethod
    def product_table_filter(api_response: dict) -> tuple[dict[str, float], list[float]]:
        """
        Extracts data from an API-recipe response and puts it into a dictionary mapping ingredient names to their IDs.

        Args:
            api_response (dict): Dictionary containing 'data' key with ingredient info.

        Returns:
            dict[str, float]: Dictionary with {ingredient_name: ingredient_id}
        """
        ingredients = {}
        ingredient_ids = []

        data = api_response.get("data", [])
        for item in data:
            name = item.get("nameIngredient")
            name = name.capitalize()
            id_ = item.get("idIngredient")
            if name is not None and id_ is not None:
                ingredients[name] = id_
                ingredient_ids.append(id_)

        return ingredients, ingredient_ids
    
    @staticmethod
    def evaluation_translation(results_json: dict) -> dict[int, dict[str, float]]:
        """
        Parses a result JSON from a find_evaluation service and returns a dictionary mapping ingredient IDs to their mean and std percentages.
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
    
    @staticmethod
    def collect_product_list() -> list[str]:
        """
        Sends a Product GET request, parses a result JSON from a find_product_list service 
        and returns a list with all product names.
        Returns:
            product_list: List of all product names in the database
        """
        product_list = []
        response = ProductManager.find_product_list("")
        product_data = response.json()

        for result in product_data.get("data", []):
            product_name = result.get("name")

            if product_name is not None:
                product_list.append(product_name)

        return product_list
    
    @staticmethod
    def collect_product_dict() -> dict[str, int]:
        """
        Sends a Product GET request, parses a result JSON from a find_product_list service 
        and returns a list with all product names.
        Returns:
            product_dictt: Dictt of all product names matched to their ids in the database
        """
        product_dict = {}
        response = ProductManager.find_product_list("")
        product_data = response.json()

        for result in product_data.get("data", []):
            product_name = result.get("name")
            product_id = result.get("id")

            if product_name is not None and product_id is not None:
                product_dict[product_name] = product_id

        return product_dict


    @staticmethod
    def collect_ingredient_dict() -> dict[str, int]:
        """
        Sends a Ingredient GET request, parses a result JSON from a find_ingredient_list service 
        and returns a list with all ingredient names.
        Returns:
            ingredient_list: List of all ingredient names in the database
        """
        ingredient_dict = {}
        response = IngredientManager.find_ingredient_list("")
        ingredient_data = response.json()

        for result in ingredient_data.get("data", []):
            ingredient_name = result.get("name")
            ingredient_id = result.get("id")

            if ingredient_name is not None and ingredient_id is not None:
                ingredient_dict[ingredient_name] = ingredient_id

        return ingredient_dict
    
    @staticmethod
    def get_ingredient_id_by_name(response_json: dict):
    
        ingredient_id = response_json['data']['id'] 

        return ingredient_id