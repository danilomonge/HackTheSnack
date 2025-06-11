import httpx
import json


class IngredientManager:
    """
    Handles API interactions for ingredient-related actions.

    Attributes:
        page (ft.Page): The Flet page object for UI updates.
        
    """
    @staticmethod
    def create_ingredient(ingredient_name):
        """
        Sends a POST request to create a ingredient in the database.

        Args:
        ingredient_name (str): The name of the ingredient to search for.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data
        """
        
        data = {
                "name": ingredient_name,
                "descripcion": ingredient_name,      # Default description
            }
        
        response = httpx.post(
                "http://localhost:8087/user-management/ingredient",
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )
        
        return response

    @staticmethod
    def find_ingredient(ingredient_name):
        """
        Searches for a ingredient by name in the data base.

        Args:
        ingredient_name (str): The name of the ingredient to search for.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data.
        """
        response = httpx.get(f"http://localhost:8087/user-management/ingredient/detail?name={ingredient_name}")

        return response
    
    @staticmethod
    def find_ingredient_list(ingredient_name):
        """
        Searches for multiple ingredients by name in the data base.

        Args:
        ingredient_name (str): The name of the ingredient to search for.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data.
        """
        response = httpx.get(f"http://localhost:8087/user-management/ingredient/list?page=1&size=10&name={ingredient_name}")

        return response

