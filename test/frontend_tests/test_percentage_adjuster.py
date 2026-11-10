import sys
import os


from frontend.src.add_product_table.logic.percentage_adjuster import PercentageAdjuster

import flet as ft


class MockTextField(ft.TextField):
    """
    Mock version of Flet's TextField with `data` and `update()` for testing the addition and decrese functionalities.
    """

    def __init__(self, value: str):
        super().__init__(value=value)
        self.data = {"last_valid": [""]}
        self.updated = False

    def update(self):
        self.updated = True


def test_increase_or_decrease_percentage():
    """
    Tests the increase_or_decrease_percentage function from PercentageAdjuster.
    """

    # Case 1: valid input, step +1.0 → result increases by 1
    field = MockTextField("25.00")
    PercentageAdjuster.increase_or_decrease_percentage(field, 1.0)
    assert field.value == "26.00"
    assert field.data["last_valid"][0] == "26.00"  # type: ignore[arg-type]
    assert field.updated

    # Case 2: without row context, the generic cap allows 100.00
    field = MockTextField("99.50")
    PercentageAdjuster.increase_or_decrease_percentage(field, 1.0)
    assert field.value == "100.00"
    assert field.data["last_valid"][0] == "100.00"  # type: ignore[arg-type]

    # Case 3: valid input, step causes result to drop below 0.00 → stay at 0.00
    field = MockTextField("0.50")
    PercentageAdjuster.increase_or_decrease_percentage(field, -1.0)
    assert field.value == "0.00"
    assert field.data["last_valid"][0] == "0.00"  # type: ignore[arg-type]

    # Case 4: input is empty string → set to 0.00
    field = MockTextField("")
    PercentageAdjuster.increase_or_decrease_percentage(field, 1.0)
    assert field.value == "0.00"
    assert field.data["last_valid"][0] == "0.00"  # type: ignore[arg-type]

    # Case 5: input is non-numeric string → set to 0.00
    field = MockTextField("abc")
    PercentageAdjuster.increase_or_decrease_percentage(field, -1.0)
    assert field.value == "0.00"
    assert field.data["last_valid"][0] == "0.00"  # type: ignore[arg-type]

    # Case 6: step = 0.0 → value remains unchanged
    field = MockTextField("40.1")
    PercentageAdjuster.increase_or_decrease_percentage(field, 0.0)
    assert field.value == "40.10"
    assert field.data["last_valid"][0] == "40.10"  # type: ignore[arg-type]

    # Case 7: input is None → set to 0.00
    field = MockTextField(None)  # type: ignore[arg-type]
    PercentageAdjuster.increase_or_decrease_percentage(field, 2.0)
    assert field.value == "0.00"
    assert field.data["last_valid"][0] == "0.00"  # type: ignore[arg-type]


def test_increase_or_decrease_percentage_respects_dynamic_limits():
    upper_field = MockTextField("40.00")
    lower_field = MockTextField("39.50")

    upper_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Sugar")),
                ft.Container(content=ft.Row(controls=[ft.IconButton(), upper_field, ft.IconButton()])),
            ]
        )
    )
    lower_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Salt")),
                ft.Container(content=ft.Row(controls=[ft.IconButton(), lower_field, ft.IconButton()])),
            ]
        )
    )

    rows = [upper_row, lower_row]
    upper_field.data = {"last_valid": ["40.00"], "rows": rows, "row": upper_row}
    lower_field.data = {"last_valid": ["39.50"], "rows": rows, "row": lower_row}

    PercentageAdjuster.increase_or_decrease_percentage(lower_field, 1.0)
    assert lower_field.value == "40.00"

    first_dynamic = MockTextField("75.00")
    second_dynamic = MockTextField("10.00")
    third_dynamic = MockTextField("5.00")

    first_dynamic_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Sugar")),
                ft.Container(content=ft.Row(controls=[ft.IconButton(), first_dynamic, ft.IconButton()])),
            ]
        )
    )
    second_dynamic_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Salt")),
                ft.Container(content=ft.Row(controls=[ft.IconButton(), second_dynamic, ft.IconButton()])),
            ]
        )
    )
    third_dynamic_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Pepper")),
                ft.Container(content=ft.Row(controls=[ft.IconButton(), third_dynamic, ft.IconButton()])),
            ]
        )
    )

    dynamic_rows = [first_dynamic_row, second_dynamic_row, third_dynamic_row]
    second_dynamic.data = {"last_valid": ["10.00"], "rows": dynamic_rows, "row": second_dynamic_row}

    PercentageAdjuster.increase_or_decrease_percentage(second_dynamic, 20.0)
    assert second_dynamic.value == "20.00"

    only_field = MockTextField("99.50")
    only_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Only")),
                ft.Container(content=ft.Row(controls=[ft.IconButton(), only_field, ft.IconButton()])),
            ]
        )
    )
    only_rows = [only_row]
    only_field.data = {"last_valid": ["99.50"], "rows": only_rows, "row": only_row}

    PercentageAdjuster.increase_or_decrease_percentage(only_field, 1.0)
    assert only_field.value == "100.00"
