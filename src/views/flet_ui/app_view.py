from typing import Optional

import flet as ft

from src.models.student import Student
from src.views.base_view import BaseView
from src.views.flet_ui.admin_view import AdminView
from src.views.flet_ui.login_view import LoginView
from src.views.flet_ui.student_view import StudentView


class AppView(BaseView):
    """
    Main application view that handles navigation and state management.
    Acts as a container and coordinator for all sub-views (login, admin, student).
    Provides common functionality for dialogs, notifications, and layout management.
    """

    def __init__(self, page: ft.Page):
        """
        Initialize the application view with necessary components and configuration.

        Args:
            page (ft.Page): The main Flet page instance for the application
        """
        self.page = page
        # Track the currently active view and student
        self.current_view: Optional[ft.View] = None
        self.current_student: Optional[Student] = None

        # Initialize all sub-views with reference to this AppView
        self.login_view = LoginView(self)
        self.admin_view = AdminView(self)
        self.student_view = StudentView(self)

        # Configure the main window properties
        self.page.title = "University Application"
        self.page.window_width = 1000
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.window_resizable = True
        self.page.window_maximizable = True
        self.page.window_minimizable = True

        # Set up page layout and styling
        self.page.padding = 20
        self.page.spacing = 20
        self.page.scroll = ft.ScrollMode.ADAPTIVE  # Enable adaptive scrolling
        self.page.theme_mode = ft.ThemeMode.LIGHT  # Set light theme

        # Create main container for centered layout
        self.main_container = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
        )

        # Add main container to the page
        self.page.add(self.main_container)

    def initialize(self):
        """Initialize the application by navigating to the login view."""
        self.navigate_to_login()

    def navigate_to_login(self):
        """
        Switch to login view.
        Clears current student state and updates the view.
        """
        self.current_view = self.login_view
        self._update_view()

    def navigate_to_admin(self):
        """
        Switch to admin view.
        Provides access to administrative functions.
        """
        self.current_view = self.admin_view
        self._update_view()

    def navigate_to_student(self, student: Student):
        """
        Switch to student view for a specific student.

        Args:
            student (Student): The student whose view should be displayed
        """
        self.current_student = student
        self.current_view = self.student_view
        self._update_view(student)

    def _update_view(self, data=None):
        """
        Update the current view with proper layout and content.

        Creates a new content container and updates the main container
        with the current view's content.

        Args:
            data: Optional data to pass to the view's display method
        """
        # Clear existing content
        self.main_container.content = None

        # Create new content container with centered column layout
        content = ft.Container(
            content=ft.Column(
                controls=[],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            width=900,
            padding=20,
        )

        # Update main container with new content
        self.main_container.content = content

        # Display current view if one is set
        if self.current_view:
            self.current_view.display(data)

        self.page.update()

    def display(self, data=None):
        """
        Implement abstract display method from BaseView.

        Delegates display to current active view since AppView
        is a container view.

        Args:
            data: Optional data to pass to the current view
        """
        if self.current_view:
            self.current_view.display(data)
        self.page.update()

    def display_error(self, message: str):
        """
        Display an error message in a modal dialog.

        Args:
            message (str): Error message to display
        """

        def close_dlg(_):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dlg)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def display_success(self, message: str):
        """
        Display a success message in a temporary snackbar.

        Args:
            message (str): Success message to display
        """
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.colors.GREEN_700,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def get_input(self, prompt: str) -> str:
        """
        Get user input via a modal dialog with a text field.

        Args:
            prompt (str): Prompt message to display to the user

        Returns:
            str: User input text, or empty string if cancelled
        """
        result = None

        def close_dlg(e):
            """Handle dialog close and save result"""
            nonlocal result
            result = text_field.value if e.control.text == "OK" else None
            dlg.open = False
            self.page.update()

        # Create input field and dialog
        text_field = ft.TextField(
            label=prompt,
            width=300,
            autofocus=True
        )
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(prompt),
            content=text_field,
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Show dialog and wait for result
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
        return result if result is not None else ""

    def confirm_action(self, message: str) -> bool:
        """
        Get user confirmation via a Yes/No dialog.

        Args:
            message (str): Confirmation message to display

        Returns:
            bool: True if user confirms (Yes), False otherwise (No)
        """
        result = False

        def handle_response(e):
            """Handle user response and save result"""
            nonlocal result
            result = e.control.text == "Yes"
            dlg.open = False
            self.page.update()

        # Create confirmation dialog
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Action"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("No", on_click=handle_response),
                ft.TextButton("Yes", on_click=handle_response),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Show dialog and wait for result
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
        return result