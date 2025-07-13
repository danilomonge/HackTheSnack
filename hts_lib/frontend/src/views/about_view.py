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
                spacing=10,
            ),
            border_radius=Styles.BORDER_RADIUS,
            padding=10,
            width= 390,
            alignment=ft.alignment.center,
            bgcolor=Styles.BOX_COLOR
        )

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    Styles.build_title("About Hack The Snack"),
                    ft.Container(
                        Styles.build_explanation(
                            "We are a group of four students currently studying at the University of Tübingen. This semester we decided to take part in a team project, which is how this app came to be. \n" \
                            "The app helps you analyze and generate recipes based on ingredient lists of products of your choice. It is designed to assist you in recreating your favorite food products at home."
                        ),
                        padding=20,
                        width=800,
                        bgcolor=Styles.BOX_COLOR,
                        border_radius=Styles.BORDER_RADIUS,
                    ),
                    ft.Text(
                        "The Team",
                        size=27,
                        weight=ft.FontWeight.BOLD,
                        color=Styles.TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="Group-1.JPG",
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        width=800,
                        alignment=ft.alignment.center,
                    ),
                    ft.Row(
                        controls=[
                            self.team_member("Emilio", "Cognitive Science",
                                            "Emilio.JPG"),
                            self.team_member("Danilo", "Medical Informatics",
                                            "Danilo.JPG"), 
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ), 
                    ft.Row(
                        controls=[
                            self.team_member("Jana", "Media Informatics",
                                            "Jana.JPG"),
                            self.team_member("Katja", "Cognitive Science",
                                            "Katja.JPG"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ), 
                    ft.Container(
                        content=ft.Image(
                            src="Group-2.JPG",
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        width=800,
                        alignment=ft.alignment.center,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,
                scroll= ft.ScrollMode.ADAPTIVE
            ),
            padding=20,
            bgcolor=Styles.BACKGROUND_COLOR,
            expand=True,
            alignment=ft.alignment.center,
        
    )
