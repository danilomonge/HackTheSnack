import flet as ft
from backend.translation import Translation
from backend.data_base_manager.evaluation_manager import EvaluationManager
from backend.data_base_manager.recipe_manager import RecipeManager
from backend.translation import Translation

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


    def build_ingredient_line_chart(self, data: dict) -> ft.LineChart:
        """
        Creates a Flet LineChart showing mean percentage of each ingredient over evaluation dates.
        Args:
            data (dict): JSON-like dict containing ingredient evaluation data.
        Returns:
            ft.LineChart: Configured LineChart displaying trends per ingredient.
        """
        ingredient_data = {}
        all_dates = set()

        # Extract and group values by ingredient name
        for item in data.get("data", []):
            name = item["ingredientName"]
            date = item["evaluationDate"]
            percentage = item["ingredientMeanPercentage"]

            if name not in ingredient_data:
                ingredient_data[name] = []
            ingredient_data[name].append((date, percentage))
            all_dates.add(date)

        # First get a sorted list of unique dates for consistent X-axis
        all_dates = sorted({record[0] for records in ingredient_data.values() for record in records})

        # Map dates to X-axis indices (0, 1, 2, ...)
        date_to_x = {date: idx for idx, date in enumerate(all_dates)}

        # Build data series for each ingredient
        lines = []
        for ingredient_name, records in ingredient_data.items():
            sorted_points = sorted(records, key=lambda x: x[0])
            points = [
                ft.LineChartDataPoint(x=date_to_x[date], y=percentage)

                for date, percentage in sorted_points # type: ignore
            ]
            
            lines.append(
                ft.LineChartData(
                    data_points=points,
                    stroke_width=3,
                    curved=True,
                    color=ft.Colors.random(ingredient_name), # type: ignore
                )
            )

        # width_per_label = 80
        # page_width = self.page.width
        # total_width = max(len(all_dates) * width_per_label, page_width) # type: ignore

        return ft.LineChart(
            data_series=lines,
            tooltip_bgcolor=ft.Colors.BLUE_GREY_100,
            left_axis=ft.ChartAxis(
                labels_size=40,
                title=ft.Text("Mean %"),
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(label=ft.Text(date), value=i)
                    for i, date in enumerate(all_dates)
                ],
                labels_size=40,
                title=ft.Text("Evaluation Date"),
            ),
            min_y=0,
            max_y=100,
            expand=True,
            height=400,
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