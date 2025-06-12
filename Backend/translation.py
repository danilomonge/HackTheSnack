
class Translation:
    """
    Filters data to be procesed in Backend and Frontend
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
            id_ = item.get("idIngredient")
            if name is not None and id_ is not None:
                ingredients[name] = id_

        return ingredients
