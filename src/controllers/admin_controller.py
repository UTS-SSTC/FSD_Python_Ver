from enum import Enum
from typing import Dict, List

from src.controllers.base_controller import BaseController
from src.models.database import Database
from src.models.student import Student


class AdminMenuOption(str, Enum):
    CLEAR = "C"
    GROUP = "G"
    PARTITION = "P"
    REMOVE = "R"
    SHOW = "S"
    EXIT = "X"

    @classmethod
    def _missing_(cls, value):
        try:
            return next(m for m in cls if m.value == value)
        except StopIteration:
            return None


class AdminController(BaseController):
    """Controls administrative operations."""

    def __init__(self, view):
        """Initialize with view and database."""
        super().__init__(view)
        self.database = Database()

    def _get_grade_from_mark(self, mark: float) -> str:
        """Get grade letter from mark."""
        if mark >= 85:
            return "HD"
        elif mark >= 75:
            return "D"
        elif mark >= 65:
            return "C"
        elif mark >= 50:
            return "P"
        else:
            return "Z"

    def group_students(self):
        """Group and display students by average grade."""
        students = self.database.load_all_students()
        if not students:
            self.view.display_error("No students found")
            return

        # Group students by average mark grade
        grade_groups: Dict[str, List[Student]] = {}
        for student in students:
            avg_mark = student.get_average_mark()
            grade = self._get_grade_from_mark(avg_mark)

            if grade not in grade_groups:
                grade_groups[grade] = []
            grade_groups[grade].append(student)

        # Sort students within each group by average mark (descending)
        for grade in grade_groups:
            grade_groups[grade].sort(
                key=lambda s: s.get_average_mark(),
                reverse=True
            )

        self.view.display_grade_groups(grade_groups)

    def partition_students(self):
        """Partition and display students by pass/fail status."""
        students = self.database.load_all_students()
        if not students:
            self.view.display_error("No students found")
            return

        passing = [s for s in students if s.is_passing()]
        failing = [s for s in students if not s.is_passing()]

        # Sort both lists by average mark (descending)
        passing.sort(key=lambda s: s.get_average_mark(), reverse=True)
        failing.sort(key=lambda s: s.get_average_mark(), reverse=True)

        self.view.display_partitioned_students(passing, failing)

    def remove_student(self, student_id: str = None):
        """Remove a student by ID."""
        student_id = student_id or self.view.get_input("Enter student ID")
        if self.database.remove_student(student_id):
            self.view.display_success(f"Student {student_id} removed successfully!")
            return True
        else:
            self.view.display_error(f"Student {student_id} not found!")
            return False

    def clear_database(self):
        """Clear all student data."""
        if self.view.confirm_action("Are you sure you want to clear all data?"):
            self.database.clear_all()
            self.view.display_success("Database cleared successfully!")
            return True
        else:
            self.view.display_success("Operation cancelled")
            return False

    def handle_choice(self, choice: str, *args, **kwargs) -> bool:
        """Handle admin menu choices."""
        try:
            option = AdminMenuOption(choice.upper())
            if option == AdminMenuOption.CLEAR:
                self.clear_database()
            elif option == AdminMenuOption.GROUP:
                self.group_students()
            elif option == AdminMenuOption.PARTITION:
                self.partition_students()
            elif option == AdminMenuOption.REMOVE:
                self.remove_student()
            elif option == AdminMenuOption.SHOW:
                students = self.database.load_all_students()
                self.view.display_all_students(students)
            elif option == AdminMenuOption.EXIT:
                return False
        except ValueError:
            self.view.display_error("Invalid option")
        return True
