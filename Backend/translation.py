from Backend.data_base_manager.product_manager import ProductManager
from Backend.data_base_manager.ingredient_manager import IngredientManager

class Translation:
    """
    Filters data to be processed in Backend and Frontend
    """ 

    @staticmethod
    def product_table_filter(api_response: dict) -> dict[str, float]:
        """
        Transforms an API-recipe response into a dictionary mapping ingredient names to their IDs.

        Args:
            api_response (dict): Dictionary containing 'data' key with ingredient info.

        Returns:
            dict[str, float]: Dictionary with {ingredient_name: ingredient_id}
        """
        ingredients = {}

        data = api_response.get("data", [])
        for item in data:
            name = item.get("nameIngredient")
            name = name.capitalize()
            id_ = item.get("idIngredient")
            if name is not None and id_ is not None:
                ingredients[name] = id_

        return ingredients
    

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
    def collect_ingredient_list() -> list[str]:
        """
        Sends a Ingredient GET request, parses a result JSON from a find_ingredient_list service 
        and returns a list with all ingredient names.

        Returns:
            ingredient_list: List of all ingredient names in the database
        """
        ingredient_list = []
        response = IngredientManager.find_ingredient_list("")
        ingredient_data = response.json()

        for result in ingredient_data.get("data", []):
            ingredient_name = result.get("name")

            if ingredient_name is not None:
                ingredient_list.append(ingredient_name)

        return ingredient_list