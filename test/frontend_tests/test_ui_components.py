import sys
import os
import httpx


from frontend.src.add_product_table.table_ui.product_table_ui import ProductTableUI
from frontend.src.add_product_table.table_ui.ingredient_row_manager import IngredientRowManager
from backend.data_base_manager.product_manager import ProductManager
from frontend.src.product_action_handler import ProductActionHandler
from frontend.src import product_action_handler


import flet as ft

class Page:
    def __init__(self):
        self.updated = False
        self.controls = [] #?
        self.views = []

    def update(self, *args, **kwargs):
        self.updated = True

    def add(self, *controls):
        self.controls.extend(controls)
        for control in controls:
            self._add_control_to_page(control)
    
    def _add_control_to_page(self, control):
        """Recursively add controls to the mock page"""
        try:
            # Set the page reference for the control
            control._Control__page = self
            
            # Handle different control types that might have nested controls
            if hasattr(control, 'controls') and control.controls:
                for child_control in control.controls:
                    self._add_control_to_page(child_control)
            
            if hasattr(control, 'content') and control.content:
                if hasattr(control.content, 'controls'):
                    for child_control in control.content.controls:
                        self._add_control_to_page(child_control)
                else:
                    self._add_control_to_page(control.content)
                    
        except (AttributeError, TypeError):
            # Some controls might not have the expected structure
            pass

def test_clear_all_functionality():
    """Tests if Clear All button properly resets all UI elements"""
    # Setup
    page = Page()
    ui = ProductTableUI(page) # type: ignore[arg-type]
    
    ui_controls = ui.build_table_ui()
    page.add(ui_controls)

    ui.product_name.value = "Test Product"
    ui.ingredient_manager.add_ingredient_row(page) # type: ignore[arg-type]
    ui.ingredient_manager.add_ingredient_row(page) # type: ignore[arg-type]
    
    assert len(ui.ingredient_manager.ingredients) == 2
    assert ui.product_name.value == "Test Product"
    
    ui.on_clearall_click()
    ui.on_add_click() 

    assert len(ui.ingredient_manager.ingredients) == 1 
    assert ui.product_name.value == ""
    assert page.updated

def test_add_ingredient_functionality():
    """Tests if Add Ingredient button creates new rows correctly"""
    page = Page()
    ui = ProductTableUI(page) # type: ignore[arg-type]
    ui_controls = ui.build_table_ui()
    page.add(ui_controls)
    
    initial_count = len(ui.ingredient_manager.ingredients)
    ui.on_add_click()
    
    assert len(ui.ingredient_manager.ingredients) == initial_count + 1
    assert page.updated


def test_submit_with_valid_data():
    """Tests submission with valid ingredient data"""
    page = Page()
    ui = ProductTableUI(page) # type: ignore[arg-type]
    ui_controls = ui.build_table_ui()
    page.add(ui_controls)
    
    ui.product_name.value = "Test Product"
    ui.ingredient_manager.add_ingredient_row(page) # type: ignore[arg-type]
    name_field = ui.ingredient_manager.ingredients[0].content.controls[0].content
    perc_field = ui.ingredient_manager.ingredients[0].content.controls[1].content.controls[1]

    name_field.value = "Test Ingredient"
    perc_field.value = "100"
    
    ui.on_submit_click()
    assert ui.feedback.value == "✅ Product is valid. Recipe generated!"

def _fill_row(ui, page, name, percentage):
    ui.ingredient_manager.add_ingredient_row(page)  # type: ignore[arg-type]
    row = ui.ingredient_manager.ingredients[-1]
    row.content.controls[0].content.value = name
    row.content.controls[1].content.controls[1].value = percentage


def _ui_with_page():
    page = Page()
    ui = ProductTableUI(page)  # type: ignore[arg-type]
    page.add(ui.build_table_ui())
    return ui, page


def test_save_is_disabled_until_a_recipe_was_generated():
    ui, page = _ui_with_page()
    assert ui.save_button.disabled is True

    ui.product_name.value = "Peanut Butter"
    _fill_row(ui, page, "Peanuts", "90")
    _fill_row(ui, page, "Salt", "10")
    ui.on_submit_click()

    assert ui.save_button.disabled is False
    assert set(ui.result_dict) == {"Peanuts", "Salt"}

    # Any edit invalidates the generated recipe.
    ui.on_user_input_change(None)
    assert ui.save_button.disabled is True


def test_search_click_shows_friendly_message_when_backend_offline(monkeypatch):
    def offline(_name):
        raise httpx.ConnectError("Connection refused")

    monkeypatch.setattr(ProductManager, "find_product", staticmethod(offline))
    ui, page = _ui_with_page()
    ui.product_name.value = "queso"
    ui.on_find_product_click(None)

    assert "offline" in ui.feedback.value.lower()
    assert ui.search_button.disabled is False  # the user can retry
    assert ui.loading_indicator.visible is False
    assert page.updated


def test_search_without_name_asks_for_one():
    ui, _ = _ui_with_page()
    ui.product_name.value = "   "
    ui.on_find_product_click(None)
    assert "please enter a product name" in ui.feedback.value.lower()


def test_save_reports_success_and_stays_disabled(monkeypatch):
    ui, page = _ui_with_page()
    ui.product_name.value = "Peanut Butter"
    _fill_row(ui, page, "Peanuts", "90")
    _fill_row(ui, page, "Salt", "10")
    ui.on_submit_click()

    saved = {}

    def fake_submit_recipe(name, result_dict):
        saved["name"] = name
        saved["ingredients"] = list(result_dict)
        return 7, [1, 2], [10, 11]

    class Created:
        status_code = 201

    monkeypatch.setattr(product_action_handler.RecipeManager, "submit_recipe", staticmethod(fake_submit_recipe))
    monkeypatch.setattr(
        product_action_handler.EvaluationManager, "create_evaluation", staticmethod(lambda *a: Created())
    )

    assert ui.on_save_recipe_click(None) is True
    assert saved == {"name": "Peanut Butter", "ingredients": ["Peanuts", "Salt"]}
    assert ui.feedback.value.startswith("✅")
    assert ui.product_id == 7 and ui.recipe_ids == [10, 11]
    assert ui.save_button.disabled is True


def test_save_reports_failure_and_allows_retry(monkeypatch):
    ui, page = _ui_with_page()
    ui.product_name.value = "Peanut Butter"
    _fill_row(ui, page, "Peanuts", "100")
    ui.on_submit_click()

    def offline(*_args):
        raise httpx.ConnectTimeout("timed out")

    monkeypatch.setattr(product_action_handler.RecipeManager, "submit_recipe", staticmethod(offline))

    assert ui.on_save_recipe_click(None) is False
    assert "offline" in ui.feedback.value.lower()
    assert ui.save_button.disabled is False


def test_autofill_loads_ingredient_names_in_order(monkeypatch):
    ui, page = _ui_with_page()
    ui.product_name.value = "peanut butter"

    class Found:
        status_code = 200

        @staticmethod
        def json():
            return {"data": {"id": 5, "name": "PEANUT BUTTER"}}

    class Recipes:
        status_code = 200

        @staticmethod
        def json():
            return {"data": [
                {"idRecipe": 1, "idProduct": 5, "idIngredient": 3, "nameIngredient": "PEANUTS"},
                {"idRecipe": 2, "idProduct": 5, "idIngredient": 4, "nameIngredient": "SEA SALT"},
            ]}

    monkeypatch.setattr(ProductManager, "find_product", staticmethod(lambda name: Found()))
    monkeypatch.setattr(
        product_action_handler.RecipeManager, "find_product_ingredient_list", staticmethod(lambda pid: Recipes())
    )

    ui._on_autofill_confirmed()

    names = [row.content.controls[0].content.value for row in ui.ingredient_manager.ingredients]
    assert names == ["Peanuts", "Sea salt"]
    assert ui.product_id == 5
    assert ui.save_button.disabled is True  # percentages must be entered and submitted first


def test_user_friendly_error_message_for_connection_failure():
    message = ProductActionHandler.get_user_friendly_error_message(
        httpx.ConnectError("Connection refused")
    )

    assert "offline" in message.lower()

    
