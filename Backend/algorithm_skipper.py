import sys

sys.dont_write_bytecode = True

import numpy as np


class AlgorithmSkipper:
    """
    Class to skip algorithms based on the input data.
    """

    @staticmethod
    def skip_algorithm(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]] | None:
        """
        Determines if the algorithm should be skipped based on the input data.
        """
        # Skip if there's only one ingredient and return a dict with that ingredient
        if AlgorithmSkipper.has_only_one_ingredient(ingredient_input):
            return AlgorithmSkipper.solve_single_ingredient_case(ingredient_input)

        # Skip if there's exactly one missing ingredient and return the dict with the missing value calculated directly
        if AlgorithmSkipper.has_exactly_one_missing(ingredient_input):
            return AlgorithmSkipper.solve_one_missing_directly(ingredient_input)

        # Skip if all ingredients are filled and total is 100% and return the dict with the values
        if AlgorithmSkipper.is_fully_filled_and_total_is_100_percent(ingredient_input):
            return AlgorithmSkipper.solve_total_is_100_percent_ingredient_case(
                ingredient_input
            )

        # Skip if all missing can be filled with their next valid value and return the dict with the values
        if AlgorithmSkipper.can_fill_all_missing_with_next_valid_value(
            ingredient_input
        ):
            return AlgorithmSkipper.solve_fill_all_missing_with_next_valid_value(
                ingredient_input
            )

        # If none of the above conditions are met, return None to indicate that the algorithm should not be skipped
        return None

    @staticmethod
    def has_only_one_ingredient(ingredient_input: dict[str, float | None]) -> bool:
        """
        Returns True if the input contains only one ingredient.
        """
        return len(ingredient_input) == 1

    @staticmethod
    def solve_single_ingredient_case(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]]:
        """
        If there's just one ingredient, its percentage is 100% with no variation.
        """
        name = next(iter(ingredient_input))
        return {name: {"mean": 100.0, "variation": 0.0}}

    @staticmethod
    def has_exactly_one_missing(ingredient_input: dict[str, float | None]) -> bool:
        """
        Returns True if exactly one ingredient is missing (value is None)
        and the estimated missing value does not exceed the amount of the previous known ingredient.
        """
        ingredient_values = list(ingredient_input.values())

        # Check if exactly one value is missing
        if ingredient_values.count(None) != 1:
            return False

        missing_value_index = ingredient_values.index(None)
        total_known_values = sum(
            value for value in ingredient_values if value is not None
        )
        estimated_missing_value = round(1.0 - total_known_values, 6)
        # If the missing value has a previous ingredient with value, check that the missing value does not exceed it
        if missing_value_index > 0:
            prev_value = ingredient_values[missing_value_index - 1]
            if prev_value is not None and estimated_missing_value > prev_value:
                return False

        # If the missing value has a next ingredient with value, check that the missing value is not less than it
        if missing_value_index < len(ingredient_values) - 1:
            next_value = ingredient_values[missing_value_index + 1]
            if next_value is not None and estimated_missing_value < next_value:
                return False

        return True

    @staticmethod
    def solve_one_missing_directly(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]] | None:
        """
        Calculates the missing value by subtracting the known total from 1.
        Useful when only one ingredient is unknown.
        """
        known = {k: v for k, v in ingredient_input.items() if v is not None}

        known_total = sum(known.values())
        missing_value = 1.0 - known_total

        if missing_value < 0:
            print("❌ Error: known percentages exceed 100%.")
            return None

        result = {}
        for name in ingredient_input:
            val = ingredient_input[name]
            if val is not None:
                result[name] = {"mean": round(val * 100, 4), "variation": 0.0}
            else:
                result[name] = {"mean": round(missing_value * 100, 4), "variation": 0.0}

        print("ℹ️ Only one missing value. Calculated directly.")
        return result

    @staticmethod
    def is_fully_filled_and_total_is_100_percent(
        ingredient_input: dict[str, float | None],
    ) -> bool:
        """
        Returns True if all values are set and sum to 100%.
        """
        values = ingredient_input.values()
        if any(v is None for v in values):
            return False
        total = sum(v for v in values if v is not None)
        return abs(total - 1.0) < 1e-6

    @staticmethod
    def solve_total_is_100_percent_ingredient_case(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]]:
        """
        Converts an input with values summing to 100% into the expected output format.
        Only uses ingredients with non-None values.
        """
        return {
            name: {"mean": round(value * 100, 4), "variation": 0.0}
            for name, value in ingredient_input.items()
            if value is not None
        }

    @staticmethod
    def can_fill_all_missing_with_next_valid_value(
        ingredient_input: dict[str, float | None],
    ) -> bool:
        """
        Returns True if each None value can be filled with the next known value
        and the total sum of all values equals 100%.
        """
        ingredient_values = list(ingredient_input.values())
        filled_values = []

        i = 0
        while i < len(ingredient_values):
            current_value = ingredient_values[i]

            if current_value is not None:
                filled_values.append(current_value)
                i += 1
            else:
                j = i + 1
                while j < len(ingredient_values) and ingredient_values[j] is None:
                    j += 1
                if j == len(ingredient_values):
                    return False  # no valid value after a None

                next_known_value = ingredient_values[j]
                filled_values.extend(
                    [next_known_value] * (j - i)
                )  # fill all None values following the current None with the next known value
                i = j

        return abs(round(sum(filled_values), 6) - 1.0) < 1e-6

    @staticmethod
    def solve_fill_all_missing_with_next_valid_value(
        ingredient_input: dict[str, float | None],
    ) -> dict[str, dict[str, float]]:
        """
        Fills each None with the next known valid value and returns a completed recipe
        with 0.0 variation for each ingredient.
        Only usable if can_fill_all_missing_with_next_value() returns True.
        """
        ingredient_items = list(ingredient_input.items())
        result: dict[str, dict[str, float]] = {}

        i = 0
        while i < len(ingredient_items):
            name, value = ingredient_items[i]

            if value is not None:
                result[name] = {"mean": round(value * 100, 4), "variation": 0.0}
                i += 1
            else:
                j = i + 1
                while j < len(ingredient_items) and ingredient_items[j][1] is None:
                    j += 1
                if j == len(ingredient_items):
                    break  # no valid value found after the None

                next_known_value = ingredient_items[j][1]
                assert (
                    next_known_value is not None
                ), "Unexpected None value after known ingredient check"
                for k in range(i, j):
                    missing_name = ingredient_items[k][0]
                    result[missing_name] = {
                        "mean": round(next_known_value * 100, 4),
                        "variation": 0.0,
                    }
                i = j

        return result
