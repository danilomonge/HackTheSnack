
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
    def get_ingredient_id_by_name(response_json: dict):
    
        ingredient_id = response_json.get("data")

        return ingredient_id
