"""
@author: Martony
"""
import flet as ft
from math import sqrt, pow, log10

def main(page: ft.Page):
    # App settings
    page.title = "Flet Calculator+"
    page.window.width = 320
    page.window.height = 660
    page.window.resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT  # Default theme
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 10

    # Calculator state
    current_input = "0"
    previous_value = None
    operation = None
    reset_input = False
    calculation_history = []
    scientific_mode = False

    # UI Elements
    display = ft.Text(
        value=current_input,
        size=30,
        text_align=ft.TextAlign.RIGHT,
        width=220,
        height=60
    )

    history_display = ft.Column(
        scroll="auto",
        height=100,
        spacing=5,
        controls=[]
    )

    def update_display():
        display.value = current_input
        page.update()

    def update_history():
        history_display.controls = [
            ft.Text(
                entry,
                size=16,
                color=ft.Colors.GREY_600,
                text_align=ft.TextAlign.RIGHT,
                width=280
            ) for entry in calculation_history[-3:]  # Show last 3 calculations
        ]
        page.update()

    def add_to_history(entry):
        calculation_history.append(entry)
        if len(calculation_history) > 20:  # Limit history to 10 entries
            calculation_history.pop(0)
        update_history()

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        theme_button.icon = (
            ft.Icons.LIGHT_MODE
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.Icons.DARK_MODE
        )
        page.update()

    def toggle_scientific_mode(e):
        nonlocal scientific_mode
        scientific_mode = not scientific_mode
        scientific_button.icon = (
            ft.Icons.KEYBOARD_ARROW_DOWN if scientific_mode else ft.Icons.KEYBOARD_ARROW_UP
        )
        page.update()
        build_ui()  # Rebuild UI to show/hide scientific buttons

    def button_click(e):
        nonlocal current_input, previous_value, operation, reset_input
        button_text = e.control.text

        if button_text in "0123456789":
            if reset_input:
                current_input = "0"
                reset_input = False
            if current_input == "0":
                current_input = button_text
            else:
                current_input += button_text

        elif button_text == ".":
            if reset_input:
                current_input = "0"
                reset_input = False
            if "." not in current_input:
                current_input += "."

        elif button_text == "C":
            current_input = "0"
            previous_value = None
            operation = None
            reset_input = False

        elif button_text in "+-*/^":
            if operation and not reset_input:
                calculate_result()
            operation = button_text
            previous_value = float(current_input)
            reset_input = True

        elif button_text == "=":
            calculate_result()

        elif button_text == "√":
            try:
                result = sqrt(float(current_input))
                add_to_history(f"√({current_input}) = {result}")
                current_input = format_result(result)
            except ValueError:
                current_input = "Error"

        elif button_text == "x²":
            result = pow(float(current_input), 2)
            add_to_history(f"({current_input})² = {result}")
            current_input = format_result(result)

        elif button_text == "log":
            try:
                result = log10(float(current_input))
                add_to_history(f"log({current_input}) = {result}")
                current_input = format_result(result)
            except ValueError:
                current_input = "Error"

        update_display()

    def calculate_result():
        nonlocal current_input, previous_value, operation, reset_input
        if operation and previous_value is not None:
            try:
                current_value = float(current_input)
                if operation == "+":
                    result = previous_value + current_value
                elif operation == "-":
                    result = previous_value - current_value
                elif operation == "*":
                    result = previous_value * current_value
                elif operation == "/":
                    if current_value == 0:
                        raise ZeroDivisionError
                    result = previous_value / current_value
                elif operation == "^":
                    result = pow(previous_value, current_value)

                # Format and store result
                formatted_result = format_result(result)
                add_to_history(f"{previous_value} {operation} {current_value} = {formatted_result}")
                current_input = formatted_result

            except (ZeroDivisionError, OverflowError):
                current_input = "Error"

            reset_input = True
            operation = None
            previous_value = None

    def format_result(result):
        return str(int(result)) if result.is_integer() else f"{result:.6f}".rstrip("0").rstrip(".")

    # Theme toggle button
    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        on_click=toggle_theme,
        tooltip="Toggle theme"
    )

    # Scientific mode toggle button
    scientific_button = ft.IconButton(
        icon=ft.Icons.KEYBOARD_ARROW_UP,
        on_click=toggle_scientific_mode,
        tooltip="Scientific functions"
    )

    def build_ui():
        # Standard buttons
        standard_buttons = [
            ["7", "8", "9", "C", "=",],
            ["4", "5", "6", "*", "x²"],
            ["1", "2", "3", "-", "!"],
            ["0", "/", "√", "+", "^"]
        ]

        # Scientific buttons (only shown in scientific mode)
        scientific_buttons = [
            ["(", ")", "π", "e", "ln"],
            ["DEL", "log", "tan", "cos", "sin",],
        ] if scientific_mode else []

        # Create buttons grid
        buttons_grid = ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        create_button(btn) for btn in row
                    ]
                ) for row in standard_buttons + scientific_buttons
            ]
        )

        # Clear and rebuild the page
        page.clean()
        page.add(
            ft.Row(
                controls=[theme_button, scientific_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                width=300
            ),
            history_display,
            ft.Container(
                content=display,
                padding=10,
                alignment=ft.alignment.center_right
            ),
            buttons_grid
        )

    def create_button(text):
        return ft.ElevatedButton(
            text=text,
            width=50 if len(text) < 3 else 50, 
            height=48,
            on_click=button_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                #color="#0C011FFF",
                padding=0
            )
        )
    # Initial UI build
    build_ui()

ft.app(target=main)
