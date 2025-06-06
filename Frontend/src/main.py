import sys

sys.dont_write_bytecode = True

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

print("BASE_DIR:", BASE_DIR)
print("Inhalt:", os.listdir(BASE_DIR))


import flet as ft
from add_product_table.table_ui.product_table_ui import ProductTableUI


def main(page: ft.Page):
    """
    Launches the Flet app with the product ingredient table UI.

    - Sets page title and layout
    - Loads the product table
    - Adds one empty ingredient row by default
    """
    page.title = "Hack The Snack"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.expand = True

    ui = ProductTableUI(page)
    page.add(ui.build_table_ui())
    ui.ingredient_manager.add_ingredient_row(page)


ft.app(target=main)
