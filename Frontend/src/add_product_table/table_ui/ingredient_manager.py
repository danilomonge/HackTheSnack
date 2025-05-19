import flet as ft
from ..logic.input_validator import InputValidator
from ..logic.percentage_adjuster import PercentageAdjuster


class IngredientManager:
    """
    Manages ingredient rows in a table.

    - Adds rows with name and percentage fields
    - Includes buttons to increase or decrease the percentage
    - Validates and formats the percentage while typing
    - Removes rows from the table when needed
    - Stores all current rows in a list
   """
    
    def __init__(self, quantity_table: ft.Column):
        """
        Creates a manager to control the ingredient rows in the table.

        Args:
            quantity_table (ft.Column): The UI column that holds all ingredient rows.
        """
        self.ingredients = []
        self.quantity_table = quantity_table

    def input_style(self):
        """
        Returns a standard style dictionary for input fields.

        Returns:
            dict: Styling options for Flet TextField inputs.
        """
        return {
            "filled": True,
            "bgcolor": "#E8F5E9",
            "border_color": "#1A3E3E",
            "color": "black",
        }

    def name_input(self, style):
        """
        Creates the ingredient name input field.

        Args:
            style (dict): Visual style to apply to the field.

        Returns:
            ft.TextField: Configured text field for the ingredient name.
        """
        return ft.TextField(label="Ingredient", width=200, **style)

    def percent_input(self, style, last_valid, page):
        """
        Creates the percentage input field with validation logic.

        Args:
            style (dict): Visual style to apply to the field.
            last_valid (list): Shared reference to the last valid value.
            page (ft.Page): Page object used for triggering UI updates.

        Returns:
            ft.TextField: Configured percentage input with on_change validation.
        """
        return ft.TextField(
            label="Percentage",
            hint_text="00.00",
            width=120,
            suffix_text="%",
            suffix_style=ft.TextStyle(color="black"),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=InputValidator.fix_input_while_typing(last_valid, page),
            data={"last_valid": last_valid},
            **style
        )

    def percent_section(self, percent_input):
        """
        Creates the section containing the percentage input with + and - buttons.

        Args:
            percent_input (ft.TextField): The input field to adjust.

        Returns:
            ft.Row: Horizontal layout with controls to modify the percentage.
        """
        return ft.Row(
            controls=[
                ft.IconButton(
                    ft.icons.REMOVE,
                    on_click=lambda e: PercentageAdjuster.increase_or_decrease_percentage(
                        percent_input, -1.0
                    ),
                    icon_size=20,
                ),
                percent_input,
                ft.IconButton(
                    ft.icons.ADD,
                    on_click=lambda e: PercentageAdjuster.increase_or_decrease_percentage(
                        percent_input, 1.0
                    ),
                    icon_size=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )

    def ingredient_row(self, name_input, percent_section, on_delete):
        """
        Assembles the full ingredient row with input fields and delete button.

        Args:
            name_input (ft.TextField): Field for the ingredient name.
            percent_section (ft.Row): Controls for adjusting percentage.
            on_delete (Callable): Function to call when delete button is clicked.

        Returns:
            ft.Container: A styled container with the complete row layout.
        """
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(content=name_input, padding=5),
                    ft.Container(content=percent_section, padding=5),
                    ft.IconButton(
                        ft.icons.DELETE,
                        on_click=lambda e: on_delete(),
                        icon_color="red",
                        icon_size=20,
                        tooltip="Remove ingredient",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            bgcolor="#F5F5F5",
            border_radius=10,
            padding=10,
            margin=5,
        )

    def add_ingredient_row(self, page: ft.Page):
        """
        Adds a new ingredient row to the table with:
        - A name input field
        - A percentage input field with +/- controls
        - A delete button to remove the row

        Args:
            page (ft.Page): The page to trigger UI updates.
        """
        last_valid = ["0.00"]
        style = self.input_style()

        name_input = self.name_input(style)
        percent_input = self.percent_input(style, last_valid, page)
        percent_section = self.percent_section(percent_input)

        row = self.ingredient_row(
            name_input, percent_section, lambda: self.remove_ingredient_row(row)
        )

        self.ingredients.append(row)
        self.quantity_table.controls.append(row)
        self.quantity_table.update()

    def remove_ingredient_row(self, row: ft.Container):
        """
        Removes a row from both the ingredient list and the UI.

        Args:
            row (ft.Container): The ingredient row to remove.
        """
        self.ingredients.remove(row)
        self.quantity_table.controls.remove(row)
        self.quantity_table.update()
