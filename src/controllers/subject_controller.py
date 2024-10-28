from enum import Enum

from src.controllers.base_controller import BaseController
from src.core.constants import PASSWORD_PATTERN
from src.models.database import Database
from src.models.student import Student
from src.models.subject import Subject
from src.views.cli.subject_view import SubjectCliView


class SubjectMenuOption(str, Enum):
    CHANGE = "C"
    ENROL = "E"
    REMOVE = "R"
    SHOW = "S"
    EXIT = "X"

    @classmethod
    def _missing_(cls, value):
        try:
            return next(m for m in cls if m.value == value)
        except StopIteration:
            return None


class SubjectController(BaseController):
    """Controls subject enrollment and management."""

    def __init__(self, view: SubjectCliView):
        """Initialize with view and database."""
        super().__init__(view)
        self.database = Database()
        self.current_student = None

    def run(self, student: Student):
        """Run with specific student context."""
        self.current_student = student
        super().run()

    def enrol_subject(self):
        """Handle subject enrollment."""
        if len(self.current_student.subjects) >= Student.MAX_SUBJECTS:
            self.view.display_error(
                f"Maximum subjects ({Student.MAX_SUBJECTS}) already enrolled!"
            )
            return

        subject = Subject()
        if self.current_student.enrol_subject(subject):
            self.database.update_student(self.current_student)
            self.view.display_enrolment_result(subject)
        else:
            self.view.display_error("Failed to enrol in subject!")

    def remove_subject(self):
        """Handle subject removal."""
        subject_id = self.view.get_input("Enter subject ID to remove")

        if self.current_student.remove_subject(subject_id):
            self.database.update_student(self.current_student)
            self.view.display_success(f"Subject {subject_id} removed successfully!")
        else:
            self.view.display_error(f"Subject {subject_id} not found!")

    def change_password(self):
        """Handle password change."""
        new_password = self.view.get_input("Enter new password")

        if not PASSWORD_PATTERN.match(new_password):
            self.view.display_error("Invalid password format!")
            return

        self.current_student.password = new_password
        if self.database.update_student(self.current_student):
            self.view.display_success("Password changed successfully!")
        else:
            self.view.display_error("Failed to change password!")

    def handle_choice(self, choice: str, *args, **kwargs) -> bool:
        """Handle subject menu choices."""
        try:
            option = SubjectMenuOption(choice.upper())
            if option == SubjectMenuOption.CHANGE:
                self.change_password()
            elif option == SubjectMenuOption.ENROL:
                self.enrol_subject()
            elif option == SubjectMenuOption.REMOVE:
                self.remove_subject()
            elif option == SubjectMenuOption.SHOW:
                self.view.display_subjects(self.current_student)
            elif option == SubjectMenuOption.EXIT:
                return False
        except ValueError:
            self.view.display_error("Invalid option")
        return True
