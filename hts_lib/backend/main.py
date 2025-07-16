import sys

sys.dont_write_bytecode = True

import os
import time 

current_path = os.path.abspath(os.path.dirname(__file__))
while not os.path.isdir(os.path.join(current_path, "Backend")):
    parent = os.path.dirname(current_path)
    if parent == current_path:
        break  # prevent infinite loop
    current_path = parent

sys.path.insert(0, current_path)

from backend.recipe_generator import RecipeGenerator

def main():

    # Example input dictionary with fixed values
    input_ingredients = {
        "Water": 0.33,
        "Salt": 0.33,
        "Sugar": None,
        "Vinegar": 0.11,
        "Oil": 0.11,
        "Spices": None,
    }
    
    start = time.perf_counter()

    calculated_ingredients_dict = RecipeGenerator.generate_recipe(input_ingredients)
    
    end = time.perf_counter()
    duration = end - start
    
    print(f"\n🕒 Execution time (generate_recipe): {duration:.6f} seconds\n")

    if calculated_ingredients_dict:
        for name, data in calculated_ingredients_dict.items():
            print(f"- {name}: {data['mean']}% ± {data['variation']}%")


if __name__ == "__main__":
    main()
