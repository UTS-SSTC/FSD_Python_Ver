import flet as ft

from src.views.flet_ui.app_view import AppView


def main(page: ft.Page):
    """Main entry point for the GUI application."""
    try:
        # Create and initialize app view
        app = AppView(page)
        app.initialize()
    except Exception as e:
        print(f"Error initializing application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    ft.app(target=main)
