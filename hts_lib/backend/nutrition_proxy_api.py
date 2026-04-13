import os

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"
USDA_API_KEY = os.getenv("USDA_API_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")


def _allowed_origins():
    """
    Builds the CORS allowlist from an environment variable.
    """
    return [origin.strip() for origin in ALLOWED_ORIGINS.split(",") if origin.strip()]


app = FastAPI(title="HackTheSnack Nutrition Proxy")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "DE"
    target_lang: str = "EN"


def _translate_to_english(text, source_lang="DE", target_lang="EN"):
    """
    Uses the DeepL API with a server-side secret.
    """
    if not DEEPL_API_KEY:
        return text

    response = httpx.post(
        DEEPL_URL,
        data={
            "auth_key": DEEPL_API_KEY,
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
        },
        timeout=10.0,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["translations"][0]["text"]


def _lookup_usda(ingredient_name):
    """
    Uses the USDA API with a server-side secret.
    """
    if not USDA_API_KEY:
        raise HTTPException(status_code=503, detail="USDA_API_KEY is not configured on the proxy.")

    searched = ingredient_name.strip().lower()
    if len(searched) < 3:
        return None

    response = httpx.get(
        SEARCH_URL,
        params={
            "query": ingredient_name,
            "api_key": USDA_API_KEY,
            "pageSize": 5,
            "dataType": ["Branded", "Branded Foods"],
        },
        timeout=10.0,
    )
    response.raise_for_status()
    payload = response.json()

    foods = payload.get("foods", [])
    if not foods:
        return None

    for food in foods:
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

    return None


@app.get("/health")
def healthcheck():
    """
    Simple healthcheck endpoint for deployments.
    """
    return {"ok": True}


@app.post("/api/translate")
def translate(request: TranslationRequest):
    """
    Translates text without exposing the DeepL secret to the browser.
    """
    try:
        translated_text = _translate_to_english(
            request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"DeepL request failed: {exc}") from exc

    return {"text": translated_text}


@app.get("/api/nutrition")
def nutrition(ingredient: str = Query(..., min_length=1)):
    """
    Returns nutrition data for an ingredient without exposing the USDA secret.
    """
    try:
        data = _lookup_usda(ingredient)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"USDA request failed: {exc}") from exc

    return {"data": data}
