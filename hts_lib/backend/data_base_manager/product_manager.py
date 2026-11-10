import httpx

from backend.data_base_manager import api_client


class ProductManager:
    """
    API calls for products (``/product`` endpoints of HackTheSnackDB).

    Product names are stored upper-case by the API, so lookups upper-case too.
    """

    @staticmethod
    def create_product(product_name: str) -> httpx.Response:
        """
        Creates a product with the default brand, category and subcategory.

        Returns:
            httpx.Response: 201 with ``{"data": product_id}`` on success,
            400 with ``DUPLICATED_ERROR`` if a product with that name exists.
        """
        name = (product_name or "").strip()
        data = {
            "name": name,
            "descripcion": name,
            "idBrand": 1,
            "idCategory": 1,
            "idSubCategory": 1,
        }
        return api_client.post("/product", data)

    @staticmethod
    def find_product(product_name: str) -> httpx.Response:
        """
        Looks a product up by its exact name (case-insensitive).

        Returns:
            httpx.Response: 200 with the product in ``data``, 404 if unknown.
        """
        return api_client.get("/product/detail", params={"name": (product_name or "").upper().strip()})

    @staticmethod
    def find_product_id(product_name: str) -> dict:
        """
        Returns the product record (``{"id": ..., "name": ..., ...}``) for a name.

        Raises:
            Exception: if the product does not exist or the request fails.
        """
        response = ProductManager.find_product(product_name)
        product = api_client.json_data(response) if response.status_code == 200 else None
        if not isinstance(product, dict) or "id" not in product:
            raise Exception(f"Failed to find the product: {product_name}")
        return product

    @staticmethod
    def find_product_list(product_name: str = "") -> httpx.Response:
        """
        Lists products whose name contains ``product_name`` (all if empty).
        """
        return api_client.get(
            "/product/list",
            params={"page": 1, "size": 100, "name": product_name or ""},
        )

    @staticmethod
    def is_backend_available(timeout: float = api_client.PROBE_TIMEOUT) -> bool:
        """
        Returns True when the API answers (waiting for a cold start if needed).
        """
        try:
            response = api_client.get(
                "/product/list",
                params={"page": 1, "size": 1, "name": ""},
                timeout=timeout,
            )
            return response.status_code < 500
        except Exception:
            return False
