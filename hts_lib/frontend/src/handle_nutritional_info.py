import flet as ft
import requests
from .styles import Styles
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

from Secure_env.env_enc_decipher import SecureEnvLoader

# Load environment variables securely to acces API keys
SecureEnvLoader.load_env()

import os

# Get API keys from environment variables
usda_key = os.environ.get("USDA_API_KEY")
deepl_key = os.environ.get("DEEPL_API_KEY")

# Route URLs for USDA and DeepL APIs
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"


def translate_to_english(text):
    """
    Translates a given text from German to English using the DeepL API.
    Args:
        text (str): The text to translate.
    Returns:
        str: The translated text.
    """
    params = {
        "auth_key": deepl_key,
        "text": text,
        "source_lang": "DE",
        "target_lang": "EN",
    }
    response = requests.post(DEEPL_URL, data=params)
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
    res = requests.get(SEARCH_URL, params=params)
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
                height=430,
                padding=10,
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
                        ft.Divider(height=10, color="transparent"),
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
                        ft.Divider(height=10, color="transparent"),
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
