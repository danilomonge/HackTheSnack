import flet as ft

from frontend.src.styles import Styles

       
class AboutView:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def open_github(self, github_url: str):
        """Opens the GitHub page in the default browser."""
        self.page.launch_url(github_url)

    def team_member(self, name: str, field: str, image_url: str, github_url: str, github_user: str ):
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
                    Styles.build_button(github_user, ft.Icons.OPEN_IN_NEW, lambda e: self.open_github(github_url))
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
                            self.team_member("Emilio", "Cognitive Science", "Emilio.JPG", "https://github.com/ERibelles12", "ERibelles12" ),
                            self.team_member("Danilo", "Medical Informatics",
                                            "Danilo.JPG", "https://github.com/danilomonge", "danilomonge"), 
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER,
                    ), 
                    ft.Row(
                        controls=[
                            self.team_member("Jana", "Media Informatics",
                                            "Jana.JPG", "https://github.com/jd-janadanner", "jd-janadanner"),
                            self.team_member("Katja", "Cognitive Science",
                                            "Katja.JPG", "https://github.com/katja-gf", "katja-gf"),
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
                    ft.Text(
                        "Project Information",
                        size=27,
                        weight=ft.FontWeight.BOLD,
                        color=Styles.TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                Styles.build_button("Github Repository", ft.Icons.OPEN_IN_NEW, lambda e: self.open_github("https://github.com/danilomonge/HackTheSnack")),
                                Styles.build_explanation_subtitle("A smart app to explore, create, and save recipes"),
                                Styles.build_explanation(
                                    "This app uses the Slice Sampling algorithm, an efficient technique within the Markov Chain Monte Carlo (MCMC) framework, "
                                    "to automatically estimate unknown ingredient proportions in food products distributed in the European Union. "
                                    "Based on the ingredients and known amounts that users enter manually into the interface, the system completes the missing parts of the recipe in a consistent and realistic way.\n"
                                ),
                                Styles.build_explanation_subtitle("Custom recipe creation and secure saving"),
                                Styles.build_explanation(
                                    "Users can freely design their own combinations of ingredients and experiment with new ideas. "
                                    "Every recipe, whether inferred or created from scratch, can be saved directly through the interface. "
                                    "Thanks to a robust database, all saved recipes remain accessible for future viewing, analysis, or reuse.\n"
                                ),
                                Styles.build_explanation_subtitle("Automatic estimation of nutritional values"),
                                Styles.build_explanation(
                                    "The app connects to the official USDA API, which allows it to automatically retrieve standard nutritional information "
                                    "for each identified ingredient, such as calories, fat, carbohydrates, and protein content. "
                                    "This enables a clear and accurate overview of each recipe’s nutritional profile.\n"
                                ),
                                Styles.build_explanation_subtitle("Multilingual support with automatic translation"),
                                Styles.build_explanation(
                                    "Ingredient names can also be written in German. With the help of the integrated DeepL API, they are automatically translated into English, "
                                    "ensuring compatibility with international nutrition databases and providing a smooth experience for multilingual users.\n"
                                ),
                                Styles.build_explanation_subtitle("A complete tool for creative minds and food enthusiasts"),
                                Styles.build_explanation(
                                    "Combining statistical inference, nutritional data, multilingual input, and recipe management, this app offers a full experience for anyone "
                                    "interested in exploring, understanding, or reimagining food recipes in a smart and creative way."
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        padding=20,
                        width=800,
                        bgcolor=Styles.BOX_COLOR,
                        border_radius=Styles.BORDER_RADIUS,
                        alignment=ft.alignment.top_left,
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
