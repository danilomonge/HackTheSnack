import flet as ft

class HomeView:

    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        content = ft.Column(
            controls=[
                ft.Text("Hack The Snack", size=40, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(
                    content=ft.Text(
                        "Project explanation here",
                        size=20,
                        text_align=ft.TextAlign.CENTER,
                        color="white",
                    ),
                    padding=20,
                    width=600,
                    bgcolor= "green",
                    border_radius=10,
                    margin=ft.margin.only(top=20, bottom=30),
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Try it out"),
                        ft.OutlinedButton("More about us"),
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
                            src="https://cdn.pixabay.com/photo/2018/01/27/21/04/oil-3112195_1280.jpg",
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