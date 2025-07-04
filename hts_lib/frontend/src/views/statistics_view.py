import flet as ft
from backend.translation import Translation
from backend.data_base_manager.evaluation_manager import EvaluationManager
from backend.data_base_manager.recipe_manager import RecipeManager
from backend.translation import Translation
from frontend.src.styles import Styles

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
            on_change=on_change,
        )

    def on_product_select(self, e):
        selected_product_name = self.product_dropdown.value
        selected_product_id = self.product_dict.get(selected_product_name)  # type: ignore

        ingredient_response = RecipeManager.find_product_ingredient_list(
            selected_product_id
        )
        ingredient_data = ingredient_response.json()
        ingredients, ids = Translation.product_table_filter(ingredient_data)

        updated_dropdown = self.build_dropdown(
            "Select Ingredient", list(ingredients.keys())
        )
        self.ingredient_dropdown = updated_dropdown
        self.ingredient_container.content = self.ingredient_dropdown
        self.page.update()

    def on_confirm(self, e):
        selected_product_name = self.product_dropdown.value
        if not selected_product_name:
            print("No product selected")
            return

        product_id = self.product_dict.get(selected_product_name)  # type: ignore
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
            ft.Control: A Column containing the chart and the legend.
        """
        # Parse the ingredient data from the provided JSON-like dict
        mock_data = self._parse_ingredient_data(data)
        # Get all unique dates and a mapping from date to x-axis position
        all_dates, date_to_x = self._get_all_dates_and_mapping(mock_data)
        # Fill in missing dates with zeros for each ingredient
        self._fill_missing_dates_with_zeros(mock_data, all_dates)
        # Get a color palette for the lines
        color_palette = self._get_color_palette()
        # Create line data for the chart
        lines = self._create_line_data(mock_data, date_to_x, color_palette)
        # Create x-axis labels based on the number of unique dates
        x_labels = self._create_x_labels(len(all_dates))
        # Create y-axis labels for percentage values
        y_labels = self._create_y_labels()
        # Create the legend (the ingredient names with colors) for the chart
        legend = self._create_legend(mock_data, color_palette)
        # Create the line chart with the prepared data
        chart = self._create_chart(lines, x_labels, y_labels)
        # Return a Column containing the legend and the chart
        return ft.Column(controls=[legend, chart])

    # ----------------- Helper Functions -----------------

    def _parse_ingredient_data(self, data):
        """
        Parses the ingredient data from the provided JSON-like dict and returns a dictionary with ingredient names as keys
        and lists of (date, percentage) tuples as values.
        """
        mock_data = {
            "TOMATE": [
                ("2025-06-28T22:00:00.000+00:00", 9.31),
                ("2025-06-30T22:00:00.000+00:00", 9.55),
                ("2025-07-01T22:00:00.000+00:00", 0.94),
                ("2025-07-02T22:00:00.000+00:00", 0.0),
                ("2025-07-03T22:00:00.000+00:00", 10.11),
                ("2025-07-04T22:00:00.000+00:00", 3.68),
                ("2025-07-05T22:00:00.000+00:00", 13.69),
                ("2025-07-06T22:00:00.000+00:00", 10.79),
            ],
            "APF": [
                ("2025-06-28T22:00:00.000+00:00", 68.69),
                ("2025-06-30T22:00:00.000+00:00", 71.45),
                ("2025-07-01T22:00:00.000+00:00", 56.31),
                ("2025-07-02T22:00:00.000+00:00", 67.21),
                ("2025-07-0T22:00:00.000+00:00", 97.06),
                ("2025-07-041T22:00:00.000+00:00", 89.32),
                ("2025-07-05T22:00:00.000+00:00", 50.0),
                ("2025-07-06T22:00:00.000+00:00", 69.89),
            ],
            "EL": [
                ("2025-06-28T22:00:00.000+00:00", 22.0),
                ("2025-06-30T22:00:00.000+00:00", 19.0),
                ("2025-07-01T22:00:00.000+00:00", 50.0),
                ("2025-07-02T22:00:00.000+00:00", 2.0),
                ("2025-07-03T22:00:00.000+00:00", 20.0),
                ("2025-07-04T22:00:00.000+00:00", 7.0),
                ("2025-07-05T22:00:00.000+00:00", 22.0),
                ("2025-07-06T22:00:00.000+00:00", 30.0),
            ],
        }
        # Convert the data into a dictionary
        for item in data.get("data", []):
            name = item["ingredientName"]
            date = item["evaluationDate"]
            percentage = item["ingredientMeanPercentage"]
            # Create a new entry for the ingredient if it doesn't exist
            if name not in mock_data:
                mock_data[name] = []
            # Add the date and percentage to the ingredient's list
            mock_data[name].append((date, percentage))
        return mock_data

    def _get_all_dates_and_mapping(self, mock_data):
        """
        Gets all unique dates from the data and creates a mapping from date to x-axis position.
        Returns a sorted list of all dates and a dictionary mapping each date to its x-axis position
        """
        # Extract all unique dates from the data
        all_dates = sorted(
            {date for records in mock_data.values() for date, _ in records}
        )
        # Map each date to its x-axis position from 1 because 0 is reserved for the initial zero point
        date_to_x = {date: idx + 1 for idx, date in enumerate(all_dates)}
        return all_dates, date_to_x

    def _fill_missing_dates_with_zeros(self, mock_data, all_dates):
        """
        Fills in missing dates for each ingredient with a zero percentage.
        Inserts an initial zero point for each ingredient and appends missing dates with a percentage of 0.0.
        """
        for ingredient in mock_data:
            # Insert an initial zero point for each ingredient so that the chart looks cleaner
            mock_data[ingredient].insert(0, ("INITIAL_ZERO", 0.0))
            existing_dates = {date for date, _ in mock_data[ingredient]}
            for missing_date in all_dates:
                # If the date is not already in the ingredient's records, append it with a percentage of 0.0
                if missing_date not in existing_dates:
                    mock_data[ingredient].append((missing_date, 0.0))

    def _get_color_palette(self):
        """
        Returns a predefined color palette for the chart lines.
        """
        return [
            "#FF5252",
            "#4CAF50",
            "#2196F3",
            "#FFC107",
            "#9C27B0",
            "#00BCD4",
            "#FF9800",
            "#8BC34A",
            "#3F51B5",
            "#E91E63",
            "#00ACC1",
            "#CDDC39",
            "#F44336",
            "#009688",
            "#673AB7",
            "#FFEB3B",
            "#9E9E9E",
            "#795548",
            "#607D8B",
            "#E0E0E0",
            "#B2FF59",
            "#FF4081",
            "#536DFE",
            "#00E5FF",
        ]

    def _create_line_data(self, mock_data, date_to_x, color_palette):
        """
        Creates line data for the chart from the given data.
        Returns a list of LineChartData objects, each representing a line for an ingredient.
        """
        lines = []

        # Iterate over each ingredient and its records to create line data points
        for idx, (ingredient, records) in enumerate(mock_data.items()):
            # Sort the records by date
            sorted_points = sorted(records, key=lambda r: r[0])

            # Spot the first real date that is not "INITIAL_ZERO" that represents the first actual recipe version
            first_real_date = next(
                (d for d, _ in sorted_points if d != "INITIAL_ZERO"), None
            )
            if not first_real_date:
                continue

            # Get the y value for the first real date
            first_real_y = next(y for d, y in sorted_points if d == first_real_date)
            points = [ft.LineChartDataPoint(x=0, y=0.0)]
            points.append(
                ft.LineChartDataPoint(x=date_to_x[first_real_date], y=first_real_y)
            )

            # Iterate through the sorted points and create LineChartDataPoint objects for each date
            for date, y in sorted_points:
                if date in ["INITIAL_ZERO", first_real_date]:
                    continue
                points.append(ft.LineChartDataPoint(x=date_to_x[date], y=y))

            # Add an additional point to ensure the line extends to the right and the chart looks better
            last_point = points[-1]
            points.append(ft.LineChartDataPoint(x=last_point.x + 1, y=last_point.y))

            # Join the points into a line with the specified color and stroke width
            lines.append(
                ft.LineChartData(
                    data_points=points,
                    stroke_width=4,
                    curved=False,
                    color=color_palette[idx % len(color_palette)],
                )
            )
        return lines

    def _create_x_labels(self, total_dates):
        """
        Creates x-axis labels for the chart, labeling each recipe version.
        """
        return [
            ft.ChartAxisLabel(
                label=ft.Container(
                    content=(
                        ft.Text(f"Recipe {i}", color="black") if i > 0 else ft.Text("")
                    ),
                    padding=ft.padding.only(top=10),
                ),
                value=i,
            )
            for i in range(total_dates + 1)
        ]

    def _create_y_labels(self):
        """
        Creates y-axis labels for the chart, labeling percentage values from 0% to 100% in steps of 10%.
        """
        return [
            ft.ChartAxisLabel(
                value=y,
                label=ft.Container(
                    content=ft.Text(f"{y}%", color="black"),
                    padding=ft.padding.only(right=5),
                ),
            )
            for y in range(0, 110, 10)
        ]

    def _create_legend(self, mock_data, color_palette):
        """
        Creates a legend for the chart, showing ingredient names with corresponding colors.
        Returns a Container with a Row of items, each containing a colored circle and the ingredient name.
        """
        items = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=12,
                            height=12,
                            bgcolor=color_palette[idx % len(color_palette)],
                            border_radius=6,
                        ),
                        ft.Text(
                            name, size=12, color="black", weight=ft.FontWeight.BOLD
                        ),
                    ],
                    spacing=5,
                ),
                padding=ft.padding.only(right=12),
            )
            for idx, name in enumerate(mock_data)
        ]

        return ft.Container(
            content=ft.Row(controls=items), padding=ft.padding.only(left=140, bottom=10)
        )

    def _create_chart(self, lines, x_labels, y_labels):
        """
        Creates the final LineChart with the provided labels, grid lines, and styling
        """
        return ft.LineChart(
            data_series=lines,  # List of LineChartData (one line per ingredient)
            tooltip_bgcolor=ft.Colors.BLUE_GREY_100,
            bgcolor=Styles.CHART_BACKGROUND_COLOR,
            left_axis=ft.ChartAxis(
                labels=y_labels,
                labels_size=50,
                labels_interval=10,
                title=ft.Container(
                    content=ft.Text(
                        "Percentage",
                        size=16,
                        color=Styles.CHART_TEXT_PERC_AND_TIME_COLOR,
                    ),
                    alignment=ft.alignment.Alignment(0.15, -0.35),
                    expand=True,
                ),
                title_size=60,
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_size=50,
                title=ft.Text(
                    "Time", size=16, color=Styles.CHART_TEXT_PERC_AND_TIME_COLOR
                ),
                title_size=20,
            ),
            min_y=0,
            max_y=100,
            horizontal_grid_lines=ft.ChartGridLines(
                color=Styles.CHART_GRID_COORDINATE_LINES_COLOR, width=0.2
            ),  # The horizontal grid lines (so that the point values are more readable)
            vertical_grid_lines=ft.ChartGridLines(
                color=Styles.CHART_GRID_COORDINATE_LINES_COLOR, width=0.2
            ),  # The vertical grid lines (so that the point values are more readable)
            expand=True,
            height=400,
        )

    def build(self):
        """
        Builds the StatisticsView UI with product and ingredient dropdowns, a chart container, and a confirm button.
        """
        dropdown_product_data, dropdown_ingredient_data = (
            self.get_products_and_ingredients()
        )

        self.product_dropdown = self.build_dropdown(
            "Select Product", dropdown_product_data, on_change=self.on_product_select
        )
        self.ingredient_dropdown = self.build_dropdown(
            "Select Ingredient", dropdown_ingredient_data
        )
        self.ingredient_container.content = self.ingredient_dropdown

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            Styles.build_title("Make Your Selection"), # Main title
                            ft.Row(
                                controls=[
                                    self.product_dropdown,
                                    self.ingredient_container,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Confirm", on_click=self.on_confirm
                                ),
                                alignment=ft.alignment.center,
                                padding=20,
                            ),
                            self.chart_container,  # Chart placeholder
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
