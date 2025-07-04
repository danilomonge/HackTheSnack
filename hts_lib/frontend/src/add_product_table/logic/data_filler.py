from FakeTheSnack.hts_lib.frontend.src.add_product_table.table_ui.ingredient_row_manager  import IngredientRowManager


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
        ingredient_manager: "IngredientRowManager"
    ) -> None:
        """
        Receive a dictionary with ingredients and percentages, and fill in the lines in the UI.

        Args:
            ingredient_data (dict[str, float]): Dictionary with name and percentage of ingredients.
            ingredient_manager (IngredientRowManager): Instance of the ingredient manager.
        """

        ingredient_manager.clear_ingredient_rows()
    
        for name, percentage in ingredient_data.items():
            # Add a new ingredient row 
            ingredient_manager.add_ingredient_row(ingredient_manager.page)

            # Get the most recent (last added) row
            row = ingredient_manager.ingredients[-1]

            # Extract inputs from the structured row
            name_input = row.content.controls[0].content
            percent_input = row.content.controls[1].content.controls[1]  # Middle element in percent_section

            # Fill values
            name_input.value = name
            percent_input.value = ""  #f"{percentage:.2f}"
        
        ingredient_manager.quantity_table.update()



