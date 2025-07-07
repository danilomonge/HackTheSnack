import flet as ft

from frontend.src.styles import Styles 


class RecipesView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            Styles.build_title("Your Recipes"),
                            ft.Container(
                                content=Styles.build_explanation(
                                    "Here you can find all your saved recipes. \n"
                                    "Click on a recipe to view its details and ingredients."
                                ),
                                padding=10,
                                bgcolor=Styles.BOX_COLOR,
                                border_radius=Styles.BORDER_RADIUS,
                                alignment=ft.alignment.center,
                                width=650,
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                        expand=True  
                    ),
                    alignment=ft.alignment.center,
                    bgcolor=Styles.BACKGROUND_COLOR,
                    expand=True,
                    padding=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )