import flet as ft
from Backend.translation import Translation
from Backend.data_base_manager.evaluation_manager import EvaluationManager
from Backend.translation import Translation

from styles import Styles  # Assumes Styles has utility methods for title and colors
import json


class StatisticsView:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_products_and_ingredients(self):
        # You would replace this with actual DB logic.
        # Example: Fetching from DB, API, or service layer.
        dropdown_products = Translation.collect_product_list()
        dropdown_ingredients = Translation.collect_ingredient_list()
        return dropdown_products, dropdown_ingredients  
    
    def build_dropdown(self, label: str, items: list[str]):
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(item) for item in items],
            width=200,
        )
    

    def build_ingredient_line_chart(self, data: dict) -> ft.LineChart:
        """
        Creates a Flet LineChart showing mean percentage of each ingredient over evaluation dates.

        Args:
            data (dict): JSON-like dict containing ingredient evaluation data.

        Returns:
            ft.LineChart: Configured LineChart displaying trends per ingredient.
        """
        ingredient_data = {}

        mock_data = {'TOMATE': [('2025-06-28T22:00:00.000+00:00', 9.31), 
                                ('2025-06-30T22:00:00.000+00:00', 9.55), 
                                ('2025-07-01T22:00:00.000+00:00', 0.94), 
                                ('2025-07-02T22:00:00.000+00:00', 0.0), 
                                ('2025-07-03T22:00:00.000+00:00', 10.11), 
                                ('2025-07-04T22:00:00.000+00:00', 3.68), 
                                ('2025-07-05T22:00:00.000+00:00', 13.69), 
                                ('2025-07-06T22:00:00.000+00:00', 10.79)], 
                        'APF': [('2025-06-28T22:00:00.000+00:00', 68.69), 
                            ('2025-06-30T22:00:00.000+00:00', 71.45), 
                            ('2025-07-01T22:00:00.000+00:00', 56.31), 
                            ('2025-07-02T22:00:00.000+00:00', 67.21), 
                            ('2025-07-0T22:00:00.000+00:00', 97.06), 
                            ('2025-07-041T22:00:00.000+00:00', 89.32), 
                            ('2025-07-05T22:00:00.000+00:00', 50.0), 
                            ('2025-07-06T22:00:00.000+00:00', 69.89)], 
                        'EL': [('2025-06-28T22:00:00.000+00:00', 22.0), 
                               ('2025-06-30T22:00:00.000+00:00', 19.0), 
                               ('2025-07-01T22:00:00.000+00:00', 50.0), 
                               ('2025-07-02T22:00:00.000+00:00', 2.0), 
                               ('2025-07-03T22:00:00.000+00:00', 20.0), 
                               ('2025-07-04T22:00:00.000+00:00', 7.0), 
                               ('2025-07-05T22:00:00.000+00:00', 22.0), 
                               ('2025-07-06T22:00:00.000+00:00', 30.0)]}

        # Extract and group values by ingredient name
        for entry in data.get("data", []):
            name = entry["ingredientName"]
            date = entry["evaluationDate"]
            percentage = entry["ingredientMeanPercentage"]

            if name and percentage is not None and date:
                if name not in ingredient_data:
                    ingredient_data[name] = []
                ingredient_data[name].append((date, percentage))
            

        # Collect all unique sorted dates
        all_dates = sorted({date for entries in mock_data.values() for date, _ in entries})
        #date_labels = [date.strftime("%Y-%m-%d") for date in all_dates]
        date_index_map = {date: idx for idx, date in enumerate(all_dates)}

        # Build data series for each ingredient
        lines = []
        for ingredient_name, records in mock_data.items():
            points = [
                ft.LineChartDataPoint(x=date_index_map[date], y=percentage)
                for date, percentage in sorted(records)
            ]
            print(points)  # should show a list of LineChartDataPoint
            print(type(points[0]))  # should show <class 'flet.LineChartDataPoint'>
            lines.append(
                ft.LineChartData(
                    data_points=points,
                    stroke_width=3,
                    curved=True,
                    color=ft.Colors.random(ingredient_name), # type: ignore
                    #legend_label=ingredient_name,
                )
            )

        width_per_label = 80
        page_width = self.page.width
        total_width = max(len(all_dates) * width_per_label, page_width) # type: ignore

        return ft.LineChart(
            data_series=lines,
            tooltip_bgcolor=ft.Colors.BLUE_GREY_100,
            min_y=0,
            max_y=100,
            #left_axis=ft.ChartAxis(title="Mean %"),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=i, label= ft.Text(d))
                    for i, d in enumerate(all_dates)
                ],          
                #title="Evaluation Date",
                #label_rotation=45,
            ),
            expand=True,
            width=total_width,
            height=400,
        )
    
    def build(self):
        dropdown_product_data, dropdown_ingredient_data = self.get_products_and_ingredients()

        # Replace this with your actual service call
        response = EvaluationManager.find_evaluation_product_ingredient(5, 0)
        data = response.json()
        chart = self.build_ingredient_line_chart(data)

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            Styles.build_title("Make Your Selection"),
                            ft.Row(
                                controls=[
                                    self.build_dropdown("Select Product", dropdown_product_data),
                                    self.build_dropdown("Select Ingredient", dropdown_ingredient_data),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            ft.Container(content=chart, padding=20),
                            ft.ElevatedButton(text="Confirm", on_click=lambda e: print("Confirmed!")),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
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