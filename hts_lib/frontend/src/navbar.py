import flet as ft
from frontend.src.styles import Styles

class NavigationBar:
    def __init__(self, page: ft.Page):
        self.page = page
        self._compact = False

    def _button_style(self, is_active: bool, hovered: bool = False):
        return ft.ButtonStyle(
            bgcolor=Styles.NAVBAR_HOVER_COLOR if hovered else Styles.NAVBAR_COLOR,
            color=Styles.NAVBAR_ACTIVE_COLOR if is_active else Styles.NAVBAR_TEXT_COLOR,
            text_style=ft.TextStyle(
                size=self._text_size(),
                weight=ft.FontWeight.BOLD,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=10, vertical=6) if self._compact
            else ft.padding.symmetric(horizontal=18, vertical=12),
            shape=ft.RoundedRectangleBorder(radius=8),
        )

    def _text_size(self) -> int:
        return 15 if self._compact else Styles.NAVBAR_TEXT_SIZE

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
            btn.style = self._button_style(is_active, hovered=getattr(e, "data", None) == "true")
            btn.update()

        def on_click(e):
            '''Handles the button click event to navigate to the specified route.
            Args:
                e (ft.ControlEvent): The event triggered by the button click.
            '''
            self.page.route = route 
            self.page.go(route)
            self.page.update()  

        label = ft.Text(
            text,
            size=self._text_size(),
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color=Styles.NAVBAR_ACTIVE_COLOR if is_active else Styles.NAVBAR_TEXT_COLOR,
        )
        btn = ft.TextButton(
            # On phones the label is used directly: an aligned Container would
            # stretch every button to the full width (one button per line).
            content=label if self._compact else ft.Container(content=label, alignment=ft.alignment.center),
            on_click=on_click,
            on_hover=on_hover,
            style=self._button_style(is_active)
        )
        return btn

    def build(self):
        # Phones: smaller buttons that wrap onto a second line instead of
        # running off the screen. Tablets: one line that scrolls if needed.
        self._compact = Styles.is_compact(self.page)
        use_scroll = (not self._compact) and bool(
            Styles._page_width(self.page) and Styles._page_width(self.page) < 900
        )

        return ft.Container(
            content=ft.Container(
                content=ft.Row(
                    [
                        self.navbar_button("Home", "/"),
                        self.navbar_button("Recipe Generator", "/generator"),
                        self.navbar_button("My Recipes", "/recipes"),
                        self.navbar_button("Statistics", "/statistics"),
                        self.navbar_button("About us", "/about"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    wrap=self._compact,
                    spacing=2 if self._compact else 10,
                    run_spacing=2,
                    scroll=ft.ScrollMode.AUTO if use_scroll else None,
                    tight=True,
                ),
                alignment=ft.alignment.center,
                width=float("inf"),
            ),
            bgcolor=Styles.NAVBAR_COLOR,
            padding=ft.padding.symmetric(horizontal=6, vertical=6) if self._compact else 10,
            height=None if self._compact else 70,
            width=float("inf"),
        )
