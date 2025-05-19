import flet as ft
from add_product_table.table_ui.ingredient_manager import IngredientManager
from add_product_table.logic.input_validator import InputValidator
from add_product_table.logic.data_builder import IngredientDataBuilder
from product_submit_handler import ProductSubmitHandler


class ProductTableUI:
    """
    Builds the UI of a table to create a product with ingredients.

    Includes:
    - An input field for the product name
    - A list of ingredient rows (each with name and percentage)
    - Buttons to add ingredients and submit the product
    - Validation and feedback display
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the product table UI.

        Args:
            page (ft.Page): The Flet page used to build and update the UI.
        """
        self.page = page
        self.ingredient_rows = ft.Column()
        self.ingredient_manager = IngredientManager(self.ingredient_rows)

        self.product_name = ft.TextField(
            label="Product Name",
            hint_text="e.g. Fruit Yogurt",
            width=400,
            filled=True,
            bgcolor="#E8F5E9",
            border_color="#1A3E3E",
            color="black",
        )

        self.feedback = ft.Text(value="", color="red", size=12, weight="bold")

    def on_add_click(self):
        """
        Handles the Add Ingredient button click.

        Adds a new ingredient row to the table.
        """
        self.ingredient_manager.add_ingredient_row(self.page)

    def on_submit_click(self):
        """
        Handles the Submit Product button click.

        Delegates validation, feedback and recipe generation to ProductSubmitHandler.
        """
        return ProductSubmitHandler.handle_submit(
            self.product_name,
            self.ingredient_manager.ingredients,
            self.feedback,
            self.page,
        )

    def build_title(self):
        """
        Creates the main title of the page.

        Returns:
            ft.Container: A container with the title text.
        """
        return ft.Container(
            ft.Text(
                "Analyze a product",
                size=34,
                weight="bold",
                color="#1A3E3E",
                text_align="center",
            ),
            alignment=ft.alignment.center,
            padding=10,
        )

    def build_name_input(self):
        """
        Creates the product name input section.

        Returns:
            ft.Container: A container with label and input field.
        """
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        ft.Text(
                            "Enter product name",
                            weight="bold",
                            size=23,
                            color="#1A3E3E",
                            text_align="center",
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=self.product_name, alignment=ft.alignment.center
                    ),
                ],
                spacing=5,
            ),
            padding=10,
        )

    def build_instruction_text(self) -> ft.Container:
        """
        Creates a short note explaining how to fill the ingredient form.

        Returns:
            ft.Container: Instructional text in a styled container.
        """
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "List the ingredients from most to least used.",
                        size=17,
                        color="#1A3E3E",
                        weight=ft.FontWeight.BOLD,
                        text_align="center",
                    ),
                    ft.Text(
                        "Only include a percentage if known; otherwise, leave it blank or use 0%.",
                        size=15,
                        color="#666666",
                        text_align="center",
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

    def build_table_header(self):
        """
        Builds the header row for the ingredient table.

        Returns:
            ft.Container: A styled header row with column titles.
        """
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        ft.Text("Ingredient", weight="bold", size=18, color="white"),
                        width=200,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        ft.Text("Percentage", weight="bold", size=18, color="white"),
                        width=120,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=40),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            bgcolor="#1A3E3E",
            padding=10,
            border_radius=10,
            margin=5,
        )

    def build_table_buttons(self):
        """
        Builds the buttons below the table (Add Ingredient, Submit Product).

        Returns:
            ft.Container: A row with the two main action buttons.
        """
        return ft.Container(
            content=ft.Row(
                [
                    ft.ElevatedButton(
                        "Add Ingredient",
                        icon=ft.icons.ADD,
                        on_click=lambda e: self.on_add_click(),
                        bgcolor="#1A3E3E",
                        color="white",
                        width=200,
                    ),
                    ft.ElevatedButton(
                        "Submit Product",
                        icon=ft.icons.ANALYTICS,
                        on_click=lambda e: self.on_submit_click(),
                        bgcolor="#1A3E3E",
                        color="white",
                        width=200,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=10,
        )

    def build_table_ui(self):
        """
        Builds the full product table interface with title, inputs, and buttons.

        Returns:
            ft.Container: The complete UI layout ready to be added to the page.
        """
        return ft.Container(
            content=ft.Column(
                [
                    self.build_title(),
                    self.build_name_input(),
                    self.build_table_header(),
                    self.build_instruction_text(),
                    self.ingredient_rows,
                    self.feedback,
                    self.build_table_buttons(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=1000,
            padding=20,
            bgcolor="#FFFFFF",
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 0),
            ),
        )
