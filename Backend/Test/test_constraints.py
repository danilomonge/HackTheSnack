from Backend.constraints import build_inequality_constraints, build_equality_constraints
import numpy as np

def test_inequality_constraints_shape_one():
    A, a = build_inequality_constraints(1)
    assert A.shape == (1, 1)
    assert a.shape == (1,)

def test_inequality_constraints_shape_four():
    A, a = build_inequality_constraints(4)
    assert A.shape == (7, 4)
    assert a.shape == (7,)

def test_inequality_constraints_shape_hundred():
    A, a = build_inequality_constraints(100)
    assert A.shape == (199, 100)
    assert a.shape == (199,)

def test_inequality_constraints_content_one():

    A, a = build_inequality_constraints(1)

    A_expected = np.array([[-1.]])
    a_expected = np.zeros(1)
    
    np.testing.assert_array_equal(A, A_expected)
    np.testing.assert_array_equal(a, a_expected)

def test_inequality_constraints_content_four():
    A, a = build_inequality_constraints(4)

    A_expected = np.array([
    [-1,  0,  0,  0],
    [ 0, -1,  0,  0],
    [ 0,  0, -1,  0],
    [ 0,  0,  0, -1],
    [-1,  1,  0,  0],
    [ 0, -1,  1,  0],
    [ 0,  0, -1,  1],
], dtype=float)
    
    a_expected = np.zeros(7)
    
    np.testing.assert_array_equal(A, A_expected)
    np.testing.assert_array_equal(a, a_expected)

def test_inequality_constraints_content_hundred():
    number_of_ingredients = 100
    A, a = build_inequality_constraints(number_of_ingredients)

    A_expected = np.zeros(
        (number_of_ingredients + number_of_ingredients - 1, number_of_ingredients)
    )

    A_expected[0:number_of_ingredients, 0:number_of_ingredients] = -np.eye(number_of_ingredients)

    for i in range(number_of_ingredients - 1):
        A_expected[number_of_ingredients + i, i] = -1
        A_expected[number_of_ingredients + i, i + 1] = 1

    a_expected = np.zeros(number_of_ingredients + number_of_ingredients - 1)

    np.testing.assert_array_equal(A, A_expected)
    np.testing.assert_array_equal(a, a_expected)

def test_equality_constraints_empty_dict():
    B, b = build_equality_constraints({}, 1)

    B_expected = np.array([[1.0]])     
    b_expected = np.array([1.0])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)

def test_equality_constraints_one_fixed_value():
    fixed_values_dict = {1: 0.5}
    B, b = build_equality_constraints(fixed_values_dict, 3)

    B_expected = np.array([
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 0.0],
    ])
    b_expected = np.array([1.0, 0.5])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)

def test_equality_constraints_three_fixed_values():
    fixed_values_dict = {1: 0.13, 4: 0.1, 5: 0.4}
    B, b = build_equality_constraints(fixed_values_dict, 6)

    B_expected = np.array([
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    ])
    b_expected = np.array([1.0, 0.13, 0.1, 0.4])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)

def test_equality_constraints_all_fixed_values():
    fixed_values_dict = {0: 0.4, 1: 0.4, 2: 0.2}
    B, b = build_equality_constraints(fixed_values_dict, 3)

    B_expected = np.array([
        [1.0, 1.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ])
    b_expected = np.array([1.0, 0.4, 0.4, 0.2])

    np.testing.assert_array_equal(B, B_expected)
    np.testing.assert_array_equal(b, b_expected)