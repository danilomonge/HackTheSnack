import httpx
import json

class ProductManager:
    """
    Handles API interactions for product-related actions.

    """
    @staticmethod
    def create_product(product_name):
        """
        Sends a POST request to create a product in the database.

        Args:
        product_name (str): The name of the product to create.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data
        """
        
        data = {
                "name": product_name,
                "descripcion": product_name,      # Default description
                "idBrand": 1,                    # Default brand ID
                "idCategory": 1,                 # Default category ID
                "idSubCategory": 1               # Default subcategory ID
            }
        
        response = httpx.post(
                "http://localhost:8087/user-management/product",
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )
        
        return response

    @staticmethod
    def find_product(product_name):
        """
        Searches for a product by name in the data base.

        Args:
        product_name (str): The name of the product to search for.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data.
        """
        response = httpx.get(f"http://localhost:8087/user-management/product/detail?name={product_name}")

        return response
    
    @staticmethod
    def find_product_id(product_name):
        """
        Searches for a product by name in the product data base and returns its id if found.

        Args:
            product_name (str): The name of the product beeing searched.

        Returns:
            id_product (int): id of the product

        """
        response = httpx.get(f"http://localhost:8087/user-management/product/detail?name={product_name}")
        
        if response.status_code == 200: 
            product_data = response.json()
            id_product = product_data['data']
            return id_product
        else:
            raise Exception(f"Failed to find the product: {product_name}")
    
    @staticmethod
    def find_product_list(product_name):
        """
        Searches for multiple products by name in the data base.

        Args:
        product_name (str): The name of the product to search for.

        Returns:
        httpx.Response: The HTTP response object returned by the API request.
                        Use response.status_code to check for success,
                        and response.json() to access the response data.
        """
        response = httpx.get(f"http://localhost:8087/user-management/product/list?page=1&size=10&name={product_name}")

        return response

