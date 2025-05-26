from math import isnan, isfinite
import flet as ft

class IngredientDataBuilder:
    @staticmethod
    def build_data_from_rows(
        ingredient_rows: list[ft.Container],
    ) -> dict[str, float | None]:
        ingredient_dict = {}

        for row in ingredient_rows:

            name_field = row.content.controls[0].content #type: ignore
            percentage_field = row.content.controls[1].content.controls[1] #type: ignore

            ingredient_name = name_field.value.strip()
            raw_input = (percentage_field.value or "").strip().replace(",", ".") #type: ignore

            percentage_value = None
            try:
                # Protects against values like 'NaN', 'nan', etc.
                if raw_input.lower() == "nan" or raw_input == "":
                    raise ValueError("Input is invalid")

                raw_float = float(raw_input)

                if isfinite(raw_float) and raw_float > 0.0:
                    percentage_value = raw_float / 100

            except Exception as e:
                print(f"⚠️ Invalid input for '{ingredient_name}': '{raw_input}' → {e}")
                percentage_value = None

            if ingredient_name:
                if percentage_value is not None and isnan(percentage_value):
                    print(f"❌ NaN detected in '{ingredient_name}' → forcing to None")
                    percentage_value = None

                ingredient_dict[ingredient_name] = percentage_value

        print("✅ Clean dictionary:", ingredient_dict)
        return ingredient_dict
