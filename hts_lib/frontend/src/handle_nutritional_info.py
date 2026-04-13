import os
import sys
from functools import lru_cache

import flet as ft
import httpx

from .styles import Styles

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

IS_WEB = sys.platform == "emscripten"

if not IS_WEB:
    from Secure_env.env_enc_decipher import SecureEnvLoader

    # Load environment variables securely to access API keys in native runs.
    SecureEnvLoader.load_env()

# Get API keys from environment variables
usda_key = os.environ.get("USDA_API_KEY")
deepl_key = os.environ.get("DEEPL_API_KEY")

# Route URLs for USDA and DeepL APIs
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"
RUNTIME_CONFIG_URL = "assets/runtime-config.json"


def _normalize_proxy_base_url(url):
    """
    Normalizes a proxy base URL by trimming spaces and trailing slashes.
    """
    if not url:
        return None
    normalized = url.strip().rstrip("/")
    return normalized or None


@lru_cache(maxsize=1)
def get_nutrition_proxy_url():
    """
    Resolves the public proxy URL used by the web build.

    The proxy URL is safe to expose because it is only an endpoint, not a secret.
    Secrets stay on the proxy server.
    """
    direct_env_value = _normalize_proxy_base_url(os.environ.get("NUTRITION_PROXY_URL"))
    if direct_env_value:
        return direct_env_value

    if not IS_WEB:
        return None

    try:
        response = httpx.get(RUNTIME_CONFIG_URL, timeout=5.0)
        response.raise_for_status()
        config = response.json()
    except Exception:
        return None

    return _normalize_proxy_base_url(config.get("nutrition_proxy_url"))


def is_nutrition_lookup_available():
    """
    Returns whether nutrition lookups are available in the current runtime.
    """
    if IS_WEB:
        return get_nutrition_proxy_url() is not None
    return bool(usda_key)


def _translate_via_proxy(text):
    """
    Translates text using the external proxy service.
    """
    proxy_url = get_nutrition_proxy_url()
    if not proxy_url:
        return text

    response = httpx.post(
        f"{proxy_url}/api/translate",
        json={"text": text, "source_lang": "DE", "target_lang": "EN"},
        timeout=10.0,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("text", text)


def _get_nutrition_via_proxy(ingredient_name):
    """
    Fetches nutrition data using the external proxy service.
    """
    proxy_url = get_nutrition_proxy_url()
    if not proxy_url:
        return None

    response = httpx.get(
        f"{proxy_url}/api/nutrition",
        params={"ingredient": ingredient_name},
        timeout=10.0,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("data")


def translate_to_english(text):
    """
    Translates a given text from German to English using the DeepL API.
    Args:
        text (str): The text to translate.
    Returns:
        str: The translated text.
    """
    if IS_WEB:
        return _translate_via_proxy(text)

    if not deepl_key:
        return text

    params = {
        "auth_key": deepl_key,
        "text": text,
        "source_lang": "DE",
        "target_lang": "EN",
    }
    response = httpx.post(DEEPL_URL, data=params, timeout=10.0)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]


def get_nutrition_usda(ingredient_name):
    """
    Fetches nutritional information for a given ingredient from the USDA API.
    Args:
        ingredient_name (str): The name of the ingredient to search for.
    Returns:
        dict: A dictionary containing nutritional values or None if not found.
    """
    if IS_WEB:
        return _get_nutrition_via_proxy(ingredient_name)

    if not usda_key:
        return None

    # Use the stripped and lowercased ingredient name for searching
    searched = ingredient_name.strip().lower()
    
    if len(ingredient_name.strip()) < 3:
        # Don't search for very short names that are likely not valid
        return None
    
    params = {
        "query": ingredient_name,
        "api_key": usda_key,
        "pageSize": 5,
        "dataType": ["Branded", "Branded Foods"],
    }
    res = httpx.get(SEARCH_URL, params=params, timeout=10.0)
    res.raise_for_status()
    data = res.json()

    # if the response is empty or no foods are found, return None
    if "foods" not in data or not data["foods"]:
        print(f"⚠️ No reliable data found for: {ingredient_name} (likely processed)")
        return None

    # Check for an exact match in the food descriptions (avoiding similar names with unreliable data)
    for food in data["foods"]:
        # Convert the food description to lowercase and strip whitespace
        name = food["description"].strip().lower()
        # If the name matches the searched ingredient, return its nutritional values
        if name == searched:
            nutrients = {n["nutrientName"]: n["value"] for n in food["foodNutrients"]}
            return {
                "name": food["description"],
                "kcal": nutrients.get("Energy", 0),
                "carbs": nutrients.get("Carbohydrate, by difference", 0),
                "fat": nutrients.get("Total lipid (fat)", 0),
                "protein": nutrients.get("Protein", 0),
                "sodium": nutrients.get("Sodium, Na", 0),
                "per": "100g",
            }

    # If no exact match was found
    print(f"❌ No exact match for: '{ingredient_name}'")
    return None



class NutritionalInfoHandler:
    """
    Handles the display of nutritional information for ingredients in a dialog.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the NutritionalInfoHandler with a Flet page instance.
        """
        self.page = page
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nutrition Info", size=16, weight=ft.FontWeight.BOLD),
            actions=[ft.TextButton("OK", 
                                   on_click=self.close_dialog,
                                   style=ft.ButtonStyle(
                                       color=Styles.ICON_COLOR,),)],
        )
        self.page.overlay.append(self.dialog)
        self.page.update()

    def show_nutritional_info(self, ingredient_name: str, amount: float):
        """
        Displays nutritional information for a given ingredient in a dialog.
        """
        self.dialog.title = ft.Text(
            f"{ingredient_name} — Estimated Nutrition Info 🌱 ", size=15, weight=ft.FontWeight.BOLD
        )
        if IS_WEB and not is_nutrition_lookup_available():
            self.dialog.content = ft.Text(
                "Nutrition lookup is not configured for the web build yet. "
                "Add a secure proxy URL in assets/runtime-config.json or via the NUTRITION_PROXY_URL build variable."
            )
            self.dialog.open = True
            self.page.update()
            return

        self.dialog.content = ft.Text("⏳ Fetching data...")
        self.dialog.open = True
        self.page.update()

        # Step 1: Try translating the ingredient name
        try:
            translated = translate_to_english(ingredient_name)
        except Exception:
            translated = ingredient_name  # fallback to original

        # Step 2: Try fetching nutritional data from USDA
        try:
            data = get_nutrition_usda(translated)
        except Exception:
            data = None

        # Step 3: Display result or fallback message if the data is not available
        if not data:
            self.dialog.content = ft.Text(
                f"😕 Sorry, we couldn't find any information for '{ingredient_name}'."
            )

        else:
            self.dialog.content = ft.Container(
                width=360,
                height=420,
                padding=8,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Proportion of {ingredient_name.lower()} in the product: {amount:.2f}%",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=Styles.ICON_COLOR,
                        ),
                        ft.Divider(height=6, color="transparent"),
                        ft.Text(
                            f"In 100g of pure {ingredient_name.lower()}, the estimated nutritional values are:",
                            weight=ft.FontWeight.BOLD,
                            size=14,
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="local_fire_department", color=Styles.ICON_COLOR, size=18),
                                ft.Text(f"Energy: {data['kcal']:.2f} kcal"),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="lunch_dining", color=Styles.ICON_COLOR, size=18),
                                ft.Text(f"Fat: {data['fat']:.2f} g"),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="ramen_dining", color=Styles.ICON_COLOR, size=18),
                                ft.Text(f"Carbohydrates: {data['carbs']:.2f} g"),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="egg", color=Styles.ICON_COLOR, size=18),
                                ft.Text(f"Protein: {data['protein']:.2f} g"),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="science", color=Styles.ICON_COLOR, size=18),
                                ft.Text(f"Sodium: {(data['sodium'] / 1000):.2f} g"),
                            ]
                        ),
                        ft.Divider(height=8, color="transparent"),
                        ft.Text(
                            f"In the given product (per 100g), {ingredient_name.lower()} contributes approximately:",
                            weight=ft.FontWeight.BOLD,
                            size=14,
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="local_fire_department", color=Styles.ICON_COLOR, size=18),
                                ft.Text(
                                    f"Energy: {(data['kcal'] * amount / 100):.2f} kcal"
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="lunch_dining", color=Styles.ICON_COLOR, size=18),
                                ft.Text(f"Fat: {(data['fat'] * amount / 100):.2f} g"),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="ramen_dining", color=Styles.ICON_COLOR, size=18),
                                ft.Text(
                                    f"Carbohydrates: {(data['carbs'] * amount / 100):.2f} g"
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="egg", color=Styles.ICON_COLOR, size=18),
                                ft.Text(
                                    f"Protein: {(data['protein'] * amount / 100):.2f} g",
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(name="science", color=Styles.ICON_COLOR, size=18),
                                ft.Text(f"Sodium: {(data['sodium'] / 1000 * amount / 100):.2f} g"),
                            ]
                        ),
                        ft.Divider(height=8, color="transparent"),
                        ft.Text(
                            f"Warning: We do not guarantee the accuracy of this data.",
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=Styles.ICON_COLOR,
                        ),
                    ],
                    spacing=6,
                ),
            )

        self.page.update()

    def close_dialog(self, e=None):
        self.dialog.open = False
        self.page.update()
