import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hts_lib.frontend.src.add_product_table.logic.input_validator import InputValidator

import flet as ft


def test_clean_percentage_input():
    """
    Tests the clean_percentage_input function from InputValidator.
    """

    # Test case 1: valid integer input → should remain unchanged
    assert InputValidator.clean_percentage_input("42") == "42"

    # Test case 2: valid decimal input with dot → keep digits and the dot
    assert InputValidator.clean_percentage_input("3.14") == "3.14"

    # Test case 3: valid decimal input with comma → comma replaced with dot
    assert InputValidator.clean_percentage_input("3,14") == "3.14"

    # Test case 4: input with letters and numbers with one valid dot → remove invalid characters
    assert InputValidator.clean_percentage_input("a1b2.3c!") == "12.3"

    # Test case 5: input with multiple dots/commas → keep only the first dot
    assert InputValidator.clean_percentage_input("1.2.3,4") == "1.234"

    # Test case 6: input with no digits at all → return empty string
    assert InputValidator.clean_percentage_input("abc$%!") == ""

    # Test case 7: completely empty string → return empty string
    assert InputValidator.clean_percentage_input("") == ""


def test_format_to_two_decimal():
    """
    Tests the format_to_two_decimal function from InputValidator.
    """

    # Case 1: input already has 2 digits before and after the dot → should stay the same
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("12.34", last_valid) == "12.34"
    assert last_valid[0] == "12.34"

    # Case 2: input has too many digits before and after the dot → cut to 2 before and 2 after
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("1234.5678", last_valid) == "12.56"
    assert last_valid[0] == "12.56"

    # Case 3: not enough digits before or after the dot → cut what’s extra but keep what’s there
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("123.4", last_valid) == "12.4"
    assert last_valid[0] == "12.4"

    # Case 4: no dot written, but more than 2 digits total → add dot after second digit
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("1234", last_valid) == "12.34"
    assert last_valid[0] == "12.34"

    # Case 5: exactly 2 digits and no dot → leave it as is, no dot added
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("12", last_valid) == "12"
    assert last_valid[0] == "12"

    # Case 6: less than 2 digits and no dot → leave it unchanged
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("1", last_valid) == "1"
    assert last_valid[0] == "1"

    # Case 7: empty string → should return empty string too
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("", last_valid) == ""
    assert last_valid[0] == ""

    # Case 8: input has more than one dot → just use the first one
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("12.34.56", last_valid) == "12.34"
    assert last_valid[0] == "12.34"

    # Case 9: input has letters or symbols → it still tries to format them following the rules
    last_valid = [""]
    assert InputValidator.format_to_two_decimal("12.a4", last_valid) == "12.a4"
    assert last_valid[0] == "12.a4"


def test_fix_input_while_typing():
    """
    Tests the fix_input_while_typing method from InputValidator using key input equivalence classes.
    """

    class TestControl:
        def __init__(self, value):
            self.value = value

    class TestEvent:
        def __init__(self, value):
            self.control = TestControl(value)

    class TestPage:
        def __init__(self):
            self.updated = False

        def update(self):
            self.updated = True

    # Case 1: digits only, more than 2 digits → dot is inserted after 2 digits
    last_valid = [""]
    page = TestPage()
    event = TestEvent("1234")
    handler = InputValidator.fix_input_while_typing(last_valid, page) # type: ignore[arg-type]
    handler(event)
    assert event.control.value == "12.34"
    assert last_valid[0] == "12.34"
    assert page.updated

    # Case 2: digits only, 2 or fewer → no dot is inserted
    last_valid = [""]
    page = TestPage()
    event = TestEvent("12")
    handler = InputValidator.fix_input_while_typing(last_valid, page) # type: ignore[arg-type]
    handler(event)
    assert event.control.value == "12"
    assert last_valid[0] == "12"
    assert page.updated

    # Case 3: digits with a dot → write only the first 2 before the dot and the first 2 after
    last_valid = [""]
    page = TestPage()
    event = TestEvent("123.456")
    handler = InputValidator.fix_input_while_typing(last_valid, page) # type: ignore[arg-type]
    handler(event)
    assert event.control.value == "12.45"
    assert last_valid[0] == "12.45"
    assert page.updated

    # Case 4: digits with a comma → comma replaced by dot
    last_valid = [""]
    page = TestPage()
    event = TestEvent("12,34")
    handler = InputValidator.fix_input_while_typing(last_valid, page) # type: ignore[arg-type]
    handler(event)
    assert event.control.value == "12.34"
    assert last_valid[0] == "12.34"
    assert page.updated

    # Case 5: digits mixed with letters/symbols → cleaned and formatted with only numbers and the first dot
    last_valid = [""]
    page = TestPage()
    event = TestEvent("a1b2.3c4")
    handler = InputValidator.fix_input_while_typing(last_valid, page) # type: ignore[arg-type]
    handler(event)
    assert event.control.value == "12.34"
    assert last_valid[0] == "12.34"
    assert page.updated

    # Case 6: multiple dots/commas → only the first dot is used
    last_valid = [""]
    page = TestPage()
    event = TestEvent("1.23.45")
    handler = InputValidator.fix_input_while_typing(last_valid, page) # type: ignore[arg-type]
    handler(event)
    assert event.control.value == "1.23"
    assert last_valid[0] == "1.23"
    assert page.updated

    # Case 7: only letters/symbols → cleaned to empty string
    last_valid = [""]
    page = TestPage()
    event = TestEvent("abc%$")
    handler = InputValidator.fix_input_while_typing(last_valid, page) # type: ignore[arg-type]
    handler(event)
    assert event.control.value == ""
    assert last_valid[0] == ""
    assert page.updated

    # Case 8: empty string → remains empty
    last_valid = [""]
    page = TestPage()
    event = TestEvent("")
    handler = InputValidator.fix_input_while_typing(last_valid, page) # type: ignore[arg-type]
    handler(event)
    assert event.control.value == ""
    assert last_valid[0] == ""
    assert page.updated
    

def test_has_product_name():
    """
    Tests the _has_product_name function from InputValidator.
    """

    # Minimal inner mock classes
    class TestField:
        def __init__(self, value):
            self.value = value

    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False

        def update(self):
            self.updated = True

    # Case 1: valid product name (non-empty, non-whitespace string)
    page = TestPage()
    message = TestText()
    name_input = TestField("Milk")
    result = InputValidator._has_product_name(name_input, message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated

    # Case 2: empty string
    page = TestPage()
    message = TestText()
    name_input = TestField("")
    result = InputValidator._has_product_name(name_input, message, page) # type: ignore[arg-type]
    assert result is False
    assert message.value == "⚠️ Please enter a product name."
    assert message.color == "red"
    assert page.updated

    # Case 3: whitespace-only string
    page = TestPage()
    message = TestText()
    name_input = TestField("   \n\t  ")
    result = InputValidator._has_product_name(name_input, message, page) # type: ignore[arg-type]
    assert message.value == "⚠️ Please enter a product name."
    assert message.color == "red"
    assert page.updated

    # Case 4: None as input value
    page = TestPage()
    message = TestText()
    name_input = TestField(None)
    result = InputValidator._has_product_name(name_input, message, page) # type: ignore[arg-type]
    assert result is False
    assert message.value == "⚠️ Please enter a product name."
    assert message.color == "red"
    assert page.updated



def test_validate_ingredient_names_and_values():
    """
    Tests the _validate_ingredient_names_and_values method from InputValidator.
    """

    class TestField:
        def __init__(self, value):
            self.value = value

    class TestRow:
        def __init__(self, name_value, percentage_value):
            self.content = type("Content", (), {})()
            self.content.controls = [ # type: ignore[arg-type]
                type("NameContainer", (), {"content": TestField(name_value)})(),
                type("PercentageContainer", (), {
                    "content": type("InnerRow", (), {
                        "controls": [None, TestField(percentage_value)]
                    })()
                })()
            ]

    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False

        def update(self):
            self.updated = True

    # Case 1: All names and values are valid
    page = TestPage()
    message = TestText()
    rows = [TestRow("Salt", "30.5"), TestRow("Sugar", "20.0")]
    total, percentages = InputValidator._validate_ingredient_names_and_values(rows, message, page) # type: ignore[arg-type]
    assert total == 50.5
    assert percentages == [30.5, 20.0]
    assert message.value == ""
    assert not page.updated

    # Case 2: Valid names, one invalid value (not a float)
    page = TestPage()
    message = TestText()
    rows = [TestRow("Butter", "abc"), TestRow("Peach", "15")]
    total, percentages = InputValidator._validate_ingredient_names_and_values(rows, message, page) # type: ignore[arg-type]
    assert total == 15.0
    assert percentages == [0.0, 15.0]
    assert message.value == ""
    assert not page.updated

    # Case 3: One empty name string
    page = TestPage()
    message = TestText()
    rows = [TestRow("Tomato", "10"), TestRow("", "5")]
    total, percentages = InputValidator._validate_ingredient_names_and_values(rows, message, page) # type: ignore[arg-type]
    assert total == 0.0
    assert percentages is None
    assert message.value.startswith("⚠️ One or more ingredients are missing a name")
    assert message.color == "red"
    assert page.updated

    # Case 4: Name with only spaces
    page = TestPage()
    message = TestText()
    rows = [TestRow("   ", "20"), TestRow("Paprika", "5")]
    total, percentages = InputValidator._validate_ingredient_names_and_values(rows, message, page) # type: ignore[arg-type]
    assert total == 0.0
    assert percentages is None
    assert message.value.startswith("⚠️ One or more ingredients are missing a name")
    assert message.color == "red"
    assert page.updated

    # Case 5: Name is None
    page = TestPage()
    message = TestText()
    rows = [TestRow(None, "20"), TestRow("Valentina Sauce", "10")]
    total, percentages = InputValidator._validate_ingredient_names_and_values(rows, message, page) # type: ignore[arg-type]
    assert total == 0.0
    assert percentages is None
    assert message.value.startswith("⚠️ One or more ingredients are missing a name")
    assert message.color == "red"
    assert page.updated


def test_check_total_not_exceed_100():
    """
    Tests the _check_total_not_exceed_100 function from InputValidator.
    """

    # Inner mock classes
    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False

        def update(self):
            self.updated = True

    # Case 1: total less than 100.0 → valid
    message = TestText()
    page = TestPage()
    result = InputValidator._check_total_not_exceed_100(99.99, message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated

    # Case 2: total exactly 100.0 → valid
    message = TestText()
    page = TestPage()
    result = InputValidator._check_total_not_exceed_100(100.0, message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated

    # Case 3: total greater than 100.0 → invalid
    message = TestText()
    page = TestPage()
    result = InputValidator._check_total_not_exceed_100(100.01, message, page) # type: ignore[arg-type]
    assert result is False
    assert "⚠️ Total percentage is" in message.value
    assert message.color == "red"
    assert page.updated


def test_check_percentage_order():
    """
    Tests the _check_percentage_order function from InputValidator.
    """

    # Inner mock classes
    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False

        def update(self):
            self.updated = True

    # Case 1: strictly descending or equal percentages → valid
    page = TestPage()
    message = TestText()
    result = InputValidator._check_percentage_order([70.0, 50.0, 30.0, 30.0, 0.0], message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated

    # Case 2: higher percentage after 0.0 → valid
    page = TestPage()
    message = TestText()
    result = InputValidator._check_percentage_order([0.0, 40.0, 30.0], message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated

    # Case 3: higher percentage after non-zero → invalid
    page = TestPage()
    message = TestText()
    result = InputValidator._check_percentage_order([20.0, 50.0], message, page) # type: ignore[arg-type]
    assert result is False
    assert "descending order" in message.value
    assert message.color == "red"
    assert page.updated

    # Case 4: single-element list → valid
    page = TestPage()
    message = TestText()
    result = InputValidator._check_percentage_order([100.0], message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated

    # Case 5: empty list → valid
    page = TestPage()
    message = TestText()
    result = InputValidator._check_percentage_order([], message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated


def test_check_total_if_filled():
    """
    Tests the _check_total_if_filled function from InputValidator.
    """

    # Inner mock classes
    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False

        def update(self):
            self.updated = True

    # Case 1: all percentages > 0.0 and total == 100.00 → valid
    message = TestText()
    page = TestPage()
    result = InputValidator._check_total_if_filled([30.0, 40.0, 30.0], 100.0, message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated

    # Case 2: all percentages > 0.0 and total ≠ 100.00 → invalid
    message = TestText()
    page = TestPage()
    result = InputValidator._check_total_if_filled([50.0, 30.0, 20.0], 99.9, message, page) # type: ignore[arg-type]
    assert result is False
    assert "must be 100%" in message.value
    assert message.color == "red"
    assert page.updated

    # Case 3: at least one percentage is 0.0 → rule does not apply → always valid
    message = TestText()
    page = TestPage()
    result = InputValidator._check_total_if_filled([50.0, 0.0, 40.0], 90.0, message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated

    # Case 4: list with only 0 percentages → treated as "not all filled" → valid
    message = TestText()
    page = TestPage()
    result = InputValidator._check_total_if_filled([0.0, 0, 00.0], 0.0, message, page) # type: ignore[arg-type]
    assert result is True
    assert message.value == ""
    assert message.color == ""
    assert not page.updated


def test_check_remaining_space_is_enough():
    """
    Tests the _check_remaining_space_is_enough function from InputValidator.
    """

    # Mock objects
    class TestField:
        def __init__(self, value):
            self.value = value

    class TestRow:
        def __init__(self, percentage_value):
            self.content = type("Content", (), {})()
            self.content.controls = [ # type: ignore[arg-type]
                None,
                type("PercContainer", (), {
                    "content": type("InnerRow", (), {
                        "controls": [None, TestField(percentage_value)]
                    })()
                })()
            ]

    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False

        def update(self):
            self.updated = True

    # Case 1: no empty fields → always valid
    message = TestText()
    page = TestPage()
    rows = [TestRow("30"), TestRow("20"), TestRow("50")]
    result = InputValidator._check_remaining_space_is_enough(rows, message, page) # type: ignore[arg-type]
    assert result is True
    assert not page.updated

    # Case 2: empty field followed by value, total needed ≤ remaining → valid
    message = TestText()
    page = TestPage()
    rows = [TestRow("40"), TestRow(""), TestRow("30")]  # remaining = 40, needed = 30
    result = InputValidator._check_remaining_space_is_enough(rows, message, page) # type: ignore[arg-type]
    assert result is True

    # Case 3: empty field followed by value, total needed > remaining → invalid
    message = TestText()
    page = TestPage()
    rows = [TestRow("90"), TestRow(""), TestRow("20")]  # remaining = 10, needed = 20
    result = InputValidator._check_remaining_space_is_enough(rows, message, page) # type: ignore[arg-type]
    assert result is False
    assert message.value.startswith("⚠️ Error 101:")
    assert message.color == "red"
    assert page.updated

    # Case 4: empty field with no value below → valid
    message = TestText()
    page = TestPage()
    rows = [TestRow("40"), TestRow("")]
    result = InputValidator._check_remaining_space_is_enough(rows, message, page) # type: ignore[arg-type]
    assert result is True

    # Case 5: multiple empty fields reuse same value, total ≤ remaining → valid
    message = TestText()
    page = TestPage()
    rows = [TestRow("40"), TestRow(""), TestRow(""), TestRow("31")]  # reused 40 twice → needed = 80 > 70
    result = InputValidator._check_remaining_space_is_enough(rows, message, page) # type: ignore[arg-type]
    assert result is False

    # Case 6: multiple empty fields reuse same value, total > remaining → invalid
    message = TestText()
    page = TestPage()
    rows = [TestRow("10"), TestRow(""), TestRow(""), TestRow("25")]  # needed = 50, remaining = 90 → valid
    result = InputValidator._check_remaining_space_is_enough(rows, message, page) # type: ignore[arg-type]
    assert result is True

    # Case 7: all values invalid (non-numeric or empty) → needed = 0 → valid
    message = TestText()
    page = TestPage()
    rows = [TestRow("abc"), TestRow(""), TestRow("$$$"), TestRow("")]
    result = InputValidator._check_remaining_space_is_enough(rows, message, page) # type: ignore[arg-type]
    assert result is True

    # Case 8: empty list of rows → valid
    message = TestText()
    page = TestPage()
    result = InputValidator._check_remaining_space_is_enough([], message, page) # type: ignore[arg-type]
    assert result is True


def test_check_no_empty_if_total_is_100():
    """
    Tests the _check_no_empty_if_total_is_100 function from InputValidator.
    """

    class TestField:
        def __init__(self, value):
            self.value = value

    class TestRow:
        def __init__(self, percentage_value):
            self.content = type("Content", (), {})()
            self.content.controls = [ # type: ignore[arg-type]
                None,
                type("PercContainer", (), {
                    "content": type("InnerRow", (), {
                        "controls": [None, TestField(percentage_value)]
                    })()
                })()
            ]

    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False
        def update(self):
            self.updated = True

    # Case 1: total = 100, no empty fields → valid
    message = TestText()
    page = TestPage()
    rows = [TestRow("60"), TestRow("40")]
    assert InputValidator._check_no_empty_if_total_is_100(rows, message, page) is True # type: ignore[arg-type]

    # Case 2: total = 100, one empty field → invalid
    message = TestText()
    page = TestPage()
    rows = [TestRow("70"), TestRow("30"), TestRow("")]
    result = InputValidator._check_no_empty_if_total_is_100(rows, message, page) # type: ignore[arg-type]
    assert result is False
    assert message.value.startswith("⚠️ Error 102")
    assert page.updated

    # Case 3: total < 100, with empty fields → valid
    message = TestText()
    page = TestPage()
    rows = [TestRow("25"), TestRow(""), TestRow(""), TestRow("50")]
    assert InputValidator._check_no_empty_if_total_is_100(rows, message, page) is True # type: ignore[arg-type]

    # Case 4: all values invalid or empty → total = 0, has empty → valid
    message = TestText()
    page = TestPage()
    rows = [TestRow(""), TestRow("abc"), TestRow("")]
    assert InputValidator._check_no_empty_if_total_is_100(rows, message, page) is True # type: ignore[arg-type]

    # Case 5: empty list → valid
    message = TestText()
    page = TestPage()
    assert InputValidator._check_no_empty_if_total_is_100([], message, page) is True # type: ignore[arg-type]


def test_check_duplicate_ingredient_names():
    """
    Tests the _check_duplicate_ingredient_names function from InputValidator.
    """

    # Mocks
    class TestField:
        def __init__(self, value):
            self.value = value

    class TestRow:
        def __init__(self, name):
            self.content = type("Content", (), {})()
            self.content.controls = [  # type: ignore[arg-type]
                type("NameContainer", (), {"content": TestField(name)}),
                None
            ]

    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False
        def update(self):
            self.updated = True

    # Case 1: all names are unique → valid
    message = TestText()
    page = TestPage()
    rows = [TestRow("Milk"), TestRow("Sugar"), TestRow("Flour")]
    assert InputValidator._check_duplicate_ingredient_names(rows, message, page) is True # type: ignore[arg-type]

    # Case 2: two names are exactly the same → invalid
    message = TestText()
    page = TestPage()
    rows = [TestRow("Salt"), TestRow("Salt")]
    result = InputValidator._check_duplicate_ingredient_names(rows, message, page) # type: ignore[arg-type]
    assert result is False
    assert message.value.startswith("⚠️ Ingredient names cannot be repeated.")
    assert page.updated

    # Case 3: same name but different casing → invalid
    message = TestText()
    page = TestPage()
    rows = [TestRow("Water"), TestRow("water")]
    result = InputValidator._check_duplicate_ingredient_names(rows, message, page) # type: ignore[arg-type]
    assert result is False


def test_validate_all_inputs():
    """
    Tests the validate_all_inputs function from InputValidator.
    """

    class TestField:
        def __init__(self, value):
            self.value = value

    class TestRow:
        def __init__(self, name, perc):
            self.content = type("Content", (), {})()
            self.content.controls = [ # type: ignore[arg-type]
                type("NameContainer", (), {"content": TestField(name)}),
                type("PercContainer", (), {
                    "content": type("InnerRow", (), {
                        "controls": [None, TestField(perc)]
                    })()
                })
            ]

    class TestText:
        def __init__(self):
            self.value = ""
            self.color = ""

    class TestPage:
        def __init__(self):
            self.updated = False
        def update(self):
            self.updated = True

    # Case 1: all valid
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("Sugar", "60"), TestRow("Salt", "40")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is True

    # Case 2: empty product name
    assert InputValidator.validate_all_inputs(
        TestField(""), [TestRow("A", "60")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is False

    # Case 3: empty ingredient name
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("", "40")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is False

    # Case 4: duplicate names (case-insensitive)
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("Milk", "50"), TestRow("milk", "50")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is False

    # Case 5: total > 100%
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("A", "80"), TestRow("B", "30")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is False

    # Case 6: percentage order invalid
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("A", "30"), TestRow("B", "50")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is False

    # Case 7: total is 100 but there’s an empty
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("A", "100"), TestRow("B", "")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is False

    # Case 8: not enough space for empty 
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("A", "60"), TestRow("E", ""), TestRow("C", "30")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is False

    # Case 9: not enough space left for various empties
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("A", "70"), TestRow("B", ""), TestRow("C", ""), TestRow("D", "10.1")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is False

    # Case 10: only one empty ingredient list
    assert InputValidator.validate_all_inputs(
        TestField("Product"), [TestRow("A", "")], # type: ignore[arg-type]
        TestText(), TestPage() # type: ignore[arg-type]
    ) is True
