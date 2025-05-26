import flet as ft


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
                message_text.value = "⚠️ One or more ingredients are missing a name."
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
            message_text.value = (
                f"⚠️ Total percentage is {total:.2f}%. It must not exceed 100%."
            )
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
                message_text.value = "⚠️ An ingredient has a higher percentage than the one above it. This is only allowed if the upper one is 0.00%."
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
            message_text.value = f"⚠️ All percentages are filled, but their total is {total:.2f}%. It must be exactly 100%."
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
                    message_text.value = "⚠️ Subtotal below an ingredient with empty quantity cannot exceed 50%."
                    message_text.color = "red"
                    page.update()
                    return False

        return True

    @staticmethod
    def _check_remaining_space_is_enough(
        rows: list[ft.Container], message_text: ft.Text, page: ft.Page
    ) -> bool:
        """
        Checks that the total of values directly below empty fields
        does not exceed the remaining available percentage.
        Allows reuse of the same value for multiple empties.
        """
        defined_total = 0.0
        next_values_after_empty = []

        # First, sum all defined values
        for row in rows:
            perc_field = row.content.controls[1].content.controls[1]  # type: ignore
            try:
                value = float(perc_field.value)
            except:
                value = 0.0
            if value > 0.0:
                defined_total += value

        # Then, for each empty, take the next defined value (even if repeated)
        for i in range(len(rows)):
            perc_field = rows[i].content.controls[1].content.controls[1]  # type: ignore

            if perc_field.value.strip():
                continue  # skip if not empty

            # Look ahead for the next defined value
            for j in range(i + 1, len(rows)):
                next_field = rows[j].content.controls[1].content.controls[1]  # type: ignore
                try:
                    next_value = float(next_field.value)
                except:
                    next_value = 0.0

                if next_field.value.strip():
                    next_values_after_empty.append(next_value)
                    break  # only take the first defined value below each empty

        total_needed_space = sum(next_values_after_empty)
        remaining = 100.0 - defined_total

        if total_needed_space > remaining:
            message_text.value = "⚠️ Not enough space left for the empty fields based on the values that follow them."
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
            message_text.value = (
                "⚠️ Total is already 100%, but there are still empty ingredient values."
            )
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
        - That total percentage is valid and logical according to rules.

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

        if not InputValidator._check_total_not_exceed_100(total, message_text, page):
            return False

        if not InputValidator._check_percentage_order(percentages, message_text, page):
            return False

        if not InputValidator._check_total_if_filled(
            percentages, total, message_text, page
        ):
            return False

        if not InputValidator._check_below_empty_not_over_50(
            ingredient_rows, message_text, page
        ):
            return False

        if not InputValidator._check_remaining_space_is_enough(
            ingredient_rows, message_text, page
        ):
            return False

        if not InputValidator._check_no_empty_if_total_is_100(
            ingredient_rows, message_text, page
        ):
            return False

        if not InputValidator._check_duplicate_ingredient_names(
            ingredient_rows, message_text, page
        ):
            return False

        # Clear the message text if all validations pass

        message_text.value = ""
        page.update()
        return True
