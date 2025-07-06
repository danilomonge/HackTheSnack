import flet as ft

from styles import Styles

       
class AboutView:
    def __init__(self, page: ft.Page):
        self.page = page

    def team_member(self, name: str, field: str, image_url: str):
        """
        Creates a team member container with name, field of study, and image.

        Args:
            name (str): Name of the team member.
            field (str): Field of study.
            image_url (str): URL of the team member's image.

        Returns:
            ft.Container: A styled container with team member information.
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(name, size=Styles.EXPLANATION_FONT_SIZE, text_align=ft.TextAlign.CENTER, color=Styles.TEXT_COLOR),
                    ft.Image(src=image_url, width=100, height=100, border_radius=50, fit=ft.ImageFit.COVER),
                    ft.Text(field, size=Styles.EXPLANATION_FONT_SIZE, text_align=ft.TextAlign.CENTER, color=Styles.TEXT_COLOR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            border_radius=Styles.BORDER_RADIUS,
            expand=True,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=Styles.BOX_COLOR
        )

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    Styles.build_title("About Hack The Snack"),
                    ft.Container(
                        Styles.build_description(
                            "This app helps you analyze and generate recipes based on ingredient lists. Is is designed to assist you in recreating your favorite food products at home."
                        ),
                        padding=20,
                        width=650,
                        bgcolor=Styles.BOX_COLOR,
                        border_radius=Styles.BORDER_RADIUS,
                    ),
                    Styles.build_subtitle("The Team"),
                    ft.Row(
                        controls=[
                            self.team_member("Emilio", "Cognitive Science",
                                            "https://image.spreadshirtmedia.net/image-server/v1/products/T1459A839PA4459PT28D152850882W4782H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=FFFFFF/strichmaennchen-sticker.jpg"),
                            self.team_member("Danilo", "Medical Informatics",
                                            "https://cdni.iconscout.com/illustration/premium/thumb/gluckliches-strichmannchen-3180113-2666423.png?f=webp"), 
                            self.team_member("Jana", "Media Informatics",
                                            "https://img.freepik.com/vektoren-premium/strichmaennchen-mann-doodle-zeichnung-isoliert_566661-1697.jpg"),
                            self.team_member("Katja", "Cognitive Science",
                                            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAdpg1zjwqCLvFvBQquT8u7Nmnp65-dcyPhg&s"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True
            ),
            padding=20,
            bgcolor=Styles.BACKGROUND_COLOR,
            expand=True,
            alignment=ft.alignment.center,
        
    )
