import flet as ft
import random

from styles import Styles 


class RecipesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.recipe_titles = ["Pizza Margherita", "Fruit Yogurt"] #self.get_recipe_titles_from_db() 

        self.recipe_images = [
            "dish_1.png",
            "dish_2.png",
            "dish_3.png",
            "dish_4.png",
            "dish_5.png",
        ]
        

    def build(self):

        def on_recipe_tap(title):
            def handler(e):
                # Route zu Detailansicht, z.B. /recipe/Pizza%20Margherita
                # self.page.go(f"/recipe/{title.replace(' ', '%20')}")
                self.page.go(f"/about")
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
                on_tap=on_recipe_tap(title)
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