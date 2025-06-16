import sys

sys.dont_write_bytecode = True

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

import flet as ft
from add_product_table.table_ui.product_table_ui import ProductTableUI
from navbar import NavigationBar
from Views.about_view import AboutView
from Views.home_view import HomeView
from Views.recipes_view import RecipesView


def main(page: ft.Page):
    """
    Launches the Flet app with the product ingredient table UI.

    - Sets page title and layout
    - Loads the home view by default
    - Initializes navigation bar and views
    - Handles route changes to switch between views
    - Adds one empty ingredient row by default
    """
    page.title = "Hack The Snack"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.expand = True

    navbar = NavigationBar(page)
    generator_view = ProductTableUI(page)
    about_view = AboutView(page)
    home_view = HomeView(page)
    recipes_view = RecipesView(page)

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        
        if page.route == "/about":
            page.views.append(
                ft.View(
                    "/about",
                    [
                        navbar.build(),
                        about_view.build(),
                    ],
                )
            )

        elif page.route == "/generator":
            page.views.append(
                ft.View(
                    "/generator",
                    [
                        navbar.build(),
                        generator_view.build_table_ui(),
                    ],
                )
            )
            generator_view.ingredient_manager.add_ingredient_row(page)
            

        
        elif page.route == "/recipes":
            page.views.append(
                ft.View(
                    "/recipes",
                    [
                        navbar.build(),
                        recipes_view.build(),
                    ],
                )
            )

        else:
            page.views.append(
                ft.View(
                    "/home",
                    [
                        navbar.build(),
                        *home_view.build().controls
                    ],
                )
            )
        
        page.update()
    
    page.on_route_change = route_change
    page.go("/")  

ft.app(target=main, assets_dir="assets")
