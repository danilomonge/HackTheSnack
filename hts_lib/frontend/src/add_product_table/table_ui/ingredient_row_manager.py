import flet as ft
from frontend.src.add_product_table.logic.input_validator import InputValidator
from frontend.src.add_product_table.logic.percentage_adjuster import PercentageAdjuster
from frontend.src.styles import Styles
from frontend.src.create_result_table.result_table_ui import RecipeResultUI

class IngredientRowManager:
    """
    Manages ingredient rows in a table.

    - Adds rows with name and percentage fields
    - Includes buttons to increase or decrease the percentage
    - Validates and formats the percentage while typing
    - Removes rows from the table when needed
    - Stores all current rows in a list
   """
    
    def __init__(self, quantity_table: ft.Column, product_name: ft.TextField, page: ft.Page, on_user_input_change=None):
        """
        Creates a manager to control the ingredient rows in the table.

        Args:
            quantity_table (ft.Column): The UI column that holds all ingredient rows.
            product_name (ft.TextField): The field for the product name.
        """
        self.ingredients = []
        self.deleted_ingredient_ids = []
        self.quantity_table = quantity_table
        self.product_name = product_name
        self.page = page
        self.on_user_input_change = on_user_input_change #Callback function


    def name_input(self, style):
        """
        Creates the ingredient name input field.

        Args:
            style (dict): Visual style to apply to the field.

        Returns:
            ft.TextField: Configured text field for the ingredient name.
        """
        return ft.TextField(label="Ingredient", width=200, on_change=self.on_user_input_change, **style)

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
            suffix_style=ft.TextStyle(),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=InputValidator.fix_input_while_typing(last_valid, page, self.on_user_input_change),
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
            name_input, percent_section, lambda: self.remove_ingredient_row(row, name_input)
        )

        self.ingredients.append(row)
        self.quantity_table.controls.append(row)
        
        try:
            self.quantity_table.update()
        except AssertionError:
            pass 

        if self.on_user_input_change: 
            self.on_user_input_change(None)

    def remove_ingredient_row(self, row: ft.Container, name_input: ft.TextField):
        """
        Removes a row from both the ingredient list and the UI.

        Args:
            row (ft.Container): The ingredient row to remove.
        """
        ingredient_name = name_input.value
        if ingredient_name:
            try:
                from backend.data_base_manager.ingredient_manager import IngredientManager
                from backend.translation import Translation

                ingredient_response = IngredientManager.find_ingredient(ingredient_name)
                ingredient_data = ingredient_response.json()
                ingredient_id = Translation.get_ingredient_id_by_name(ingredient_data)

                if ingredient_id is not None and ingredient_id not in self.deleted_ingredient_ids:
                    self.deleted_ingredient_ids.append(ingredient_id)
            except Exception:
                # Removing a row must still work even when the external backend is unavailable.
                pass

        self.ingredients.remove(row)
        self.quantity_table.controls.remove(row)
        self.quantity_table.update()

        if self.on_user_input_change: 
            self.on_user_input_change(None)

    def clear_all(self):
        """
        Clears all ingredient rows and the product name from the table and resets the list.
        Also removes any generated recipe from the results section.
        """
        
        # Clear ingredients and product name
        self.ingredients.clear()
        self.product_name.value = ""
        self.quantity_table.controls.clear()
        
        # Clear the generated recipe using the new static method
        RecipeResultUI.clear_current_result(self.page)
        
        # Trigger user input change callback
        if self.on_user_input_change:
            self.on_user_input_change(None)
        
        # Update the UI
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

        if self.on_user_input_change:  # NEW
            self.on_user_input_change(None)

    def initialize_with_empty_row(self):
        """
        Initializes the ingredient table with one empty row.
        """
        if len(self.quantity_table.controls) == 0:
            self.add_ingredient_row(self.page)

