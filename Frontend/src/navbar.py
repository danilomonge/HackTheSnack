import flet as ft
from styles import Styles

class NavigationBar:
    def __init__(self, page: ft.Page):
        self.page = page

    def navbar_button(self, text, route):
        """
        Creates a navigation button for the navbar.

        Args:
            text (str): The text to display on the button.
            route (str): The route to navigate to when the button is clicked.

        Returns:
            ft.TextButton: Configured text button for navigation.
        """
        return ft.TextButton(
            text,
            on_click=lambda _: self.page.go(route),
            style=ft.ButtonStyle(
                color=Styles.NAVBAR_TEXT_COLOR,
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
            )
        )
        
    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    self.navbar_button("Home", "/"),
                    self.navbar_button("Recipe Generator", "/generator"),
                    self.navbar_button("My Recipes", "/recipes"),		
                    self.navbar_button("About us", "/about"),	
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=Styles.NAVBAR_COLOR,
            padding=10,
        )