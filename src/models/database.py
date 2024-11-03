import json
import os
from typing import List, Optional

from src.models.student import Student


class Database:
    """Handles persistence of student data to/from file storage."""

    DEFAULT_PATH = "students.data"

    def __init__(self, filename: str = None):
        """Initialize database with specified filename."""
        self.filename = filename or self.DEFAULT_PATH
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the data file if it doesn't exist."""
        # No need to create directories, just create file if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def load_all_students(self) -> List[Student]:
        """Load all students from the database file."""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [Student.from_dict(student_data) for student_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_all_students(self, students: List[Student]):
        """Save all students to the database file."""
        with open(self.filename, "w") as f:
            json.dump([s.to_dict() for s in students], f, indent=2)

    def add_student(self, student: Student) -> bool:
        """Add a new student to the database."""
        students = self.load_all_students()
        if any(s.email == student.email for s in students):
            return False
        students.append(student)
        self.save_all_students(students)
        return True

    def get_student_by_email(self, email: str) -> Optional[Student]:
        """Find a student by email address."""
        students = self.load_all_students()
        for student in students:
            if student.email == email:
                return student
        return None

    def update_student(self, student: Student) -> bool:
        """Update an existing student's information."""
        students = self.load_all_students()
        for i, s in enumerate(students):
            if s.id == student.id:
                students[i] = student
                self.save_all_students(students)
                return True
        return False

    def remove_student(self, student_id: str) -> bool:
        """Remove a student from the database by ID."""
        students = self.load_all_students()
        initial_count = len(students)
        students = [s for s in students if s.id != student_id]
        if len(students) < initial_count:
            self.save_all_students(students)
            return True
        return False

    def clear_all(self):
        """Remove all students from the database."""
        self.save_all_students([])
