import flet as ft
from frontend.src.styles import Styles

class AutofillConfirmationWindow:
    def __init__(self, page: ft.Page, on_confirm, on_cancel=None):
        self.page = page
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Product found!"),
            content=ft.Text("Do you want to autofill the ingredient table?"),
            actions=[
                ft.TextButton(
                    "Yes",
                    on_click=self._handle_confirm,
                    style=ft.ButtonStyle(
                        color=Styles.ICON_COLOR,
                    )
                ),
                ft.TextButton(
                    "No",
                    on_click=self._handle_cancel,
                    style=ft.ButtonStyle(
                        color=Styles.ICON_COLOR,
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _handle_confirm(self, e):
        self.dialog.open = False
        self.page.update()
        if self.on_confirm:
            self.on_confirm()

    def _handle_cancel(self, e):
        self.dialog.open = False
        self.page.update()
        if self.on_cancel:
            self.on_cancel()

    def show_dialog(self):
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()