"""Command-line demo of the recipe generator (no UI, no database)."""

import sys
import os
import time

# Make `backend` importable when this file is run directly:
#   python hts_lib/backend/main.py
HTS_LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, HTS_LIB_DIR)

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
