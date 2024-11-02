import flet as ft

from src.models.student import Student
from src.models.subject import Subject
from src.views.base_view import BaseView


class SubjectView(BaseView):
    """
    View for displaying subject details and enrollment results.
    Provides dialog-based interfaces for:
    - Showing enrollment results
    - Displaying student's enrolled subjects
    - Viewing academic performance summaries
    """

    def __init__(self, app_view):
        """
        Initialize the subject view.

        Args:
            app_view: Parent application view for navigation and shared functionality
        """
        self.app_view = app_view
        self.page = app_view.page

    def display_enrolment_result(self, subject: Subject):
        """
        Display a dialog showing the results of a successful subject enrollment.
        Shows subject ID, mark, and grade for the newly enrolled subject.

        Args:
            subject (Subject): The newly enrolled subject with its assigned details
        """
        # Create content column with enrollment details
        content = ft.Column(
            controls=[
                ft.Text("Subject Enrollment Result", size=20),
                ft.Text(f"Subject ID: {subject.id}"),
                ft.Text(f"Mark: {subject.mark:.1f}"),  # Format mark to 1 decimal place
                ft.Text(f"Grade: {subject.grade}"),
            ],
            spacing=10
        )

        # Create and show success dialog
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Enrollment Successful"),
            content=content,
            actions=[
                # Close dialog using lambda function to set open property
                ft.TextButton("Close", on_click=lambda e: setattr(self.page.dialog, 'open', False))
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def display_subjects(self, student: Student):
        """
        Display a dialog showing all enrolled subjects for a student.
        Includes subject details and overall performance summary if subjects exist.

        Args:
            student (Student): The student whose subjects to display
        """
        # Create main content column with scrollable layout
        content = ft.Column(
            controls=[ft.Text("Enrolled Subjects", size=20)],
            scroll=ft.ScrollMode.AUTO  # Enable scrolling for many subjects
        )

        if not student.subjects:
            # Display message when no subjects are enrolled
            content.controls.append(ft.Text("No subjects enrolled"))
        else:
            # Add each subject's details
            for subject in student.subjects:
                content.controls.append(
                    ft.Text(f"Subject {subject.id}: Mark = {subject.mark:.1f}, Grade = {subject.grade}")
                )

            # Calculate and add performance summary
            avg_mark = student.get_average_mark()
            content.controls.extend([
                ft.Text(""),  # Blank line separator
                ft.Text(f"Average Mark: {avg_mark:.1f}"),
                ft.Text(f"Status: {'PASS' if student.is_passing() else 'FAIL'}")
            ])

        # Create and show dialog with subject information
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Subject Details"),
            content=content,
            actions=[
                # Close dialog using lambda function to set open property
                ft.TextButton("Close", on_click=lambda e: setattr(self.page.dialog, 'open', False))
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def display(self, data=None):
        """
        Display subject view (not used directly).
        This view only provides dialog-based displays triggered by other views.

        Args:
            data: Optional data parameter (unused)
        """
        pass

    # Interface methods that delegate to app_view

    def display_error(self, message: str):
        """
        Display an error message using the app view's error display mechanism.

        Args:
            message (str): Error message to display
        """
        self.app_view.display_error(message)

    def display_success(self, message: str):
        """
        Display a success message using the app view's success display mechanism.

        Args:
            message (str): Success message to display
        """
        self.app_view.display_success(message)

    def get_input(self, prompt: str) -> str:
        """
        Get user input using the app view's input mechanism.

        Args:
            prompt (str): Prompt message to display to the user

        Returns:
            str: User input text
        """
        return self.app_view.get_input(prompt)

    def confirm_action(self, message: str) -> bool:
        """
        Get user confirmation using the app view's confirmation mechanism.

        Args:
            prompt (str): Confirmation message to display

        Returns:
            bool: True if user confirms, False otherwise
        """
        return self.app_view.confirm_action(message)