import numpy as np
import sys
import os
from pytest import approx


from backend.recipe_generator import RecipeGenerator 




def test_build_output_dict():
    """
    Tests the build_output_dict function from RecipeGenerator.
    """

    # Case 1: Basic structure with 3 ingredients
    ingredient_input: dict[str, float | None] = {"A": 70.0, "B": 20.0, "C": 10.0}
    means = np.array([70.0, 20.0, 10.0])
    stds = np.array([3.0, 2.0, 1.0])
    expected_output = {
        "A": {"mean": 70.0, "variation": 3.0},
        "B": {"mean": 20.0, "variation": 2.0},
        "C": {"mean": 10.0, "variation": 1.0},
    }
    assert RecipeGenerator.build_output_dict(ingredient_input, means, stds) == expected_output

    # Case 2: One ingredient
    ingredient_input = {"X": 0}  
    means = np.array([100.0])
    stds = np.array([0.0])
    expected_output = {"X": {"mean": 100.0, "variation": 0.0}}
    assert RecipeGenerator.build_output_dict(ingredient_input, means, stds) == expected_output


def test_solve_with_mcmc():
    """
    Tests the solve_with_mcmc function from RecipeGenerator.
    """

    # Case 1: Valid input, with only one ingredient in the middle missing
    ingredient_input = {
        "Water": 0.6,
        "Salt": None,
        "Sugar": 0.2
    }
    result = RecipeGenerator.solve_with_mcmc(ingredient_input)
    
    expected_output = {
        "Water": {"mean": 60.0, "variation": 0.0},
        "Salt": {"mean": 20.0, "variation": 0.0},
        "Sugar": {"mean": 20.0, "variation": 0.0}
    }
    
    assert result == expected_output

    # Case 2: Valid input, with multiple ingredients missing at the end
    input_ingredients = {
        "Water": 0.33,
        "Salt": 0.33,
        "Sugar": 0.33,
        "Vinegar": None,
        "Oil": None,
    }
    
    result = RecipeGenerator.solve_with_mcmc(input_ingredients)
    
    expected_output = {
        "Water": {"mean": 33.0, "variation": 0.0},
        "Salt": {"mean": 33.0, "variation": 0.0},
        "Sugar": {"mean": 33.0, "variation": 0.0},
        "Vinegar": {"mean": approx(0.73, abs=0.3), "variation": approx(0.3, abs=0.3)},
        "Oil": {"mean": approx(0.27, abs=0.3), "variation": approx(0.3, abs=0.3)},
    }
    assert result == expected_output
    
    # Case 3: Valid input, with no ingredients missing
    input_ingredients: dict[str, float | None] = {
        "Water": 0.2763,
        "Sugar": 0.1917,
        "Oil": 0.1375,
        "Salt": 0.1128,
        "Vinegar": 0.0849,
        "LemonJuice": 0.0652,
        "Pepper": 0.0496,
        "Garlic": 0.0351,
        "Onion": 0.0273,
        "Herbs": 0.0196 
        }
    
    result = RecipeGenerator.solve_with_mcmc(input_ingredients)
    
    expected_output = {
        "Water": {"mean": 27.63, "variation": 0.0},
        "Sugar": {"mean": 19.17, "variation": 0.0},
        "Oil": {"mean": 13.75, "variation": 0.0},
        "Salt": {"mean": 11.28, "variation": 0.0},
        "Vinegar": {"mean": 8.49, "variation": 0.0},
        "LemonJuice": {"mean": 6.52, "variation": 0.0},
        "Pepper": {"mean": 4.96, "variation": 0.0},
        "Garlic": {"mean": 3.51, "variation": 0.0},
        "Onion": {"mean": 2.73, "variation": 0.0},
        "Herbs": {"mean": 1.96, "variation": 0.0}
    }
    assert result == expected_output
    
    # Case 4: valid input with two ingredients in the middle missing (goes into MCMC)
    
    input_ingredients = {
        "Water": 0.2763,
        "Sugar": None,
        "Oil": 0.1375,
        "Salt": 0.1128,
        "Vinegar": 0.0849,
        "LemonJuice": None,
        "Pepper": None,
        "Garlic": None,
        "Onion": 0.0273,
        "Herbs": 0.0196 
        }
    
    result = RecipeGenerator.solve_with_mcmc(input_ingredients)
    
    expected_output = {
        "Water": {"mean": approx(27.63, abs=0.01), "variation": 0.0},
        "Sugar": {"mean": approx(17.9, abs=4.8), "variation": approx(4.89, abs=4.89)},
        "Oil": {"mean": 13.75, "variation": 0.0},
        "Salt": {"mean": 11.28, "variation": 0.0},
        "Vinegar": {"mean": 8.49, "variation": 0.0},
        "LemonJuice": {"mean": approx(6.88, abs=2.22), "variation": approx(2.22, abs=2.22)},
        "Pepper": {"mean": approx(5.36, abs=2.51), "variation": approx(2.51, abs=2.51)},
        "Garlic": {"mean": approx(4.06, abs=1.6), "variation": approx(1.6, abs=1.6)},
        "Onion": {"mean": 2.73, "variation": 0.0},
        "Herbs": {"mean": 1.96, "variation": 0.0}
    }
    
    assert result == expected_output
    
    # Case 5: Valid input with one ingredient missing in the middle and one at the end (finds initial point in eps=0)
    input_ingredients = {
        "Water": 0.33,
        "Salt": 0.33,
        "Sugar": None,
        "Vinegar": 0.11,
        "Oil": 0.11,
        "Spices": None,
    }
    
    result = RecipeGenerator.solve_with_mcmc(input_ingredients)
    
    expected_output = {
        "Water": {"mean": 33.0, "variation": 0.0},
        "Salt": {"mean": 33.0, "variation": 0.0},
        "Sugar": {"mean": approx(11.54, abs=0.58), "variation": approx(0.58, abs=0.58)},
        "Vinegar": {"mean": 11.0, "variation": 0.0},
        "Oil": {"mean": 11.0, "variation": 0.0},
        "Spices": {"mean": approx(0.46, abs=0.58), "variation": approx(0.58, abs=0.58)},
    }   
    
    assert result == expected_output
    
    # Case 6: Valid input with ingredients missing at different positions
    input_ingredients = {
        "Water": 0.227,
        "Butter": 0.22,
        "Salt": None,
        "Sugar": 0.0555,
        "Flour": None,
        "Yeast": None,
        "Pepper": 0.0555,
        "Oil": 0.0555,
        "Vinegar": 0.05,
        "Milk": None,
    }
    
    result = RecipeGenerator.solve_with_mcmc(input_ingredients)
    
    expected_output = {
        "Water": {"mean": 22.7, "variation": 0.0},
        "Butter": {"mean": 22.0, "variation": 0.0},
        "Salt": {"mean": 22.0, "variation": 0.0},
        "Sugar": {"mean": 5.55, "variation": 0.0},
        "Flour": {"mean": 5.55, "variation": 0.0},
        "Yeast": {"mean": 5.55, "variation": 0.0},
        "Pepper": {"mean": 5.55, "variation": 0.0},
        "Oil": {"mean": 5.55, "variation": 0.0},
        "Vinegar": {"mean": 5.0, "variation": 0.0},
        "Milk": {"mean": 0.55, "variation": 0.0},
    }
    
    assert result == expected_output
    
    # Case 7: Valid input with all ingredients missing 
    input_ingredients = {
        "Water": None,
        "Sugar": None,
        "LemonJuice": None,
        "Pepper": None,
        "Garlic": None,
        }
    
    result = RecipeGenerator.solve_with_mcmc(input_ingredients)
    
    expected_output = {
        "Water": {"mean": approx(47.62, abs=27.51), "variation": approx(27.51, abs=27.51)},
        "Sugar": {"mean": approx(25.15, abs=15.71), "variation": approx(15.71, abs=15.71)},
        "LemonJuice": {"mean": approx(14.41, abs=12.05), "variation": approx(14.41, abs=12.05)},
        "Pepper": {"mean": approx(8.66, abs=9.48), "variation": approx(9.48, abs=9.48)},
        "Garlic": {"mean": approx(4.16, abs=5.94), "variation": approx(5.94, abs=5.94)},
    }   
    
    assert result == expected_output
    
    # Case 8: Invalid input with fixed values too high
    input_ingredients = {
        "Water": 0.95,
        "Sugar": 0.1,
        "LemonJuice": None,
        "Pepper": None,
        "Garlic": None,
    }
    result = RecipeGenerator.solve_with_mcmc(input_ingredients)
    
    assert result is None, "Expected None for invalid input with fixed values too high"


def test_generate_recipe():
    """
    Tests the generate_recipe function from RecipeGenerator.
    """

    # Case 1: Only one ingredient, should return 100% directly (skipped)
    input_data: dict[str, float | None] = {"Only": None}
    expected_output = {"Only": {"mean": 100.0, "variation": 0.0}}
    assert RecipeGenerator.generate_recipe(input_data) == expected_output

    # Case 2: Fully filled input, total = 100% → skipping should apply
    input_data = {"A": 0.6, "B": 0.4}
    result = RecipeGenerator.generate_recipe(input_data)
    assert result == {
        "A": {"mean": 60.0, "variation": 0.0},
        "B": {"mean": 40.0, "variation": 0.0},
    }

    # Case 3: Exactly one missing, valid sum → skipping should apply
    input_data = {"A": 0.6, "B": None, "C": 0.2}
    result = RecipeGenerator.generate_recipe(input_data)
    assert result == {
        "A": {"mean": 60.0, "variation": 0.0},
        "B": {"mean": 20.0, "variation": 0.0},
        "C": {"mean": 20.0, "variation": 0.0},
    }

    # Case 4: Multiple missing, skipping fails → MCMC should run
    input_data = {"X": 0.6, "Y": None, "Z": None}
    assert result is not None

    # Case 5: Invalid input (fixed values too high) → should return None
    input_data = {"A": 0.95, "B": 0.1, "C": None}
    assert RecipeGenerator.generate_recipe(input_data) is None
    
