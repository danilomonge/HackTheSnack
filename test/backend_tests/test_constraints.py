import numpy as np
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from hts_lib.backend.algorithm.constraints import Constraints  


def test_inequality_constraints_shape_one():
    """
    Tests the shape of matrix A and vector a, if the number of ingredient is one.

    """
    A, a = Constraints.build_inequality_constraints(1)
    assert A.shape == (1, 1)
    assert a.shape == (1,)


def test_inequality_constraints_shape_four():
    """
    Tests the shape of matrix A and vector a, if the number of ingredient is four.

    """
    A, a = Constraints.build_inequality_constraints(4)
    assert A.shape == (7, 4)
    assert a.shape == (7,)


def test_inequality_constraints_shape_hundred():
    """
    Tests the shape of matrix A and vector a, if the number of ingredient is hundred.

    """
    A, a = Constraints.build_inequality_constraints(100)
    assert A.shape == (199, 100)
    assert a.shape == (199,)


def test_inequality_constraints_content_one():
    """
    Tests the content of matrix A and vector a, if the number of ingredient is one.

    """
    A, a = Constraints.build_inequality_constraints(1)

    A_expected = np.array([[-1.0]])
    a_expected = np.zeros(1)

    np.testing.assert_array_equal(A, A_expected)
    np.testing.assert_allclose(a, a_expected, rtol=1e-7, atol=1e-4)

    assert np.array_equal(np.signbit(A), np.signbit(A_expected)), "Sign mismatch detected in matrix 'A' (likely due to 0.0 vs -0.0)"


def test_inequality_constraints_content_four():
    """
    Tests the content of matrix A and vector a, if the number of ingredient is four.

    """
    A, a = Constraints.build_inequality_constraints(4)

    A_expected = np.array([
    [-1.0, -0.0, -0.0, -0.0],
    [-0.0, -1.0, -0.0, -0.0],
    [-0.0, -0.0, -1.0, -0.0],
    [-0.0, -0.0, -0.0, -1.0],
    [-1.0,  1.0,  0.0,  0.0],
    [ 0.0, -1.0,  1.0,  0.0],
    [ 0.0,  0.0, -1.0,  1.0],
    ], dtype=float)

    a_expected = np.zeros(7)

    np.testing.assert_array_equal(A, A_expected)
    np.testing.assert_allclose(a, a_expected, rtol=1e-7, atol=1e-4)


    assert np.array_equal(np.signbit(A), np.signbit(A_expected)), "Sign mismatch detected in matrix 'A' (likely due to 0.0 vs -0.0)"


def test_inequality_constraints_content_hundred():
    """
    Tests the content of matrix A and vector a, if the number of ingredient is hundred.

    """
    number_of_ingredients = 100
    A, a = Constraints.build_inequality_constraints(number_of_ingredients)

    A_expected = np.zeros(
        (number_of_ingredients + number_of_ingredients - 1, number_of_ingredients)
    )

    A_expected[0:number_of_ingredients, 0:number_of_ingredients] = -np.eye(
        number_of_ingredients
    )

    for i in range(number_of_ingredients - 1):
        A_expected[number_of_ingredients + i, i] = -1
        A_expected[number_of_ingredients + i, i + 1] = 1

    a_expected = np.zeros(number_of_ingredients + number_of_ingredients - 1)

    np.testing.assert_array_equal(A, A_expected)
    np.testing.assert_allclose(a, a_expected, rtol=1e-7, atol=1e-4)


    assert np.array_equal(np.signbit(A), np.signbit(A_expected)), "Sign mismatch detected in matrix 'A' (likely due to 0.0 vs -0.0)"
    

def test_equality_constraints_empty_dict_one_ingredient():
    """
    Tests if matrix B and vector b are right, if there are no fixed values and only one ingredient.

    """
    B, b = Constraints.build_equality_constraints({}, 1)

    B_expected = np.array([[1.0]])
    b_expected = np.array([1.0])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)


def test_equality_constraints_empty_dict_three_ingredients():
    """
    Tests if matrix B and vector b are right, if there are no fixed values and three ingredients.

    """
    B, b = Constraints.build_equality_constraints({}, 3)

    B_expected = np.array([[1.0, 1.0, 1.0]])
    b_expected = np.array([1.0])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)


def test_equality_constraints_one_fixed_value():
    """
    Tests if matrix B and vector b are right, if there is one fixed value.

    """
    fixed_values_dict = {1: 0.5}
    B, b = Constraints.build_equality_constraints(fixed_values_dict, 3)

    B_expected = np.array(
        [
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )
    b_expected = np.array([1.0, 0.5])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)


def test_equality_constraints_three_fixed_values():
    """
    Tests if matrix B and vector b are right, if there are three fixed values.

    """
    fixed_values_dict = {1: 0.13, 4: 0.1, 5: 0.4}
    B, b = Constraints.build_equality_constraints(fixed_values_dict, 6)

    B_expected = np.array(
        [
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        ]
    )
    b_expected = np.array([1.0, 0.13, 0.1, 0.4])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)


def test_equality_constraints_all_fixed_values():
    """
    Tests if matrix B and vector b are right, if all the values are fixed.

    """
    fixed_values_dict = {0: 0.4, 1: 0.4, 2: 0.2}
    B, b = Constraints.build_equality_constraints(fixed_values_dict, 3)

    B_expected = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    b_expected = np.array([1.0, 0.4, 0.4, 0.2])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)