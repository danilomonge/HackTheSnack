import flet as ft
from backend.translation import Translation
from backend.data_base_manager.evaluation_manager import EvaluationManager
from backend.data_base_manager.recipe_manager import RecipeManager
from backend.translation import Translation
from frontend.src.styles import Styles

from styles import Styles  # Assumes Styles has utility methods for title and colors
import json


class StatisticsView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.product_dropdown = ft.Dropdown
        self.ingredient_dropdown = ft.Dropdown
        self.chart_container = ft.Container()
        self.product_dict = {}
        self.ingredient_dict = {}
        self.ingredient_container = ft.Container()
        
    def get_products_and_ingredients(self):
        self.product_dict = Translation.collect_product_dict()

        self.ingredient_dict = Translation.collect_ingredient_dict()
        dropdown_products = list(self.product_dict.keys())
        dropdown_ingredients = list(self.ingredient_dict.keys())
        return dropdown_products, dropdown_ingredients  

    def build_dropdown(self, label: str, items: list[str], on_change=None):
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(item) for item in items],
            width=200,
            on_change=on_change
        )
    
    def on_product_select(self, e):
        selected_product_name = self.product_dropdown.value
        selected_product_id = self.product_dict.get(selected_product_name) # type: ignore

        ingredient_response = RecipeManager.find_product_ingredient_list(selected_product_id)
        ingredient_data = ingredient_response.json()
        ingredients, ids = Translation.product_table_filter(ingredient_data)

        updated_dropdown = self.build_dropdown("Select Ingredient", list(ingredients.keys()))
        self.ingredient_dropdown = updated_dropdown
        self.ingredient_container.content = self.ingredient_dropdown
        self.page.update()
    
    def on_confirm(self, e):
        selected_product_name = self.product_dropdown.value
        if not selected_product_name:
            print("No product selected")
            return
        
        product_id = self.product_dict.get(selected_product_name) # type: ignore
        if not product_id:
            print("Product ID not found for selected name.")
            return
        
        response = EvaluationManager.find_evaluation_product_ingredient(product_id, 0)
        data = response.json()
        chart = self.build_ingredient_line_chart(data)

        self.chart_container.content = chart
        self.page.update()


    def build_ingredient_line_chart(self, data: dict) -> ft.Control:
        """
        Creates a styled Flet LineChart showing mean percentage of each ingredient over evaluation dates.

        Args:
            data (dict): JSON-like dict containing ingredient evaluation data.

        Returns:
            ft.Control: A Row with LineChart and aligned legend on the right.
        """
        mock_data = {
            'TOMATE': [
                ('2025-06-28T22:00:00.000+00:00', 9.31),
                ('2025-06-30T22:00:00.000+00:00', 9.55),
                ('2025-07-01T22:00:00.000+00:00', 0.94),
                ('2025-07-02T22:00:00.000+00:00', 0.0),
                ('2025-07-03T22:00:00.000+00:00', 10.11),
                ('2025-07-04T22:00:00.000+00:00', 3.68),
                ('2025-07-05T22:00:00.000+00:00', 13.69),
                ('2025-07-06T22:00:00.000+00:00', 10.79)
            ],
            'APF': [
                ('2025-06-28T22:00:00.000+00:00', 68.69),
                ('2025-06-30T22:00:00.000+00:00', 71.45),
                ('2025-07-01T22:00:00.000+00:00', 56.31),
                ('2025-07-02T22:00:00.000+00:00', 67.21),
                ('2025-07-0T22:00:00.000+00:00', 97.06),
                ('2025-07-041T22:00:00.000+00:00', 89.32),
                ('2025-07-05T22:00:00.000+00:00', 50.0),
                ('2025-07-06T22:00:00.000+00:00', 69.89)
            ],
            'EL': [
                ('2025-06-28T22:00:00.000+00:00', 22.0),
                ('2025-06-30T22:00:00.000+00:00', 19.0),
                ('2025-07-01T22:00:00.000+00:00', 50.0),
                ('2025-07-02T22:00:00.000+00:00', 2.0),
                ('2025-07-03T22:00:00.000+00:00', 20.0),
                ('2025-07-04T22:00:00.000+00:00', 7.0),
                ('2025-07-05T22:00:00.000+00:00', 22.0),
                ('2025-07-06T22:00:00.000+00:00', 30.0)
            ]
        }

        for item in data.get("data", []):
            name = item["ingredientName"]
            date = item["evaluationDate"]
            percentage = item["ingredientMeanPercentage"]
            if name not in mock_data:
                mock_data[name] = []
            mock_data[name].append((date, percentage))

        all_dates = sorted({record[0] for records in mock_data.values() for record in records})
        date_to_x = {date: idx for idx, date in enumerate(all_dates)}
        color_palette = ["#FF5252", "#4CAF50", "#2196F3", "#FFC107", "#9C27B0", "#00BCD4"]

        lines = []
        for idx, (ingredient_name, records) in enumerate(mock_data.items()): 
            sorted_points = sorted(records, key=lambda x: x[0])
            points = [
                ft.LineChartDataPoint(x=date_to_x[date], y=percentage)
                for date, percentage in sorted_points
            ]
            lines.append(
                ft.LineChartData(
                    data_points=points,
                    stroke_width=4,
                    curved=True,
                    color=color_palette[idx % len(color_palette)],
                )
            )

        x_labels = [
            ft.ChartAxisLabel(
                label=ft.Container(
                    content=ft.Text(f"Day {i+1}", color="black"),
                    padding=ft.padding.only(top=10)
                ),
                value=i + 0.5
            )
            for i in range(len(all_dates))
        ]

        y_labels = [
            ft.ChartAxisLabel(
                value=y,
                label=ft.Container(
                    content=ft.Text(f"{y}%", color="black"),
                    padding=ft.padding.only(right=5)
                )
            )
            for y in range(0, 110, 10)
        ]

        legend_items = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(width=12, height=12, bgcolor=color_palette[idx % len(color_palette)], border_radius=6),
                        ft.Text(ingredient_name, size=12, color="black", weight=ft.FontWeight.BOLD),
                    ],
                    spacing=5
                ),
                padding=ft.padding.only(right=12)
            )
            for idx, ingredient_name in enumerate(mock_data.keys())
        ]

        legend = ft.Container(
            content=ft.Row(controls=legend_items),
            padding=ft.padding.only(left=140, bottom=10)  
        )

        chart = ft.LineChart(
            data_series=lines,
            tooltip_bgcolor=ft.Colors.BLUE_GREY_100,
            bgcolor=Styles.INPUT_FILL_COLOR,
            left_axis=ft.ChartAxis(
                labels=y_labels,
                labels_size=50,
                labels_interval=10,
                title=ft.Container(
                    content=ft.Text("Percentage", size=16, color=Styles.BUTTON_FILL_DISABLED_COLOR),
                    alignment=ft.alignment.Alignment(0.15, -0.35),
                    expand=True,
                ),
                title_size=60,
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_size=40,
                title=ft.Text("Time", size=16, color=Styles.BUTTON_FILL_DISABLED_COLOR),
                title_size=20,
            ),
            min_y=0,
            max_y=100,
            expand=True,
            height=400,
        )

        return ft.Column(
            controls=[
                legend,
                chart
            ]
        )




    def build(self):
        dropdown_product_data, dropdown_ingredient_data = self.get_products_and_ingredients()
    
        self.product_dropdown = self.build_dropdown(
            "Select Product",
            dropdown_product_data,
            on_change=self.on_product_select
        )
        self.ingredient_dropdown = self.build_dropdown("Select Ingredient", dropdown_ingredient_data)
        self.ingredient_container.content = self.ingredient_dropdown

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            Styles.build_title("Make Your Selection"),
                            ft.Row(
                                controls=[
                                    self.product_dropdown,
                                    self.ingredient_container
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Confirm",
                                    on_click=self.on_confirm
                                ),
                                alignment=ft.alignment.center,
                                padding=20,
                            ),
                            self.chart_container  # Chart placeholder
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    bgcolor=Styles.BACKGROUND_COLOR,
                    expand=True,
                    padding=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )