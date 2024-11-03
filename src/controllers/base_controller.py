from abc import ABC, abstractmethod

from src.views.base_view import BaseView


class BaseController(ABC):
    """Abstract base controller providing common functionality."""

    def __init__(self, view: BaseView):
        """Initialize controller with a view."""
        self.view = view

    @abstractmethod
    def handle_choice(self, choice: str, *args, **kwargs) -> bool:
        """Handle user menu choice."""
        pass

    def run(self, *args, **kwargs):
        """Run the controller's main loop."""
        running = True
        while running:
            self.view.display()
            choice = self.view.get_input("Enter your choice")
            running = self.handle_choice(choice, *args, **kwargs)
