import sys

sys.dont_write_bytecode = True

import os

current_path = os.path.abspath(os.path.dirname(__file__))
while not os.path.isdir(os.path.join(current_path, "Backend")):
    parent = os.path.dirname(current_path)
    if parent == current_path:
        break  # prevent infinite loop
    current_path = parent

sys.path.insert(0, current_path)

from Input.validation import validate
from recipe_generator import RecipeGenerator

from Input.constraints_preparation import prepare_constraints_dict
from computation import MCMC


def main():
    # test_dict = {"ingredient1": 0.2, "ingredient2": 0.3, "ingredient3": 0.5}
    # number_of_ingredients = len(test_dict)

    # if validate(test_dict) == True:
    #     print("Valid input")  # for testing purposes
    #     # next check if the product already exists in the database

    #     # if not prepare constraints:
    #     fixed_value_dict = prepare_constraints_dict(test_dict)

    #     # build the constraints
    #     A, a = constraints.build_inequality_constraints(number_of_ingredients)
    #     B, b = constraints.build_equality_constraints(
    #         fixed_value_dict, number_of_ingredients
    #     )

    #     # start the computation
    #     MCMC(A, a, B, b, num_iter=int(1e6), thinning=int(1e4))

    #     # results now need to be sent to output

    # else:
    #     print("Invalid input")
    #     # return error message to user

    # Example input dictionary with fixed values
    input_ingredients = {
        "Lentils": 0.63,
        "Water": None,
        "Onions": None,
        "Oil": None,
        "Salt": None,
        "Pepper": None,
        "Garlic": 0.02,
        "Spices": None,
    }

    calculated_ingredients_dict = RecipeGenerator.generate_recipe(input_ingredients)

    if calculated_ingredients_dict:
        for name, data in calculated_ingredients_dict.items():
            print(f"- {name}: {data['value']}% ± {data['variation']}%")


if __name__ == "__main__":
    main()
