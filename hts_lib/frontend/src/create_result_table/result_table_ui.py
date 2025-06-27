import flet as ft
from frontend.src.styles import Styles


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

        self.toggle_button = Styles.primary_button(
            "Show Explanation",
            icon=ft.Icons.INFO,
            on_click=self.toggle_explanation
        )

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
                        "Explanation of your results: \n"
                        "The amount shows the average percentage that each ingredient in your recipe has. \n "
                        "The variation shows you how much the percentage might vary.\n",
                    ),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(vertical=6, horizontal=10),
            bgcolor=Styles.BOX_COLOR,
            visible=False,
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
        rows = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Ingredient", weight=ft.FontWeight.BOLD, width=200, color=Styles.TEXT_COLOR),
                        ft.Text("% Amount", weight=ft.FontWeight.BOLD, width=100, color=Styles.TEXT_COLOR),
                        ft.Text("± Variation", weight=ft.FontWeight.BOLD, width=120, color=Styles.TEXT_COLOR),
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
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(name, width=200, color=Styles.TEXT_COLOR),
                            ft.Text(f"{data['mean']}%", width=100, color=Styles.TEXT_COLOR),
                            ft.Text(f"±{data['variation']}%", width=120, color=Styles.TEXT_COLOR),
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
