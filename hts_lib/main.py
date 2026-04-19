import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

import flet as ft
from frontend.src.navbar import NavigationBar
from frontend.src.styles import Styles
from backend.data_base_manager.db_config import initialize_db_url


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
    if not getattr(page, "web", False):
        page.window.icon = "icon/icon.ico"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.expand = True
    page.bgcolor = Styles.BACKGROUND_COLOR

    # Resolve the FakeTheSnackDB API base URL once at startup.
    # Reads from: env var USER_MANAGEMENT_BASE_URL > runtime-config.json > localhost fallback
    initialize_db_url(page)

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
            bgcolor=Styles.BACKGROUND_COLOR,
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
                        bgcolor=Styles.BACKGROUND_COLOR,
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
                                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            ),
                        ],
                        bgcolor=Styles.BACKGROUND_COLOR,
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
                loading_content = ft.Container(
                    content=ft.Column(
                        [ft.ProgressRing(color=Styles.BUTTON_FILL_COLOR),
                         ft.Text("Loading recipes...", color=Styles.TEXT_COLOR)],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
                page.views.append(ft.View("/recipes", [navbar.build(), loading_content], bgcolor=Styles.BACKGROUND_COLOR))
                page.update()

                from frontend.src.views.recipes_view import RecipesView
                recipes_view = RecipesView(page)
                page.views[-1] = ft.View(
                    "/recipes",
                    [navbar.build(), recipes_view.build()],
                    bgcolor=Styles.BACKGROUND_COLOR,
                )
            except Exception as ex:
                page.views[-1] = build_unavailable_view(
                    "/recipes",
                    "My recipes",
                    f"This section is temporarily unavailable in the web build.\n\n{ex}",
                )
        elif page.route == "/statistics":
            try:
                loading_content = ft.Container(
                    content=ft.Column(
                        [ft.ProgressRing(color=Styles.BUTTON_FILL_COLOR),
                         ft.Text("Loading statistics...", color=Styles.TEXT_COLOR)],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
                page.views.append(ft.View("/statistics", [navbar.build(), loading_content], bgcolor=Styles.BACKGROUND_COLOR))
                page.update()

                from frontend.src.views.statistics_view import StatisticsView
                statistics_view = StatisticsView(page)
                page.views[-1] = ft.View(
                    "/statistics",
                    [navbar.build(), statistics_view.build()],
                    bgcolor=Styles.BACKGROUND_COLOR,
                )
            except Exception as ex:
                page.views[-1] = build_unavailable_view(
                    "/statistics",
                    "Statistics",
                    f"This section is temporarily unavailable in the web build.\n\n{ex}",
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
                            ft.Column(
                                home_view.build().controls,
                                scroll=ft.ScrollMode.AUTO,
                                expand=True,
                                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            ),
                        ],
                        bgcolor=Styles.BACKGROUND_COLOR,
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

ft.app(
    target=main,
    assets_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets"),
    web_renderer=ft.WebRenderer.HTML,
)
