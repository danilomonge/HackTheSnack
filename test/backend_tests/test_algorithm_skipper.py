import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from hts_lib.backend.algorithm_skipper import AlgorithmSkipper


def test_has_only_one_ingredient():
    assert AlgorithmSkipper.has_only_one_ingredient({"A": None}) is True
    assert AlgorithmSkipper.has_only_one_ingredient({"A": 0.5, "B": 0.5}) is False


def test_solve_single_ingredient_case():
    result = AlgorithmSkipper.solve_single_ingredient_case({"Salt": None})
    assert result == {"Salt": {"mean": 100.0, "variation": 0.0}}


def test_has_exactly_one_missing_valid():
    assert (
        AlgorithmSkipper.has_exactly_one_missing({"A": 0.6, "B": None, "C": 0.2})
        is True
    )


def test_has_exactly_one_missing_invalid_order():
    assert (
        AlgorithmSkipper.has_exactly_one_missing({"A": 0.7, "B": None, "C": 0.5})
        is False
    )
    assert (
        AlgorithmSkipper.has_exactly_one_missing({"A": 0.1, "B": None, "C": 0.7})
        is False
    )
    assert (
        AlgorithmSkipper.has_exactly_one_missing({"A": 0.7, "B": None, "C": 0.1})
        is True
    )


def test_solve_one_missing_directly_valid():
    result = AlgorithmSkipper.solve_one_missing_directly(
        {"A": 0.7, "B": None, "C": 0.1}
    )
    assert result is not None, "Expected a result, got None"
    assert result["B"]["mean"] == 20.0


def test_solve_one_missing_directly_invalid_overflow():
    result = AlgorithmSkipper.solve_one_missing_directly(
        {"A": 0.8, "B": None, "C": 0.4}
    )
    assert result is None


def test_is_fully_filled_and_total_is_100_percent_true():
    assert (
        AlgorithmSkipper.is_fully_filled_and_total_is_100_percent(
            {"A": 0.5, "B": 0.3, "C": 0.2}
        )
        is True
    )


def test_is_fully_filled_and_total_is_100_percent_false_due_to_none():
    assert (
        AlgorithmSkipper.is_fully_filled_and_total_is_100_percent(
            {"A": 0.5, "B": None, "C": 0.2}
        )
        is False
    )


def test_solve_total_is_100_percent_ingredient_case():
    result = AlgorithmSkipper.solve_total_is_100_percent_ingredient_case(
        {"A": 0.5, "B": 0.5}
    )
    assert result == {
        "A": {"mean": 50.0, "variation": 0.0},
        "B": {"mean": 50.0, "variation": 0.0},
    }


def test_can_fill_all_missing_with_next_valid_value_true():
    assert (
        AlgorithmSkipper.can_fill_all_missing_with_next_valid_value(
            {"A": 0.5, "B": None, "C": 0.1, "D": 0.1, "E": 0.1, "F": 0.1}
        )
        is True
    )


def test_can_fill_all_missing_with_next_valid_value_false():
    assert (
        AlgorithmSkipper.can_fill_all_missing_with_next_valid_value(
            {"A": None, "B": None}
        )
        is False
    )


def test_solve_fill_all_missing_with_next_valid_value():
    result = AlgorithmSkipper.solve_fill_all_missing_with_next_valid_value(
        {"A": 0.3, "B": None, "C": 0.3, "D": None, "E": 0.4}
    )
    assert result["B"]["mean"] == 30.0
    assert result["D"]["mean"] == 40.0


def test_skip_algorithm_cases():
    # Case 1: Only one ingredient (None)
    assert AlgorithmSkipper.skip_algorithm({"Only": None}) == {
        "Only": {"mean": 100.0, "variation": 0.0}
    }

    # Case 2: Exactly one missing, but invalid (B would be 0)
    assert AlgorithmSkipper.skip_algorithm({"A": 0.7, "B": None, "C": 0.3}) is None

    # Case 3: Total is 100%
    assert AlgorithmSkipper.skip_algorithm({"A": 0.5, "B": 0.5}) == {
        "A": {"mean": 50.0, "variation": 0.0},
        "B": {"mean": 50.0, "variation": 0.0},
    }

    # Case 4: Exactly one missing, valid completion
    result = AlgorithmSkipper.skip_algorithm({"A": 0.6, "B": None, "C": 0.2})
    assert result == {
        "A": {"mean": 60.0, "variation": 0.0},
        "B": {"mean": 20.0, "variation": 0.0},
        "C": {"mean": 20.0, "variation": 0.0},
    }

    # Case 5: Fill missing with next valid (B and D filled from C and E)
    result = AlgorithmSkipper.skip_algorithm(
        {"A": 0.5, "B": None, "C": 0.2, "D": None, "E": 0.05}
    )
    assert result == {
        "A": {"mean": 50.0, "variation": 0.0},
        "B": {"mean": 20.0, "variation": 0.0},
        "C": {"mean": 20.0, "variation": 0.0},
        "D": {"mean": 05.0, "variation": 0.0},
        "E": {"mean": 05.0, "variation": 0.0},
    }

    # Case 6: Does not match any skipping condition
    result = AlgorithmSkipper.skip_algorithm({"A": 0.4, "B": None, "C": 0.4})
    assert result is None
