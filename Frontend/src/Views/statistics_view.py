import flet as ft
from Backend.translation import Translation

from styles import Styles  # Assumes Styles has utility methods for title and colors


class StatisticsView:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_products_and_ingredients(self):
        # You would replace this with actual DB logic.
        # Example: Fetching from DB, API, or service layer.
        dropdown_products = Translation.collect_product_list()
        dropdown_ingredients = Translation.collect_ingredient_list()
        return dropdown_products, dropdown_ingredients  
    
    def build_dropdown(self, label: str, items: list[str]):
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(item) for item in items],
            width=200,
        )

    def build(self):
        dropdown_product_data, dropdown_ingredient_data = self.get_products_and_ingredients()

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            Styles.build_title("Make Your Selection"),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        self.build_dropdown("Option 1", dropdown_product_data),
                                        self.build_dropdown("Option 2", dropdown_ingredient_data),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                padding=10,
                                bgcolor=Styles.BOX_COLOR,
                                border_radius=Styles.BORDER_RADIUS,
                                alignment=ft.alignment.center,
                                width=500,
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Confirm",
                                    on_click=lambda e: print("Confirmed!")
                                ),
                                alignment=ft.alignment.center,
                                padding=20,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    ),
                    alignment=ft.alignment.center,
                    bgcolor=Styles.BACKGROUND_COLOR,
                    expand=True,
                    padding=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )