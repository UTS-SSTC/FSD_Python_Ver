from typing import Dict, Any

from src.models.student import Student
from src.views.cli.base_cli_view import BaseCliView


class StudentCliView(BaseCliView):
    """CLI view for student-related operations."""

    def display(self, data: Any = None):
        self.display_header("Student System")
        self.display_menu([("l", "login"), ("r", "register"), ("x", "exit")])

    def display_registration_form(self) -> Dict[str, str]:
        """Display registration form and get input."""
        self.display_header("Student Registration")
        return {
            "name": self.get_input("Enter name"),
            "email": self.get_input("Enter email"),
            "password": self.get_input("Enter password"),
            "confirm_password": self.get_input("Enter confirm password")
        }

    def display_login_form(self) -> Dict[str, str]:
        """Display login form and get input."""
        self.display_header("Student Login")
        return {
            "email": self.get_input("Enter email"),
            "password": self.get_input("Enter password"),
        }

    def display_student_details(self, student: Student):
        """Display student details."""
        self.display_header("Student Details")
        print(f"ID: {student.id}")
        print(f"Name: {student.name}")
        print(f"Email: {student.email}")
