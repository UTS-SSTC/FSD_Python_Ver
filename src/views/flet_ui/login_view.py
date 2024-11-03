import flet as ft

from src.controllers.student_controller import StudentController
from src.models.database import Database
from src.models.student import Student
from src.views.base_view import BaseView


class LoginView(BaseView):
    """
    Login view for student authentication and registration.
    Provides a dual-mode interface for both login and registration functionality.
    Handles form validation, user authentication, and new student registration.
    """

    def __init__(self, app_view):
        """
        Initialize the login view with all necessary components.

        Args:
            app_view: Parent application view instance for navigation and shared functionality
        """
        self.app_view = app_view
        self.page = app_view.page
        self.student_controller = StudentController(self)
        self.database = Database()

        # Flag to track whether view is in registration or login mode
        self.is_register_mode = False

        # Initialize form input fields
        # Email field - visible in both modes
        self.email_field = ft.TextField(
            label="Email",
            hint_text="Enter your email",
            width=300,
        )
        # Password field - visible in both modes
        self.password_field = ft.TextField(
            label="Password",
            hint_text="Enter your password",
            password=True,  # Hide password characters
            can_reveal_password=True,  # Allow toggling password visibility
            width=300,
        )
        # Name field - only visible in register mode
        self.name_field = ft.TextField(
            label="Name",
            hint_text="Enter your name",
            width=300,
            visible=False,
        )
        # Confirm password field - only visible in register mode
        self.confirm_password_field = ft.TextField(
            label="Confirm Password",
            hint_text="Confirm your password",
            password=True,
            can_reveal_password=True,
            width=300,
            visible=False
        )

        # Initialize persistent UI elements
        # Header text showing current mode
        self.mode_text = ft.Text("Login", size=30, text_align=ft.TextAlign.CENTER)
        # Button to switch between login and register modes
        self.mode_button = ft.TextButton(
            text="Switch to Register",
            on_click=self.switch_mode
        )
        # Main action button for login/register
        self.submit_button = ft.ElevatedButton(
            text="Login",
            on_click=self.handle_submit,
            width=200
        )
        # Button for admin access
        self.admin_button = ft.TextButton(
            text="Admin Access",
            on_click=lambda _: self.app_view.navigate_to_admin()
        )

    def switch_mode(self, e=None):
        """
        Switch between login and registration modes.
        Updates UI elements visibility and text content accordingly.
        Clears all form fields when switching modes.

        Args:
            e: Optional event parameter (not used)
        """
        self.is_register_mode = not self.is_register_mode

        # Toggle visibility of registration-specific fields
        self.name_field.visible = self.is_register_mode
        self.confirm_password_field.visible = self.is_register_mode

        # Update text content based on mode
        self.mode_text.value = "Register" if self.is_register_mode else "Login"
        self.mode_button.text = "Switch to Login" if self.is_register_mode else "Switch to Register"
        self.submit_button.text = "Register" if self.is_register_mode else "Login"

        # Clear all input fields
        self.email_field.value = ""
        self.password_field.value = ""
        self.name_field.value = ""
        self.confirm_password_field.value = ""

        self.page.update()

    def handle_submit(self, e):
        """
        Handle form submission for both login and registration.
        Delegates to appropriate handler based on current mode.

        Args:
            e: Event parameter (not used)
        """
        if self.is_register_mode:
            if self._handle_register():
                self.switch_mode()  # Switch back to login mode after successful registration
        else:
            self._handle_login()

    def display(self, data=None):
        """
        Display the login/registration form with appropriate layout.
        Creates a centered column layout with all form elements.

        Args:
            data: Optional data to display (not used in this view)
        """
        # Create main content column with all form elements
        content = ft.Column(
            controls=[
                # Title section
                ft.Container(
                    content=self.mode_text,
                    alignment=ft.alignment.center,
                ),
                # Form fields section
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.name_field,
                            self.email_field,
                            self.password_field,
                            self.confirm_password_field
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    alignment=ft.alignment.center,
                ),
                # Action buttons section
                ft.Container(
                    content=self.submit_button,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=self.mode_button,
                    alignment=ft.alignment.center,
                ),
                ft.Divider(),
                ft.Container(
                    content=self.admin_button,
                    alignment=ft.alignment.center,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        # Update the main container with the form content
        if hasattr(self.app_view, 'main_container'):
            self.app_view.main_container.content = ft.Container(
                content=content,
                width=400,  # Fixed width for consistent form layout
                padding=20,
                alignment=ft.alignment.center,
            )
        else:
            self.page.clean()
            self.page.add(content)

        self.page.update()

    def _handle_login(self):
        """
        Process login form submission.
        Validates credentials and navigates to student view on success.

        Returns:
            bool: True if login successful, False otherwise
        """
        email = self.email_field.value
        password = self.password_field.value

        # Validate required fields
        if not email:
            self.display_error("Please enter your email.")
            return False

        if not password:
            self.display_error("Please enter your password.")
            return False

        # Authenticate user
        student = self.database.get_student_by_email(email)
        if student and student.password == password:
            self.display_success("Login successful!")
            self.app_view.navigate_to_student(student)
            return True
        else:
            self.display_error("Invalid credentials!")
            return False

    def _handle_register(self):
        """
        Process registration form submission.
        Validates input fields, creates new student account if valid.

        Returns:
            bool: True if registration successful, False otherwise
        """
        # Get form values
        name = self.name_field.value
        email = self.email_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        # Validate required fields
        if not all([name, email, password, confirm_password]):
            self.display_error("All fields are required!")
            return False

        # Validate password match
        if password != confirm_password:
            self.display_error("Passwords do not match!")
            return False

        # Create student instance
        student = Student(name=name, email=email, password=password)

        # Validate email and password format
        if not self.student_controller._validate_email(email):
            return False
        if not self.student_controller._validate_password(password):
            return False

        # Check for existing account
        if self.database.get_student_by_email(email):
            self.display_error("Student already exists!")
            return False

        # Attempt to add student to database
        if self.database.add_student(student):
            self.display_success("Registration successful! Please login.")
            return True
        else:
            self.display_error("Registration failed!")
            return False

    # Interface methods that delegate to app_view
    def display_error(self, message: str):
        """Display error message via app view."""
        self.app_view.display_error(message)

    def display_success(self, message: str):
        """Display success message via app view."""
        self.app_view.display_success(message)

    def get_input(self, prompt: str) -> str:
        """Get user input via app view."""
        return self.app_view.get_input(prompt)

    def confirm_action(self, message: str) -> bool:
        """Get user confirmation via app view."""
        return self.app_view.confirm_action(message)