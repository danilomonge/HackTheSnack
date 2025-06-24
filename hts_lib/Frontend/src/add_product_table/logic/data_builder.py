from math import isfinite
import flet as ft
from typing import Optional


class IngredientDataBuilder:
    """
    Reads ingredient rows from the UI and turns them into a dictionary
    with cleaned ingredient names and percentages.
    """

    @staticmethod
    def build_data_from_rows(
        ingredient_rows: list[ft.Container],
    ) -> dict[str, float | None]:
        """
        Goes through each row of the ingredient table and extracts cleaned values.

        Args:
            ingredient_rows (list[ft.Container]): UI rows with inputs.

        Returns:
            dict[str, float | None]: Dictionary with names and valid percentages.
        """
        ingredient_dict = {}

        for row in ingredient_rows:
            name_and_percentage = IngredientDataBuilder.get_values_from_row(row)
            if name_and_percentage:
                name, percentage = name_and_percentage
                ingredient_dict[name] = percentage

        return ingredient_dict

    @staticmethod
    def get_values_from_row(row: ft.Container) -> Optional[tuple[str, float | None]]:
        """
        Tries to get the name and percentage from one row.

        Returns:
            tuple or None: (name, percentage) if valid, else None.
        """
        name_field = IngredientDataBuilder.get_name_input(row)
        percent_field = IngredientDataBuilder.get_percent_input(row)

        if not name_field or not percent_field:
            return None

        name_raw = name_field.value or ""
        percent_raw = percent_field.value or ""

        name_clean = name_raw.strip()
        percent_clean = percent_raw.strip().replace(",", ".")

        percent_value = IngredientDataBuilder.convert_to_float(percent_clean)

        return (name_clean, percent_value) if name_clean else None

    @staticmethod
    def get_name_input(row: ft.Container) -> Optional[ft.TextField]:
        """
        Gets the TextField where the user wrote the ingredient name.

        Returns:
            ft.TextField or None
        """
        content = getattr(row, "content", None)
        controls = getattr(content, "controls", None)
        if not isinstance(controls, list) or len(controls) < 2:
            return None

        name_container = controls[0]
        if not name_container or not hasattr(name_container, "content"):
            return None
        content = getattr(name_container, "content", None)
        return content if isinstance(content, ft.TextField) else None

    @staticmethod
    def get_percent_input(row: ft.Container) -> Optional[ft.TextField]:
        """
        Gets the TextField where the user entered the percentage.

        Returns:
            ft.TextField or None
        """

        # -----------------------------------------------
        # UI structure of one ingredient row (ft.Container):
        #
        # Container (row)
        # └── content: Row
        #     ├── controls[0]: Container
        #     │     └── content: TextField (ingredient name)
        #     ├── controls[1]: Container
        #     │     └── content: Row
        #     │           ├── controls[0]: IconButton (minus)
        #     │           ├── controls[1]: TextField (percentage input)
        #     │           └── controls[2]: IconButton (plus)
        #     └── controls[2]: IconButton (delete row)
        # -----------------------------------------------

        content = getattr(row, "content", None)
        controls = getattr(content, "controls", None)
        if not isinstance(controls, list) or len(controls) < 2:
            return None

        percent_container = controls[1]
        percent_section = getattr(percent_container, "content", None)
        percent_controls = getattr(percent_section, "controls", None)

        if not isinstance(percent_controls, list) or len(percent_controls) < 2:
            return None

        percent_field = percent_controls[1]
        return percent_field if isinstance(percent_field, ft.TextField) else None

    @staticmethod
    def convert_to_float(raw: str) -> Optional[float]:
        """
        Tries to turn a string like "25.0" into a float in decimal format (0.25).

        Args:
            raw (str): Raw input from the user.

        Returns:
            float or None: If it's a valid number, returns it as a fraction. Else, None.
        """
        try:
            if raw.lower() == "nan" or raw == "":
                return None

            number = float(raw)

            if isfinite(number) and number > 0.0:
                return number / 100

        except Exception:
            return None

        return None
