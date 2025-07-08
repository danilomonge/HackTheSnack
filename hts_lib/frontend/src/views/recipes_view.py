import flet as ft
import random

from styles import Styles 


class RecipesView:
    def __init__(self, page: ft.Page):
        self.page = page

        self.recipe_titles = {"Pizza Margherita": 12, "Fruit Yogurt": 1} # Translation.collect_product_list()

        self.recipe_images = [
            "dish_1.png",
            "dish_2.png",
            "dish_3.png",
            "dish_4.png",
            "dish_5.png",
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
            
    
    def open_recipe_overlay(self, recipe_id):
        """Öffnet das Overlay mit den Rezeptdaten"""
        
        recipe_title = self.get_recipe_title_by_id(recipe_id)
        recipe_data = self.recipe_data  # recipe_data = Translation.get_last_evaluation(recipe_id)
        
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
                    border_radius=5,
                    margin=ft.margin.only(bottom=5)
                )
            )
        
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
                    
                    # Recipe Information
                    ft.Container(
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
                                ft.Column(
                                    controls=ingredients_controls,
                                    spacing=2
                                ),
                            ],
                            spacing=15,
                            scroll=ft.ScrollMode.AUTO
                        ),
                        height=400,
                        padding=20
                    )
                ],
                spacing=20
            ),
            bgcolor=Styles.BOX_COLOR,
            border_radius=Styles.BORDER_RADIUS,
            padding=30,
            width=600,
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
        

    def build(self):

        def create_recipe_handler(title):
            def handler(e):
                recipe_id = self.recipe_titles.get(title)
                if recipe_id:
                    self.open_recipe_overlay(recipe_id)
                else:
                    print(f"Keine ID für Rezept '{title}' gefunden")
            return handler
         
        recipe_containers = [
             ft.GestureDetector(
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
                on_tap=create_recipe_handler(title)
            )
            for title in self.recipe_titles
        ]


        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            Styles.build_title("Your Recipes"),
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
                            ft.Row(
                                controls=recipe_containers,
                                spacing=20,
                                alignment=ft.MainAxisAlignment.START,
                                scroll=ft.ScrollMode.AUTO
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                        expand=True  
                    ),
                    alignment=ft.alignment.center,
                    bgcolor=Styles.BACKGROUND_COLOR,
                    expand=True,
                    padding=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )