import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

import flet as ft
from frontend.src.navbar import NavigationBar

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
    page.window.icon = "icon/icon.ico"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.expand = True

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
                            ft.Text(title, size=28, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                message,
                                size=16,
                                text_align=ft.TextAlign.CENTER,
                                width=600,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=16,
                    ),
                ),
            ],
        )

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
            try:
                from frontend.src.views.about_view import AboutView

                about_view = AboutView(page)
                page.views.append(
                    ft.View(
                        "/about",
                        [
                            navbar.build(),
                            about_view.build(),
                        ],
                    )
                )
            except Exception as ex:
                page.views.append(
                    build_unavailable_view(
                        "/about",
                        "About us",
                        f"This section is temporarily unavailable in the web build.\n\n{ex}",
                    )
                )
        elif page.route == "/generator":
            try:
                from frontend.src.add_product_table.table_ui.product_table_ui import ProductTableUI

                generator_view = ProductTableUI(page)
                page.views.append(
                    ft.View(
                        "/generator",
                        [
                            navbar.build(),
                            ft.Column(
                                [
                                    generator_view.build_table_ui(),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                                expand=True,
                            ),
                        ],
                    )
                )
                generator_view.ingredient_manager.initialize_with_empty_row()
            except Exception as ex:
                page.views.append(
                    build_unavailable_view(
                        "/generator",
                        "Recipe generator",
                        f"This section is not ready in the web build yet.\n\n{ex}",
                    )
                )
        elif page.route == "/recipes":
            try:
                from frontend.src.views.recipes_view import RecipesView

                recipes_view = RecipesView(page)
                page.views.append(
                    ft.View(
                        "/recipes",
                        [
                            navbar.build(),
                            recipes_view.build(),
                        ],
                    )
                )
            except Exception as ex:
                page.views.append(
                    build_unavailable_view(
                        "/recipes",
                        "My recipes",
                        f"This section is temporarily unavailable in the web build.\n\n{ex}",
                    )
                )
        elif page.route == "/statistics":
            try:
                from frontend.src.views.statistics_view import StatisticsView

                statistics_view = StatisticsView(page)
                page.views.append(
                    ft.View(
                        "/statistics",
                        [
                            navbar.build(),
                            statistics_view.build(),
                        ],
                    )
                )
            except Exception as ex:
                page.views.append(
                    build_unavailable_view(
                        "/statistics",
                        "Statistics",
                        f"This section is temporarily unavailable in the web build.\n\n{ex}",
                    )
                )
        else:
            try:
                from frontend.src.views.home_view import HomeView

                home_view = HomeView(page)
                page.views.append(
                    ft.View(
                        "/home",
                        [
                            navbar.build(),
                            *home_view.build().controls,
                        ],
                    )
                )
            except Exception as ex:
                page.views.append(
                    build_unavailable_view(
                        "/home",
                        "HackTheSnack",
                        f"The home page could not be loaded.\n\n{ex}",
                    )
                )

        page.update()

    page.on_route_change = route_change
    page.go("/")  

ft.app(target=main, assets_dir="assets")
