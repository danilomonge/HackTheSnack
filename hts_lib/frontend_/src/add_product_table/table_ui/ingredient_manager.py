import flet as ft
from frontend_.src.add_product_table.logic.input_validator import InputValidator
from frontend_.src.add_product_table.logic.percentage_adjuster import PercentageAdjuster
from frontend_.src.styles import Styles

class IngredientManager:
    """
    Manages ingredient rows in a table.

    - Adds rows with name and percentage fields
    - Includes buttons to increase or decrease the percentage
    - Validates and formats the percentage while typing
    - Removes rows from the table when needed
    - Stores all current rows in a list
   """
    
    def __init__(self, quantity_table: ft.Column, product_name: ft.TextField, page: ft.Page):
        """
        Creates a manager to control the ingredient rows in the table.

        Args:
            quantity_table (ft.Column): The UI column that holds all ingredient rows.
            product_name (ft.TextField): The field for the product name.
        """
        self.ingredients = []
        self.quantity_table = quantity_table
        self.product_name = product_name
        self.page = page


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
            suffix_style=ft.TextStyle(color=Styles.TEXT_COLOR),
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
                Styles.icon_button(
                    ft.Icons.REMOVE,
                    lambda e: PercentageAdjuster.increase_or_decrease_percentage(
                        percent_input, -1.0
                    ),
                    Styles.TEXT_COLOR),
                percent_input,
                Styles.icon_button(
                    ft.Icons.ADD,
                    lambda e: PercentageAdjuster.increase_or_decrease_percentage(
                        percent_input, 1.0
                    ),
                    Styles.TEXT_COLOR),
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
                    Styles.icon_button(ft.Icons.DELETE,lambda e: on_delete(), Styles.RED_COLOR, "Remove ingredient"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            bgcolor=Styles.TABLE_ROW_COLOR,
            border_radius=Styles.BORDER_RADIUS,
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
        style = Styles.input_style()

        name_input = self.name_input(style)
        percent_input = self.percent_input(style, last_valid, page)
        percent_section = self.percent_section(percent_input)

        row = self.ingredient_row(
            name_input, percent_section, lambda: self.remove_ingredient_row(row)
        )

        self.ingredients.append(row)
        self.quantity_table.controls.append(row)
        #self.quantity_table.update()
        try:
            self.quantity_table.update()
        except AssertionError:
            pass  # Ignoriere den Fehler vorerst

    def remove_ingredient_row(self, row: ft.Container):
        """
        Removes a row from both the ingredient list and the UI.

        Args:
            row (ft.Container): The ingredient row to remove.
        """
        self.ingredients.remove(row)
        self.quantity_table.controls.remove(row)
        self.quantity_table.update()

    def clear_all(self):
        """
        Clears all ingredient rows and the product name from the table and resets the list.
        """
        self.ingredients.clear()
        self.product_name.value = "" 
        self.quantity_table.controls.clear()

        recipe_to_remove = []

        if hasattr(self.page, 'controls'):
            recipe_to_remove = [
                control for control in self.page.controls #type: ignore
                if isinstance(control, ft.Container) and 
                any(isinstance(text, ft.Text) and text.value == "Generated Recipe" 
                    for text in getattr(control.content, 'controls', []))
            ]
        for recipe in recipe_to_remove:
            self.page.controls.remove(recipe) # type: ignore


        self.quantity_table.update()
        self.product_name.update()
        self.page.update()
    
    def clear_ingredient_rows(self):
        """
        Clears only the ingredient rows from the table, without modifying the product name input.
        """
        self.ingredients.clear()
        self.quantity_table.controls.clear()
        self.quantity_table.update()

    def initialize_with_empty_row(self):
        """
        Initializes the ingredient table with one empty row.
        """
        if len(self.quantity_table.controls) == 0:
            self.add_ingredient_row(self.page)


