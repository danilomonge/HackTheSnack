import sys
import os

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hts_lib.frontend.src.add_product_table.logic.percentage_adjuster import PercentageAdjuster

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

    # Case 2: valid input, step causes result to exceed 99.99 → stay at 99.99
    field = MockTextField("99.50")
    PercentageAdjuster.increase_or_decrease_percentage(field, 1.0)
    assert field.value == "99.99"
    assert field.data["last_valid"][0] == "99.99"  # type: ignore[arg-type]

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
