import httpx
import json

class RecipeManager:
    """
    Handles API interactions for product-ingredient associations (recipies) actions.

    Attributes:
        page (ft.Page): The Flet page object for UI updates.
        
    """
    @staticmethod
    def associate_product_ingredient(idProduct, idIngredient):
        """
        Sends a POST request to relate an ingrredient to a Porduct in the database.

        Args:
        idProduct (int):     The number of the product beeing associated.
        idIngredient (int):  The number of the ingredient beeing associated.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data
        """
        
        data = {
                "idPorduct": idProduct,
                "idIngredient": idIngredient,    
                "fechaRegistro": "2025-06-05",                 #Needs to be updated to take into account the creation date
            }
        
        response = httpx.post(
                "http://localhost:8087/user-management/recipe",
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )
        
        return response

    @staticmethod
    def delete_product_ingredient(idProduct):
        """
        Deletes the association between a product and their ingredients.

        Args:
        idProduct (int):     The number of the product beeing associated.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data.
        """
        
        response = httpx.get(f"http://localhost:8087/user-management/product/detail?name={idProduct}")
        
        return response
    
    @staticmethod
    def find_product_ingredient_list(idProduct):
        """
        Searches for the ingredients related to a product.

        Args:
        idProduct (int):     The number of the product beeing associated.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data.
        """
        response = httpx.get(f"http://localhost:8087/user-management/recipe/list?page=1&size=10&orderBy&orderType&id={idProduct}")

        return response

