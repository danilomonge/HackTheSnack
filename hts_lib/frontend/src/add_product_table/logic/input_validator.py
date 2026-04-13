import flet as ft
from ...styles import Styles


class InputValidator:
    """
    Helps clean and check percentage inputs in a product form.

    - Formats numbers while typing (e.g. turns "1234" into "12.34")
    - Makes sure all ingredients have names and valid percentages
    - Checks that the total doesn’t go over 100%
    - Makes sure lower ingredients don’t have higher values than the ones above
    - If all percentages are filled, they must add up to exactly 100%
    """

    @staticmethod
    def get_max_percentage_for_row(
        rows: list[ft.Container],
        current_row: ft.Container | None,
    ) -> float:
        """
        Returns the maximum allowed percentage for one row.

        Rules:
        - If there is only one ingredient row, the max is 100.00.
        - With multiple rows, the max is 99.99.
        - A lower row cannot exceed any filled row above it.
        """
        if len(rows) <= 1:
            return 100.0

        max_value = 99.99
        if current_row is None:
            return max_value

        for row in rows:
            if row is current_row:
                break

            perc_field = row.content.controls[1].content.controls[1]  # type: ignore
            try:
                above_value = float((perc_field.value or "").strip())
            except Exception:
                above_value = 0.0

            if above_value > 0.0:
                max_value = min(max_value, above_value)

        return max_value

    @classmethod
    def clamp_percentage_value(
        cls,
        rows: list[ft.Container],
        current_row: ft.Container | None,
        numeric_value: float,
    ) -> float:
        """
        Clamps a percentage value to the allowed range for the current row.
        """
        max_value = cls.get_max_percentage_for_row(rows, current_row)
        return max(0.0, min(max_value, numeric_value))

    @staticmethod
    def clean_percentage_input(value: str) -> str:
        """
        Takes a user input string and filters it to keep only digits and one decimal point.
        What it does:
        - Replaces commas with dots to handle different decimal formats.
        - Removes any other characters that aren't digits or the first dot it finds.
        - Returns a simplified string that looks like a valid number (or part of one).

        Args:
        value (str): The input entered by the user (e.g. from a text field).

        Returns:
        str: A cleaned version of the input that keeps only valid numeric characters.
        """

        value = value.replace(",", ".")
        cleaned = ""
        dot_found = False
        for ch in value:
            if ch.isdigit():
                cleaned += ch
            elif ch == "." and not dot_found:
                cleaned += ch
                dot_found = True
        return cleaned

    @staticmethod
    def format_to_two_decimal(value: str, last_valid_ref: list[str]) -> str:
        """
        Formats a number string to have up to 3 digits before and 2 after the dot.

        It does not auto-insert a decimal separator. This keeps typing natural for
        values like 10, 90, and 100 while still trimming invalid extra digits.

        Args:
        value (str): The cleaned number string (e.g. "1234", "12.345").
        last_valid_ref (list[str]): A one-item list used to store the latest valid input.

        Returns:
        str: A formatted string like "100", "12.34", or "9.5".
        """

        if "." in value:
            int_part, dec_part = value.split(".")[:2]
            int_part = int_part[:3]
            dec_part = dec_part[:2]
            value = int_part + "." + dec_part
        else:
            value = value[:3]
        last_valid_ref[0] = value
        return value

    @classmethod
    def fix_input_while_typing(cls, last_valid: list[str], page: ft.Page, on_change_extra=None):
        """
        Returns a function for on_change that formats the input while typing.

        It:
        - Cleans unwanted characters (like commas or letters),
        - Formats the number as a percentage (max 2 digits before/after dot),
        - Updates the text field and saves the latest valid input,
        - Refreshes the UI.

        Args:
            last_valid (list[str]): Stores the last valid formatted string.
            page (ft.Page): The Flet page to trigger updates.
            on_change_extra (Callable, optional): Additional logic to run after formatting.

        Returns:
            function: To use as a TextField's on_change handler.
        """
        def handler(event):
            control = event.control
            control.value = cls.format_to_two_decimal(
                cls.clean_percentage_input(event.control.value), last_valid
            )

            rows = []
            current_row = None
            control_data = getattr(control, "data", None)
            if isinstance(control_data, dict):
                rows = control_data.get("rows") or []
                current_row = control_data.get("row")

            try:
                numeric_value = float(control.value)
                numeric_value = cls.clamp_percentage_value(rows, current_row, numeric_value)
                if "." in control.value:
                    control.value = f"{numeric_value:.2f}".rstrip("0").rstrip(".")
                else:
                    if numeric_value.is_integer():
                        control.value = str(int(numeric_value))
                    else:
                        control.value = f"{numeric_value:.2f}".rstrip("0").rstrip(".")
                last_valid[0] = control.value
            except Exception:
                pass

            page.update()
            if on_change_extra:
                on_change_extra(event)

        return handler

    @staticmethod
    def _has_product_name(
        name_input: ft.TextField, message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Checks that the product name is not empty.
        """
        name = (name_input.value or "").strip()
        if not name:
            message_text.value = "⚠️ Please enter a product name."
            message_text.color = "red"
            page.update()
            return False
        return True

    @staticmethod
    def _validate_ingredient_names_and_values(
        rows: list[ft.Container], message_text: ft.Text, page: ft.Page
    ) -> tuple[float, list[float] | None]:
        """
        Validates that each ingredient has a name and reads percentage values.

        Returns:
            tuple: (total percentage, list of individual percentages)
                If any name is missing, returns (0.0, None)
        """
        total = 0.0
        percentages = []

        for row in rows:
            name_field = row.content.controls[0].content  # type: ignore
            perc_field = row.content.controls[1].content.controls[1]  # type: ignore

            name = (name_field.value or "").strip()
            if not name:
                message_text.value = "⚠️ One or more ingredients are missing a name. Please check your input again."
                message_text.color = "red"
                page.update()
                return 0.0, None

            try:
                value = float(perc_field.value)
            except:
                value = 0.0

            total += value
            percentages.append(value)

        return total, percentages

    @staticmethod
    def _check_total_not_exceed_100(
        total: float, message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Checks that the total percentage does not go over 100%.
        """
        if total > 100.0:
            message_text.value = f"⚠️ Total percentage is {total:.2f}%. It must not exceed 100%. Please check your inputs again."
            message_text.color = "red"
            page.update()
            return False
        return True

    @staticmethod
    def _check_percentage_order(
        percentages: list[float], message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Checks that lower rows do not have higher percentages than the rows above them,
        unless the one above is 0.00%.
        """
        for i in range(len(percentages) - 1):
            if percentages[i] != 0.0 and percentages[i] < percentages[i + 1]:
                message_text.value = "⚠️ Ingredient percentages must be in descending order. Please check your inputs again."
                message_text.color = "red"
                page.update()
                return False
        return True

    @staticmethod
    def _check_total_if_filled(
        percentages: list[float], total: float, message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        If all percentages are non-zero, the total must be exactly 100.00%.
        """
        if all(p > 0.0 for p in percentages) and round(total, 2) != 100.00:
            message_text.value = f"⚠️ Total is {total:.2f}%, but it must be 100% when all ingredients are filled. Please adjust the values."
            message_text.color = "red"
            page.update()
            return False
        return True

    @staticmethod
    def _check_first_percentage_is_large_enough(
        percentages: list[float], message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Ensures the first ingredient is large enough to allow a descending recipe.
        """
        if len(percentages) <= 1:
            return True

        first_value = percentages[0]
        if first_value <= 0.0:
            return True

        minimum_required = round(100.0 / len(percentages), 2)
        if first_value < minimum_required:
            message_text.value = (
                f"⚠️ The first ingredient is too small for a recipe with {len(percentages)} ingredients. "
                f"It must be at least {minimum_required:.2f}%."
            )
            message_text.color = "red"
            page.update()
            return False

        return True


    @staticmethod
    def _check_remaining_space_is_enough(
        rows: list[ft.Container], message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Checks if there is enough space to support empty fields by simulating
        their values with the next valid number below each one.
        """
        defined_total = 0.0
        total_needed_space = 0.0

        # Sum all valid defined values
        for row in rows:
            perc_field = row.content.controls[1].content.controls[1]  # type: ignore
            try:
                value = float(perc_field.value)
            except:
                value = 0.0
            if value > 0.0:
                defined_total += value

        # For each empty field, add the next valid value (can be reused)
        for i in range(len(rows)):
            perc_field = rows[i].content.controls[1].content.controls[1]  # type: ignore

            if perc_field.value.strip():
                continue

            for j in range(i + 1, len(rows)):
                next_field = rows[j].content.controls[1].content.controls[1]  # type: ignore
                try:
                    next_value = float(next_field.value)
                except:
                    next_value = 0.0

                if next_field.value.strip():
                    total_needed_space += next_value
                    break

        remaining = 100.0 - defined_total

        if total_needed_space > remaining:
            message_text.value = "⚠️ Error 101: Please check your inputs again or read the instructions."
            message_text.color = "red"
            page.update()
            return False

        return True

    @staticmethod
    def _check_no_empty_if_total_is_100(
        rows: list[ft.Container], message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Prevents having empty ingredient fields when the total already equals 100%.
        """
        total = 0.0
        has_empty = False

        for row in rows:
            perc_field = row.content.controls[1].content.controls[1]  # type: ignore
            value_str = perc_field.value.strip()

            if not value_str:
                has_empty = True
                continue

            try:
                value = float(value_str)
            except:
                value = 0.0

            total += value

        if has_empty and abs(total - 100.0) < 1e-6:
            message_text.value = "⚠️ Error 102: Please check your inputs again or read the instructions."
            message_text.color = "red"
            page.update()
            return False

        return True

    @staticmethod
    def _check_duplicate_ingredient_names(
        rows: list[ft.Container], message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Checks that no ingredient name is repeated (case-insensitive).
        """
        seen = set()

        for row in rows:
            name_field = row.content.controls[0].content  # type: ignore
            name = name_field.value.strip().lower()

            if not name:
                continue  # skip empty names

            if name in seen:
                message_text.value = "⚠️ Ingredient names cannot be repeated."
                message_text.color = "red"
                page.update()
                return False

            seen.add(name)

        return True
    

    @staticmethod
    def validate_all_inputs(
        product_name_input: ft.TextField,
        ingredient_rows: list[ft.Container],
        message_text: ft.Text,
        page: ft.Page,
    ) -> bool:
        """
        Validates all required fields for product creation.

        It checks:
        - That the product name is filled in.
        - That each ingredient has a name and a valid percentage.
        - That the total percentage is within valid and logical limits.
        - That ingredient order, empties, and duplicates follow the rules.

        Shows an error message if something is invalid.

        Returns:
            bool: True if all inputs are valid, False otherwise.
        """
        if not InputValidator._has_product_name(product_name_input, message_text, page):
            return False

        total, percentages = InputValidator._validate_ingredient_names_and_values(
            ingredient_rows, message_text, page
        )
        if percentages is None:
            return False

        checks = [
            lambda: InputValidator._check_total_not_exceed_100(total, message_text, page),
            lambda: InputValidator._check_percentage_order(percentages, message_text, page),
            lambda: InputValidator._check_first_percentage_is_large_enough(percentages, message_text, page),
            lambda: InputValidator._check_total_if_filled(percentages, total, message_text, page),
            lambda: InputValidator._check_remaining_space_is_enough(ingredient_rows, message_text, page),
            lambda: InputValidator._check_no_empty_if_total_is_100(ingredient_rows, message_text, page),
            lambda: InputValidator._check_duplicate_ingredient_names(ingredient_rows, message_text, page),
        ]

        for check in checks:
            if not check():
                return False

        message_text.value = ""
        page.update()
        return True
