"""USDA nutrition lookup and translation (server-side logic).

Used by desktop runs (``frontend/src/handle_nutritional_info.py``), which call
USDA directly with the key from the local environment. Translation uses the free
MyMemory API, which needs no key; the web build calls it from the browser too.

The public web build must not contain the USDA key, so it gets nutrition facts
from the HackTheSnackDB API (``/api/nutrition``, plus ``/api/translate`` as a
translation fallback), which implements the same rules server-side (exact branded
matches, median of every nutrient, MyMemory with the German ingredient context).
Keep both in sync.
"""

from __future__ import annotations

import statistics

import httpx

USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
MYMEMORY_URL = "https://api.mymemory.translated.net/get"
#: Prefixed to German input for MyMemory: with this context it answers with machine
#: translation instead of noisy translation-memory matches ("Zucker" -> "Sugars").
GERMAN_CONTEXT = "Zutat: "

#: How many USDA search hits are checked for an exact name match.
USDA_PAGE_SIZE = 25
TIMEOUT = 15.0


def translate(text: str, source_lang: str = "DE", target_lang: str = "EN", email: str | None = None) -> str:
    """
    Translates ``text`` with the free MyMemory API (no key, account or card).
    Returns blank text unchanged. Language codes are case-insensitive.

    ``email`` is an optional contact address for MyMemory (raises its free limit
    from 5,000 to 50,000 characters a day). German input gets ``GERMAN_CONTEXT``,
    which is cut from the answer again.

    Raises:
        httpx.HTTPError: if MyMemory rejects the request or its daily quota is used up.
    """
    if not text.strip():
        return text
    source_lang, target_lang = source_lang.lower(), target_lang.lower()
    text = text.strip()
    with_context = source_lang == "de"
    params = {"q": GERMAN_CONTEXT + text if with_context else text, "langpair": f"{source_lang}|{target_lang}"}
    if email and email.strip():
        params["de"] = email.strip()
    response = httpx.get(MYMEMORY_URL, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    body = response.json()

    # An exhausted daily quota still answers HTTP 200, with a warning as "translation".
    status = str(body.get("responseStatus"))
    if status != "200" or body.get("quotaFinished"):
        request = httpx.Request("GET", MYMEMORY_URL)
        code = int(status) if status.isdigit() and int(status) >= 400 else 503
        raise httpx.HTTPStatusError("MyMemory quota or error", request=request, response=httpx.Response(code, request=request))

    translated = ((body.get("responseData") or {}).get("translatedText") or "").strip()
    if with_context and ":" in translated:
        translated = translated.split(":", 1)[1].strip()
    return translated or text


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
