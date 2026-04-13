import os
import sys

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

if sys.platform != "emscripten":
    from Secure_env.env_enc_decipher import SecureEnvLoader

    SecureEnvLoader.load_env()

SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"


def _allowed_origins():
    """
    Builds the CORS allowlist from an environment variable.
    """
    raw_value = os.environ.get("ALLOWED_ORIGINS", "*")
    return [origin.strip() for origin in raw_value.split(",") if origin.strip()]


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
    deepl_key = os.environ.get("DEEPL_API_KEY")
    if not deepl_key:
        return text

    response = httpx.post(
        DEEPL_URL,
        data={
            "auth_key": deepl_key,
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
    usda_key = os.environ.get("USDA_API_KEY")
    if not usda_key:
        raise HTTPException(status_code=503, detail="USDA_API_KEY is not configured on the proxy.")

    searched = ingredient_name.strip().lower()
    if len(searched) < 3:
        return None

    response = httpx.get(
        SEARCH_URL,
        params={
            "query": ingredient_name,
            "api_key": usda_key,
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
