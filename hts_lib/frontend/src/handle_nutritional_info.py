import json
import os
import sys
from urllib.parse import urljoin, urlsplit, urlunsplit

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

usda_key = os.environ.get("USDA_API_KEY")
deepl_key = os.environ.get("DEEPL_API_KEY")

SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"
RUNTIME_CONFIG_PATH = os.path.join(BASE_DIR, "assets", "runtime-config.json")


def _normalize_url(value):
    if not value:
        return ""
    return str(value).strip().rstrip("/")


def _build_same_origin_asset_url(page: ft.Page, asset_name: str) -> str | None:
    page_url = getattr(page, "url", None)
    if not page_url:
        return None

    parsed = urlsplit(page_url)
    path = parsed.path or "/"
    if not path.endswith("/"):
        path = path.rsplit("/", 1)[0] + "/"

    base_url = urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))
    return urljoin(base_url, asset_name)


def _load_runtime_config(page: ft.Page | None = None) -> dict:
    env_proxy_url = _normalize_url(os.environ.get("NUTRITION_PROXY_URL"))
    if env_proxy_url:
        return {"nutrition_proxy_url": env_proxy_url}

    if page is not None and IS_WEB:
        config_url = _build_same_origin_asset_url(page, "runtime-config.json")
        if config_url:
            response = httpx.get(config_url, timeout=10.0)
            response.raise_for_status()
            return response.json()

    if os.path.exists(RUNTIME_CONFIG_PATH):
        with open(RUNTIME_CONFIG_PATH, "r", encoding="utf-8") as config_file:
            return json.load(config_file)

    return {}


def get_nutrition_proxy_url(page: ft.Page | None = None) -> str:
    try:
        runtime_config = _load_runtime_config(page)
    except Exception:
        return ""

    return _normalize_url(runtime_config.get("nutrition_proxy_url"))


def _proxy_endpoint(proxy_url: str, route_name: str) -> str:
    proxy_url = _normalize_url(proxy_url)
    if proxy_url.endswith(f"/api/{route_name}"):
        return proxy_url
    return f"{proxy_url}/api/{route_name}"


def _translate_via_proxy(text: str, page: ft.Page | None = None) -> str:
    proxy_url = get_nutrition_proxy_url(page)
    if not proxy_url:
        return text

    response = httpx.post(
        _proxy_endpoint(proxy_url, "translate"),
        json={"text": text, "source_lang": "DE", "target_lang": "EN"},
        timeout=10.0,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("text", text)


def _get_nutrition_via_proxy(page: ft.Page | None, ingredient_name: str):
    proxy_url = get_nutrition_proxy_url(page)
    if not proxy_url:
        return None

    response = httpx.get(
        _proxy_endpoint(proxy_url, "nutrition"),
        params={"ingredient": ingredient_name},
        timeout=15.0,
    )
    response.raise_for_status()

    payload = response.json()
    data = payload.get("data") if isinstance(payload, dict) else None

    if not isinstance(data, dict):
        return None

    return {
        "name": data.get("name", ingredient_name),
        "kcal": float(data.get("kcal", 0) or 0),
        "carbs": float(data.get("carbs", 0) or 0),
        "fat": float(data.get("fat", 0) or 0),
        "protein": float(data.get("protein", 0) or 0),
        "sodium": float(data.get("sodium", 0) or 0),
        "per": data.get("per", "100g"),
    }


def translate_to_english(text: str, page: ft.Page | None = None):
    """
    Translates a given text from German to English.
    """
    if IS_WEB:
        try:
            return _translate_via_proxy(text, page)
        except Exception:
            return text

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


def get_nutrition_usda(ingredient_name: str, page: ft.Page | None = None):
    """
    Fetches nutritional information for a given ingredient.
    """
    if IS_WEB:
        return _get_nutrition_via_proxy(page, ingredient_name)

    if not usda_key:
        return None

    searched = ingredient_name.strip().lower()

    if len(ingredient_name.strip()) < 3:
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

    if "foods" not in data or not data["foods"]:
        print(f"⚠️ No reliable data found for: {ingredient_name} (likely processed)")
        return None

    for food in data["foods"]:
        name = food["description"].strip().lower()
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

    print(f"❌ No exact match for: '{ingredient_name}'")
    return None


class NutritionalInfoHandler:
    """
    Handles the display of nutritional information for ingredients in a dialog.
    """

    def __init__(self, page: ft.Page):
        self.page = page
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nutrition Info", size=16, weight=ft.FontWeight.BOLD),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(color=Styles.ICON_COLOR),
                )
            ],
        )
        self.page.overlay.append(self.dialog)
        self.page.update()

    def show_nutritional_info(self, ingredient_name: str, amount: float):
        self.dialog.title = ft.Text(
            f"{ingredient_name} — Estimated Nutrition Info 🌱 ",
            size=15,
            weight=ft.FontWeight.BOLD,
        )
        self.dialog.content = ft.Text("⏳ Fetching data...")
        self.dialog.open = True
        self.page.update()

        try:
            translated = translate_to_english(ingredient_name, self.page)
        except Exception:
            translated = ingredient_name

        try:
            data = get_nutrition_usda(translated, self.page)
        except Exception:
            data = None

        if not data:
            if IS_WEB and not get_nutrition_proxy_url(self.page):
                self.dialog.content = ft.Text(
                    "Nutrition lookup is not configured for the web build yet. "
                    "Add a secure proxy URL in assets/runtime-config.json "
                    "or via the NUTRITION_PROXY_URL build variable."
                )
            else:
                self.dialog.content = ft.Text(
                    f"😕 Sorry, we couldn't find any information for '{ingredient_name}'."
                )
        else:
            self._render_nutrition_result(ingredient_name, amount, data)

        self.page.update()

    def close_dialog(self, e=None):
        self.dialog.open = False
        self.page.update()

    def _render_nutrition_result(self, ingredient_name: str, amount: float, data: dict):
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
                            ft.Text(f"Energy: {(data['kcal'] * amount / 100):.2f} kcal"),
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
                            ft.Text(f"Carbohydrates: {(data['carbs'] * amount / 100):.2f} g"),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Icon(name="egg", color=Styles.ICON_COLOR, size=18),
                            ft.Text(f"Protein: {(data['protein'] * amount / 100):.2f} g"),
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
                        "Warning: We do not guarantee the accuracy of this data.",
                        size=10,
                        weight=ft.FontWeight.BOLD,
                        color=Styles.ICON_COLOR,
                    ),
                ],
                spacing=6,
            ),
        )
