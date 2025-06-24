import flet as ft
from styles import Styles


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
        Formats a number string to have up to 2 digits before and after the dot.

        If the dot is missing, it adds one after the first two digits.
        It also saves the final formatted value in last_valid_ref so it can be reused later.

        Args:
        value (str): The cleaned number string (e.g. "1234", "12.345").
        last_valid_ref (list[str]): A one-item list used to store the latest valid input.

        Returns:
        str: A formatted string like "12.34".
        """

        if "." in value:
            int_part, dec_part = value.split(".")[:2]
            int_part = int_part[:2]
            dec_part = dec_part[:2]
            value = int_part + "." + dec_part
        else:
            if len(value) > 2:
                value = value[:2] + "." + value[2:]
        last_valid_ref[0] = value
        return value

    @classmethod
    def fix_input_while_typing(cls, last_valid: list[str], page: ft.Page):
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

        Returns:
            function: To use as a TextField's on_change handler.
        """
        return lambda event: (
            setattr(
                event.control,
                "value",
                cls.format_to_two_decimal(
                    cls.clean_percentage_input(event.control.value), last_valid
                ),
            ),
            # Update the page to reflect changes in the UI
            page.update(),
        )

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
                message_text.value = "⚠️ One or more ingredients are missing a name. Please check and fill in all ingredient names."
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
            message_text.value = f"⚠️ Total percentage is {total:.2f}%. It must not exceed 100%. Please reduce one ore more ingredients."
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
                message_text.value = "⚠️ Ingredient percentages must be in descending order. Please make sure that the first ingredient that you enter has the highest percentage, and each one below must be equal or smaller."
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
    def _check_below_empty_not_over_50(
        rows: list[ft.Container], message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Ensures subtotal below a row with empty or invalid percentage does not exceed 50%.
        """

        found_empty = False
        subtotal = 0.0

        for row in rows:
            perc_field = row.content.controls[1].content.controls[1]  # type: ignore

            raw_value = (perc_field.value or "").strip()

            try:
                value = float(raw_value)
            except ValueError:
                value = None

            if value is None or raw_value == "":
                found_empty = True
                subtotal = 0.0
            elif found_empty:
                subtotal += value
                if subtotal > 50.0:
                    message_text.value = "⚠️ Ingredients below an empty row must not total more than 50%. Please reduce the values below the empty ingredient."
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
            message_text.value = "⚠️ Not enough space left for the empty fields based on the values that follow them. Please lower the values that come after empty fields."
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
            message_text.value = "⚠️ Total is already 100%, but there are still empty ingredient values. Please reduce one or more percentages."
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
    def _check_empty_position_valid(
        rows: list[ft.Container], message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Checks if each empty or zero field can be filled without breaking the descending order constraint.

        For each None or 0 field:
        - Other empty/zero fields are filled with the next valid value below.
        - The current one gets the remaining value: 100 - sum of the rest.
        - It must not be greater than the field directly above it.
        """

        # Extract all percentage values from the rows, converts them to float and handles empty/zero as None
        original = []
        for row in rows:
            perc_field = row.content.controls[1].content.controls[1]  # type: ignore
            try:
                value = float((perc_field.value or "").strip())
                if value == 0:
                    original.append(None)  # Treat 0 as empty
                else:
                    original.append(value)
            except:
                original.append(None)

        # Skips already filled fields and processes only those that are None
        for i, val in enumerate(original):
            if val is not None:
                continue

            # Creates a copy of the original list to simulate filling
            simulated = original[:]

            # Fill all empty fields except the one with index i with their next valid value
            for j in range(len(simulated)):
                if j == i or simulated[j] is not None:
                    continue
                next_valid = next((x for x in simulated[j + 1:] if x is not None), None)
                # If no valid value is found, use a small default value
                simulated[j] = next_valid if next_valid is not None else 0.01


            # Calculates the fill value for the current empty field by substracting 100 - the sum of all others
            others_sum = sum(
                v for j, v in enumerate(simulated) if j != i and v is not None
            )
            fill_value = round(100 - others_sum, 5)
            original[i] = fill_value
            simulated[i] = fill_value

            # Compares the fill value with the previous field to ensure it does not exceed it
            if (
                i > 0
                and simulated[i - 1] is not None
                and fill_value > round(simulated[i - 1], 5)
            ):
                message_text.value = "⚠️ Invalid position for empty or zero ingredients. Try changing their order or erasing them."
                message_text.color = "red"
                page.update()
                return False

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
            lambda: InputValidator._check_total_if_filled(percentages, total, message_text, page),
            lambda: InputValidator._check_below_empty_not_over_50(ingredient_rows, message_text, page),
            lambda: InputValidator._check_remaining_space_is_enough(ingredient_rows, message_text, page),
            lambda: InputValidator._check_no_empty_if_total_is_100(ingredient_rows, message_text, page),
            lambda: InputValidator._check_duplicate_ingredient_names(ingredient_rows, message_text, page),
            lambda: InputValidator._check_empty_position_valid(ingredient_rows, message_text, page),
        ]

        for check in checks:
            if not check():
                return False

        message_text.value = ""
        page.update()
        return True
