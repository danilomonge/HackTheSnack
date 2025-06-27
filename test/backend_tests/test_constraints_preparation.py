import sys

sys.dont_write_bytecode = True
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from Backend.Input.constraints_preparation import prepare_constraints_dict


def test_prepare_constraints_dict():
    """
    Tests the prepare_constraints_dict function.
    """
    # Test case 1: Normal case
    input_dict = {
        "ingredient1": 10.0,
        "ingredient2": None,
        "ingredient3": 20.0,
        "ingredient4": None,
        "ingredient5": 30.0,
    }
    expected_output = {0: 10.0, 2: 20.0, 4: 30.0}
    assert prepare_constraints_dict(input_dict) == expected_output

    # Test case 2: All values None
    input_dict = {"ingredient1": None, "ingredient2": None, "ingredient3": None}
    expected_output = {}
    assert prepare_constraints_dict(input_dict) == expected_output

    # Test case 3: All values have percentages
    input_dict = {"ingredient1": 10.0, "ingredient2": 5.0, "ingredient3": 20.0}
    expected_output = {0: 10.0, 1: 5.0, 2: 20.0}
    assert prepare_constraints_dict(input_dict) == expected_output
