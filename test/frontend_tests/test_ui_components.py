import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hts_lib.frontend.src.add_product_table.table_ui.product_table_ui import ProductTableUI
from hts_lib.frontend.src.add_product_table.table_ui.ingredient_row_manager import IngredientRowManager


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

    