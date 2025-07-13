import flet as ft
from frontend.src.styles import Styles
from frontend.src.handle_nutritional_info import NutritionalInfoHandler


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
        
        self.explanation_visible = False

        self.result_text_container = self.build_result_text()
        self.result_text_container.visible = False  

        self.toggle_button = Styles.build_button(
            "Show Explanation",
            icon=ft.Icons.INFO,
            on_click=self.toggle_explanation
        )
        self.ingredient_rows: list[tuple[ft.Container, ft.Container, ft.Container]] = []
        self.nutrition_handler = NutritionalInfoHandler(page)

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
                    Styles.build_explanation(
                        "💬 Explanation of your results:"
                    ),
                    Styles.build_explanation(
                        "• Amount: shows the average percentage that each ingredient in your recipe has."
                    ),
                    Styles.build_explanation(
                        "• Variation: shows you how much the percentage might vary."
                    ),
                    Styles.build_explanation(
                        "• Nutrition facts: gives the standard nutritional info of the selected ingredient."
                    ),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(vertical=6, horizontal=10),
            bgcolor=Styles.BOX_COLOR,
            visible=False,
            )
    
    def make_icon_button(self, ingredient_name, amount):
        return ft.IconButton(
            icon="search",
            tooltip="View nutrition info",
            on_click=lambda e: self.nutrition_handler.show_nutritional_info(ingredient_name, amount)
        )

    def toggle_explanation(self, e):
        """
        Toggles the visibility of the explanation text.
        Args:
            e (ft.ControlEvent): The event triggered by the button click.
        """
        container = self.result_text_container 
        container.visible = not container.visible
        e.control.text = "Hide Explanation" if container.visible else "Show Explanation"
        self.page.update()

    def build_result_table(self, result: dict[str, dict[str, float]]):
        """
        Builds the result table.

        Args:
            result (dict): Recipe output.
        """
        
        col_widths = {
        "ingredient": 160,
        "amount": 130,
        "variation": 130,
        "actions": 130,
        }
        
        rows = [
            ft.Container(
                content=ft.Row(
                    [
                    ft.Container(
                        content=ft.Text("Ingredient", weight=ft.FontWeight.BOLD, color="#4d4d4d"),
                        width=col_widths["ingredient"],
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Text("% Amount", weight=ft.FontWeight.BOLD, color="#4d4d4d"),
                        width=col_widths["amount"],
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Text("± Variation", weight=ft.FontWeight.BOLD, color="#4d4d4d"),
                        width=col_widths["variation"],
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Text("Nutrition Facts", weight=ft.FontWeight.BOLD, color="#4d4d4d"),
                        width=col_widths["actions"],
                        alignment=ft.alignment.center,
                    ),
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor=Styles.TABLE_HEADER_COLOR,
                padding=10,
                border_radius=Styles.BORDER_RADIUS,
                margin=5,
            )
        ]

        for i, (name, data) in enumerate(result.items()):
            ingredient_text = ft.Container(
                content=ft.Text(name, color="#666666"),
                width=col_widths["ingredient"],
                alignment=ft.alignment.center,
            )
            amount_text = ft.Container(
                content=ft.Text(f"{data['mean']}%", color="#666666"),
                width=col_widths["amount"],
                alignment=ft.alignment.center,
            )
            variation_text = ft.Container(
                content=ft.Text(f"±{data['variation']}%", color="#666666"),
                width=col_widths["variation"],
                alignment=ft.alignment.center,
            )
            icon_button = ft.Container(
                content=self.make_icon_button(name, data['mean']),
                width=col_widths["actions"],
                alignment=ft.alignment.center,
            )

            self.ingredient_rows.append((ingredient_text, amount_text, variation_text))
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                        ingredient_text,
                        amount_text,
                        variation_text,
                        icon_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    bgcolor=Styles.TABLE_ROW_COLOR,
                    padding=10,
                    border_radius=Styles.BORDER_RADIUS,
                    margin=5,
                )
            )

        self.table.controls.clear()
        self.table.controls.extend(rows)
        self.page.update()

    @staticmethod
    def clear_current_result(page: ft.Page):
        """
        Clears the current recipe result and resets the display to default state.
        
        Args:
            page (ft.Page): The Flet page instance.
        """
        if RecipeResultUI._current_result_container:
            # Find the results section container and clear it
            generator_view = next(
                (view for view in page.views if view.route == "/generator"),
                None
            )
            
            if generator_view and len(generator_view.controls) > 1:
                main_column = generator_view.controls[1]
                if isinstance(main_column, ft.Column):
                    container = main_column.controls[0]
                    if isinstance(container, ft.Container):
                        responsive_row = container.content
                        if isinstance(responsive_row, ft.ResponsiveRow):
                            if len(responsive_row.controls) >= 2:
                                results_container_wrapper = responsive_row.controls[1]
                                if isinstance(results_container_wrapper, ft.Container):
                                    # Reset the results section to default state
                                    results_container_wrapper.content = ft.Column(
                                        [
                                            Styles.build_title("Generated Recipe"),
                                            ft.Text("Recipe will appear here after analysis...", 
                                                color=Styles.TEXT_COLOR, italic=True),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=10,
                                    )
                                    
            # Reset the static variable
            RecipeResultUI._current_result_container = None
            page.update()


    def build_result_section(self) -> ft.Container:
        """
        Creates the UI container with result title, message and table.

        Returns:
            ft.Container: Container with result data.
        """
        return ft.Container(
            content=ft.Column(
                [
                    Styles.build_title("Generated Recipe"),
                    self.message,
                    self.toggle_button,
                    self.result_text_container,
                    self.table,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            padding=ft.padding.only(top=0, left=20, right=20, bottom=20),
            width=400,
            bgcolor=Styles.BACKGROUND_COLOR,
            border_radius=Styles.BORDER_RADIUS,
            expand=True,
        )

    @staticmethod
    def display_recipe_result(page: ft.Page, recipe_data: dict[str, dict[str, float]] | None
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
                main_column = generator_view.controls[1]
                if isinstance(main_column, ft.Column):
                    container = main_column.controls[0]
                    if isinstance(container, ft.Container):
                        responsive_row = container.content
                        if isinstance(responsive_row, ft.ResponsiveRow):
                            # Get the second container (results section) from ResponsiveRow
                            if len(responsive_row.controls) >= 2:
                                results_container_wrapper = responsive_row.controls[1]
                                if isinstance(results_container_wrapper, ft.Container):

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
                                    else: result_ui.show_error()

                                    # Step 4: Add to page and update
                                    result_container = result_ui.build_result_section()
                                    results_container_wrapper.content = result_container
                                    RecipeResultUI._current_result_container = result_container #type: ignore
                                    page.update()
