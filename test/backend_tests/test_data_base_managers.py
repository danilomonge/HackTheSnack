"""Tests of the HackTheSnackDB client code against an in-memory fake API.

The fake implements the endpoints the app uses with the same status codes and
payloads as the real Spring Boot API, so the save / sync / autofill logic is
tested without a network connection.
"""

from urllib.parse import parse_qs, urlsplit

import httpx
import pytest

from backend.data_base_manager import api_client
from backend.data_base_manager.evaluation_manager import EvaluationManager
from backend.data_base_manager.product_manager import ProductManager
from backend.data_base_manager.recipe_manager import RecipeManager
from backend.translation import Translation


class FakeApi:
    """Minimal in-memory version of the HackTheSnackDB REST API."""

    def __init__(self):
        self.products = {}      # id -> name
        self.ingredients = {}   # id -> name
        self.recipes = {}       # id -> {"product", "ingredient", "active"}
        self.evaluations = []
        self.requests = []

    # -- helpers
    @staticmethod
    def _response(status, data=None, success=True):
        request = httpx.Request("GET", "http://api.test")
        return httpx.Response(status, json={"success": success, "errors": [], "data": data}, request=request)

    def _route(self, method, url, params=None, payload=None):
        path = urlsplit(url).path.replace("/user-management", "")
        params = {k: v for k, v in (params or {}).items()}
        self.requests.append((method, path, params, payload))
        return path, params

    # -- HTTP verbs used by api_client
    def get(self, url, params=None, timeout=None):
        path, params = self._route("GET", url, params)
        if path == "/product/detail":
            for pid, name in self.products.items():
                if name == params["name"]:
                    return self._response(200, {"id": pid, "name": name})
            return self._response(404, success=False)
        if path == "/product/list":
            return self._response(200, [{"id": i, "name": n} for i, n in self.products.items()])
        if path == "/ingredient/detail":
            for iid, name in self.ingredients.items():
                if name == params["name"]:
                    return self._response(200, {"id": iid, "name": name})
            return self._response(404, success=False)
        if path == "/ingredient/list":
            return self._response(200, [{"id": i, "name": n} for i, n in self.ingredients.items()])
        if path == "/recipe/list":
            product = int(params["id"])
            items = [
                {"idRecipe": rid, "idProduct": r["product"], "idIngredient": r["ingredient"],
                 "nameIngredient": self.ingredients[r["ingredient"]]}
                for rid, r in self.recipes.items() if r["product"] == product and r["active"]
            ]
            return self._response(200, items)
        if path == "/recipe/detailRecipeByProduct":
            for rid, r in self.recipes.items():
                if r["product"] == int(params["idProduct"]) and r["ingredient"] == int(params["idIngredient"]) and r["active"]:
                    return self._response(200, {"idRecipe": rid})
            return self._response(404, success=False)
        raise AssertionError(f"unexpected GET {path}")

    def post(self, url, json=None, headers=None, timeout=None):
        path, _ = self._route("POST", url, payload=json)
        if path == "/product":
            name = json["name"].upper()
            if name in self.products.values():
                return self._response(400, success=False)
            pid = len(self.products) + 1
            self.products[pid] = name
            return self._response(201, pid)
        if path == "/ingredient":
            name = json["name"].upper()
            if name in self.ingredients.values():
                return self._response(400, success=False)
            iid = len(self.ingredients) + 1
            self.ingredients[iid] = name
            return self._response(201, iid)
        if path == "/recipe":
            for rid, r in self.recipes.items():
                if r["product"] == json["idProduct"] and r["ingredient"] == json["idIngredient"]:
                    if r["active"]:
                        return self._response(400, success=False)
                    r["active"] = True
                    return self._response(201, rid)
            rid = len(self.recipes) + 1
            self.recipes[rid] = {"product": json["idProduct"], "ingredient": json["idIngredient"], "active": True}
            return self._response(201, rid)
        if path == "/evaluation":
            self.evaluations.append(json)
            return self._response(201, len(self.evaluations))
        raise AssertionError(f"unexpected POST {path}")

    def delete(self, url, params=None, timeout=None):
        path, params = self._route("DELETE", url, params)
        if path == "/recipe/deleteByProduct":
            for r in self.recipes.values():
                if r["product"] == int(params["idProduct"]) and r["ingredient"] == int(params["idIngredient"]):
                    r["active"] = False
            return self._response(200, True)
        raise AssertionError(f"unexpected DELETE {path}")


@pytest.fixture
def api(monkeypatch):
    fake = FakeApi()
    monkeypatch.setattr(api_client.httpx, "get", fake.get)
    monkeypatch.setattr(api_client.httpx, "post", fake.post)
    monkeypatch.setattr(api_client.httpx, "delete", fake.delete)
    return fake


def test_names_are_url_encoded():
    request = httpx.Request("GET", api_client.url("/product/detail"), params={"name": "M&M'S CRÈME 50%"})
    query = parse_qs(urlsplit(str(request.url)).query)
    assert query == {"name": ["M&M'S CRÈME 50%"]}


def test_product_lookup_is_case_insensitive(api):
    ProductManager.create_product("Peanut Butter")
    assert ProductManager.find_product("  peanut butter ").status_code == 200
    assert ProductManager.find_product_id("peanut butter")["id"] == 1
    with pytest.raises(Exception):
        ProductManager.find_product_id("unknown")


def test_submit_recipe_creates_everything_once(api):
    result = {"Peanuts": {"mean": 90.0, "variation": 0.0}, "Salt": {"mean": 10.0, "variation": 0.0}}
    product_id, ingredient_ids, recipe_ids = RecipeManager.submit_recipe("Peanut Butter", result)

    assert (product_id, ingredient_ids, recipe_ids) == (1, [1, 2], [1, 2])

    # Saving the same recipe again reuses product, ingredients and associations.
    assert RecipeManager.submit_recipe("peanut butter", result) == (1, [1, 2], [1, 2])
    assert len(api.recipes) == 2


def test_submit_recipe_removes_ingredients_that_were_deleted(api):
    RecipeManager.submit_recipe("Trail Mix", {"Nuts": {}, "Raisins": {}, "Chocolate": {}})
    RecipeManager.submit_recipe("Trail Mix", {"Nuts": {}, "Chocolate": {}})

    listing = RecipeManager.find_product_ingredient_list(1).json()["data"]
    assert [item["nameIngredient"] for item in listing] == ["NUTS", "CHOCOLATE"]

    # Adding it back re-activates the old association.
    _, _, recipe_ids = RecipeManager.submit_recipe("Trail Mix", {"Nuts": {}, "Raisins": {}, "Chocolate": {}})
    assert recipe_ids == [1, 2, 3]


def test_submit_recipe_requires_ingredients(api):
    with pytest.raises(ValueError):
        RecipeManager.submit_recipe("Empty", {})


def test_evaluation_payload_mirrors_first_result_item():
    payload = EvaluationManager.build_results_payload(
        3, [7, 8], [70, 80],
        {"Peanuts": {"mean": 85.71, "variation": 1.5}, "Salt": {"mean": 14.29, "variation": 1.5}},
    )
    assert payload["idProduct"] == 3
    assert payload["idIngredient"] == 7 and payload["idRecipe"] == 70
    assert payload["ingredientMeanPercentage"] == 85.71
    assert payload["resultList"][1] == {
        "recipeId": 80, "ingredientId": 8, "ingredientMeanPercentage": 14.29, "ingredientStdPercentage": 1.5,
    }


def test_evaluation_payload_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        EvaluationManager.build_results_payload(1, [1], [1, 2], {"a": {}})


def test_evaluation_query_leaves_out_unused_filters(api, monkeypatch):
    captured = {}
    monkeypatch.setattr(api_client.httpx, "get", lambda url, params=None, timeout=None: captured.update(params=params))
    EvaluationManager.find_evaluation_product_ingredient(0, 5)
    assert captured["params"] == {"idProduct": "", "idIngredient": 5}


def test_product_table_filter_keeps_label_order():
    response = {"data": [
        {"idIngredient": 4, "nameIngredient": "WHEAT FLOUR"},
        {"idIngredient": 2, "nameIngredient": "SUGAR"},
        {"idIngredient": 9, "nameIngredient": "SALT"},
    ]}
    names, ids = Translation.product_table_filter(response)
    assert list(names) == ["Wheat flour", "Sugar", "Salt"]
    assert ids == [4, 2, 9]


def test_product_table_filter_resolves_missing_names(api):
    api.ingredients = {1: "PEANUTS", 2: "SALT"}
    names, ids = Translation.product_table_filter({"data": [{"idIngredient": 2}, {"idIngredient": 1}]})
    assert names == {"Salt": 2, "Peanuts": 1}
    assert ids == [2, 1]


def test_collect_product_dict_reports_errors_only_when_asked(monkeypatch):
    def offline(*args, **kwargs):
        raise httpx.ConnectError("Connection refused")

    monkeypatch.setattr(api_client.httpx, "get", offline)
    assert Translation.collect_product_dict() == {}
    with pytest.raises(httpx.ConnectError):
        Translation.collect_product_dict(raise_errors=True)


# ------------------------------------------------------------------ warm-up

class _FakeJsFunction:
    """Stands in for the browser's ``Function`` constructor (Pyodide ``js`` module)."""

    created = []

    @classmethod
    def new(cls, *args):
        source = args[-1]
        calls = []

        def function(*call_args):
            calls.append(call_args)
            # Like the real function: returns undefined, so no promise reaches Python.
            return None

        cls.created.append((args[:-1], source, calls))
        return function


def test_web_warm_up_pings_without_cors_and_swallows_errors(monkeypatch):
    import sys
    import types

    fake_js = types.SimpleNamespace(Function=_FakeJsFunction, fetch=lambda *a: pytest.fail("raw fetch used"))
    monkeypatch.setitem(sys.modules, "js", fake_js)
    monkeypatch.setattr(api_client, "IS_WEB", True)
    _FakeJsFunction.created.clear()

    api_client.warm_up("https://api.test/actuator/health", "", "https://proxy.test/health")

    assert len(_FakeJsFunction.created) == 1
    params, source, calls = _FakeJsFunction.created[0]
    assert "no-cors" in source and ".catch(" in source and "return" not in source
    assert calls == [("https://api.test/actuator/health",), ("https://proxy.test/health",)]


def test_desktop_warm_up_uses_a_background_thread(monkeypatch):
    seen = []
    monkeypatch.setattr(api_client, "IS_WEB", False)
    monkeypatch.setattr(api_client.httpx, "get", lambda url, timeout=None: seen.append(url))

    class ImmediateThread:
        def __init__(self, target, daemon):
            self.target = target
            assert daemon

        def start(self):
            self.target()

    monkeypatch.setattr(api_client.threading, "Thread", ImmediateThread)
    api_client.warm_up("https://api.test/actuator/health", "")
    assert seen == ["https://api.test/actuator/health"]


def test_warm_up_targets_ping_each_service_once():
    api = "https://api.test/user-management"
    # Nutrition served by the API itself: one ping is enough.
    assert api_client.warm_up_targets(api, api + "/") == [api + "/actuator/health"]
    # A separate nutrition proxy is woken too.
    assert api_client.warm_up_targets(api, "https://proxy.test") == [
        api + "/actuator/health",
        "https://proxy.test/health",
    ]
    assert api_client.warm_up_targets(api, "") == [api + "/actuator/health"]
