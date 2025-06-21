import flet as ft


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
        self.message = ft.Text(value="", size=14, color="red")

    def show_recipe(self, result: dict[str, dict[str, float]]):
        """
        Displays the recipe result in a table.

        Args:
            result (dict): Final recipe data.
        """
        self.message.value = "✅ Recipe created successfully!"
        self.message.color = "#67CD6B" 
        self.message.weight = ft.FontWeight.BOLD
        self.page.update()
        self.build_result_table(result)

    def show_error(self):
        """
        Displays an error message if generation failed.
        """
        self.message.value = "❌ Could not generate recipe. Please check your inputs."
        self.message.color = "red"
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
                        size=13,
                        color="#1A3E3E",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(vertical=6, horizontal=10),
            bgcolor="#F5F5F5",
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
                    ft.Text("Ingredient", weight=ft.FontWeight.BOLD, width=200, color="#4d4d4d"),
                    ft.Text("% Amount", weight=ft.FontWeight.BOLD, width=100, color="#4d4d4d"),
                    ft.Text("± Variation", weight=ft.FontWeight.BOLD, width=120, color="#4d4d4d"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
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
                        "Generated Recipe", size=26, weight=ft.FontWeight.BOLD, color="#1A3E3E"
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
            bgcolor="#FAFAFA",
            border_radius=10,
        )
        

    @staticmethod
    def display_recipe_result(
        page: ft.Page, recipe_data: dict[str, dict[str, float]] | None
    ):
        """
        Displays the given recipe result on the page.

        Args:
            page (ft.Page): The current Flet page instance.
            recipe_data (dict or None): A dictionary with ingredient names as keys and
                values as {"mean": float, "variation": float}. If None, an error is shown.
        """
        # Step 1: Remove any existing result container
        if RecipeResultUI._current_result_container:
            try:
                page.controls.remove(RecipeResultUI._current_result_container)  # type: ignore
            except ValueError:
                pass

        # Step 2: Set up the UI
        result_ui = RecipeResultUI(page)

        # Step 3: Show result or error
        if recipe_data:
            result_ui.show_recipe(recipe_data)  # type: ignore
        else:
            result_ui.show_error()

        # Step 4: Add to page and update
        result_container = result_ui.build_result_section()
        page.controls.append(result_container)  # type: ignore
        RecipeResultUI._current_result_container = result_container
        page.update()

        