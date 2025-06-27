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

from backend_.recipe_generator import RecipeGenerator

def main():

    # Example input dictionary with fixed values
    input_ingredients = {
        "Lentils": 0.63,
        "Water": None,
        "Carrots": None,
        "Onions": None,
        "Oil": None,
        "Salt": None,
        "Pepper": None,
        "Garlic": 0.016,
    }

    calculated_ingredients_dict = RecipeGenerator.generate_recipe(input_ingredients)

    if calculated_ingredients_dict:
        for name, data in calculated_ingredients_dict.items():
            print(f"- {name}: {data['mean']}% ± {data['variation']}%")


if __name__ == "__main__":
    main()
