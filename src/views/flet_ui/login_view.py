import flet as ft

from src.controllers.student_controller import StudentController
from src.models.database import Database
from src.models.student import Student
from src.views.base_view import BaseView


class LoginView(BaseView):
    """Login view for student authentication and registration."""

    def __init__(self, app_view):
        self.app_view = app_view
        self.page = app_view.page
        self.student_controller = StudentController(self)
        self.database = Database()

        # Track current mode
        self.is_register_mode = False

        # Create UI controls
        self.email_field = ft.TextField(
            label="Email",
            hint_text="Enter your email",
            width=300,
        )
        self.password_field = ft.TextField(
            label="Password",
            hint_text="Enter your password",
            password=True,
            can_reveal_password=True,
            width=300,
        )
        self.name_field = ft.TextField(
            label="Name",
            hint_text="Enter your name",
            width=300,
            visible=False,
        )

        # Create persistent UI elements
        self.mode_text = ft.Text("Login", size=30, text_align=ft.TextAlign.CENTER)
        self.mode_button = ft.TextButton(
            text="Switch to Register",
            on_click=self.switch_mode
        )
        self.submit_button = ft.ElevatedButton(
            text="Login",
            on_click=self.handle_submit,
            width=200
        )
        self.admin_button = ft.TextButton(
            text="Admin Access",
            on_click=lambda _: self.app_view.navigate_to_admin()
        )

    def switch_mode(self, e=None):
        """Switch between login and register modes."""
        self.is_register_mode = not self.is_register_mode

        # Update UI elements
        self.name_field.visible = self.is_register_mode
        self.mode_text.value = "Register" if self.is_register_mode else "Login"
        self.mode_button.text = "Switch to Login" if self.is_register_mode else "Switch to Register"
        self.submit_button.text = "Register" if self.is_register_mode else "Login"

        # Clear fields
        self.email_field.value = ""
        self.password_field.value = ""
        self.name_field.value = ""

        self.page.update()

    def handle_submit(self, e):
        """Handle form submission."""
        if self.is_register_mode:
            if self._handle_register():
                self.switch_mode()
        else:
            self._handle_login()

    def display(self, data=None):
        """Display the login view."""
        # Create main content
        content = ft.Column(
            controls=[
                ft.Container(
                    content=self.mode_text,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.name_field,
                            self.email_field,
                            self.password_field,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    alignment=ft.alignment.center,
                ),
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

        # Update main container content
        if hasattr(self.app_view, 'main_container'):
            self.app_view.main_container.content = ft.Container(
                content=content,
                width=400,  # Set a fixed width for the login form
                padding=20,
                alignment=ft.alignment.center,
            )
        else:
            self.page.clean()
            self.page.add(content)

        self.page.update()

    def _handle_login(self):
        """Handle login form submission."""
        email = self.email_field.value
        password = self.password_field.value

        if not all([email, password]):
            self.display_error("All fields are required!")
            return False

        student = self.database.get_student_by_email(email)
        if student and student.password == password:
            self.display_success("Login successful!")
            self.app_view.navigate_to_student(student)
            return True
        else:
            self.display_error("Invalid credentials!")
            return False

    def _handle_register(self):
        """Handle registration form submission."""
        name = self.name_field.value
        email = self.email_field.value
        password = self.password_field.value

        if not all([name, email, password]):
            self.display_error("All fields are required!")
            return False

        # Create a new student instance
        student = Student(name=name, email=email, password=password)

        # Validate email and password format
        if not self.student_controller._validate_email(email):
            return False
        if not self.student_controller._validate_password(password):
            return False

        # Check if student already exists
        if self.database.get_student_by_email(email):
            self.display_error("Student already exists!")
            return False

        # Add student to database
        if self.database.add_student(student):
            self.display_success("Registration successful! Please login.")
            return True
        else:
            self.display_error("Registration failed!")
            return False

    def display_error(self, message: str):
        """Display error message."""
        self.app_view.display_error(message)

    def display_success(self, message: str):
        """Display success message."""
        self.app_view.display_success(message)

    def get_input(self, prompt: str) -> str:
        """Get user input."""
        return self.app_view.get_input(prompt)

    def confirm_action(self, message: str) -> bool:
        """Get user confirmation."""
        return self.app_view.confirm_action(message)