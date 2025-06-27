import flet as ft
from frontend_.src.add_product_table.table_ui.ingredient_manager import IngredientManager
from frontend_.src.add_product_table.logic.input_validator import InputValidator
from frontend_.src.add_product_table.logic.data_builder import IngredientDataBuilder
from frontend_.src.product_submit_handler import ProductSubmitHandler
from frontend_.src.styles import Styles
from frontend_.src.product_action_handler import ProductActionHandler
from frontend_.src.add_product_table.table_ui.autofill_confirmation_window import AutofillConfirmationWindow
from backend_.data_base_manager.product_manager import ProductManager


class ProductTableUI:
    """
    Builds the UI of a table to create a product with ingredients.

    Includes:
    - An input field for the product name
    - Buttons to search and create a product
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
        self.result_text = ft.Text(value="", color=Styles.GREEN_COLOR, size=12, weight=ft.FontWeight.BOLD)

        self.instruction_container = self.build_instruction_text()

        style = Styles.input_style()

        self.product_name = ft.TextField(
            label="Product Name",
            hint_text="e.g. Fruit Yogurt",
            width=400,
            **style
        )

        self.ingredient_manager = IngredientManager(
            self.ingredient_rows,
            self.product_name,
            self.page 
        )

        self.feedback = ft.Text(value="", color=Styles.RED_COLOR, size=12, weight=ft.FontWeight.BOLD)

        self.autofill_dialog_handler = AutofillConfirmationWindow(
            self.page,
            on_confirm = ProductActionHandler.handle_search_and_fill(
            self.product_name,
            self.feedback,
            self.page,
            self.ingredient_manager
        )
        )
        
    def on_find_product_click(self, e):
        """
        Handles the find Product button click by calling ProductCreator.
        """
        found = ProductActionHandler.check_if_product_exists(
            self.product_name,
            self.feedback,
            self.page,
        )
        if found:
           dialog = AutofillConfirmationWindow(
            self.page,
            on_confirm=lambda: ProductActionHandler.handle_search_and_fill(
                self.product_name,
                self.feedback,
                self.page,
                self.ingredient_manager),
            on_cancel=lambda: print("Cancelled.")
            )
           dialog.show_dialog()
    
    def on_create_product_click(self, e):
        """
        Handles the find Product button click by calling ProductCreator.
        """
        return ProductActionHandler.handle_create_product(
            self.product_name,
            self.feedback,
            self.page,
        )

    def on_add_click(self):
        """
        Handles the Add Ingredient button click.

        Adds a new ingredient row to the table.
        """
        self.ingredient_manager.add_ingredient_row(self.page)

    def on_clearall_click(self):
        """
        Handles the Clear All button click.

        Clears all ingredient rows from the table and resets the product name.
        """
        self.ingredient_manager.clear_all()

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


    def build_name_input(self):
        """
        Creates the product name input section with a Find button.

        Returns:
            ft.Container: A container with label, input field, and find button.
        """
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        Styles.build_subtitle(
                            "Enter product name"
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.product_name,
                                Styles.primary_button(
                                    text="Search",
                                    on_click=self.on_find_product_click,
                                    icon=ft.Icons.SEARCH,
                                ),
                                Styles.primary_button(
                                    text="Create",
                                    on_click=self.on_create_product_click,
                                    icon=ft.Icons.CREATE,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=self.result_text,
                        alignment=ft.alignment.center,
                        padding=5,
                    )
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
                    Styles.build_explanation(
                        "List the ingredients from most to least used.",
                    ),
                    Styles.build_explanation(
                        "Only include a percentage if known; otherwise, leave it blank or use 0%."
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
    
    def toggle_instruction(self, e: ft.ControlEvent):
        """
        Toggles the visibility of the instruction text.
        Args:
            e (ft.ControlEvent): The event triggered by the button click.
        """
        container = self.instruction_container  
        container.visible = not container.visible
        e.control.text = "Hide Instructions" if container.visible else "Show Instructions"
        self.page.update()


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
                        ft.Text("Ingredient", weight=ft.FontWeight.BOLD, size=18, color=Styles.TABLE_HEADER_FONT_COLOR),
                        width=200,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        ft.Text("Percentage", weight=ft.FontWeight.BOLD, size=18, color=Styles.TABLE_HEADER_FONT_COLOR),
                        width=120,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=40),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            bgcolor=Styles.TABLE_HEADER_COLOR,
            padding=10,
            border_radius=Styles.BORDER_RADIUS,
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
                    Styles.primary_button(
                        "Add Ingredient",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: self.on_add_click(),
                    ),

                    Styles.primary_button(
                        "Submit Product",
                        icon=ft.Icons.ANALYTICS,
                        on_click=lambda e: self.on_submit_click(),
                    ),
                    Styles.primary_button(
                        "Clear All",
                        icon=ft.Icons.CLEAR,
                        on_click=lambda e: (self.on_clearall_click(), self.on_add_click()),
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
        # Input section stays the same, just wrapped in a container
        input_section = ft.Container(
            content=ft.Column(
                [
                    Styles.build_title("Analyze a product"),
                    self.build_name_input(),
                    Styles.primary_button("Show Instructions", on_click=self.toggle_instruction, icon=ft.Icons.INFO), 
                    self.instruction_container,
                    self.build_table_header(),
                    self.ingredient_rows,
                    self.feedback,
                    self.build_table_buttons(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=700,  
        )

        # Container for results that will be filled later
        # In ProductTableUI.__init__, create a placeholder
        self.results_section = ft.Container(
            content=ft.Column(
                [
                    Styles.build_title("Generated Recipe"),
                    ft.Text("Recipe will appear here after analysis...", 
                        color=Styles.TEXT_COLOR, italic=True),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=700,
            padding=ft.padding.only(top=0, left=20, right=20, bottom=20),
        )

        return ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Container(
                        content=input_section,
                        col={"sm": 12, "md": 6, "lg": 6},  # Full width on small, half on medium+
                    ),
                    ft.Container(
                        content=self.results_section,
                        col={"sm": 12, "md": 6, "lg": 6},  # Full width on small, half on medium+
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            expand=True,
            alignment=ft.alignment.top_left,
            padding=20,
            bgcolor=Styles.BACKGROUND_COLOR,
        )
    
    
