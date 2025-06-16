from Frontend.src.add_product_table.table_ui.ingredient_manager  import IngredientManager


class DataFiller:
    """
    Class for populating the ingredient input UI with data.

    Provides static methods to fill ingredient rows
    in the UI using a given dictionary of ingredient names and their corresponding
    percentages.
    """

    @staticmethod
    def fill_rows_from_data(
        ingredient_data: dict[str, float],
        ingredient_manager: "IngredientManager"
    ) -> None:
        """
        Receive a dictionary with ingredients and percentages, and fill in the lines in the UI.

        Args:
            ingredient_data (dict[str, float]): Dictionary with name and percentage of ingredients.
            ingredient_manager (IngredientManager): Instance of the ingredient manager.
        """
        style = ingredient_manager.input_style()

        ingredient_manager.clear_all()

        for name, percentage in ingredient_data.items():
            last_valid = [f"{percentage:.2f}"]

            name_input = ingredient_manager.name_input(style)
            name_input.value = name

            percent_input = ingredient_manager.percent_input(style, last_valid=[], page=ingredient_manager.page)
            percent_input.value = ""    #f"{percentage:.2f}"

            percent_section = ingredient_manager.percent_section(percent_input)

            # Row creation
            row = ingredient_manager.ingredient_row(
                name_input, percent_section,
                lambda r=None: ingredient_manager.remove_ingredient_row(row)
            )

            ingredient_manager.ingredients.append(row)
            ingredient_manager.quantity_table.controls.append(row)

        ingredient_manager.quantity_table.update()




