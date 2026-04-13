import flet as ft
from .input_validator import InputValidator

class PercentageAdjuster:
    """
    Adjusts a percentage value in a text field when clicking + or - buttons.

    - Keeps the value between 0.00 and 99.99
    - Fixes format to two decimal places
    - Resets to 0.00 if the input is invalid
    - Stores the new valid value in control.data["last_valid"]
    """

    @staticmethod
    def increase_or_decrease_percentage(input_field: ft.TextField, step: float):
        """
        Adds or subtracts a value from the current percentage in a text field.

        - Makes sure the result stays within 0.00 to 99.99
        - Formats it to two decimal places
        - Updates the input field and saves the new value

        Args:
            input_field (ft.TextField): The text field to update.
            step (float): The value to add or subtract (e.g. +1.0 or -1.0).
        """
        rows = []
        current_row = None
        input_data = getattr(input_field, "data", None)
        if isinstance(input_data, dict):
            rows = input_data.get("rows") or []
            current_row = input_data.get("row")

        try:
            current_value = float(input_field.value) #type: ignore (caught below)
            updated_value = InputValidator.clamp_percentage_value(
                rows,
                current_row,
                current_value + step,
            )
        except:
            updated_value = 0.0

        new_value_str = f"{updated_value:.2f}"
        input_field.value = new_value_str
        input_field.data["last_valid"][0] = new_value_str #type: ignore
        input_field.update()
