"""Data models for the university application."""

from src.models.base_model import BaseModel
from src.models.database import Database
from src.models.student import Student
from src.models.subject import Subject

__all__ = ["BaseModel", "Student", "Subject", "Database"]
