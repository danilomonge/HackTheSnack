import flet as ft
#from styles import PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_SIZE, BODY_SIZE
PRIMARY_COLOR = "green"
BACKGROUND_COLOR = "black"
TEXT_COLOR = "white"

TITLE_SIZE = 40
BODY_SIZE = 18


class HomeView:

    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        content = ft.Column(
            controls=[
                ft.Text("Hack The Snack", size=65, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(
                    content=ft.Text(
                        "Recreate your favorite food products at home with the help of our food hacker \n - \n Crack it · Cook it · Love it",
                        size=BODY_SIZE,
                        text_align=ft.TextAlign.CENTER,
                        color="white",
                    ),
                    padding=30,
                    width=650,
                    bgcolor="#90C976",
                    border=ft.border.all(1, "white"),
                    border_radius=40,
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        color="rgba(0,0,0,0.25)",
                        offset=ft.Offset(0, 4)
                              ),
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Try it out",
                            color="white",
                            on_click=lambda e: self.page.go("/generator"),
                            ),
                        ft.OutlinedButton(
                            "More about us",
                            style=ft.ButtonStyle(
                            color="white",
                            overlay_color=PRIMARY_COLOR,
                            side=ft.BorderSide(1, "white")
                            ),
                            on_click=lambda e: self.page.go("/about"),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
        )


        return ft.View(
            route="/",
            controls=[
                ft.Stack(
                    controls=[
                        ft.Image(
                            src="Picture_ingredients_mushrooms.png",
                            width=float("inf"),  # Full width
                            height=float("inf"),  # Full height
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.Container(
                            content=content,
                            alignment=ft.alignment.center,
                            padding=50,
                            expand=True,
                        )
                    ],
                    expand=True
                )
            ]
        )