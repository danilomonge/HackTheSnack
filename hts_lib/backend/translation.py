from backend.data_base_manager.product_manager import ProductManager
from backend.data_base_manager.ingredient_manager import IngredientManager
from backend.data_base_manager.evaluation_manager import EvaluationManager
from datetime import datetime

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
            product_dict: Dict of all product names matched to their ids in the database
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
    def get_last_evaluation(product_id) -> dict[str, dict[str, float]]:
        """
        Parses an Evaluation API response and returns a dictionary
        with the latest evaluation percentage per ingredient.

        Args:
            evaluation_data (dict): JSON response from Evaluation API.

        Returns:
            dict[str, dict[str, float]]: Mapping of ingredient name to
                                     {"mean": ..., "variation": ...}
        """
        evaluation_response = EvaluationManager.find_evaluation_product_ingredient(product_id, 0)
        evaluation_data = evaluation_response.json()
        latest_evaluations = {}

        for entry in evaluation_data.get("data", []):
            name = entry["ingredientName"]
            date_str = entry["evaluationDate"]
            mean = entry["ingredientMeanPercentage"]
            variation = entry["ingredientStdPercentage"]

            if not (name and date_str and mean is not None and variation is not None):
                continue

            try:
                date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            except ValueError:
                continue

            if name not in latest_evaluations or date > latest_evaluations[name]["date"]:
                latest_evaluations[name] = {
                    "date": date,
                    "mean": round(mean, 2),
                    "variation": round(variation, 2)
                }

        # Strip out the date field from final output
        return {
            name: {
                "mean": data["mean"],
                "variation": data["variation"]
            }
            for name, data in latest_evaluations.items()
        }
    
    @staticmethod
    def get_all_evaluations(product_id) -> dict[str, dict[str, dict[str, float]]]:
        """
        Retrieves all evaluations for a given product ID, grouped by date.

        Args:
            product_id (int): The ID of the product to retrieve evaluations for.

        Returns:
            dict[str, dict[str, dict[str, float]]]: A dict where:
                - key is the evaluation date (str)
                - value is a dict of ingredient names to their statistics:
                    {
                        "2025-01-15": {
                            "Tomato": {"mean": 12.5, "variation": 1.2},
                            "Cheese": {"mean": 5.0, "variation": 0.8},
                            ...
                        },
                        "2025-01-10": {
                            ...
                        }
                    }
        """
        evaluation_response = EvaluationManager.find_evaluation_product_ingredient(product_id, 0)
        evaluation_data = evaluation_response.json()
        
        evaluations_by_date = {}
        for entry in evaluation_data.get("data", []):
            # Get the date and format it to YYYY-MM-DD
            date_str = entry["evaluationDate"]
            try:
                date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                formatted_date = date.strftime("%Y-%m-%d")
            except ValueError:
                continue

            # Initialize the date dict if it doesn't exist
            if formatted_date not in evaluations_by_date:
                evaluations_by_date[formatted_date] = {}

            # Add the ingredient data to that date
            ingredient_name = entry["ingredientName"]
            evaluations_by_date[formatted_date][ingredient_name] = {
                "mean": round(entry["ingredientMeanPercentage"], 2),
                "variation": round(entry["ingredientStdPercentage"], 2)
            }

        return evaluations_by_date
