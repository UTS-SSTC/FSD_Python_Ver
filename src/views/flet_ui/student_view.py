from typing import Optional

import flet as ft

from src.controllers.subject_controller import SubjectController
from src.core.constants import PASSWORD_PATTERN
from src.models.student import Student
from src.views.base_view import BaseView


class StudentView(BaseView):
    """
    Student view for managing enrollments and account settings.
    Provides interface for:
    - Viewing enrolled subjects and grades
    - Managing subject enrollment
    - Changing password
    - Viewing academic performance
    """

    def __init__(self, app_view):
        """
        Initialize the student view with necessary components.

        Args:
            app_view: Parent application view for navigation and shared functionality
        """
        self.app_view = app_view
        self.page = app_view.page
        self.subject_controller = SubjectController(self)
        self.current_student: Optional[Student] = None

        # Initialize subjects table with columns for ID, Mark, and Grade
        self.subjects_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Mark")),
                ft.DataColumn(ft.Text("Grade")),
            ],
            rows=[]
        )

    def display(self, student: Student):
        """
        Display the student dashboard with all functionality.

        Args:
            student (Student): The student whose information to display
        """
        # Store current student context
        self.current_student = student
        self.subject_controller.current_student = student

        def handle_enroll(e):
            """
            Handle subject enrollment request.
            Checks maximum subject limit before proceeding.
            """
            if len(student.subjects) >= Student.MAX_SUBJECTS:
                self.display_error(f"Maximum subjects ({Student.MAX_SUBJECTS}) already enrolled!")
                return
            self.subject_controller.enrol_subject()
            self._refresh_subjects()

        def handle_remove(e):
            """
            Handle subject removal request.
            Shows dialog with current subjects and removal confirmation.
            """
            if not self.current_student.subjects:
                self.display_error("No subjects to remove!")
                return

            def handle_cancel(e):
                """Close the removal dialog"""
                dlg.open = False
                self.page.update()

            def handle_remove_confirm(e):
                """Process subject removal after confirmation"""
                dlg.open = False
                subject_id = text_field.value
                if subject_id:
                    if self.current_student.remove_subject(subject_id):
                        if self.subject_controller.database.update_student(self.current_student):
                            self.display_success(f"Subject {subject_id} removed successfully!")
                            self._refresh_subjects()
                        else:
                            self.display_error("Failed to update database!")
                    else:
                        self.display_error(f"Subject {subject_id} not found!")
                self.page.update()

            # Create subject removal dialog
            text_field = ft.TextField(
                label="Subject ID",
                hint_text="Enter subject ID to remove"
            )

            dlg = ft.AlertDialog(
                title=ft.Text("Remove Subject"),
                content=ft.Column([
                    ft.Text("Currently enrolled subjects:"),
                    ft.Column([
                        ft.Text(f"ID: {subject.id}, Grade: {subject.grade}, Mark: {subject.mark:.1f}")
                        for subject in self.current_student.subjects
                    ]),
                    text_field
                ]),
                actions=[
                    ft.TextButton("Cancel", on_click=handle_cancel),
                    ft.TextButton("Remove", on_click=handle_remove_confirm),
                ],
            )

            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

        def handle_change_password(e):
            """
            Handle password change request.
            Shows dialog with password requirements and validation.
            """

            def handle_cancel(e):
                """Close the password change dialog"""
                dlg.open = False
                self.page.update()

            def handle_change_confirm(e):
                """
                Process password change after validation.
                Checks:
                - All fields filled
                - Passwords match
                - Old password correct
                - New password meets requirements
                """
                dlg.open = False
                old_password = old_password_field.value
                new_password = password_field.value
                confirm_password = confirm_password_field.value

                if all([old_password, new_password, confirm_password]):
                    # Validate password change
                    if new_password != confirm_password:
                        self.display_error("Passwords do not match!")
                        return
                    if old_password != self.current_student.password:
                        self.display_error("Old passwords error!")
                        return
                    if new_password == self.current_student.password:
                        self.display_error("Old passwords cannot be used!")
                        return
                    if not PASSWORD_PATTERN.match(new_password):
                        self.display_error(
                            "Invalid password format! Must start with uppercase, "
                            "contain at least 5 letters followed by 3+ digits"
                        )
                        return

                    # Update password
                    self.current_student.password = new_password
                    if self.subject_controller.database.update_student(self.current_student):
                        self.display_success("Password changed successfully!")
                    else:
                        self.display_error("Failed to update password in database!")
                else:
                    self.display_error("All fields are required!")
                self.page.update()

            # Create password change form fields
            old_password_field = ft.TextField(
                label="Old Password",
                hint_text="Enter your old password",
                password=True,
                can_reveal_password=True,
                width=300
            )

            password_field = ft.TextField(
                label="New Password",
                hint_text="Start with uppercase, 5+ letters, 3+ digits",
                password=True,
                can_reveal_password=True,
                width=300
            )

            confirm_password_field = ft.TextField(
                label="Confirm New Password",
                hint_text="Reenter your new password",
                password=True,
                can_reveal_password=True,
                width=300
            )

            # Create password change dialog
            dlg = ft.AlertDialog(
                title=ft.Text("Change Password"),
                content=ft.Column([
                    ft.Text("Password Requirements:"),
                    ft.Text("• Must start with an uppercase letter"),
                    ft.Text("• Must contain at least 5 letters"),
                    ft.Text("• Must end with 3 or more digits"),
                    ft.Text("Example: Password123"),
                    old_password_field,
                    password_field,
                    confirm_password_field
                ]),
                actions=[
                    ft.TextButton("Cancel", on_click=handle_cancel),
                    ft.TextButton("Change", on_click=handle_change_confirm),
                ],
            )

            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

        def handle_logout(e):
            """
            Handle logout request.
            Clears current student state and returns to login view.
            """
            self.current_student = None
            self.subject_controller.current_student = None
            self.app_view.navigate_to_login()

        # Create main content layout
        content = ft.Column(
            controls=[
                # Welcome header
                ft.Container(
                    content=ft.Text(f"Welcome, {student.name}!", size=30),
                    alignment=ft.alignment.center,
                ),
                # Student ID display
                ft.Container(
                    content=ft.Text(f"Student ID: {student.id}", size=16),
                    alignment=ft.alignment.center,
                ),
                # Action buttons row
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Enroll in Subject",
                                on_click=handle_enroll
                            ),
                            ft.ElevatedButton(
                                text="Remove Subject",
                                on_click=handle_remove
                            ),
                            ft.ElevatedButton(
                                text="Change Password",
                                on_click=handle_change_password
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    alignment=ft.alignment.center,
                ),
                # Subjects section
                ft.Container(
                    content=ft.Text("Enrolled Subjects:", size=20),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=self.subjects_table,
                    alignment=ft.alignment.center,
                    padding=20,
                ),
                # Logout button
                ft.Container(
                    content=ft.TextButton(
                        text="Logout",
                        on_click=handle_logout
                    ),
                    alignment=ft.alignment.center,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        # Update main container
        if hasattr(self.app_view, 'main_container'):
            self.app_view.main_container.content = ft.Container(
                content=content,
                expand=True,
                alignment=ft.alignment.center,
            )
        else:
            self.page.clean()
            self.page.add(content)

        # Initialize subjects table
        self._refresh_subjects()
        self.page.update()

    def _refresh_subjects(self):
        """
        Refresh the subjects table display with current enrollment data.
        Shows all enrolled subjects with their marks and grades.
        Adds a summary row with average mark and pass/fail status if subjects exist.
        """
        # Clear existing rows from table
        self.subjects_table.rows.clear()

        # Add a row for each enrolled subject
        for subject in self.current_student.subjects:
            self.subjects_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(subject.id)),
                        ft.DataCell(ft.Text(f"{subject.mark:.1f}")),  # Format mark to 1 decimal place
                        ft.DataCell(ft.Text(subject.grade)),
                    ]
                )
            )

        # Add summary row if student has any subjects
        if self.current_student.subjects:
            avg_mark = self.current_student.get_average_mark()
            status = "PASS" if self.current_student.is_passing() else "FAIL"
            # Add summary row with average mark and colored pass/fail status
            self.subjects_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Average", italic=True)),
                        ft.DataCell(ft.Text(f"{avg_mark:.1f}", italic=True)),
                        ft.DataCell(
                            ft.Text(
                                status,
                                color=ft.colors.GREEN if status == "PASS" else ft.colors.RED
                            )
                        ),
                    ]
                )
            )

        # Update the page to reflect changes
        self.page.update()

    def display_enrolment_result(self, subject):
        """
        Display a dialog showing the results of a successful subject enrollment.

        Args:
            subject: The newly enrolled subject with its assigned mark and grade
        """

        def close_dialog(e):
            """Close the enrollment result dialog"""
            self.page.dialog.open = False
            self.page.update()

        # Create content showing subject details
        content = ft.Column(
            controls=[
                ft.Text("Subject Enrollment Result", size=20),
                ft.Text(f"Subject ID: {subject.id}"),
                ft.Text(f"Mark: {subject.mark:.1f}"),  # Format mark to 1 decimal place
                ft.Text(f"Grade: {subject.grade}"),
            ],
            spacing=10
        )

        # Create and show the success dialog
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Enrollment Successful"),
            content=content,
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ],
        )
        self.page.dialog.open = True
        self.page.update()

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
            message (str): Confirmation message to display

        Returns:
            bool: True if user confirms, False otherwise
        """
        return self.app_view.confirm_action(message)