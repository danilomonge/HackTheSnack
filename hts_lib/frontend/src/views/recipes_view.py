import flet as ft
import random
from backend.translation import Translation
from styles import Styles 


class RecipesView:
    def __init__(self, page: ft.Page):
        self.page = page

        self.recipe_titles = {title: idx for idx, title in enumerate(Translation.collect_product_list())}


        self.recipe_images = [
            "recipe_img.png"
        ]

        self.recipe_overlay = None

        # Testing Dict
        self.recipe_data = {
            "Tomato": {
                "mean": 12.5,
                "variation": 1.2
            },
            "Cheese": {
                "mean": 5.0,
                "variation": 0.8
            },
            "Basil": {
                "mean": 0.5,
                "variation": 0.1
            }
        }

        self.recipe_versions = {
            "2025-01-15": {
                "Tomato": {"mean": 12.5, "variation": 1.2},
                "Cheese": {"mean": 5.0, "variation": 0.8},
                "Basil": {"mean": 0.5, "variation": 0.1}
            },
            "2025-01-10": {
                "Tomato": {"mean": 11.0, "variation": 1.0},
                "Cheese": {"mean": 4.5, "variation": 0.6},
                "Basil": {"mean": 0.4, "variation": 0.1}
            },
            "2024-01-05": {
                "Tomato": {"mean": 13.0, "variation": 1.5},
                "Cheese": {"mean": 5.5, "variation": 1.0},
                "Basil": {"mean": 0.6, "variation": 0.2},
                "Tomatos": {"mean": 13.0, "variation": 1.5},
                "Tomatooo": {"mean": 13.0, "variation": 1.5},
                "Cheeeese": {"mean": 5.5, "variation": 1.0},
                "Baesil": {"mean": 0.6, "variation": 0.2},
                "Tomeatos": {"mean": 13.0, "variation": 1.5},
                "Tomaeto": {"mean": 13.0, "variation": 1.5},
                "Cheeese": {"mean": 5.5, "variation": 1.0},
                "Basiel": {"mean": 0.6, "variation": 0.2},
                "Tomatoes": {"mean": 13.0, "variation": 1.5}, 

            }
        }

        self.current_selected_version = None
        self.search_text = ""
        self.filtered_titles = list(self.recipe_titles.keys())

        self.recipes_container = ft.Row(
            controls=[],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO
        )


    def filter_recipes(self, query):
        self.search_text = query
        query_lower = query.lower()
        self.filtered_titles = [
            title for title in self.recipe_titles
            if query_lower in title.lower()
        ]
        self.update_recipe_containers()

    



    def get_recipe_title_by_id(self, recipe_id):
        """
        Hilfsfunktion um den Titel anhand der ID zu finden
        """
        for title, id_val in self.recipe_titles.items():
            if id_val == recipe_id:
                return title
        return f"Rezept #{recipe_id}"
    
    def close_overlay(self, e):
        if self.recipe_overlay:
            try:
                self.recipe_overlay.open = False
                self.page.update()
            except Exception as ex:
                print(f"Fehler beim Schließen: {ex}")

    def on_version_selected(self, version_date):
        """Handler für Versions-Auswahl"""
        def handler(e):
            self.current_selected_version = version_date
            self.update_recipe_display()
        return handler
    
    def update_recipe_containers(self):
        self.recipes_container.controls.clear()
        for title in self.filtered_titles:
            container = ft.GestureDetector(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=random.choice(self.recipe_images),
                                fit=ft.ImageFit.COVER,
                            ),
                            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=Styles.TEXT_COLOR),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=Styles.RECIPE_CONTAINER_COLOR,
                    border_radius=Styles.BORDER_RADIUS,
                    padding=10,
                    margin=5,
                    width=250
                ),
                on_tap=self.create_recipe_handler(title)
            )
            self.recipes_container.controls.append(container)
        self.page.update()

    

    def update_recipe_display(self):
        """Aktualisiert die Rezept-Anzeige mit der ausgewählten Version"""
        if not self.recipe_overlay or not self.current_selected_version:
            return
        
        try:
            # Vereinfachte Aktualisierung - komplettes Overlay neu laden fixxxxx
            recipe_id = next(iter(self.recipe_titles.values()))  # Temporär für Demo
            self.open_recipe_overlay(recipe_id)
        except Exception as ex:
            print(f"Fehler beim Aktualisieren: {ex}")
    
    def create_version_selector(self, recipe_id):
        """Erstellt die Versions-Auswahl"""

        versions_data = self.recipe_versions # versions_data = Translation.get_all_evaluations(recipe_id)
        
        if not versions_data or len(versions_data) <= 1:
            return None  
            
        sorted_versions = sorted(versions_data.keys(), reverse=True)
        
        if not self.current_selected_version:
            self.current_selected_version = sorted_versions[0]
        
        version_buttons = []
        for version_date in sorted_versions:
            is_selected = version_date == self.current_selected_version
            
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
                    on_click=self.on_version_selected(version_date)
                )
            )
        
        return ft.Column(
            controls=[
                ft.Text(
                    "Versions:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=Styles.TEXT_COLOR
                ),
                ft.Column(
                    controls=version_buttons,
                    spacing=2,
                    scroll=ft.ScrollMode.AUTO
                )
            ],
            spacing=10
        )
    
    def create_ingredients_list(self, recipe_data):
        """Erstellt die Zutaten-Liste basierend auf den Daten"""
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
    
            
    
    def open_recipe_overlay(self, recipe_id):
        """Öffnet das Overlay mit den Rezeptdaten"""
        
        recipe_title = self.get_recipe_title_by_id(recipe_id)
        versions_data = self.recipe_versions  # versions_data = Translation.get_all_evaluations(recipe_id)  
        
        if versions_data and len(versions_data) > 1:
            if not self.current_selected_version:
                self.current_selected_version = max(versions_data.keys())
            recipe_data = versions_data.get(self.current_selected_version, self.recipe_data)
        else:
            # Fallback 
            recipe_data = self.recipe_data  # recipe_data = Translation.get_last_evaluation(recipe_id)
            self.current_selected_version = None
        
        ingredients_controls = self.create_ingredients_list(recipe_data)
        
        version_selector = self.create_version_selector(recipe_id)
        
        main_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Ingredients:",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=Styles.TEXT_COLOR
                    ),
                    ft.Text(
                        "Per 100g:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=Styles.TEXT_COLOR
                    ),
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
                    ft.Container(
                        width=1,
                        bgcolor=Styles.TEXT_COLOR,
                        height=500
                    ),
                    main_content
                ],
                spacing=10,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        else:
            recipe_content = main_content


        
        overlay_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                recipe_title,
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=Styles.TEXT_COLOR
                            ),
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

        if self.recipe_overlay:
            self.close_overlay(None)
        
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
            def handler(e):
                recipe_id = self.recipe_titles.get(title)
                if recipe_id:
                    self.open_recipe_overlay(recipe_id)
                else:
                    print(f"Keine ID für Rezept '{title}' gefunden")
            return handler 

    def build(self):

        search_field = ft.TextField(
            label="Search recipes",
            value=self.search_text,
            on_change=lambda e: self.filter_recipes(e.control.value),
            width=300,
            bgcolor=Styles.INPUT_FILL_COLOR,
            border_radius=Styles.BORDER_RADIUS,
            color=Styles.TEXT_COLOR,
            border_color=Styles.INPUT_BORDER_COLOR,
            label_style=ft.TextStyle(
                color=Styles.TEXT_COLOR),
            cursor_color=Styles.TEXT_COLOR
        )

        # Initial befüllen, falls leer
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
