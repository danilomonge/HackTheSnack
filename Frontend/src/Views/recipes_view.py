import flet as ft


class RecipesView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Your Recipes", size=32, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )