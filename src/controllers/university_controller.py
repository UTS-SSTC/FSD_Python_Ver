from enum import Enum

from src.controllers.admin_controller import AdminController
from src.controllers.base_controller import BaseController
from src.controllers.student_controller import StudentController
from src.views.cli.admin_view import AdminCliView
from src.views.cli.student_view import StudentCliView
from src.views.cli.university_view import UniversityCliView


class UniversityMenuOption(str, Enum):
    ADMIN = "A"
    STUDENT = "S"
    EXIT = "X"

    @classmethod
    def _missing_(cls, value):
        try:
            return next(m for m in cls if m.value == value)
        except StopIteration:
            return None


class UniversityController(BaseController):
    """Controls the main university system menu and navigation."""

    def __init__(self):
        """Initialize with views and sub-controllers."""
        super().__init__(UniversityCliView())
        self.student_controller = StudentController(StudentCliView())
        self.admin_controller = AdminController(AdminCliView())

    def handle_choice(self, choice: str, *args, **kwargs) -> bool:
        """Handle university menu choices."""
        try:
            option = UniversityMenuOption(choice.upper())
            if option == UniversityMenuOption.ADMIN:
                self.admin_controller.run()
                return True
            elif option == UniversityMenuOption.STUDENT:
                self.student_controller.run()
                return True
            elif option == UniversityMenuOption.EXIT:
                self.view.display_success("Goodbye!")
                return False
        except ValueError:
            self.view.display_error("Invalid option")
        return True
