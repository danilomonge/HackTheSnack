import flet as ft
from backend.data_base_manager.product_manager import ProductManager
from frontend.src.add_product_table.table_ui.ingredient_row_manager import IngredientRowManager
from frontend.src.product_submit_handler import ProductSubmitHandler
from frontend.src.styles import Styles
from frontend.src.add_product_table.table_ui.autofill_confirmation_window import AutofillConfirmationWindow


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
        self.is_web = bool(getattr(page, "web", False))
        self.backend_available = False
        self.ingredient_rows = ft.Column()
        self.result_text = ft.Text(value="", color=Styles.GREEN_COLOR, size=12, weight=ft.FontWeight.BOLD)
        self.product_id = 0
        self.ingredient_ids = []
        self.recipe_ids = []
        self.result_dict = dict 
        self.is_submitted = False
        
        self.instruction_container = self.build_instruction_text()

        style = Styles.input_style()

        self.product_name = ft.TextField(
            label="Product Name",
            hint_text="e.g. Fruit Yogurt",
            **style
        )
        self.product_name.on_change = self.on_user_input_change

        self.ingredient_manager = IngredientRowManager(
            self.ingredient_rows,
            self.product_name,
            self.page,
            on_user_input_change = self.on_user_input_change
        )

        self.search_button = Styles.build_button(
                                    text="Search",
                                    on_click=self.on_find_product_click,
                                    icon=ft.Icons.SEARCH,
                                )
        
        self.save_button = Styles.build_button(
            text="Save",
            on_click=self.on_save_recipe_click,
            icon=ft.Icons.CREATE,
        )
        self.save_button.disabled = True

        self.feedback = ft.Text(value="", color=Styles.RED_COLOR, size=12, weight=ft.FontWeight.BOLD)

        self.loading_indicator = ft.ProgressBar(visible=False, color=Styles.LOADINGBAR_COLOR, bgcolor= Styles.LOADINGBAR_BACKGROUNDCOLOR)

        if self.is_web:
            self.result_text.value = (
                "Web mode: recipe generation works locally here, but search/save features need the backend service."
            )
            self.result_text.color = Styles.TEXT_COLOR

        self.refresh_backend_status(update_page=False)
        
    def on_find_product_click(self, e):
        """
        Handles the find Product button click by calling ProductCreator.
        """
        self.refresh_backend_status()
        if not self.backend_available:
            self.feedback.value = self.get_backend_unavailable_message()
            self.feedback.color = Styles.RED_COLOR
            self.page.update()
            return

        from frontend.src.product_action_handler import ProductActionHandler

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
                self.ingredient_manager,
                self.store_submission_results),
            on_cancel=lambda: print("Cancelled.")
            )
           dialog.show_dialog()

    def on_add_click(self):
        """
        Handles the Add Ingredient button click.

        Adds a new ingredient row to the table.
        """
        self.ingredient_manager.add_ingredient_row(self.page)
        self.disable_save_button()


    def on_clearall_click(self):
        """
        Handles the Clear All button click.

        Clears all ingredient rows from the table and resets the product name.
        """
        self.ingredient_manager.clear_all()
        self.disable_save_button()


    def on_submit_click(self):
        """
        Handles the Submit Product button click.

        Delegates validation, feedback and recipe generation to ProductSubmitHandler.
        """
        self.loading_indicator.visible = True
        self.page.update()

        result = ProductSubmitHandler.handle_submit(
            self.product_name,
            self.ingredient_manager.ingredients,
            self.feedback,
            self.page,
            self.store_submission_results,
            self.loading_indicator
        )

        self.loading_indicator.visible = False
        self.page.update()

        if result:  # Only if submit was successful
            self.is_submitted = True
            if not self.is_web:
                self.update_save_button_state(enabled=True)
            else:
                self.update_save_button_state(enabled=False)
            

        return result
    
    def on_save_recipe_click(self, e):
        """
        Handles the save recipe button click action.

        Stores recipe and evaluation information in the database
        """
        self.refresh_backend_status()
        if not self.backend_available:
            self.feedback.value = self.get_backend_unavailable_message()
            self.feedback.color = Styles.RED_COLOR
            self.page.update()
            return None

        from frontend.src.product_action_handler import ProductActionHandler

        self.update_save_button_state(enabled=False)
        delete_ingredients = self.ingredient_manager.deleted_ingredient_ids
        ProductActionHandler.handle_delete_ingredients(self.product_id, delete_ingredients)
        self.ingredient_manager.deleted_ingredient_ids.clear()
        
        return ProductActionHandler.handle_save_new_recipe(self.product_name, 
                                                        self.result_dict, 
                                                        self.store_submission_results)
            
    
    def store_submission_results(self, product_id, ingredient_ids, recipe_ids, result_dict):
        if product_id is not None:
            self.product_id = product_id
        if ingredient_ids is not None:
            self.ingredient_ids = ingredient_ids
        if recipe_ids is not None:
            self.recipe_ids = recipe_ids
        if result_dict is not None:
            self.result_dict = result_dict

    def on_user_input_change(self, e=None): 
        self.is_submitted = False
        self.update_save_button_state(enabled=False)
        self.page.update()
    
    def disable_save_button(self):
        self.is_submitted = False
        self.update_save_button_state(enabled=False)
        self.page.update()

    def get_backend_unavailable_message(self) -> str:
        if self.is_web:
            return "⚠️ Search and save are unavailable in this web version because the backend service is not connected."
        return "⚠️ Search and save are unavailable right now because the database service is offline. Please try again in a moment."

    def refresh_backend_status(self, update_page: bool = True):
        self.backend_available = False if self.is_web else ProductManager.is_backend_available()
        self.update_search_button_state(enabled=self.backend_available)
        self.update_save_button_state(enabled=self.is_submitted and self.backend_available)
        if update_page:
            self.page.update()

    def update_search_button_state(self, enabled: bool):
        self.search_button.disabled = not enabled
        self.search_button.bgcolor = Styles.BUTTON_FILL_COLOR if enabled else Styles.BUTTON_FILL_DISABLED_COLOR
        self.search_button.color = ft.Colors.WHITE if enabled else ft.Colors.GREY_600
        if enabled:
            self.search_button.tooltip = "Click to search product"
        elif self.is_web:
            self.search_button.tooltip = "Search is unavailable in the web build because it needs the backend service"
        else:
            self.search_button.tooltip = "Search is unavailable because the database service is offline"

    def update_save_button_state(self, enabled: bool):
        if not self.backend_available:
            self.save_button.disabled = True
            self.save_button.bgcolor = Styles.BUTTON_FILL_DISABLED_COLOR
            self.save_button.color = ft.Colors.GREY_600
            if self.is_web:
                self.save_button.tooltip = "Save is unavailable in the web build because it needs the backend service"
            else:
                self.save_button.tooltip = "Save is unavailable because the database service is offline"
            return

        self.save_button.disabled = not enabled
        self.save_button.bgcolor = Styles.BUTTON_FILL_COLOR if enabled else Styles.BUTTON_FILL_DISABLED_COLOR
        self.save_button.color = ft.Colors.WHITE if enabled else ft.Colors.GREY_600
        self.save_button.tooltip = "Click to save recipe" if enabled else "Submit first before saving"
        self.page.update()

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
                        Styles.build_subtitle("Enter product name"),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.product_name,
                                self.search_button,
                                self.save_button,
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
                Styles.build_explanation_subtitle("How to fill the ingredient form"),
                ft.Divider(height=6, color="transparent"),
                Styles.build_explanation(
                    "List the ingredients from most to least used. Only include a percentage if known; otherwise, leave it blank or use 0%."
                ),
                Styles.build_explanation(
                    "If there is only one ingredient, it may be 100%. If there are multiple ingredients, each filled value must stay at or below 99.99%."
                ),
                ft.Divider(height=6, color="transparent"),
                Styles.build_explanation(
                    "The total of all ingredients must add up to 100%. Empty ingredient rows must be lower or equal to the value above, and higher or equal to the value below."
                ),
                Styles.build_explanation(
                    "Make sure enough percentage space is left for undefined ingredients so that the final sum is exactly 100%."
                ),
                ft.Divider(height=12, color="transparent"),
                Styles.build_explanation_subtitle("Explanation of errors"),
                ft.Divider(height=6, color="transparent"),
                Styles.build_explanation_subtitle("⚠️ Error 101:"),
                Styles.build_explanation(
                    "There is not enough space left for the empty fields based on the values that follow them. Please lower the values that come after empty fields."
                ),
                ft.Divider(height=4, color="transparent"),
                Styles.build_explanation_subtitle("⚠️ Error 102:"),
                Styles.build_explanation(
                    "The total is already 100%, but there are still empty ingredient values. Please reduce one or more percentages."
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
                        width=210,
                        alignment=ft.alignment.center,
                        padding=5,
                    ),
                    ft.Container(
                        content=ft.Text("Percentage", weight=ft.FontWeight.BOLD, size=18, color=Styles.TABLE_HEADER_FONT_COLOR),
                        width=194,
                        alignment=ft.alignment.center,
                        padding=5,
                    ),
                    ft.Container(width=32),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            width=600,
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
                    Styles.build_button(
                        "Add Ingredient",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: self.on_add_click(),
                    ),

                    Styles.build_button(
                        "Submit Product",
                        icon=ft.Icons.ANALYTICS,
                        on_click=lambda e: self.on_submit_click(),
                    ),
                    Styles.build_button(
                        "Clear All",
                        icon=ft.Icons.CLEAR,
                        on_click=lambda e: (self.on_clearall_click(), self.on_add_click()),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=10,
        )

    def build_table_ui(self):
        """
        Builds the full product table interface with title, inputs, and buttons.

        Returns:
            ft.Container: The complete UI layout ready to be added to the page.
        """

        input_section = ft.Container(
            content=ft.Column(
                [
                    Styles.build_title("Analyze a product"),
                    self.build_name_input(),
                    Styles.build_button("Show Instructions", on_click=self.toggle_instruction, icon=ft.Icons.INFO),
                    self.instruction_container,
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column([
                                    self.build_table_header(),
                                    self.ingredient_rows,
                                ]),
                                width=600,
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    self.feedback,
                    self.build_table_buttons(),
                    ft.Container(
                        content=self.loading_indicator,
                        alignment=ft.alignment.center,
                        padding=10,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
        )
        self.results_section = ft.Container(
            content=ft.Column(
                [
                    Styles.build_title("Generated Recipe"),
                    ft.Row(
                        [
                            ft.ProgressRing(width=16, height=16, stroke_width=2, color=Styles.TEXT_COLOR),
                            ft.Text("Recipe will appear here after analysis...",
                                color=Styles.TEXT_COLOR, italic=True),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                height=850,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.padding.only(top=0, left=20, right=20, bottom=20),
        )

        return ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Container(
                        content=input_section,
                        col={"sm": 12, "md": 12, "lg": 12, "xl":6},
                    ),
                    ft.Container(
                        content=self.results_section,
                        col={"sm": 12, "md": 12, "lg": 12, "xl":6},
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            expand=True,
            alignment=ft.alignment.top_left,
            padding=20,
            bgcolor=Styles.BACKGROUND_COLOR,
        )
