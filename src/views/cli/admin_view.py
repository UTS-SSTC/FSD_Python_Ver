from typing import List, Dict, Any

from src.views.base_view import BaseView


class AdminCliView(BaseView):
    """CLI view for admin-related operations."""

    def display(self, data: Any = None):
        print("\nAdmin System")
        print("-" * 50)
        print("(c) clear database: Clear all data")
        print("(g) group students: Group by grade")
        print("(p) partition students: Partition PASS/FAIL")
        print("(r) remove student: Remove by ID")
        print("(s) show: Show all students")
        print("(x) exit")
        print("-" * 50)

    def _format_header(self, title: str):
        """Format a section header."""
        print(f"\n{title}")
        print("=" * 50)

    def _display_student_info(self, student):
        """Display student information in a formatted way."""
        # Basic information
        print(f"Student ID: {student.id}")
        print(f"Name: {student.name}")
        print(f"Email: {student.email}")

        # Subject information
        if student.subjects:
            print("\nEnrolled Subjects:")
            print("-" * 20)
            for subject in student.subjects:
                print(f"Subject {subject.id}")
                print(f"  Mark: {subject.mark:.1f}")
                print(f"  Grade: {subject.grade}")
            print("-" * 20)
            print(f"Average Mark: {student.get_average_mark():.1f}")
            print(f"Overall Status: {'PASS' if student.is_passing() else 'FAIL'}")
        else:
            print("\nNo subjects enrolled")
        print("\n" + "-" * 50)

    def display_all_students(self, students: List[Any]):
        """Display all students in the system."""
        if not students:
            print("\nNo students found.")
            return

        self._format_header("All Students")
        for student in students:
            self._display_student_info(student)

    def display_grade_groups(self, groups: Dict[str, List[Any]]):
        """Display students grouped by grade."""
        if not groups:
            print("\nNo students found.")
            return

        self._format_header("Students Grouped by Average Grade")

        # Display groups in specific order
        grade_order = ['HD', 'D', 'C', 'P', 'Z']
        for grade in grade_order:
            if grade in groups and groups[grade]:
                print(f"\nGrade {grade} Students:")
                print("-" * 50)

                for student in groups[grade]:
                    self._display_student_info(student)

    def display_partitioned_students(self, passing: List[Any], failing: List[Any]):
        """Display students partitioned by pass/fail status."""
        self._format_header("Student Pass/Fail Partition")

        if passing:
            print("\nPassing Students:")
            print("-" * 50)
            for student in passing:
                self._display_student_info(student)
        else:
            print("\nNo passing students.")

        if failing:
            print("\nFailing Students:")
            print("-" * 50)
            for student in failing:
                self._display_student_info(student)
        else:
            print("\nNo failing students.")

    def display_error(self, message: str):
        """Display error message."""
        print(f"\nError: {message}")

    def display_success(self, message: str):
        """Display success message."""
        print(f"\nSuccess: {message}")

    def get_input(self, prompt: str) -> str:
        """Get user input."""
        return input(f"\n{prompt}: ").strip()

    def confirm_action(self, message: str) -> bool:
        """Get user confirmation."""
        response = input(f"\n{message} (y/n): ").strip().lower()
        return response == 'y'
