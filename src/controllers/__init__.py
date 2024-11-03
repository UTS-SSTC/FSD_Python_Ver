"""Controllers for the university application."""

from src.controllers.admin_controller import AdminController
from src.controllers.base_controller import BaseController
from src.controllers.student_controller import StudentController
from src.controllers.subject_controller import SubjectController
from src.controllers.university_controller import UniversityController

__all__ = [
    'BaseController',
    'UniversityController',
    'StudentController',
    'SubjectController',
    'AdminController'
]
