import httpx

from backend.data_base_manager import api_client
from backend.data_base_manager.ingredient_manager import IngredientManager
from backend.data_base_manager.product_manager import ProductManager


class RecipeManager:
    """
    API calls for product ↔ ingredient associations (``/recipe`` endpoints).
    """

    @staticmethod
    def get_or_create_product_id(product_name: str) -> int:
        """
        Returns the id of a product, creating it first if it does not exist.

        Raises:
            Exception: if the product can neither be created nor found.
        """
        response = ProductManager.create_product(product_name)
        if response.status_code == 201:
            product_id = api_client.json_data(response)
            if product_id is not None:
                return product_id
        if response.status_code in (400, 409):  # already exists
            return ProductManager.find_product_id(product_name)["id"]
        raise Exception(f"Failed to create product {product_name!r} (HTTP {response.status_code})")

    @staticmethod
    def submit_recipe(product_name: str, ingredient_dict: dict) -> tuple[int, list[int], list[int]]:
        """
        Stores a product and its ingredient list in the database.

        * Creates the product and any new ingredients.
        * Associates every ingredient of ``ingredient_dict`` with the product.
        * Removes associations of ingredients that are no longer in the list,
          so the stored recipe always matches what the user saved.

        Args:
            product_name: name of the product.
            ingredient_dict: ingredient names as keys (in label order).

        Returns:
            (product_id, ingredient_ids, recipe_ids), the lists in the same order
            as ``ingredient_dict``.

        Raises:
            Exception: if any request fails.
        """
        if not ingredient_dict:
            raise ValueError("A recipe needs at least one ingredient.")

        ingredient_ids = IngredientManager.create_ingredient_list(ingredient_dict)
        product_id = RecipeManager.get_or_create_product_id(product_name)
        recipe_ids = RecipeManager.associate_ingredients_to_product(product_id, ingredient_ids)
        RecipeManager.remove_ingredients_not_in(product_id, ingredient_ids)
        return product_id, ingredient_ids, recipe_ids

    @staticmethod
    def associate_product_ingredient(idProduct: int, idIngredient: int) -> httpx.Response:
        """
        Associates an ingredient with a product.

        Returns:
            httpx.Response: 201 with ``{"data": recipe_id}``; 400 if they are already associated.
        """
        return api_client.post("/recipe", {"idProduct": idProduct, "idIngredient": idIngredient})

    @staticmethod
    def associate_ingredients_to_product(idProduct: int, ingredient_ids: list[int]) -> list[int]:
        """
        Associates all ingredient ids with a product (existing associations are reused).

        Returns:
            list[int]: recipe ids, one per ingredient, in the same order.

        Raises:
            Exception: if an association can neither be created nor found.
        """
        recipe_ids = []
        for id_ingredient in ingredient_ids:
            response = RecipeManager.associate_product_ingredient(idProduct, id_ingredient)
            recipe_id = None
            if response.status_code == 201:
                recipe_id = api_client.json_data(response)
            elif response.status_code == 400:
                detail = RecipeManager.find_detail_product_ingredient(idProduct, id_ingredient)
                if detail.status_code == 200:
                    recipe_id = (api_client.json_data(detail, {}) or {}).get("idRecipe")
            if recipe_id is None:
                raise Exception(
                    f"Failed to associate ingredient {id_ingredient} with product {idProduct} "
                    f"(HTTP {response.status_code})"
                )
            recipe_ids.append(recipe_id)
        return recipe_ids

    @staticmethod
    def remove_ingredients_not_in(idProduct: int, keep_ingredient_ids: list[int]) -> list[int]:
        """
        Removes the product's associations whose ingredient is not in ``keep_ingredient_ids``.

        Returns:
            list[int]: ids of the ingredients that were removed.
        """
        response = RecipeManager.find_product_ingredient_list(idProduct)
        current = api_client.json_data(response, []) if response.status_code == 200 else []
        keep = set(keep_ingredient_ids)
        removed = []
        for item in current:
            ingredient_id = item.get("idIngredient")
            if ingredient_id is not None and ingredient_id not in keep:
                RecipeManager.delete_product_ingredient(idProduct, ingredient_id)
                removed.append(ingredient_id)
        return removed

    @staticmethod
    def delete_product_ingredient(idProduct: int, idIngredient: int) -> httpx.Response:
        """
        Removes the association between a product and an ingredient.
        """
        return api_client.delete(
            "/recipe/deleteByProduct",
            params={"idProduct": idProduct, "idIngredient": idIngredient},
        )

    @staticmethod
    def find_product_ingredient_list(idProduct: int) -> httpx.Response:
        """
        Lists the active ingredients of a product, in label order. Each item has
        ``idRecipe``, ``idProduct``, ``idIngredient`` and ``nameIngredient``.
        """
        return api_client.get("/recipe/list", params={"id": idProduct})

    @staticmethod
    def find_detail_product_ingredient(idProduct: int, idIngredient: int) -> httpx.Response:
        """
        Gets one product-ingredient association (``data.idRecipe``).
        """
        return api_client.get(
            "/recipe/detailRecipeByProduct",
            params={"idProduct": idProduct, "idIngredient": idIngredient},
        )
