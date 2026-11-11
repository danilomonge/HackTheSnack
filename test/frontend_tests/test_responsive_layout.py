"""Phone layout: views fit narrow screens without changing the control structure."""

import flet as ft
import pytest

from frontend.src.add_product_table.logic.data_builder import IngredientDataBuilder
from frontend.src.add_product_table.table_ui.product_table_ui import ProductTableUI
from frontend.src.navbar import NavigationBar
from frontend.src.styles import Styles


class FakePage:
    def __init__(self, width=None, height=844):
        self.width = width
        self.height = height
        self.route = "/generator"
        self.overlay = []
        self.updated = False

    def update(self, *args, **kwargs):
        self.updated = True

    def go(self, route):
        self.route = route


@pytest.mark.parametrize(
    "width, compact",
    [(None, False), (0, False), (390, True), (639, True), (640, False), (1280, False)],
)
def test_is_compact(width, compact):
    assert Styles.is_compact(FakePage(width)) is compact


def test_fit_width():
    assert Styles.fit_width(FakePage(None), 600) == 600
    assert Styles.fit_width(FakePage(1280), 600) == 600
    assert Styles.fit_width(FakePage(390), 600) == 350
    assert Styles.fit_width(FakePage(220), 600) == 200  # never collapses


def _generator(width):
    page = FakePage(width)
    ui = ProductTableUI(page)  # type: ignore[arg-type]
    ui.build_table_ui()
    ui.ingredient_manager.add_ingredient_row(page)  # type: ignore[arg-type]
    return page, ui


def test_phone_ingredient_rows_wrap_and_fit_the_screen():
    page, ui = _generator(390)
    row = ui.ingredient_manager.ingredients[0]

    assert row.width <= 390 - 32
    assert row.content.wrap is True
    name_container, percent_container, delete_container = row.content.controls
    inner_width = row.width - 2 * 10  # row padding
    # line 1: the name alone; line 2: percentage controls + delete button
    assert name_container.width <= inner_width
    assert name_container.width + percent_container.width > inner_width
    assert percent_container.width + delete_container.width + row.content.spacing <= inner_width


def test_phone_rows_keep_the_structure_the_table_logic_reads():
    page, ui = _generator(390)
    row = ui.ingredient_manager.ingredients[0]
    row.content.controls[0].content.value = "Peanuts"
    row.content.controls[1].content.controls[1].value = "12.5"

    assert IngredientDataBuilder.get_values_from_row(row) == ("Peanuts", 0.125)  # shares are fractions


def test_desktop_layout_is_unchanged():
    page, ui = _generator(1280)
    row = ui.ingredient_manager.ingredients[0]
    assert row.width == 600
    assert row.content.wrap is False
    assert [c.width for c in row.content.controls] == [210, 194, 32]


def test_phone_navbar_wraps_instead_of_overflowing():
    compact_bar = NavigationBar(FakePage(390)).build()
    desktop_bar = NavigationBar(FakePage(1280)).build()

    assert compact_bar.content.content.wrap is True
    assert compact_bar.height is None  # grows to two lines
    assert desktop_bar.content.content.wrap is False
    assert desktop_bar.height == 70
