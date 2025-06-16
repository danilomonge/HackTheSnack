import flet as ft
from .calculate_recipe_result import RecipeResultCalculator
from styles import Styles


class RecipeResultUI:
    """
    Builds the UI to show the recipe result using the provided data.
    """

    # Static variable to keep track of the current result container
    _current_result_container = None

    def __init__(self, page: ft.Page):
        """
        Sets up the result UI.

        Args:
            page (ft.Page): The Flet page to update.
        """
        self.page = page
        self.table = ft.Column()
        self.message = ft.Text(value="", size=Styles.FEEDBACK_FONT_SIZE, color=Styles.RED_COLOR)

    def show_recipe(self, result: dict[str, dict[str, float]]):
        """
        Displays the recipe result in a table.

        Args:
            result (dict): Final recipe data.
        """
        self.message.value = "✅ Recipe created successfully!"
        self.message.color = Styles.GREEN_COLOR
        self.message.weight = ft.FontWeight.BOLD
        self.page.update()
        self.build_result_table(result)

    def show_error(self):
        """
        Displays an error message if generation failed.
        """
        self.message.value = "❌ Could not generate recipe. Please check your inputs."
        self.message.color = Styles.RED_COLOR
        self.page.update()
    
    def build_result_text(self) -> ft.Container:
        """
        Creates a short note explaining the mean and std.

        Returns:
            ft.Container: Instructional text in a styled container.
        """
        return ft.Container(
            content = ft.Column(
                [
                    ft.Text(
                        "Explanation of your results: \n"
                        "The amount shows the average percentage that each ingredient in your recipe has. \n "
                        "The variation shows you how much the percentage might vary.\n",
                        size= Styles.EXPLANATION_FONT_SIZE,
                        color=Styles.EXPLANATION_FONT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(vertical=6, horizontal=10),
            bgcolor=Styles.BOX_COLOR,
            )

    def build_result_table(self, result: dict[str, dict[str, float]]):
        """
        Builds the result table.

        Args:
            result (dict): Recipe output.
        """
        rows = [
            ft.Row(
                [
                    ft.Text("Ingredient", weight=ft.FontWeight.BOLD, width=200, color=Styles.TEXT_COLOR),
                    ft.Text("% Amount", weight=ft.FontWeight.BOLD, width=100, color=Styles.TEXT_COLOR),
                    ft.Text("± Variation", weight=ft.FontWeight.BOLD, width=120, color=Styles.TEXT_COLOR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]

        for name, data in result.items():
            rows.append(
                ft.Row(
                    [
                        ft.Text(name, width=200, color=Styles.TEXT_COLOR),
                        ft.Text(f"{data['mean']}%", width=100, color=Styles.TEXT_COLOR),
                        ft.Text(f"±{data['variation']}%", width=120, color=Styles.TEXT_COLOR),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        self.table.controls.clear()
        self.table.controls.extend(rows)
        self.page.update()


    def build_result_section(self) -> ft.Container:
        """
        Creates the UI container with result title, message and table.

        Returns:
            ft.Container: Container with result data.
        """
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Generated Recipe", size=Styles.TITLE_SIZE, weight=ft.FontWeight.BOLD, color=Styles.TEXT_COLOR
                    ),
                    self.message,
                    self.build_result_text(),
                    self.table,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            width=1000,
            bgcolor=Styles.TABLE_ROW_COLOR,
            border_radius=Styles.BORDER_RADIUS,
        )
    
    @staticmethod
    def generate_and_display_recipe(
        page: ft.Page, ingredient_input: dict[str, float | None]
    ):
        """
        Generates a recipe and displays it in the current view.

        Args:
            page (ft.Page): The current Flet page instance.
            ingredient_input (dict): Ingredient names and their percentages.
        """
        # Get the generator view column that contains the UI
        generator_view = next(
            (view for view in page.views if view.route == "/generator"),
            None
        )
        
        if generator_view and len(generator_view.controls) > 1:
        # Safely access the column that contains our content
            column = generator_view.controls[1]
            if isinstance(column, ft.Column) and hasattr(column, 'controls'):
                # Remove old result if exists
                if RecipeResultUI._current_result_container:
                    try:
                        column.controls.remove(RecipeResultUI._current_result_container)
                    except ValueError:
                        pass

                # Generate new result
                recipe_calculator = RecipeResultCalculator()
                result_ui = RecipeResultUI(page)
                
                if recipe_calculator.calculate_recipe(ingredient_input):
                    recipe_data = recipe_calculator.get_recipe_result()
                    result_ui.show_recipe(recipe_data) # type: ignore
                else:
                    result_ui.show_error()

                # Add new result to view
                result_container = result_ui.build_result_section()
                column.controls.append(result_container)

                RecipeResultUI._current_result_container = result_container
                page.update()