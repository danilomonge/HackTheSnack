import flet as ft
import random
from backend.translation import Translation
from styles import Styles


class RecipesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.recipe_titles = {}
        self.recipe_images = ["recipe_img.png"]
        self.recipe_overlay = None
        self.search_text = ""

        self.recipes_row = ft.Row(
            controls=[],
            wrap=True, 
            spacing=20,  
            width=660,
        )
        self.recipes_container = ft.Column(
            controls=[self.recipes_row],
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
        )

    def load_recipes(self):
        """Load recipes from backend"""
        self.recipe_titles = Translation.collect_product_dict()
        self.filtered_titles = list(self.recipe_titles.keys())
        self.update_recipe_containers()

    def filter_recipes(self, query):
        """
        Filter recipes based on the search query.
        Args:
            query (str): The search query string.
        """
        self.search_text = query
        query_lower = query.lower()
        self.filtered_titles = [
            title for title in self.recipe_titles
            if query_lower in title.lower()
        ]
        self.update_recipe_containers()

    def get_recipe_title_by_id(self, recipe_id):
        """
        Get the recipe title by its ID.
        """
        for title, id_val in self.recipe_titles.items():
            if id_val == recipe_id:
                return title
        return f"Rezept #{recipe_id}"

    def close_overlay(self, e=None):
        """
        Close the recipe overlay if it is open.
        Args:
            e: Optional event parameter.
        """
        if self.recipe_overlay:
            try:
                self.recipe_overlay.open = False
                self.page.update()
            except Exception as ex:
                print(f"Fehler beim Schließen: {ex}")

    def update_recipe_containers(self):
        """Update the recipe containers based on the filtered titles"""
        if not self.filtered_titles:
            self.recipes_row.controls.clear()
            self.recipes_row.controls.append(
                ft.Text(
                    "No recipes found.",
                    size=16,
                    color=Styles.TEXT_COLOR,
                    weight=ft.FontWeight.BOLD
                )
            )
            self.page.update()
            return
        self.recipes_row.controls.clear()
        
        for title in self.filtered_titles:
            container = ft.GestureDetector(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=random.choice(self.recipe_images),
                                fit=ft.ImageFit.COVER,
                            ),
                            ft.Text(
                                title, 
                                size=18, 
                                weight=ft.FontWeight.BOLD, 
                                color=Styles.TEXT_COLOR,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=Styles.RECIPE_CONTAINER_COLOR,
                    border_radius=Styles.BORDER_RADIUS,
                    padding=10,
                    margin=5,
                    width=190,
                    height=180,
                ),
                on_tap=self.create_recipe_handler(title)
            )
            self.recipes_row.controls.append(container)
        self.page.update()
    

    def create_ingredients_list(self, recipe_data):
        """
        Creates a list of ingredient controls for the recipe overlay.
        Args:
            recipe_data (dict): The recipe data containing ingredient statistics.
        Returns:
            list[ft.Container]: A list of Flet Container controls for each ingredient.
        """
        if not recipe_data:
            return [
                ft.Container(
                    content=ft.Text(
                        "⚠️ This recipe doesn't have any ingredients.",
                        size=16,
                        color=Styles.TEXT_COLOR,
                        weight=ft.FontWeight.BOLD
                    ),
                    padding=20,
                    bgcolor=Styles.RECIPE_CONTAINER_COLOR,
                    border_radius=Styles.BORDER_RADIUS,
                    alignment=ft.alignment.center
                )
            ]

        ingredients_controls = []
        for ingredient, data in recipe_data.items():
            mean_amount = data["mean"]
            variation = data.get("variation", 0)

            amount_text = f"{mean_amount}g"
            if variation > 0:
                amount_text += f" (±{variation}g)"

            ingredients_controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                ingredient,
                                size=16,
                                color=Styles.TEXT_COLOR,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                amount_text,
                                size=16,
                                color=Styles.TEXT_COLOR
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=ft.padding.symmetric(vertical=5, horizontal=10),
                    bgcolor=Styles.RECIPE_CONTAINER_COLOR,
                    margin=ft.margin.only(bottom=5),
                    border_radius=Styles.BORDER_RADIUS
                )
            )
        return ingredients_controls


    def create_version_selector(self, recipe_id, sorted_versions, selected_version):
        """        
        Creates a version selector for the recipe overlay.
        Args:
            recipe_id (str): The ID of the recipe.
            sorted_versions (list): A list of version dates.
            selected_version (str): The currently selected version date.
        """
        if len(sorted_versions) <= 1:
            return None

        version_buttons = []

        for version_date in sorted_versions:
            is_selected = version_date == selected_version

            def make_click_handler(version=version_date):
                def handler(e):
                    self.open_recipe_overlay(recipe_id, version)
                return handler

            version_buttons.append(
                ft.Container(
                    content=ft.Text(
                        version_date,
                        size=12,
                        color=Styles.TEXT_COLOR if not is_selected else Styles.BOX_COLOR,
                        weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL
                    ),
                    bgcolor=Styles.RECIPE_CONTAINER_COLOR if not is_selected else Styles.TEXT_COLOR,
                    border_radius=Styles.BORDER_RADIUS,
                    padding=ft.padding.symmetric(vertical=5, horizontal=10),
                    margin=ft.margin.only(bottom=5),
                    on_click=make_click_handler()
                )
            )

        return ft.Column(
            controls=[
                ft.Text("Versions:", size=16, weight=ft.FontWeight.BOLD, color=Styles.TEXT_COLOR),
                ft.Column(controls=version_buttons, spacing=2, scroll=ft.ScrollMode.AUTO)
            ],
            spacing=10
        )

    def build_overlay_content(self, recipe_title, ingredients_controls, version_selector):
        """
        Builds the content for the recipe overlay.
        Args:
            recipe_title (str): The title of the recipe.
            ingredients_controls (list): List of ingredient controls.
            version_selector (ft.Column): The version selector control. 
        Returns:
            ft.Container: The complete overlay content as a Flet Container.
        """

        main_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Ingredients:", size=20, weight=ft.FontWeight.BOLD, color=Styles.TEXT_COLOR),
                    ft.Text("Per 100g:", size=16, weight=ft.FontWeight.BOLD, color=Styles.TEXT_COLOR),
                    ft.Container(
                        content=ft.Column(
                            controls=ingredients_controls,
                            spacing=2,
                            scroll=ft.ScrollMode.ALWAYS
                        ),
                        height=370
                    )
                ],
                spacing=15,
            ),
            padding=20,
            expand=True
        )

        if version_selector:
            recipe_content = ft.Row(
                controls=[
                    version_selector,
                    ft.Container(width=1, bgcolor=Styles.TEXT_COLOR, height=500),
                    main_content
                ],
                spacing=10,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        else:
            recipe_content = main_content

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(recipe_title, size=24, weight=ft.FontWeight.BOLD, color=Styles.TEXT_COLOR),
                            Styles.icon_button(
                                icon=ft.Icons.CLOSE,
                                on_click=self.close_overlay,
                                color=Styles.TEXT_COLOR
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    recipe_content
                ],
                spacing=20
            ),
            bgcolor=Styles.BOX_COLOR,
            border_radius=25,
            padding=30,
            width=750, 
            height=600
        )

    def open_recipe_overlay(self, recipe_id, selected_version=None):
        """
        Opens the recipe overlay for a given recipe ID and version.
        Args:
            recipe_id (int): The ID of the recipe to open.
            selected_version (str, optional): The version date to select. Defaults to None.
        """
        recipe_title = self.get_recipe_title_by_id(recipe_id)
        versions_data = Translation.get_all_evaluations(recipe_id) or {}

        sorted_versions = sorted(versions_data.keys(), reverse=True)
        if not sorted_versions:
            recipe_data = Translation.get_last_evaluation(recipe_id)
            version_selector = None
        else:
            if not selected_version or selected_version not in versions_data:
                selected_version = sorted_versions[0]
            recipe_data = versions_data[selected_version]
            version_selector = self.create_version_selector(recipe_id, sorted_versions, selected_version)

        ingredients_controls = self.create_ingredients_list(recipe_data)
        overlay_content = self.build_overlay_content(recipe_title, ingredients_controls, version_selector)

        if self.recipe_overlay:
            self.close_overlay()

        self.recipe_overlay = ft.AlertDialog(
            modal=True,
            content=overlay_content,
            bgcolor=Styles.BOX_COLOR,
            content_padding=0
        )

        self.page.overlay.append(self.recipe_overlay)
        self.recipe_overlay.open = True
        self.page.update()

    def create_recipe_handler(self, title):
        """ 
        Creates a handler for recipe click events.
        Args:   
            title (str): The title of the recipe.
        Returns:
            function: The event handler function.
        """
        def handler(e):
            recipe_id = self.recipe_titles.get(title)
            if recipe_id:
                self.open_recipe_overlay(recipe_id)
            else:
                print(f"Keine ID für Rezept '{title}' gefunden")
        return handler

    def build(self):
        """
        Builds the main content for the RecipesView.
        Returns:
            ft.Container: The main container for the RecipesView.
        """
        self.load_recipes()

        search_field = ft.TextField(
            label="Search recipes",
            value=self.search_text,
            on_change=lambda e: self.filter_recipes(e.control.value),
            width=300,
            bgcolor=Styles.INPUT_FILL_COLOR,
            border_radius=Styles.BORDER_RADIUS,
            color=Styles.TEXT_COLOR,
            border_color=Styles.INPUT_BORDER_COLOR,
            label_style=ft.TextStyle(color=Styles.TEXT_COLOR),
            cursor_color=Styles.TEXT_COLOR
        )

        if not self.recipes_container.controls:
            self.update_recipe_containers()

        column_content = ft.Column(
            controls=[
                Styles.build_title("Your Recipes"),
                search_field,
                ft.Container(
                    content=Styles.build_explanation(
                        "Here you can find all your saved recipes. \n"
                        "Click on a recipe to view its details and ingredients."
                    ),
                    padding=10,
                    bgcolor=Styles.BOX_COLOR,
                    border_radius=Styles.BORDER_RADIUS,
                    alignment=ft.alignment.center,
                    width=650,
                ),
                self.recipes_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        return ft.Container(
            content=column_content,
            bgcolor=Styles.BACKGROUND_COLOR,
            expand=True,
        )
