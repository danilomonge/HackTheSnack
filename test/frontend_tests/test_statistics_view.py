"""Tests of the Statistics page logic (no backend needed)."""

import flet as ft

from backend.translation import Translation
from frontend.src.views import statistics_view
from frontend.src.views.statistics_view import StatisticsView


class Page:
    def __init__(self):
        self.updated = 0

    def update(self, *args, **kwargs):
        self.updated += 1


RESULTS = {"data": [
    {"ingredientName": "PEANUTS", "productName": "PEANUT BUTTER", "evaluationDate": "2026-04-19T10:38:45.544+00:00", "ingredientMeanPercentage": 85.7},
    {"ingredientName": "SALT", "productName": "PEANUT BUTTER", "evaluationDate": "2026-04-19T10:38:45.544+00:00", "ingredientMeanPercentage": 14.3},
    {"ingredientName": "PEANUTS", "productName": "PEANUT BUTTER", "evaluationDate": "2026-04-20T09:00:00.000+00:00", "ingredientMeanPercentage": 73.0},
]}


def test_only_ingredient_parsing_handles_empty_data():
    view = StatisticsView(Page())  # type: ignore[arg-type]
    assert view._parse_only_ingredient_data({"data": []}) == ({}, set())


def test_chart_is_built_for_product_results():
    view = StatisticsView(Page())  # type: ignore[arg-type]
    chart = view.build_ingredient_line_chart(RESULTS)
    assert isinstance(chart, ft.Column)
    line_chart = chart.controls[1]
    assert isinstance(line_chart, ft.LineChart)
    assert len(line_chart.data_series) == 2  # PEANUTS and SALT


def test_confirm_without_selection_shows_a_hint():
    page = Page()
    view = StatisticsView(page)  # type: ignore[arg-type]
    view.build()
    view.on_confirm(None)
    assert "select a product" in view.status_text.value.lower()


def test_confirm_with_no_saved_results_says_so(monkeypatch):
    page = Page()
    view = StatisticsView(page)  # type: ignore[arg-type]
    view.build()
    view.product_dict = {"PEANUT BUTTER": 1}
    view.product_dropdown.value = "PEANUT BUTTER"

    class Empty:
        status_code = 200

        @staticmethod
        def json():
            return {"data": []}

    monkeypatch.setattr(
        statistics_view.EvaluationManager, "find_evaluation_product_ingredient", staticmethod(lambda p, i: Empty())
    )
    view.on_confirm(None)
    assert "no saved recipes" in view.status_text.value.lower()
    assert view.chart_container.content is None


def test_load_dropdown_data_reports_offline_database(monkeypatch):
    page = Page()
    view = StatisticsView(page)  # type: ignore[arg-type]
    view.build()

    def offline(raise_errors=False):
        raise ConnectionError("Connection refused")

    monkeypatch.setattr(Translation, "collect_product_dict", staticmethod(offline))
    view.load_dropdown_data()
    assert "offline" in view.status_text.value.lower()
