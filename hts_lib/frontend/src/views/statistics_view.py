from datetime import datetime, timedelta

import flet as ft

from backend.data_base_manager.evaluation_manager import EvaluationManager
from backend.data_base_manager.recipe_manager import RecipeManager
from backend.translation import Translation
from frontend.src.styles import Styles


class StatisticsView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.product_dropdown = ft.Dropdown()
        self.ingredient_dropdown = ft.Dropdown()
        self.status_text = ft.Text("", size=Styles.FEEDBACK_FONT_SIZE, color=Styles.TEXT_COLOR,
                                   text_align=ft.TextAlign.CENTER)
        self.chart_container = ft.Container()
        self.product_dict = {}
        self.ingredient_dict = {}
        self.ingredient_container = ft.Container()
        self.only_ingredient = False

    def get_products_and_ingredients(self):
        """Loads products and ingredients; raises if the database is unreachable."""
        self.product_dict = Translation.collect_product_dict(raise_errors=True)
        self.ingredient_dict = Translation.collect_ingredient_dict(raise_errors=True)
        dropdown_products = list(self.product_dict.keys())
        dropdown_ingredients = list(self.ingredient_dict.keys())

        return dropdown_products, dropdown_ingredients

    def build_dropdown(self, label: str, items: list[str], on_change=None):
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(item) for item in items],
            # Phones: one full-width dropdown per line.
            width=Styles.fit_width(self.page, 320, margin=64) if Styles.is_compact(self.page) else 200,
            border_color=Styles.BUTTON_FILL_COLOR,
            focused_border_color=Styles.BUTTON_FILL_COLOR,
            text_style=ft.TextStyle(color=Styles.TEXT_COLOR, size=16),
            on_change=on_change,
        )

    def on_product_select(self, e):
        """
        Limits the ingredient dropdown to the ingredients of the selected product.
        """
        selected_product_id = self.product_dict.get(self.product_dropdown.value)  # type: ignore[arg-type]
        ingredients = {}
        if selected_product_id:
            try:
                ingredient_response = RecipeManager.find_product_ingredient_list(selected_product_id)
                ingredients, _ = Translation.product_table_filter(ingredient_response.json())
            except Exception:
                self.status_text.value = "⚠️ The ingredients of this product could not be loaded."
                self.status_text.color = Styles.RED_COLOR

        self.ingredient_dropdown = self.build_dropdown("Select Ingredient", list(ingredients.keys()))
        self.ingredient_container.content = self.ingredient_dropdown
        self.page.update()

    def on_confirm(self, e):
        """
        Draws the chart for the selection:
        * product only      -> every ingredient of the product over its saved versions;
        * ingredient only   -> that ingredient across all products;
        * product + ingredient -> that ingredient in that product.
        """
        selected_product_name = self.product_dropdown.value
        selected_ingredient_name = self.ingredient_dropdown.value

        if not selected_product_name and not selected_ingredient_name:
            self.status_text.value = "⚠️ Select a product, an ingredient, or both."
            self.status_text.color = Styles.RED_COLOR
            self.page.update()
            return

        product_id = self.product_dict.get(selected_product_name) if selected_product_name else 0  # type: ignore[arg-type]
        ingredient_id = (
            self.ingredient_dict.get(selected_ingredient_name.upper()) if selected_ingredient_name else 0
        )
        self.only_ingredient = bool(selected_ingredient_name and not selected_product_name)

        if (selected_product_name and not product_id) or (selected_ingredient_name and not ingredient_id):
            self.status_text.value = "⚠️ The selection is no longer available. Please reload the page."
            self.status_text.color = Styles.RED_COLOR
            self.page.update()
            return

        self.status_text.value = "⏳ Loading statistics…"
        self.status_text.color = Styles.TEXT_COLOR
        self.page.update()

        try:
            response = EvaluationManager.find_evaluation_product_ingredient(product_id, ingredient_id)
            data = response.json() if response.status_code == 200 else {"data": []}
        except Exception:
            data = None

        if data is None:
            self.status_text.value = "⚠️ The database service is offline or still starting up. Please try again."
            self.status_text.color = Styles.RED_COLOR
            self.chart_container.content = None
        elif not data.get("data"):
            self.status_text.value = "No saved recipes for this selection yet."
            self.status_text.color = Styles.TEXT_COLOR
            self.chart_container.content = None
        else:
            self.status_text.value = ""
            self.chart_container.content = self.build_ingredient_line_chart(data)
        self.page.update()

    def on_clear(self, e):
        """Resets both dropdowns and removes the chart."""
        if isinstance(self.product_dropdown, ft.Dropdown):
            self.product_dropdown.value = None

        if isinstance(self.ingredient_dropdown, ft.Dropdown):
            self.ingredient_dropdown.value = None

        # Show all ingredients again (product selection had narrowed the list).
        self.ingredient_dropdown = self.build_dropdown("Select Ingredient", list(self.ingredient_dict.keys()))
        self.ingredient_container.content = self.ingredient_dropdown
        self.status_text.value = ""
        self.chart_container.content = None
        self.page.update()

    def build_ingredient_line_chart(self, data: dict) -> ft.Control:
        """
        Creates a styled Flet LineChart showing mean percentage of each ingredient over evaluation dates.

        Args:
            data (dict): JSON-like dict containing ingredient evaluation data.

        Returns:
            ft.Control: A Column containing the chart and the legend.
        """
        # Check the ehckbox status and parse the ingredient data from the provided JSON-like dict
        if not self.only_ingredient:
            ingredient_data, dates = self._parse_product_and_ingredient_data(data)
        else: 
            ingredient_data, dates = self._parse_only_ingredient_data(data)
        # Get all unique dates and a mapping from date to x-axis position
        all_dates, date_to_x = self._get_all_dates_and_mapping(dates)
        # Fill in missing dates with zeros for each ingredient
        self._fill_missing_dates_with_zeros(ingredient_data, all_dates)
        # Get a color palette for the lines
        color_palette = self._get_color_palette()
        # Create line data for the chart
        lines = self._create_line_data(ingredient_data, date_to_x, color_palette)
        # Create x-axis labels based on the number of unique dates
        x_labels = self._create_x_labels(len(all_dates))
        # Create y-axis labels for percentage values
        y_labels = self._create_y_labels()
        # Create the legend (the ingredient names with colors) for the chart
        legend = self._create_legend(ingredient_data, color_palette)
        # Create the line chart with the prepared data
        chart = self._create_chart(lines, x_labels, y_labels)
        # Return a Column containing the legend and the chart
        return ft.Column(controls=[legend, chart])

    # ----------------- Helper Functions -----------------

    def _parse_product_and_ingredient_data(self, data):
        """
        Parses the ingredient data from the provided JSON-like dict and returns a dictionary with ingredient names as keys
        and lists of (date, percentage) tuples as values.
        """
        ingredient_data = {}
        all_dates = set()
        
        # Convert the data into a dictionary
        for item in data.get("data", []):
            name = item["ingredientName"]
            date = item["evaluationDate"]
            percentage = item["ingredientMeanPercentage"]
            # Create a new entry for the ingredient if it doesn't exist
            if name not in ingredient_data:
                ingredient_data[name] = []
            # Add the date and percentage to the ingredient's list
            ingredient_data[name].append((date, percentage))
            all_dates.add(date)
        return ingredient_data, all_dates
    
    def _parse_only_ingredient_data(self, data):
        """
        Parses ingredient data and aligns evaluations across products.
        Assigns virtual ISO dates for evaluation rounds to keep compatibility.
        Returns:
            - product_data: dict with product names as keys and lists of (virtual_date, percentage) tuples as values
            - all_dates: set of virtual ISO dates for the x-axis
        """
        product_data = {}
        eval_rounds = {}

        # Group data by product
        for item in data.get("data", []):
            product_name = item["productName"]
            date = item["evaluationDate"]
            percentage = item["ingredientMeanPercentage"]

            if product_name not in product_data:
                product_data[product_name] = []
                eval_rounds[product_name] = []

            eval_rounds[product_name].append(date)
            product_data[product_name].append((date, percentage))

        if not eval_rounds:
            return {}, set()

        # Determine max number of evaluations
        max_evals = max(len(evals) for evals in eval_rounds.values())

        # Generate virtual ISO dates (e.g., 2025-01-01, 2025-02-01, …)
        base_date = datetime(2025, 1, 1)  # Arbitrary starting point
        virtual_dates = [
            (base_date + timedelta(days=30 * i)).date().isoformat()
            for i in range(max_evals)
        ]

        aligned_product_data = {}

        for product, records in product_data.items():
            # Sort records by actual date
            sorted_records = sorted(records, key=lambda r: datetime.fromisoformat(r[0]))
            aligned_points = []

            for i, v_date in enumerate(virtual_dates):
                if i < len(sorted_records):
                    _, percentage = sorted_records[i]
                else:
                    # Fill missing evaluations with 0.0 or None
                    percentage = 0.0
                aligned_points.append((v_date, percentage))

            aligned_product_data[product] = aligned_points

        return aligned_product_data, set(virtual_dates)
    

    def _get_all_dates_and_mapping(self, all_dates):
        """
        Gets all unique dates from the data and creates a mapping from date to x-axis position.
        Returns a sorted list of all dates and a dictionary mapping each date to its x-axis position
        """
        # Extract all unique dates from the data
        all_dates = sorted(
            all_dates,
            key=lambda d: datetime.fromisoformat(d)
        )
        # Map each date to its x-axis position from 1 because 0 is reserved for the initial zero point
        date_to_x = {date: idx + 1 for idx, date in enumerate(all_dates)}
        return all_dates, date_to_x

    def _fill_missing_dates_with_zeros(self, ingredient_data, all_dates):
        """
        Fills in missing dates for each ingredient with a zero percentage.
        Inserts an initial zero point for each ingredient and appends missing dates with a percentage of 0.0.
        """
        for ingredient in ingredient_data:
            # Insert an initial zero point for each ingredient so that the chart looks cleaner
            ingredient_data[ingredient].insert(0, ("0000-00-00T00:00:00.000+00:00", 0.0))
            existing_dates = {date for date, _ in ingredient_data[ingredient]}
            for missing_date in all_dates:
                # If the date is not already in the ingredient's records, append it with a percentage of 0.0
                if missing_date not in existing_dates:
                    ingredient_data[ingredient].append((missing_date, 0.0))

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

    def _create_line_data(self, ingredient_data, date_to_x, color_palette):
        """
        Creates line data for the chart from the given data.
        Returns a list of LineChartData objects, each representing a line for an ingredient.
        """
        lines = []

        # Iterate over each ingredient and its records to create line data points
        for idx, (ingredient, records) in enumerate(ingredient_data.items()):
            # Sort the records by date
            sorted_points = sorted(records, key=lambda r: r[0])
            
            # Check if ingredient was in first recipe (earliest date in all data)
            first_date_in_all = min(date_to_x, key=lambda d: datetime.fromisoformat(d))
            appeared_in_first_recipe = any(
                date == first_date_in_all and y > 0.0 for date, y in sorted_points
            )
            
            points = []

            # Add filler point only if ingredient was in first recipe
            if appeared_in_first_recipe:
                points.append(ft.LineChartDataPoint(x=0, y=0.0))

            # Add real data points starting from when ingredient first appeared
            for date, y in sorted_points:
                if y > 0.0:
                    points.append(ft.LineChartDataPoint(x=date_to_x[date], y=y))

            if len(points) <= 1:
                continue

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
                        ft.Text(f"{i}", color=Styles.TEXT_COLOR) if i > 0 else ft.Text("")
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

    def _create_legend(self, ingredient_data, color_palette):
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
            for idx, name in enumerate(ingredient_data)
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
                labels_interval=1,
                title=ft.Text(
                    "Saved recipes", size=16, color=Styles.CHART_TEXT_PERC_AND_TIME_COLOR
                ),
                title_size=20,
            ),
            min_y=0,
            max_y=100,
            horizontal_grid_lines=ft.ChartGridLines(
                interval=10, color=Styles.CHART_GRID_COORDINATE_LINES_COLOR, width=0.2
            ),  # one horizontal line per 10 %
            vertical_grid_lines=ft.ChartGridLines(
                interval=1, color=Styles.CHART_GRID_COORDINATE_LINES_COLOR, width=0.2
            ),  # one vertical line per saved recipe version
            expand=True,
            height=400,
        )

    def load_dropdown_data(self):
        """Fetches products and ingredients and fills the dropdowns."""
        self.status_text.value = "⏳ Loading products… The database may need up to a minute to wake up."
        self.status_text.color = Styles.TEXT_COLOR
        self.page.update()

        try:
            dropdown_product_data, dropdown_ingredient_data = self.get_products_and_ingredients()
        except Exception:
            self.status_text.value = "⚠️ The database service is offline or still starting up. Please reload the page in a moment."
            self.status_text.color = Styles.RED_COLOR
            self.page.update()
            return
        self.product_dropdown.options = [ft.dropdown.Option(item) for item in dropdown_product_data]
        self.ingredient_dropdown.options = [ft.dropdown.Option(item) for item in dropdown_ingredient_data]

        if dropdown_product_data:
            self.status_text.value = ""
        else:
            self.status_text.value = "No saved recipes yet. Save one in the Recipe Generator to see statistics."
        self.page.update()

    def build(self):
        """
        Builds the StatisticsView UI with empty dropdowns (data loads in background).
        """
        self.product_dropdown = self.build_dropdown(
            "Select Product", [], on_change=self.on_product_select
        )
        self.ingredient_dropdown = self.build_dropdown(
            "Select Ingredient", []
        )
        self.ingredient_container.content = self.ingredient_dropdown

        buttons_row = ft.Row(
            [
                Styles.build_button(
                    text="Confirm",
                    icon=ft.Icons.CHECK,
                    on_click=self.on_confirm
                ),
                Styles.build_button(
                    text="Clear",
                    icon=ft.Icons.CLEAR,
                    on_click=self.on_clear,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            Styles.build_title("Your Recipe Statistics"), # Main title
                            ft.Row(
                                controls=[
                                    self.product_dropdown,
                                    self.ingredient_container,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                                run_spacing=12,
                                wrap=Styles.is_compact(self.page),
                            ),
                            buttons_row,
                            self.status_text,
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
            spacing=20
        )
