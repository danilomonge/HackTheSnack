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
        """
        Handles route changes to update the page views based on the current route.
        """
        # Clear views but ensure we don't process the same route twice
        page.views.clear()
        
        # Add a small delay to ensure proper cleanup
        import time
        time.sleep(0.01)  # 10ms delay
        
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
                        ft.Column([
                            generator_view.build_table_ui(),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        )
                    ],
                )
            )
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
