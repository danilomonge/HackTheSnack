from backend.data_base_manager.product_manager import ProductManager
from backend.data_base_manager.ingredient_manager import IngredientManager
from backend.data_base_manager.evaluation_manager import EvaluationManager
from datetime import datetime

class Translation:
    """
    Converts HackTheSnackDB API responses into the dictionaries the UI uses.
    """

    @staticmethod
    def product_table_filter(api_response: dict) -> tuple[dict[str, int], list[int]]:
        """
        Extracts the ingredients of a ``/recipe/list`` response, in label order.

        Args:
            api_response (dict): JSON with a ``data`` list of
                ``{"idIngredient": int, "nameIngredient": str, ...}`` items.

        Returns:
            tuple: ``({display_name: ingredient_id}, [ingredient_id, ...])``.
            Display names are capitalized ("PEANUTS" -> "Peanuts").
        """
        ingredients: dict[str, int] = {}
        ingredient_ids: list[int] = []
        items = (api_response or {}).get("data") or []

        # Older API versions did not send names: resolve them with one list call.
        names_by_id: dict[int, str] = {}
        if any(item.get("nameIngredient") is None for item in items):
            names_by_id = {v: k for k, v in Translation.collect_ingredient_dict().items()}

        for item in items:
            id_ = item.get("idIngredient")
            name = item.get("nameIngredient") or names_by_id.get(id_)
            if id_ is None or not name:
                continue
            display_name = name.capitalize()
            if display_name in ingredients:
                continue
            ingredients[display_name] = id_
            ingredient_ids.append(id_)

        return ingredients, ingredient_ids

    @staticmethod
    def collect_product_dict(raise_errors: bool = False) -> dict[str, int]:
        """
        Fetches all products.

        Args:
            raise_errors: re-raise connection/HTTP errors instead of returning {}.

        Returns:
            dict[str, int]: product name -> product id ({} if none or on error).
        """
        try:
            response = ProductManager.find_product_list("")
            if response.status_code >= 500:
                raise Exception(f"HTTP {response.status_code}")
            product_dict = {}
            for result in response.json().get("data") or []:
                product_name = result.get("name")
                product_id = result.get("id")
                if product_name is not None and product_id is not None:
                    product_dict[product_name] = product_id
            return product_dict
        except Exception:
            if raise_errors:
                raise
            return {}

    @staticmethod
    def get_last_evaluation(product_id) -> dict[str, dict[str, float]]:
        """
        Parses an Evaluation API response and returns a dictionary
        with the latest evaluation percentage per ingredient.

        Returns:
            dict[str, dict[str, float]]: Mapping of ingredient name to
                                     {"mean": ..., "variation": ...}, or {} on error.
        """
        try:
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
        except Exception:
            return {}

    @staticmethod
    def get_all_evaluations(product_id) -> dict[str, dict[str, dict[str, float]]]:
        try:
            evaluation_response = EvaluationManager.find_evaluation_product_ingredient(product_id, 0)
            evaluation_data = evaluation_response.json()

            evaluations_by_date = {}
            for entry in evaluation_data.get("data", []):
                date_str = entry["evaluationDate"]
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                    # The API stores UTC; label versions in the viewer's local time
                    # (the OS zone on the desktop, the browser's zone under Pyodide).
                    # Seconds are kept so versions saved in the same minute stay apart.
                    formatted_date = date.astimezone().strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

                # Initialize the date dict if it doesn't exist
                if formatted_date not in evaluations_by_date:
                    evaluations_by_date[formatted_date] = {}

                ingredient_name = entry["ingredientName"]
                # Wenn bereits eine Evaluation für diesen Ingredient existiert, füge Nummer hinzu
                base_name = ingredient_name
                counter = 1
                while ingredient_name in evaluations_by_date[formatted_date]:
                    ingredient_name = f"{base_name} ({counter})"
                    counter += 1

                evaluations_by_date[formatted_date][ingredient_name] = {
                    "mean": round(entry["ingredientMeanPercentage"], 2),
                    "variation": round(entry["ingredientStdPercentage"], 2)
                }

            return evaluations_by_date
        except Exception:
            return {}


    @staticmethod
    def collect_ingredient_dict(raise_errors: bool = False) -> dict[str, int]:
        """
        Fetches all ingredients.

        Args:
            raise_errors: re-raise connection/HTTP errors instead of returning {}.

        Returns:
            dict[str, int]: ingredient name (upper-case) -> id ({} if none or on error).
        """
        try:
            response = IngredientManager.find_ingredient_list("")
            if response.status_code >= 500:
                raise Exception(f"HTTP {response.status_code}")
            ingredient_dict = {}
            for result in response.json().get("data") or []:
                ingredient_name = result.get("name")
                ingredient_id = result.get("id")
                if ingredient_name is not None and ingredient_id is not None:
                    ingredient_dict[ingredient_name] = ingredient_id
            return ingredient_dict
        except Exception:
            if raise_errors:
                raise
            return {}
