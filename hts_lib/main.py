"""HackTheSnack — Flet application entry point.

Run on the desktop:   cd hts_lib && python main.py
Run in the browser:   cd hts_lib && flet run --web main.py
Static web build:     cd hts_lib && flet build web   (see README)
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import flet as ft

from backend.data_base_manager import api_client
from backend.data_base_manager.db_config import (
    get_nutrition_proxy_url,
    get_user_management_url,
    initialize_db_url,
)
from frontend.src.navbar import NavigationBar
from frontend.src.styles import Styles

#: Routes the app knows; anything else shows the home page.
ROUTES = ("/", "/generator", "/recipes", "/statistics", "/about")


def main(page: ft.Page):
    """
    Sets up the page, resolves the backend URLs and renders the view of the
    current route (Home, Recipe Generator, My Recipes, Statistics, About us).
    """
    page.title = "Hack The Snack"
    if not getattr(page, "web", False):
        page.window.icon = "icon/icon.ico"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.bgcolor = Styles.BACKGROUND_COLOR

    # Resolve the API base URL once (env var > runtime-config.json > localhost).
    initialize_db_url(page)

    # Wake the free-tier backend in the background so the first Search,
    # Save or nutrition lookup does not have to wait for a cold start.
    api_client.warm_up(*api_client.warm_up_targets(get_user_management_url(), get_nutrition_proxy_url(page)))

    navbar = NavigationBar(page)

    def build_unavailable_view(route: str, title: str, message: str) -> ft.View:
        return ft.View(
            route,
            [
                navbar.build(),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=40,
                    content=ft.Column(
                        [
                            ft.Text(title, size=28, weight=ft.FontWeight.BOLD, color=Styles.TEXT_COLOR),
                            ft.Text(message, size=16, text_align=ft.TextAlign.CENTER, width=600),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=16,
                    ),
                ),
            ],
            bgcolor=Styles.BACKGROUND_COLOR,
            padding=0,
        )

    def show_view(route: str, title: str, build, load=None):
        """
        Renders a view; ``load`` (optional) fetches its data afterwards.

        The view is drawn first so a loading indicator is visible, then the data
        is loaded with ``page.run_thread`` (a real thread on desktop; runs inline
        in the browser, where Pyodide has no threads).
        """
        try:
            page.views.append(
                ft.View(route, [navbar.build(), build()], bgcolor=Styles.BACKGROUND_COLOR, padding=0)
            )
            page.update()
            if load is not None:
                page.run_thread(load)
        except Exception as ex:
            page.views.clear()
            page.views.append(
                build_unavailable_view(route, title, f"This section could not be loaded.\n\n{ex}")
            )
            page.update()

    def route_change(e: ft.RouteChangeEvent | None = None):
        """
        Replaces the visible view with the one for ``page.route``.
        """
        route = page.route if page.route in ROUTES else "/"
        page.views.clear()

        if route == "/about":
            from frontend.src.views.about_view import AboutView

            show_view("/about", "About us", AboutView(page).build)

        elif route == "/generator":
            from frontend.src.add_product_table.table_ui.product_table_ui import ProductTableUI

            generator_view = ProductTableUI(page)

            def build_generator():
                return ft.Column(
                    [generator_view.build_table_ui()],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                )

            show_view("/generator", "Recipe generator", build_generator,
                      generator_view.ingredient_manager.initialize_with_empty_row)

        elif route == "/recipes":
            from frontend.src.views.recipes_view import RecipesView

            recipes_view = RecipesView(page)
            show_view("/recipes", "My recipes", recipes_view.build, recipes_view.load_recipes)

        elif route == "/statistics":
            from frontend.src.views.statistics_view import StatisticsView

            statistics_view = StatisticsView(page)
            show_view("/statistics", "Statistics", statistics_view.build, statistics_view.load_dropdown_data)

        else:
            from frontend.src.views.home_view import HomeView

            home_view = HomeView(page)

            def build_home():
                return ft.Column(
                    home_view.build().controls,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                )

            show_view("/", "HackTheSnack", build_home)

    page.on_route_change = route_change
    # Open the route from the URL (e.g. a shared link to #/recipes), not always Home.
    page.go(page.route if page.route in ROUTES else "/")


# Started at import time (no __main__ guard) so the same file works for
# `python main.py`, `flet run` and the static `flet build web` bundle.
ft.app(
    target=main,
    assets_dir=os.path.join(BASE_DIR, "assets"),
)
