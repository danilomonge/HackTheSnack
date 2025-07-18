import sys


def prepare_constraints_dict(input_dict):
    """
    Filters the user input (ingredient dict) to include only entries where the value is not None.
    Returns a new dictionary with the index of the fixed-value-ingredient of the original dictionary as the key and the float (amount) as the value.

    Args:
        dict[str, float] - Input dictionary with string keys and float values

    Return:
        dict[int, float] - Filtered dictionary with indices as keys and positive floats as values
    """
    fixed_value_dict = {
        index: value
        for index, (key, value) in enumerate(input_dict.items())
        if value is not None and value > 0
    }
    return fixed_value_dict
