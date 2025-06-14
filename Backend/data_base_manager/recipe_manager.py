import httpx
import json
from Backend.data_base_manager.ingredient_manager import IngredientManager
from Backend.data_base_manager.product_manager import ProductManager


class RecipeManager:
    """
    Handles API interactions for product-ingredient associations (recipies) actions.

    Attributes:
        page (ft.Page): The Flet page object for UI updates.
        
    """

    @staticmethod
    def submit_recipe(product_name, ingredient_dict):
        """
        creates and associates a product with a series of ingredients

        Args:
        product_name (str):     The name of the product.
        ingredient_dict (dict):  The ingredient dictionary with percentage values

        """
        #submit ingredient list
        id_ingredients = IngredientManager.create_ingredient_list(ingredient_dict)
        
        #submit product
        product_response = ProductManager.create_product(product_name)

        if product_response.status_code == 201: 
            product_data = product_response.json()
            id_product = product_data['data']
        else:
            id_product = ProductManager.find_product_id(product_name)

        RecipeManager.associate_ingredients_to_product(id_product, id_ingredients)
        

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
                "idProduct": idProduct,
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
    def associate_ingredients_to_product(idProduct: int, ingredient_ids: list[int]) -> None:
        """
        Associates all ingredient IDs to a given product ID via the API.

        Args:
            idProduct (int): The product ID to associate with.
            ingredient_ids (list[int]): List of ingredient IDs to associate.
        """
        for id_ingredient in ingredient_ids:
            response = RecipeManager.associate_product_ingredient(idProduct, id_ingredient)

            if response.status_code == 201:
                    print(f"Associated ingredient {id_ingredient} with product {idProduct}")

            elif response.status_code == 400:
                print(f"Allready associated {id_ingredient} with product {idProduct}")

            else:    
                print(f"Error: {response.status_code} while associating ingredient {id_ingredient}")

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
        idIngredient (int):  The number of the ingredient beeing associated.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data.
        """
        response = httpx.get(f"http://localhost:8087/user-management/recipe/list?page=1&size=10&orderBy&orderType&id={idProduct}")

        return response
