import flet as ft

class Styles:
    """
    Contains global styles and constants for the Flet application.
    
    - Defines colors, sizes, and padding used throughout the app
    - Provides utility functions for creating styled buttons and inputs
    """


    NAVBAR_COLOR = "#a3b188"
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

    BUTTON_FILL_COLOR = "#2b321f"
    BUTTON_TEXT_COLOR = "#FFFFFF"

    BOX_COLOR = "#F0F4E3" 


    FEEDBACK_FONT_SIZE = 16
    # Red -> error and delete button
    RED_COLOR = "#BB2020"
    # Green -> success and confirm button
    GREEN_COLOR = "#67CD6B"

    TITLE_SIZE = 40
    SUBTITLE_SIZE = 23
    BODY_SIZE = 18
    ICON_SIZE = 20

    BORDER_RADIUS = 10

    @staticmethod
    def primary_button(text, icon=None, on_click=None):
        return ft.ElevatedButton(text, icon=icon, on_click=on_click, color=Styles.BUTTON_TEXT_COLOR,bgcolor=Styles.BUTTON_FILL_COLOR,)

    ICON_BUTTON_SIZE = 20


    @staticmethod
    def icon_button(icon, on_click, color, tooltip=None):
        return ft.IconButton(icon=icon,
                             on_click=on_click,
                             icon_color=color,
                             icon_size=Styles.ICON_BUTTON_SIZE,
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
    def build_title():
            """
            Creates the main title of the page.

            Returns:
                ft.Container: A container with the title text.
            """
            return ft.Container(
                ft.Text(
                    "Analyze a product",
                    size=34,
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