"""USDA nutrition lookup and DeepL translation (server-side logic).

Used in two places, so the behaviour is identical everywhere:

* ``backend/nutrition_proxy_api.py``: the FastAPI proxy that keeps the API keys
  secret for the public web build.
* ``frontend/src/handle_nutritional_info.py``: desktop runs, which call the
  services directly with keys from the local environment.

Only depends on ``httpx`` so the proxy stays lightweight.
"""

from __future__ import annotations

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

    Only an exact (case-insensitive) name match among the branded foods is
    accepted, so a vague query never returns data for a different food.

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

    for food in response.json().get("foods") or []:
        if str(food.get("description", "")).strip().lower() != searched:
            continue
        nutrients = {n.get("nutrientName"): n.get("value", 0) for n in food.get("foodNutrients") or []}
        return {
            "name": food["description"],
            "kcal": float(nutrients.get("Energy", 0) or 0),
            "carbs": float(nutrients.get("Carbohydrate, by difference", 0) or 0),
            "fat": float(nutrients.get("Total lipid (fat)", 0) or 0),
            "protein": float(nutrients.get("Protein", 0) or 0),
            "sodium": float(nutrients.get("Sodium, Na", 0) or 0),
            "per": "100g",
        }
    return None
