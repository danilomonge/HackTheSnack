"""Tests of the FastAPI nutrition proxy (USDA / DeepL calls are mocked)."""

import httpx
import pytest
from fastapi.testclient import TestClient

from hts_lib.backend import nutrition_proxy_api as proxy


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(proxy, "USDA_API_KEY", "usda-key")
    monkeypatch.setattr(proxy, "DEEPL_API_KEY", "deepl-key:fx")
    return TestClient(proxy.app)


def test_health(client):
    assert client.get("/health").json() == {"ok": True}


def test_nutrition_returns_data(client, monkeypatch):
    monkeypatch.setattr(proxy, "lookup_usda", lambda name, key: {"name": name.upper(), "kcal": 1.0})
    response = client.get("/api/nutrition", params={"ingredient": "salt"})
    assert response.status_code == 200
    assert response.json() == {"data": {"name": "SALT", "kcal": 1.0}}


def test_nutrition_requires_a_key(client, monkeypatch):
    monkeypatch.setattr(proxy, "USDA_API_KEY", None)
    assert client.get("/api/nutrition", params={"ingredient": "salt"}).status_code == 503


def test_nutrition_reports_upstream_errors_without_leaking_urls(client, monkeypatch):
    def failing(name, key):
        request = httpx.Request("GET", "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=secret")
        raise httpx.HTTPStatusError("boom", request=request, response=httpx.Response(429, request=request))

    monkeypatch.setattr(proxy, "lookup_usda", failing)
    response = client.get("/api/nutrition", params={"ingredient": "salt"})
    assert response.status_code == 502
    assert "secret" not in response.text


def test_translate(client, monkeypatch):
    monkeypatch.setattr(proxy, "translate", lambda text, key, src, dst: "Sugar")
    assert client.post("/api/translate", json={"text": "Zucker"}).json() == {"text": "Sugar"}
