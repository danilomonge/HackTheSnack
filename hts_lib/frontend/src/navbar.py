import flet as ft
from frontend.src.styles import Styles

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
        is_active = route == self.page.route

        def on_hover(e: ft.ControlEvent):
            '''Handles the hover event to change button style based on active state.
            Args:
                e (ft.ControlEvent): The event triggered by the button hover.
            '''
            if getattr(e, "data", None) == "true":
                btn.style = ft.ButtonStyle(
                    bgcolor=Styles.NAVBAR_HOVER_COLOR,
                    color=Styles.NAVBAR_ACTIVE_COLOR if is_active else Styles.NAVBAR_TEXT_COLOR,
                    text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
                )
            else:
                btn.style = ft.ButtonStyle(
                    bgcolor=Styles.NAVBAR_COLOR,
                    color=Styles.NAVBAR_ACTIVE_COLOR if is_active else Styles.NAVBAR_TEXT_COLOR,
                    text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
                )
            btn.update()

        def on_click(e):
            '''Handles the button click event to navigate to the specified route.
            Args:
                e (ft.ControlEvent): The event triggered by the button click.
            '''
            self.page.route = route 
            self.page.go(route)
            self.page.update()  

        btn = ft.TextButton(
            text,
            on_click=on_click,
            on_hover=on_hover,
            style=ft.ButtonStyle(
                bgcolor=Styles.NAVBAR_COLOR,
                color=Styles.NAVBAR_ACTIVE_COLOR if is_active else Styles.NAVBAR_TEXT_COLOR,
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
            )
        )
        return btn

    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    self.navbar_button("Home", "/"),
                    self.navbar_button("Recipe Generator", "/generator"),
                    self.navbar_button("My Recipes", "/recipes"),
                    self.navbar_button("Statistics", "/statistics"),
                    self.navbar_button("About us", "/about"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=False,
            ),
            bgcolor=Styles.NAVBAR_COLOR,
            padding=10,
            height=70,
            width=float("inf"),
        )
