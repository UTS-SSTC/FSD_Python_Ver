"""Flet UI views for the university application."""

from src.views.flet_ui.admin_view import AdminView
from src.views.flet_ui.app_view import AppView
from src.views.flet_ui.login_view import LoginView
from src.views.flet_ui.student_view import StudentView
from src.views.flet_ui.subject_view import SubjectView

__all__ = [
    'AppView',
    'LoginView',
    'AdminView',
    'StudentView',
    'SubjectView'
]
