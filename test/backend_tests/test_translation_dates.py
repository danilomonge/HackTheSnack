"""Saved versions are labelled in the viewer's local time.

The API returns UTC timestamps. On the desktop the local time zone comes from
the OS; in the browser (Pyodide) ``astimezone()`` uses the browser's zone.
"""

import time

import httpx
import pytest

from backend.translation import Translation


def _listing(*items):
    request = httpx.Request("GET", "http://api.test/evaluation/listResult")
    return httpx.Response(200, json={"success": True, "errors": [], "data": list(items)}, request=request)


def _item(evaluation_id, name, date, mean):
    return {"evaluationId": evaluation_id, "ingredientName": name, "evaluationDate": date,
            "ingredientMeanPercentage": mean, "ingredientStdPercentage": 1.0}


@pytest.fixture
def berlin_time(monkeypatch):
    if not hasattr(time, "tzset"):
        pytest.skip("time.tzset is not available on this platform")
    monkeypatch.setenv("TZ", "Europe/Berlin")
    time.tzset()
    yield
    monkeypatch.undo()
    time.tzset()


def test_versions_are_labelled_in_local_time(monkeypatch, berlin_time):
    monkeypatch.setattr(
        "backend.translation.EvaluationManager.find_evaluation_product_ingredient",
        lambda product_id, ingredient_id: _listing(
            _item(1, "PEANUTS", "2026-07-10T23:25:45.000+00:00", 70.0),   # summer: UTC+2
            _item(1, "SALT", "2026-07-10T23:25:45.000+00:00", 30.0),
            _item(2, "PEANUTS", "2026-11-10T23:25:45.000+00:00", 80.0),   # winter: UTC+1
            _item(2, "SALT", "2026-11-10T23:25:45.000+00:00", 20.0),
        ),
    )

    versions = Translation.get_all_evaluations(1)

    assert list(versions) == ["2026-07-11 01:25:45", "2026-11-11 00:25:45"]
    assert versions["2026-11-11 00:25:45"]["PEANUTS"]["mean"] == 80.0
