"""USDA nutrition lookup and DeepL translation (server-side logic).

Used by desktop runs (``frontend/src/handle_nutritional_info.py``), which call
USDA and DeepL directly with keys from the local environment.

The public web build must not contain the keys, so it calls the HackTheSnackDB
API instead (``/api/nutrition``, ``/api/translate``), which implements the same
rules server-side (exact branded matches, median of every nutrient, DeepL
Free/Pro host from the key, header authentication). Keep both in sync.
"""

from __future__ import annotations

import statistics

import httpx

USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DEEPL_FREE_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_PRO_URL = "https://api.deepl.com/v2/translate"

#: How many USDA search hits are checked for an exact name match.
USDA_PAGE_SIZE = 25
TIMEOUT = 15.0


def deepl_endpoint(api_key: str) -> str:
    """DeepL Free keys end with ":fx" and use a different host than Pro keys."""
    return DEEPL_FREE_URL if api_key.strip().endswith(":fx") else DEEPL_PRO_URL


def translate(text: str, api_key: str | None, source_lang: str = "DE", target_lang: str = "EN") -> str:
    """
    Translates ``text`` with DeepL. Returns the text unchanged when no key is set.

    Uses header authentication (``Authorization: DeepL-Auth-Key …``); DeepL
    no longer accepts the legacy ``auth_key`` form parameter.

    Raises:
        httpx.HTTPError: if DeepL rejects the request.
    """
    if not api_key or not text.strip():
        return text

    response = httpx.post(
        deepl_endpoint(api_key),
        headers={"Authorization": f"DeepL-Auth-Key {api_key.strip()}"},
        json={"text": [text], "source_lang": source_lang, "target_lang": target_lang},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    translations = response.json().get("translations") or []
    return translations[0].get("text", text) if translations else text


def lookup_usda(ingredient_name: str, api_key: str | None) -> dict | None:
    """
    Nutrition facts per 100 g for an ingredient from the USDA FoodData Central API.

    Only exact (case-insensitive) name matches among the branded foods are
    accepted, so a vague query never returns data for a different food. Each
    value is the median over all exact matches, so a single unusual product
    (e.g. heavily salted peanuts) does not decide the result.

    Returns:
        ``{"name", "kcal", "carbs", "fat", "protein", "sodium" (mg), "per"}`` or None.

    Raises:
        httpx.HTTPError: if the USDA API request fails.
    """
    searched = (ingredient_name or "").strip().lower()
    if not api_key or len(searched) < 3:
        return None

    response = httpx.get(
        USDA_SEARCH_URL,
        params={
            "query": ingredient_name.strip(),
            "api_key": api_key,
            "pageSize": USDA_PAGE_SIZE,
            "dataType": "Branded",
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()

    matches = [
        food for food in response.json().get("foods") or []
        if str(food.get("description", "")).strip().lower() == searched
    ]
    if not matches:
        return None

    per_food = [
        {n.get("nutrientName"): n.get("value") for n in food.get("foodNutrients") or []}
        for food in matches
    ]

    def median_of(nutrient_name: str) -> float:
        values = [float(n[nutrient_name]) for n in per_food if n.get(nutrient_name) is not None]
        return float(statistics.median(values)) if values else 0.0

    return {
        "name": matches[0]["description"],
        "kcal": median_of("Energy"),
        "carbs": median_of("Carbohydrate, by difference"),
        "fat": median_of("Total lipid (fat)"),
        "protein": median_of("Protein"),
        "sodium": median_of("Sodium, Na"),
        "per": "100g",
    }
