import sys
import os



from frontend.src.product_submit_handler import ProductSubmitHandler
import frontend.src.product_submit_handler as handler_module

import flet as ft
from frontend.src.styles import Styles


class testField(ft.TextField):
    def __init__(self, value=""):
        super().__init__()
        self.value = value
        self.data = {"last_valid": ["0.00"]}
        self.update_called = False

    def update(self):
        self.update_called = True


class testText(ft.Text):
    def __init__(self):
        super().__init__()
        self.value = ""
        self.color = ""

class FakeRecipeManager:
    @staticmethod
    def submit_recipe(name, ingredients):
        # Simulates saving a recipe to a fake database
        print(f"(Fake DB) Saved: {name} with {ingredients}")


class testPage:
    """
    Simulates a basic Flet page with controls and an update method.
    """

    def __init__(self):
        self.controls = []
        self.updated = False
        self.views = []

    def update(self):
        self.updated = True

def test_handle_submit():
    """
    Tests the handle_submit function from ProductSubmitHandler.
    """
    
    handler_module.RecipeManager = FakeRecipeManager
    
    # Fake callback and loading indicator
    def fake_store_values_callback(a, b, c, result_dict=None):
        print(f"(Fake Callback) Result: {result_dict}")

    fake_loading_indicator = object()

    # Case 1: valid input → should print success message
    name_input = testField("Pasta Box")
    row1 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Pasta")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value="60"),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )
    )
    row2 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Tomato Sauce")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value="40"),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )
    )
    msg = testText()
    page = testPage()

    handler_module.ProductSubmitHandler.handle_submit(name_input, [row1, row2], msg, page, fake_store_values_callback, fake_loading_indicator)  # type: ignore[arg-type]
    assert msg.value == "✅ Product is valid. Recipe generated!"
    assert msg.color == Styles.GREEN_COLOR
    assert page.updated  # type: ignore[arg-type]

    # Case 2: empty product name → should print error message
    name_input = testField("   ")
    handler_module.ProductSubmitHandler.handle_submit(name_input, [row1, row2], msg, page, fake_store_values_callback, fake_loading_indicator)  # type: ignore[arg-type]
    assert msg.value == "⚠️ Please enter a product name."
    assert msg.color == Styles.RED_COLOR

    # Case 3: one ingredient missing name → should print error message
    invalid_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="   ")),  # missing name
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value="40"),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )
    )
    name_input = testField("Energy Bar")
    handler_module.ProductSubmitHandler.handle_submit(name_input, [invalid_row, row2], msg, page, fake_store_values_callback, fake_loading_indicator)  # type: ignore[arg-type]
    assert "missing a name" in msg.value

    # Case 4: total percentage > 100 → should print error message
    row1 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Bread")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value="60"),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )
    )
    row2 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Cheese")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value="60"),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )
    )
    name_input = testField("Cheese Sandwich")
    handler_module.ProductSubmitHandler.handle_submit(name_input, [row1, row2], msg, page, fake_store_values_callback, fake_loading_indicator)  # type: ignore[arg-type]
    assert "must not exceed 100%" in msg.value

    # Case 5: first ingredient too small for the number of rows → should show validation error
    row1 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Water")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value="10"),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )
    )
    row2 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Salt")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value=""),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )
    )
    row3 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.TextField(value="Sugar")),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(),
                            ft.TextField(value=""),
                            ft.IconButton(),
                        ]
                    )
                ),
            ]
        )
    )
    name_input = testField("Impossible Recipe")
    handler_module.ProductSubmitHandler.handle_submit(
        name_input,
        [row1, row2, row3],
        msg,
        page,
        fake_store_values_callback,
        fake_loading_indicator,
    )  # type: ignore[arg-type]
    assert "first ingredient is too small" in msg.value
