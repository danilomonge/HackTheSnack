import flet as ft

#from Frontend.src.styles import PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_SIZE, BODY_SIZE
PRIMARY_COLOR="#358E5D"
BACKGROUND_COLOR="#358E5D"
TEXT_COLOR="white"
TITLE_SIZE=28
BODY_SIZE=18

       
class AboutView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        return ft.Column(
            controls=[
                ft.Text("About Hack The Snack", size=TITLE_SIZE, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "This app helps you analyze and generate recipes based on ingredient lists.",
                    size=BODY_SIZE,
                ),
                ft.Text("The Team:", size=BODY_SIZE, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Jana",
                                        size=BODY_SIZE,
                                        text_align=ft.TextAlign.CENTER,
                                        color=TEXT_COLOR,
                                    ),
                                    ft.Image(
                                        src="https://img.freepik.com/vektoren-premium/strichmaennchen-mann-doodle-zeichnung-isoliert_566661-1697.jpg",
                                        width=100,
                                        height=100,
                                        border_radius=50,
                                        fit=ft.ImageFit.COVER,
                                    ),
                                    ft.Text(
                                        "media informatics",
                                        size=BODY_SIZE,
                                        text_align=ft.TextAlign.CENTER,
                                        color=TEXT_COLOR,
                                    ),

                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            border=ft.border.all(1, "black"),
                            expand=True,
                            padding=10,
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Emilio",
                                        size=BODY_SIZE,
                                        text_align=ft.TextAlign.CENTER,
                                        color=TEXT_COLOR,
                                    ),
                                    ft.Image(
                                        src="https://image.spreadshirtmedia.net/image-server/v1/products/T1459A839PA4459PT28D152850882W4782H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/strichmaennchen-sticker.jpg",
                                        width=100,
                                        height=100,
                                        border_radius=50,
                                        fit=ft.ImageFit.COVER,
                                    ),
                                    ft.Text(
                                        "cognitive science",
                                        size=BODY_SIZE,
                                        text_align=ft.TextAlign.CENTER,
                                        color=TEXT_COLOR,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            border=ft.border.all(1, "black"),
                            expand=True,
                            padding=10,
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Danilo",
                                        size=BODY_SIZE,
                                        text_align=ft.TextAlign.CENTER,
                                        color=TEXT_COLOR,
                                    ),
                                    ft.Image(
                                        src="https://i.pinimg.com/736x/70/9f/f9/709ff92ec7c90bcf617c8e83d0b7a80d.jpg",
                                        width=100,
                                        height=100,
                                        border_radius=50,
                                        fit=ft.ImageFit.COVER,
                                    ),
                                    ft.Text(
                                        "medical informatics",
                                        size=BODY_SIZE,
                                        text_align=ft.TextAlign.CENTER,
                                        color=TEXT_COLOR,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            border=ft.border.all(1, "black"),
                            expand=True,
                            padding=10,
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Katja",
                                        size=BODY_SIZE,
                                        text_align=ft.TextAlign.CENTER,
                                        color=TEXT_COLOR,
                                    ),
                                    ft.Image(
                                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAdpg1zjwqCLvFvBQquT8u7Nmnp65-dcyPhg&s",
                                        width=100,
                                        height=100,
                                        border_radius=50,
                                        fit=ft.ImageFit.COVER,
                                    ),
                                    ft.Text(
                                        "cognitive science",
                                        size=BODY_SIZE,
                                        text_align=ft.TextAlign.CENTER,
                                        color=TEXT_COLOR,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            border=ft.border.all(1, "black"),
                            expand=True,
                            padding=10,
                            alignment=ft.alignment.center
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True
        )