from Frontend.src.add_product_table.table_ui.ingredient_manager  import IngredientManager


class DataFiller:
    """
    
    """

    @staticmethod
    def fill_rows_from_data(
        ingredient_data: dict[str, float],
        ingredient_manager: "IngredientManager"
    ) -> None:
        """
        Recibe un diccionario con ingredientes y porcentajes, y llena los renglones en la UI.

        Args:
            ingredient_data (dict[str, float]): Diccionario con nombre y porcentaje de ingredientes.
            ingredient_manager (IngredientManager): Instancia del administrador de ingredientes.
        """
        style = ingredient_manager.input_style()

        for name, percentage in ingredient_data.items():
            last_valid = [f"{percentage:.2f}"]

            name_input = ingredient_manager.name_input(style)
            name_input.value = name

            percent_input = ingredient_manager.percent_input(style, last_valid, ingredient_manager.page)
            percent_input.value = f"{percentage:.2f}"

            percent_section = ingredient_manager.percent_section(percent_input)

            # Row creation
            row = ingredient_manager.ingredient_row(
                name_input, percent_section,
                lambda r=None: ingredient_manager.remove_ingredient_row(row)
            )

            ingredient_manager.ingredients.append(row)
            ingredient_manager.quantity_table.controls.append(row)

        ingredient_manager.quantity_table.update()




