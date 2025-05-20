import flet as ft
from .calculate_recipe_result import RecipeResultCalculator


class RecipeResultUI:
    """
    Builds the UI to show the recipe result using the provided data.
    """

    def __init__(self, page: ft.Page):
        """
        Sets up the result UI.

        Args:
            page (ft.Page): The Flet page to update.
        """
        self.page = page
        self.table = ft.Column()
        self.message = ft.Text(value="", size=14, color="red")

    def show_recipe(self, result: dict[str, dict[str, float]]):
        """
        Displays the recipe result in a table.

        Args:
            result (dict): Final recipe data.
        """
        self.message.value = "✅ Recipe created successfully!"
        self.message.color = "green"
        self.page.update()
        self.build_result_table(result)

    def show_error(self):
        """
        Displays an error message if generation failed.
        """
        self.message.value = "❌ Could not generate recipe. Please check your inputs."
        self.message.color = "red"
        self.page.update()

    def build_result_table(self, result: dict[str, dict[str, float]]):
        """
        Builds the result table.

        Args:
            result (dict): Recipe output.
        """
        rows = [
            ft.Row(
                [
                    ft.Text("Ingredient", weight=ft.FontWeight.BOLD, width=200, color="#4d4d4d"),
                    ft.Text("% Amount", weight=ft.FontWeight.BOLD, width=100, color="#4d4d4d"),
                    ft.Text("± Variation", weight=ft.FontWeight.BOLD, width=120, color="#4d4d4d"),
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        ]

        for name, data in result.items():
            rows.append(
                ft.Row(
                    [
                        ft.Text(name, width=200, color="#666666"),
                        ft.Text(f"{data['mean']}%", width=100, color="#666666"),
                        ft.Text(f"±{data['variation']}%", width=120, color="#666666"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
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
                        "Generated Recipe", size=26, weight=ft.FontWeight.BOLD, color="#1A3E3E"
                    ),
                    self.message,
                    self.table,
                ],
                spacing=10,
            ),
            padding=20,
            width=600,
            bgcolor="#FAFAFA",
            border_radius=10,
        )
        

    @staticmethod
    def generate_and_display_recipe(
        page: ft.Page, ingredient_input: dict[str, float | None]
    ):
        """
        Handles the full process: generates a recipe and displays the results on the page.

        Args:
            page (ft.Page): The current Flet page instance.
            ingredient_input (dict): A dictionary with ingredient names as keys and
                                    either fixed percentages or None as values.
        """
        # Step 1: Set up the calculator and UI
        recipe_calculator = RecipeResultCalculator()
        result_ui = RecipeResultUI(page)

        # Step 2: Try generating the recipe
        success = recipe_calculator.calculate_recipe(ingredient_input)

        # Step 3: Show result or error message
        if success:
            recipe_data = recipe_calculator.get_recipe_result()
            result_ui.show_recipe(recipe_data)
        else:
            result_ui.show_error()

        # Step 4: Add the result section to the page
        page.controls.append(result_ui.build_result_section())
        page.update()
