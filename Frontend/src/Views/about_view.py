import flet as ft


class AboutView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        return ft.Column(
            controls=[
                ft.Text("About Hack The Snack", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "This app helps you analyze and generate recipes based on ingredient lists.",
                    size=16,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )