def validate(input_dict: dict[str, float | None]):
    """
    Validates the input data:
    - Values can be float or None.
    - Ignores None in total.
    - No numeric value may be <= 0.
    - Total sum of numeric values must not exceed 100.

    Args:
        input_data: dict[str, float | None] - Ingredient names and their percentages (or None).

    Returns:
        True if valid, False if not.
    """
    total_percentage = 0

    for ingredient, percentage in input_dict.items():
        if percentage is None:
            continue
        if not isinstance(percentage, (int, float)) or percentage <= 0:
            return False
        total_percentage += percentage

    return total_percentage <= 100