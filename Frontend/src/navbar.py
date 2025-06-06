import flet as ft

class NavigationBar:
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.TextButton(
                        "Home",
                        on_click=lambda _: self.page.go("/home"),
                    ),
                    ft.TextButton(
                        "Recipe Generator",
                        on_click=lambda _: self.page.go("/generator"),
                    ),
                    ft.TextButton(
                        "My Recipes",
                        on_click=lambda _: self.page.go("/recipes"),
                    ),
                    ft.TextButton(
                        "About us",
                        on_click=lambda _: self.page.go("/about"),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor="#1A3E3E",
            padding=10,
        )