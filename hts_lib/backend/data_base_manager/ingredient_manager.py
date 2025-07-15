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
                "description": ingredient_name,      # Default description
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
        response = httpx.get(f"http://localhost:8087/user-management/ingredient/list?page=1&size=500&name={ingredient_name}")

        return response
    
    @staticmethod
    def create_ingredient_list(ingredient_dict: dict) -> list[int]:
        """
        Takes a dictionary of ingredients and searches or creates them in the backend.

        Args:
            ingredient_dict (dict[str, int]): Dictionary mapping ingredient names to their IDs.

        Returns:
            list[int]: List of ingredient IDs.
        """
        ingredient_ids = []

        for name in ingredient_dict.keys():
            # Search for the ingredient
            response = IngredientManager.find_ingredient(name)
            
            #if found, add id to the list
            if response.status_code == 200 and response.json().get("success"):
                data = response.json().get("data")
                if data:
                    ingredient_ids.append(data["id"])
                    continue
            
            # If not found or failed, create the ingredient and add id to the list
            create_response = IngredientManager.create_ingredient(name)
            if create_response.status_code == 201 and create_response.json().get("success"):
                id_ingredient = create_response.json().get("data")
                ingredient_ids.append(id_ingredient)
                continue

            else:
                raise Exception(f"Failed to create ingredient: {name}")

        return ingredient_ids

