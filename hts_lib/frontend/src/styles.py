import flet as ft

class Styles:
    """
    Contains global styles and constants for the Flet application.
    
    - Defines colors, sizes, and padding used throughout the app
    - Provides utility functions for creating styled buttons and inputs
    """

    LOADINGBAR_COLOR = "#a3b188"
    LOADINGBAR_BACKGROUNDCOLOR = "#f7f9f0" 
    HOVER_COLOR = "#DEE5CA" 


    NAVBAR_COLOR = "#a3b188"
    NAVBAR_ACTIVE_COLOR = "#2b321f"
    NAVBAR_HOVER_COLOR = "#8D9B72"
    NAVBAR_TEXT_COLOR = "#FFFFFF"

    INPUT_FILL_COLOR = "#f7f9f0" 
    INPUT_BORDER_COLOR = "#2b321f"
    INPUT_EXPLANATION_COLOR = "#2b321f"
    INPUT_GREY_COLOR = "#92B795" 

    TABLE_HEADER_COLOR = "#a3b188"
    TABLE_HEADER_FONT_COLOR = "#2b321f"
    TABLE_ROW_COLOR = "#F0F4E3" 
    BACKGROUND_COLOR = "#FFFFFF"
    TEXT_COLOR = "#2b321f"
    EXPLANATION_FONT_COLOR = "#2b321f"
    EXPLANATION_FONT_SIZE = 14

    ICON_COLOR = "#a3b188"
    SEARCH_ICON_COLOR = "#2b321f"
    CHART_TEXT_SIZE = 13

    BUTTON_FILL_COLOR = "#2b321f"
    BUTTON_FILL_DISABLED_COLOR = "#CBD4BB"
    BUTTON_TEXT_COLOR = "#FFFFFF"

    BOX_COLOR = "#F0F4E3" 
    
    CHART_BACKGROUND_COLOR = "#f7f9f0" 
    CHART_TEXT_PERC_AND_TIME_COLOR = "#979D8E"
    CHART_GRID_COORDINATE_LINES_COLOR = "#979D8E"
    

    RECIPE_CONTAINER_COLOR = "#a3b188"


    FEEDBACK_FONT_SIZE = 16
    # Red -> error and delete button
    RED_COLOR = "#BB2020"
    # Green -> success feedback message
    GREEN_COLOR = "#2E7D32"

    TITLE_SIZE = 40
    SUBTITLE_SIZE = 23
    BOX_SIZE = 18
    ICON_SIZE = 20
    CHART_TEXT_SIZE = 16
    NAVBAR_TEXT_SIZE = 18
    BUTTON_TEXT_SIZE = 18

    BORDER_RADIUS = 10

    # ------------------------------------------------------------ responsive
    #: Below this window width (phones) views switch to their compact layout.
    COMPACT_MAX_WIDTH = 640

    @staticmethod
    def _page_width(page) -> float:
        width = getattr(page, "width", None)
        return float(width) if isinstance(width, (int, float)) and width > 0 else 0.0

    @staticmethod
    def is_compact(page) -> bool:
        """True on narrow screens (phones), where views use their compact layout."""
        width = Styles._page_width(page)
        return 0 < width < Styles.COMPACT_MAX_WIDTH

    @staticmethod
    def fit_width(page, desktop_width: float, margin: float = 40) -> float:
        """``desktop_width`` on large screens; on narrow ones the screen width minus ``margin``."""
        width = Styles._page_width(page)
        if not width:
            return desktop_width
        return max(200.0, min(float(desktop_width), width - margin))

    @staticmethod
    def build_button(text, icon=None, on_click=None):
        btn = ft.ElevatedButton(
            text + " ",
            icon=icon,
            on_click=on_click,
            on_hover=lambda e: Styles._handle_button_hover(e, btn),
            color=Styles.BUTTON_TEXT_COLOR,
            bgcolor=Styles.BUTTON_FILL_COLOR,
            style=ft.ButtonStyle(
                color=Styles.BUTTON_TEXT_COLOR,
                text_style=ft.TextStyle(
                    size=Styles.BUTTON_TEXT_SIZE,
                    weight=ft.FontWeight.W_500,
                ),
                padding=ft.padding.symmetric(horizontal=22, vertical=18),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
        )
        return btn

    @staticmethod
    def _handle_button_hover(e: ft.ControlEvent, btn: ft.ElevatedButton):
        hovered = getattr(e, "data", None) == "true"
        btn.bgcolor = "#44512d" if hovered and not btn.disabled else (
            Styles.BUTTON_FILL_DISABLED_COLOR if btn.disabled else Styles.BUTTON_FILL_COLOR
        )
        btn.update()

    ICON_BUTTON_SIZE = 20


    @staticmethod
    def icon_button(icon, on_click, color, tooltip=None):
        return ft.IconButton(icon=icon,
                             on_click=on_click,
                             icon_color=color,
                             icon_size=Styles.ICON_BUTTON_SIZE,
                             hover_color= Styles.HOVER_COLOR,
                             tooltip=tooltip)

    @staticmethod
    def input_style():
        """
        Returns a standard style dictionary for input fields.

        Returns:
            dict: Styling options for Flet TextField inputs.
        """
        return {
            "filled": True,
            "bgcolor": Styles.INPUT_FILL_COLOR,
            "border_color": Styles.INPUT_BORDER_COLOR,
            "color": Styles.TEXT_COLOR,
            "label_style": {
                "color": Styles.TEXT_COLOR,
            },
            "cursor_color": Styles.TEXT_COLOR,
        }


    @staticmethod
    def build_title(text: str):
            """
            Creates the main title of the page.

            Returns:
                ft.Container: A container with the title text.
            """
            return ft.Container(
                ft.Text(
                    text,
                    size=Styles.TITLE_SIZE,
                    weight=ft.FontWeight.BOLD,
                    color=Styles.TEXT_COLOR,
                    text_align=ft.TextAlign.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=10,
            )
    
    @staticmethod
    def build_subtitle(text):
        """
        Creates a smaller title for sections.

        Args:
            text (str): The title text to display.

        Returns:
            ft.Text: A styled text element.
        """
        return ft.Text(
            text,
            size=Styles.SUBTITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=Styles.TEXT_COLOR,
            text_align=ft.TextAlign.CENTER,
        )
    

    @staticmethod
    def build_explanation(text: str):
        """
        Creates an explanatory text with specific styling.

        Args:
            text (str): The explanation text to display.

        Returns:
            ft.Text: A styled text element.
        """
        return ft.Text(
            text,
            size=Styles.EXPLANATION_FONT_SIZE,
            color=Styles.EXPLANATION_FONT_COLOR,
            text_align=ft.TextAlign.LEFT,
        )
        
    @staticmethod
    def build_explanation_subtitle(text: str):
        """
        Creates a bold subtitle text with the same style as explanations.
        
        Args:
            text (str): The subtitle text to display.
            
        Returns:
            ft.Text: A styled text element.
        """
        return ft.Text(
            text,
            size=Styles.EXPLANATION_FONT_SIZE,
            weight=ft.FontWeight.BOLD,
            color=Styles.EXPLANATION_FONT_COLOR,
            text_align=ft.TextAlign.LEFT,
        )
    

    @staticmethod
    def build_description(text: str):
        """
        Creates an description text with specific styling.

        Args:
            text (str): The description text to display.

        Returns:
            ft.Text: A styled text element.
        """
        return ft.Text(
            text,
            size=Styles.EXPLANATION_FONT_SIZE,
            weight=ft.FontWeight.BOLD,
            color=Styles.EXPLANATION_FONT_COLOR,
            text_align=ft.TextAlign.CENTER,
            font_family= "Arial",
        )
