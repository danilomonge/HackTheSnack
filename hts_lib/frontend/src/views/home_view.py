import flet as ft
from frontend.src.styles import Styles


class HomeView:

    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        content = ft.Column(
            controls=[
                ft.Image(
                src="hts_lib/assets/Title.png",
                width=700,
                fit=ft.ImageFit.CONTAIN,  ),
                ft.Container(
                    content=Styles.build_description(
                        "Recreate your favorite food products at home with the help of our food hacker \n - \n Crack it · Cook it · Love it"
                    ),
                    padding=30,
                    width=650,
                    bgcolor=Styles.BOX_COLOR,
                    border_radius=Styles.BORDER_RADIUS,
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        color="rgba(0,0,0,0.25)",
                        offset=ft.Offset(0, 4)
                              ),
                ),
                ft.Row(
                    controls=[
                        Styles.build_button(
                            "Try it out",
                            on_click=lambda e: self.page.go("/generator"),
                            icon=ft.Icons.FAVORITE,
                            ),
                        Styles.build_button(
                            "More about us",
                            on_click=lambda e: self.page.go("/about"),
                            icon=ft.Icons.INFO,
                            ),
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
            scroll=ft.ScrollMode.AUTO,
        )


        return ft.View(
            route="/",
            controls=[
                ft.Stack(
                    controls=[
                        ft.Image(
                            src="hts_lib/assets/bg_test.png",
                            width=float("inf"),
                            height=float("inf"),
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