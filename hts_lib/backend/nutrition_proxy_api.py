"""Nutrition / translation proxy for the public web build.

The web app runs entirely in the visitor's browser, so it must not contain the
USDA and DeepL API keys. This tiny FastAPI service holds the keys and exposes:

* ``GET  /health``                         → ``{"ok": true}``
* ``GET  /api/nutrition?ingredient=sugar`` → ``{"data": {...} | null}``
* ``POST /api/translate``                  → ``{"text": "..."}``

Run locally:  ``uvicorn hts_lib.backend.nutrition_proxy_api:app --reload``
Environment:  ``USDA_API_KEY``, ``DEEPL_API_KEY``, ``ALLOWED_ORIGINS`` (comma-separated).
"""

import os

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from hts_lib.backend.nutrition_service import lookup_usda, translate

USDA_API_KEY = os.getenv("USDA_API_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")


def _allowed_origins() -> list[str]:
    """CORS allowlist from the ALLOWED_ORIGINS environment variable."""
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


@app.get("/health")
def healthcheck():
    """Health check used by Render."""
    return {"ok": True}


@app.post("/api/translate")
def translate_text(request: TranslationRequest):
    """Translates text without exposing the DeepL key to the browser."""
    try:
        translated = translate(request.text, DEEPL_API_KEY, request.source_lang, request.target_lang)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"DeepL request failed with HTTP {exc.response.status_code}") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="DeepL request failed") from exc
    return {"text": translated}


@app.get("/api/nutrition")
def nutrition(ingredient: str = Query(..., min_length=1, max_length=200)):
    """Nutrition facts per 100 g without exposing the USDA key to the browser."""
    if not USDA_API_KEY:
        raise HTTPException(status_code=503, detail="USDA_API_KEY is not configured on the proxy.")
    try:
        data = lookup_usda(ingredient, USDA_API_KEY)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"USDA request failed with HTTP {exc.response.status_code}") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="USDA request failed") from exc
    return {"data": data}
