import sys
import os


from frontend.src.add_product_table.logic.data_builder import IngredientDataBuilder

import flet as ft


class testRow(ft.Container):
    """
    Simulates a row in the ingredient table, following the structure expected by IngredientDataBuilder.
    """

    def __init__(self, name_value: str, perc_value: str):
        super().__init__()

        name_field = ft.TextField(value=name_value)
        perc_field = ft.TextField(value=perc_value)

        self.content = ft.Row(
            controls=[
                ft.Container(content=name_field),  # controls[0]: name
                ft.Container(
                    content=ft.Row(  # controls[1]: percentage section
                        controls=[ft.IconButton(), perc_field, ft.IconButton()]
                    )
                ),
            ]
        )


class noNameRow(ft.Container):
    """
    Simulates a row missing the name field (get_name_input will fail).
    """

    def __init__(self):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Container(content=None),  # no valid name TextField
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value="50"),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )


class noPercRow(ft.Container):
    """
    Simulates a row missing the percentage field (get_percent_input will fail).
    """

    def __init__(self):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Salt")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.Text(),
                            ft.IconButton(),  # ft.Text() instead of ft.TextField
                        ]
                    )
                ),
            ]
        )


class brokenRow(ft.Container):
    """
    Simulates an invalid row with missing or broken content.
    """

    def __init__(self):
        super().__init__()
        self.content = None  # No content


class NoPercentContent(ft.Container):
    """
    Simulates a row where the percent container exists but its content is missing.
    """

    def __init__(self):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Name")),
                ft.Container(),  # content is None
            ]
        )


class ShortPercentControls(ft.Container):
    """
    Simulates a row where the percentage container is present but has too few controls.
    """

    def __init__(self):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Name")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton()  # Only one control, should be at least 2
                        ]
                    )
                ),
            ]
        )


class noNameContentRow(ft.Container):
    """
    Simulates a row where the name field container exists but has no 'content',
    causing get_name_input to return None.
    """

    def __init__(self):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Container(),  # No 'content' inside, simulates missing name field
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value="5"),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )


def test_build_data_from_rows():
    """
    Tests the build_data_from_rows function from IngredientDataBuilder.
    """

    # Case 1: valid name and valid float → included with converted value
    row1 = testRow("Sugar", "70")
    row2 = testRow("Salt", "30")
    result = IngredientDataBuilder.build_data_from_rows([row1, row2])
    assert result == {"Sugar": 0.7, "Salt": 0.3}

    # Case 2: valid name, invalid percentage → value becomes None
    row = testRow("Water", "abc")
    result = IngredientDataBuilder.build_data_from_rows([row])
    assert result == {"Water": None}

    # Case 3: empty name → skipped
    row = testRow("   ", "50")
    result = IngredientDataBuilder.build_data_from_rows([row])
    assert result == {}

    # Case 4: empty percentage string → value becomes None
    row = testRow("Lemon", "")
    result = IngredientDataBuilder.build_data_from_rows([row])
    assert result == {"Lemon": None}

    # Case 5: percentage is "NaN" → value becomes None
    row = testRow("Milk", "NaN")
    result = IngredientDataBuilder.build_data_from_rows([row])
    assert result == {"Milk": None}

    # Case 6: duplicate names → last one kept
    row1 = testRow("Oil", "60")
    row2 = testRow("Oil", "20")
    result = IngredientDataBuilder.build_data_from_rows([row1, row2])
    assert result == {"Oil": 0.2}

    # Case 7: empty input list → returns empty dict
    result = IngredientDataBuilder.build_data_from_rows([])
    assert result == {}

    # Case 8: percentage with comma instead of dot → handled correctly
    row = testRow("Love:)", "25,5")
    result = IngredientDataBuilder.build_data_from_rows([row])
    assert result == {"Love:)": 0.255}


def test_get_values_from_row():
    """
    Tests the get_values_from_row function from IngredientDataBuilder.
    """

    # Case 1: valid name and valid float percentage
    row = testRow("Sugar", "70")
    assert IngredientDataBuilder.get_values_from_row(row) == ("Sugar", 0.7)

    # Case 2: valid name, invalid percentage → percentage becomes None
    row = testRow("Salt", "abc")
    assert IngredientDataBuilder.get_values_from_row(row) == ("Salt", None)

    # Case 3: valid name, empty percentage → percentage becomes None
    row = testRow("Pfirschsaft", "")
    assert IngredientDataBuilder.get_values_from_row(row) == ("Pfirschsaft", None)

    # Case 4: name is only whitespace → returns None
    row = testRow("   ", "30")
    assert IngredientDataBuilder.get_values_from_row(row) is None

    # Case 5: both name and percentage are invalid → returns None
    row = testRow(" ", " ")
    assert IngredientDataBuilder.get_values_from_row(row) is None

    # Case 6: percentage has comma → converted to float
    row = testRow("Stevia", "25,5")
    assert IngredientDataBuilder.get_values_from_row(row) == ("Stevia", 0.255)

    # Case 7: name field is missing → returns None
    row = noNameRow()
    assert IngredientDataBuilder.get_values_from_row(row) is None

    # Case 8: percentage field is missing → returns None
    row = noPercRow()
    assert IngredientDataBuilder.get_values_from_row(row) is None

    # Case 9: row content is missing → returns None
    row = brokenRow()
    assert IngredientDataBuilder.get_values_from_row(row) is None

    # Case 10: name container has no content → returns None
    row = noNameContentRow()
    assert IngredientDataBuilder.get_values_from_row(row) is None

    # Case 11: percent container exists but content is missing → returns None
    row = NoPercentContent()
    assert IngredientDataBuilder.get_values_from_row(row) is None

    # Case 12: percent content controls too short → returns None
    row = ShortPercentControls()
    assert IngredientDataBuilder.get_values_from_row(row) is None


def test_get_name_input():
    """
    Tests the get_name_input function from IngredientDataBuilder.
    """

    # Case 1: valid row → should return a TextField
    row = testRow("Sugar", "20")
    name_field = IngredientDataBuilder.get_name_input(row)
    assert isinstance(name_field, ft.TextField)
    assert name_field.value == "Sugar"

    # Case 2: row with no TextField in name field (Text instead) → should return None
    row = noNameRow()
    result = IngredientDataBuilder.get_name_input(row)
    assert result is None

    # Case 3: row.content is None → should return None
    row = brokenRow()
    result = IngredientDataBuilder.get_name_input(row)
    assert result is None

    # Case 4: row.content.controls is not a list or is too short → should return None
    row = ft.Container(content=ft.Row(controls=[]))  # Empty controls list
    result = IngredientDataBuilder.get_name_input(row)
    assert result is None

    # Case 5: controls[0] is missing content → should return None
    row = noNameContentRow()
    result = IngredientDataBuilder.get_name_input(row)
    assert result is None


def test_get_percent_input():
    """
    Tests the get_percent_input function from IngredientDataBuilder.
    """

    # Case 1: fully valid row structure → should return a TextField
    row = testRow("Honey", "15")
    percent_field = IngredientDataBuilder.get_percent_input(row)
    assert isinstance(percent_field, ft.TextField)
    assert percent_field.value == "15"

    # Case 2: row with percentage field as Text (not TextField) → should return None
    row = noPercRow()
    result = IngredientDataBuilder.get_percent_input(row)
    assert result is None

    # Case 3: row with no content (broken row) → should return None
    row = brokenRow()
    result = IngredientDataBuilder.get_percent_input(row)
    assert result is None

    # Case 4: row with percent container content = None → should return None
    row = NoPercentContent()
    result = IngredientDataBuilder.get_percent_input(row)
    assert result is None

    # Case 5: row with too few controls inside percent container → should return None
    row = ShortPercentControls()
    result = IngredientDataBuilder.get_percent_input(row)
    assert result is None


def test_convert_to_float():
    """
    Tests the convert_to_float function from IngredientDataBuilder.
    """

    # Case 1: valid positive integer string → converted to decimal
    assert IngredientDataBuilder.convert_to_float("50") == 0.5

    # Case 2: valid positive decimal string → converted to decimal
    assert IngredientDataBuilder.convert_to_float("25.5") == 0.255

    # Case 3: float value is 0.0 → not > 0 → should return None
    assert IngredientDataBuilder.convert_to_float("0.0") is None

    # Case 4: negative float value → not > 0 → should return None
    assert IngredientDataBuilder.convert_to_float("-10") is None

    # Case 5: empty string → should return None
    assert IngredientDataBuilder.convert_to_float("") is None

    # Case 6: string is "NaN" (any case) → should return None
    assert IngredientDataBuilder.convert_to_float("NaN") is None
    assert IngredientDataBuilder.convert_to_float("nan") is None

    # Case 7: non-numeric string → conversion fails → should return None
    assert IngredientDataBuilder.convert_to_float("abc") is None
    assert IngredientDataBuilder.convert_to_float("25a") is None

    # Case 8: string is "infinite" or "-infinite" → not finite → should return None
    assert IngredientDataBuilder.convert_to_float("inf") is None
    assert IngredientDataBuilder.convert_to_float("-inf") is None

    # Case 9: string is only whitespace → conversion fails → should return None
    assert IngredientDataBuilder.convert_to_float("   ") is None
