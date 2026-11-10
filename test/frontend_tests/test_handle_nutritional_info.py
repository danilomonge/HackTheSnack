"""Tests of the nutrition lookup and translation.

The unit tests mock HTTP, so they need no network and no API keys.
The live tests at the bottom run only when USDA_API_KEY / DEEPL_API_KEY are set.
"""

import os

import httpx
import pytest

from backend import nutrition_service
from frontend.src import handle_nutritional_info as nutrition_ui


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            request = httpx.Request("GET", "https://example.test")
            raise httpx.HTTPStatusError("error", request=request, response=httpx.Response(self.status_code, request=request))


USDA_SUGAR = {
    "foods": [
        {"description": "SUGAR SUBSTITUTE", "foodNutrients": [{"nutrientName": "Energy", "value": 10}]},
        {
            "description": "SUGAR",
            "foodNutrients": [
                {"nutrientName": "Energy", "value": 375},
                {"nutrientName": "Carbohydrate, by difference", "value": 100},
                {"nutrientName": "Total lipid (fat)", "value": 0},
                {"nutrientName": "Protein", "value": 0},
                {"nutrientName": "Sodium, Na", "value": 0},
            ],
        },
    ]
}


# --------------------------------------------------------------------- USDA

def test_lookup_usda_returns_exact_match(monkeypatch):
    calls = {}

    def fake_get(url, params=None, timeout=None):
        calls["params"] = params
        return FakeResponse(USDA_SUGAR)

    monkeypatch.setattr(nutrition_service.httpx, "get", fake_get)
    data = nutrition_service.lookup_usda("Sugar", "key")

    assert data == {"name": "SUGAR", "kcal": 375.0, "carbs": 100.0, "fat": 0.0, "protein": 0.0, "sodium": 0.0, "per": "100g"}
    assert calls["params"]["dataType"] == "Branded"
    assert calls["params"]["api_key"] == "key"


def test_lookup_usda_rejects_partial_matches(monkeypatch):
    monkeypatch.setattr(nutrition_service.httpx, "get", lambda *a, **k: FakeResponse(USDA_SUGAR))
    assert nutrition_service.lookup_usda("Sugar cane", "key") is None


@pytest.mark.parametrize("name", ["", "12", "  ab "])
def test_lookup_usda_ignores_too_short_names(monkeypatch, name):
    monkeypatch.setattr(nutrition_service.httpx, "get", lambda *a, **k: pytest.fail("no request expected"))
    assert nutrition_service.lookup_usda(name, "key") is None


def test_lookup_usda_without_key_returns_none(monkeypatch):
    monkeypatch.setattr(nutrition_service.httpx, "get", lambda *a, **k: pytest.fail("no request expected"))
    assert nutrition_service.lookup_usda("sugar", None) is None


# -------------------------------------------------------------------- DeepL

@pytest.mark.parametrize(
    "key, expected_url",
    [
        ("abc:fx", nutrition_service.DEEPL_FREE_URL),
        ("abc", nutrition_service.DEEPL_PRO_URL),
    ],
)
def test_deepl_endpoint_depends_on_key_type(key, expected_url):
    assert nutrition_service.deepl_endpoint(key) == expected_url


def test_translate_uses_header_authentication(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured.update(url=url, headers=headers, json=json)
        return FakeResponse({"translations": [{"text": "Sugar"}]})

    monkeypatch.setattr(nutrition_service.httpx, "post", fake_post)
    assert nutrition_service.translate("Zucker", "secret:fx") == "Sugar"
    assert captured["headers"] == {"Authorization": "DeepL-Auth-Key secret:fx"}
    assert captured["json"] == {"text": ["Zucker"], "source_lang": "DE", "target_lang": "EN"}
    assert captured["url"] == nutrition_service.DEEPL_FREE_URL


def test_translate_without_key_returns_input(monkeypatch):
    monkeypatch.setattr(nutrition_service.httpx, "post", lambda *a, **k: pytest.fail("no request expected"))
    assert nutrition_service.translate("Zucker", None) == "Zucker"


# --------------------------------------------------------- UI module (desktop)

def test_desktop_helpers_use_environment_keys(monkeypatch):
    monkeypatch.setattr(nutrition_ui, "IS_WEB", False)
    monkeypatch.setenv("USDA_API_KEY", "usda-key")
    monkeypatch.setenv("DEEPL_API_KEY", "deepl-key:fx")
    monkeypatch.setattr(nutrition_service.httpx, "get", lambda *a, **k: FakeResponse(USDA_SUGAR))
    monkeypatch.setattr(
        nutrition_service.httpx, "post", lambda *a, **k: FakeResponse({"translations": [{"text": "sugar"}]})
    )

    assert nutrition_ui.translate_to_english("Zucker") == "sugar"
    assert nutrition_ui.get_nutrition_usda("sugar")["kcal"] == 375.0


# ------------------------------------------------------------ UI module (web)

def test_web_build_uses_the_proxy(monkeypatch):
    monkeypatch.setattr(nutrition_ui, "IS_WEB", True)
    monkeypatch.setattr(nutrition_ui, "get_nutrition_proxy_url", lambda page=None: "https://proxy.test/")
    requested = {}

    def fake_get(url, params=None, timeout=None):
        requested["url"] = url
        requested["params"] = params
        return FakeResponse({"data": {"name": "SALT", "kcal": 0, "sodium": 39300}})

    monkeypatch.setattr(nutrition_ui.httpx, "get", fake_get)
    data = nutrition_ui.get_nutrition_usda("salt")

    assert requested == {"url": "https://proxy.test/api/nutrition", "params": {"ingredient": "salt"}}
    assert data["sodium"] == 39300.0 and data["fat"] == 0.0 and data["per"] == "100g"


def test_web_translation_falls_back_to_input_when_proxy_fails(monkeypatch):
    monkeypatch.setattr(nutrition_ui, "IS_WEB", True)
    monkeypatch.setattr(nutrition_ui, "get_nutrition_proxy_url", lambda page=None: "https://proxy.test")
    monkeypatch.setattr(nutrition_ui.httpx, "post", lambda *a, **k: FakeResponse({}, status_code=502))
    assert nutrition_ui.translate_to_english("Zucker") == "Zucker"


def test_web_without_proxy_returns_no_data(monkeypatch):
    monkeypatch.setattr(nutrition_ui, "IS_WEB", True)
    monkeypatch.setattr(nutrition_ui, "get_nutrition_proxy_url", lambda page=None: "")
    assert nutrition_ui.get_nutrition_usda("salt") is None


# ---------------------------------------------------------------- live APIs

live_usda = pytest.mark.skipif(not os.getenv("LIVE_USDA_API_KEY"), reason="set LIVE_USDA_API_KEY to run")
live_deepl = pytest.mark.skipif(not os.getenv("LIVE_DEEPL_API_KEY"), reason="set LIVE_DEEPL_API_KEY to run")


@live_usda
def test_live_usda_salt():
    data = nutrition_service.lookup_usda("salt", os.environ["LIVE_USDA_API_KEY"])
    assert data is not None
    assert abs(data["sodium"] - 39300) < 1000


@live_deepl
def test_live_deepl_translation():
    translated = nutrition_service.translate("Zucker", os.environ["LIVE_DEEPL_API_KEY"])
    assert "sugar" in translated.lower()
