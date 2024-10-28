from enum import Enum

from src.controllers.base_controller import BaseController
from src.controllers.subject_controller import SubjectController
from src.core.constants import EMAIL_PATTERN, PASSWORD_PATTERN
from src.models.database import Database
from src.models.student import Student
from src.views.cli.student_view import StudentCliView
from src.views.cli.subject_view import SubjectCliView


class StudentMenuOption(str, Enum):
    LOGIN = "L"
    REGISTER = "R"
    EXIT = "X"

    @classmethod
    def _missing_(cls, value):
        try:
            return next(m for m in cls if m.value == value)
        except StopIteration:
            return None


class StudentController(BaseController):
    """Controls student registration and login."""

    def __init__(self, view: StudentCliView):
        """Initialize with view and database."""
        super().__init__(view)
        self.database = Database()
        self.subject_controller = SubjectController(SubjectCliView())

    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        if not EMAIL_PATTERN.match(email):
            self.view.display_error(
                "Invalid email format. Must end with @university.com"
            )
            return False
        return True

    def _validate_password(self, password: str) -> bool:
        """Validate password format."""
        if not PASSWORD_PATTERN.match(password):
            self.view.display_error(
                "Invalid password format. Must start with uppercase, "
                "contain at least 5 letters followed by 3+ digits"
            )
            return False
        return True

    def register(self):
        """Handle student registration."""
        form_data = self.view.display_registration_form()

        if not self._validate_email(form_data["email"]):
            return
        if not self._validate_password(form_data["password"]):
            return

        if self.database.get_student_by_email(form_data["email"]):
            self.view.display_error("Student already exists!")
            return

        student = Student(
            name=form_data["name"],
            email=form_data["email"],
            password=form_data["password"],
        )

        if self.database.add_student(student):
            self.view.display_success("Registration successful!")
        else:
            self.view.display_error("Registration failed!")

    def login(self):
        """Handle student login."""
        form_data = self.view.display_login_form()

        student = self.database.get_student_by_email(form_data["email"])
        if student and student.password == form_data["password"]:
            self.view.display_success("Login successful!")
            self.subject_controller.run(student)
        else:
            self.view.display_error("Invalid credentials!")

    def handle_choice(self, choice: str, *args, **kwargs) -> bool:
        """Handle student menu choices."""
        try:
            option = StudentMenuOption(choice.upper())
            if option == StudentMenuOption.LOGIN:
                self.login()
                return True
            elif option == StudentMenuOption.REGISTER:
                self.register()
                return True
            elif option == StudentMenuOption.EXIT:
                return False
        except ValueError:
            self.view.display_error("Invalid option")
        return True
