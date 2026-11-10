"""Nutrition facts dialog of the recipe result table.

Where the data comes from:

* **Web build** (GitHub Pages / Pyodide): the nutrition proxy configured in
  ``assets/runtime-config.json`` (``nutrition_proxy_url``). The browser never
  sees the USDA / DeepL keys.
* **Desktop run**: USDA and DeepL directly, with ``USDA_API_KEY`` /
  ``DEEPL_API_KEY`` from the environment or from the encrypted
  ``Secure_env/.env.enc`` file.
"""

import os
import sys

import flet as ft
import httpx

from backend import nutrition_service
from backend.data_base_manager.db_config import get_nutrition_proxy_url

from .styles import Styles

IS_WEB = sys.platform == "emscripten"

if not IS_WEB:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from Secure_env.env_enc_decipher import SecureEnvLoader

    # Loads USDA_API_KEY / DEEPL_API_KEY for native runs (no-op if unavailable).
    SecureEnvLoader.load_env()

#: The proxy runs on a free Render instance that may need ~1 minute to wake up.
PROXY_TIMEOUT = 75.0


def _proxy_endpoint(proxy_url: str, route_name: str) -> str:
    proxy_url = (proxy_url or "").strip().rstrip("/")
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
        timeout=PROXY_TIMEOUT,
    )
    response.raise_for_status()
    return response.json().get("text", text)


def _get_nutrition_via_proxy(page: ft.Page | None, ingredient_name: str):
    proxy_url = get_nutrition_proxy_url(page)
    if not proxy_url:
        return None

    response = httpx.get(
        _proxy_endpoint(proxy_url, "nutrition"),
        params={"ingredient": ingredient_name},
        timeout=PROXY_TIMEOUT,
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


def translate_to_english(text: str, page: ft.Page | None = None) -> str:
    """
    Translates an ingredient name from German to English (unchanged if
    translation is unavailable).
    """
    if IS_WEB:
        try:
            return _translate_via_proxy(text, page)
        except Exception:
            return text
    return nutrition_service.translate(text, os.environ.get("DEEPL_API_KEY"))


def get_nutrition_usda(ingredient_name: str, page: ft.Page | None = None):
    """
    Nutrition facts per 100 g for an ingredient, or None if no exact match exists.
    """
    if IS_WEB:
        return _get_nutrition_via_proxy(page, ingredient_name)
    return nutrition_service.lookup_usda(ingredient_name, os.environ.get("USDA_API_KEY"))


class NutritionalInfoHandler:
    """
    Shows the nutrition facts of one ingredient in a dialog.
    One dialog per page is created and reused.
    """

    def __init__(self, page: ft.Page):
        self.page = page
        self.dialog = getattr(page, "_hts_nutrition_dialog", None)
        if self.dialog is None:
            self.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Nutrition Info", size=16, weight=ft.FontWeight.BOLD),
                actions=[
                    ft.TextButton(
                        "OK",
                        on_click=self.close_dialog,
                        style=ft.ButtonStyle(color=Styles.TEXT_COLOR),
                    )
                ],
            )
            page.overlay.append(self.dialog)
            setattr(page, "_hts_nutrition_dialog", self.dialog)
        else:
            self.dialog.actions[0].on_click = self.close_dialog

    def show_nutritional_info(self, ingredient_name: str, amount: float):
        self.dialog.title = ft.Text(
            f"{ingredient_name} — Estimated Nutrition Info 🌱",
            size=15,
            weight=ft.FontWeight.BOLD,
        )
        self.dialog.content = ft.Row(
            [
                ft.ProgressRing(width=16, height=16, stroke_width=2, color=Styles.TEXT_COLOR),
                ft.Text("Fetching nutrition data… The first lookup can take up to a minute."),
            ],
            tight=True,
        )
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

    @staticmethod
    def _row(icon: str, text: str) -> ft.Row:
        return ft.Row([ft.Icon(name=icon, color=Styles.TEXT_COLOR, size=18), ft.Text(text)])

    def _render_nutrition_result(self, ingredient_name: str, amount: float, data: dict):
        share = float(amount) / 100
        sodium_g = data["sodium"] / 1000
        self.dialog.content = ft.Container(
            width=360,
            height=420,
            padding=8,
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"Proportion of {ingredient_name.lower()} in the product: {float(amount):.2f}%",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=Styles.TEXT_COLOR,
                    ),
                    ft.Divider(height=6, color="transparent"),
                    ft.Text(
                        f"In 100g of pure {ingredient_name.lower()}, the estimated nutritional values are:",
                        weight=ft.FontWeight.BOLD,
                        size=14,
                    ),
                    self._row("local_fire_department", f"Energy: {data['kcal']:.2f} kcal"),
                    self._row("lunch_dining", f"Fat: {data['fat']:.2f} g"),
                    self._row("ramen_dining", f"Carbohydrates: {data['carbs']:.2f} g"),
                    self._row("egg", f"Protein: {data['protein']:.2f} g"),
                    self._row("science", f"Sodium: {sodium_g:.2f} g"),
                    ft.Divider(height=8, color="transparent"),
                    ft.Text(
                        f"In the given product (per 100g), {ingredient_name.lower()} contributes approximately:",
                        weight=ft.FontWeight.BOLD,
                        size=14,
                    ),
                    self._row("local_fire_department", f"Energy: {data['kcal'] * share:.2f} kcal"),
                    self._row("lunch_dining", f"Fat: {data['fat'] * share:.2f} g"),
                    self._row("ramen_dining", f"Carbohydrates: {data['carbs'] * share:.2f} g"),
                    self._row("egg", f"Protein: {data['protein'] * share:.2f} g"),
                    self._row("science", f"Sodium: {sodium_g * share:.2f} g"),
                    ft.Divider(height=8, color="transparent"),
                    ft.Text(
                        "Warning: We do not guarantee the accuracy of this data.",
                        size=10,
                        weight=ft.FontWeight.BOLD,
                        color=Styles.TEXT_COLOR,
                    ),
                ],
                spacing=6,
                scroll=ft.ScrollMode.AUTO,
            ),
        )
