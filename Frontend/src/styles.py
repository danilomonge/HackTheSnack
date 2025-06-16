import flet as ft

PRIMARY_COLOR = "green"
BACKGROUND_COLOR = "#358E5D"
TEXT_COLOR = "white"

TITLE_SIZE = 40
BODY_SIZE = 18

PADDING = 20
CORNER_RADIUS = 10


def primary_button(text, icon=None, on_click=None):
    return ft.ElevatedButton(text, icon=icon, on_click=on_click)

def secondary_button(text, icon=None, on_click=None):
    return ft.OutlinedButton(text, icon=icon, on_click=on_click)



