import sys
import os
import pytest

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from hts_lib.frontend.src.handle_nutritional_info import translate_to_english, get_nutrition_usda


@pytest.mark.parametrize("german_word, expected_english", [
    ("Zucker", "sugar"),
    ("Milch", "milk"),
    ("Kartoffel", "potato"),
])
def test_translate_to_english(german_word, expected_english):
    translated = translate_to_english(german_word)
    assert expected_english.lower() in translated.lower()


@pytest.mark.parametrize("ingredient_name", [
    "sugar",
    "milk",
    "egg",
])
def test_get_nutrition_usda_valid(ingredient_name):
    data = get_nutrition_usda(ingredient_name)
    assert data is not None
    assert "kcal" in data
    assert isinstance(data["kcal"], (float, int))
    assert "protein" in data
    assert isinstance(data["protein"], (float, int))


@pytest.mark.parametrize("ingredient_name", [
    "xxxyyyzzz",     # nonsense word
    "12",            # too short
    "!!!",           # symbols
])
def test_get_nutrition_usda_invalid(ingredient_name):
    result = get_nutrition_usda(ingredient_name)
    assert result is None


def test_translate_and_get_usda_for_salz():
    """
    Tests the integration of translate_to_english and get_nutrition_usda
    using the German word 'salz' (salt).
    """
    german_word = "salz"
    translated = translate_to_english(german_word)

    # Check that the translation is correct
    assert "salt" in translated.lower()

    # Get nutrition info using translated name
    data = get_nutrition_usda(translated)

    # Check that the data is not None and contains expected values
    assert data is not None
    assert data["kcal"] == 0.0
    assert data["fat"] == 0.0
    assert data["carbs"] == 0.0
    assert data["protein"] == 0.0

    # Sodium value should be around 39.3g for 100g of salt (39300 mg)
    assert abs(data["sodium"] - 39300) < 100
