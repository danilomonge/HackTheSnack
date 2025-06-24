import sys
import os

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from hts_lib.Frontend.src.product_submit_handler import ProductSubmitHandler
import hts_lib.Frontend.src.product_submit_handler as handler_module

import flet as ft


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

    def update(self):
        self.updated = True

def test_handle_submit():
    """
    Tests the handle_submit function from ProductSubmitHandler.
    """
    
    handler_module.RecipeManager = FakeRecipeManager

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

    handler_module.ProductSubmitHandler.handle_submit(name_input, [row1, row2], msg, page)  # type: ignore[arg-type]
    assert msg.value == "✅ Product is valid. Recipe generated!"
    assert msg.color == "#67CD6B"
    assert page.updated  # type: ignore[arg-type]

    # Case 2: empty product name → should print error message
    name_input = testField("   ")
    handler_module.ProductSubmitHandler.handle_submit(name_input, [row1, row2], msg, page)  # type: ignore[arg-type]
    assert msg.value == "⚠️ Please enter a product name."
    assert msg.color == "red"

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
    handler_module.ProductSubmitHandler.handle_submit(name_input, [invalid_row, row2], msg, page)  # type: ignore[arg-type]
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
    handler_module.ProductSubmitHandler.handle_submit(name_input, [row1, row2], msg, page)  # type: ignore[arg-type]
    assert "must not exceed 100%" in msg.value
