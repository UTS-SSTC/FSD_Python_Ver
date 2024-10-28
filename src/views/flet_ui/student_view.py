from typing import Optional

import flet as ft

from src.controllers.subject_controller import SubjectController
from src.core.constants import PASSWORD_PATTERN
from src.models.student import Student
from src.views.base_view import BaseView


class StudentView(BaseView):
    """Student view for managing enrollments and account."""

    def __init__(self, app_view):
        self.app_view = app_view
        self.page = app_view.page
        self.subject_controller = SubjectController(self)
        self.current_student: Optional[Student] = None

        # Create UI controls
        self.subjects_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Mark")),
                ft.DataColumn(ft.Text("Grade")),
            ],
            rows=[]
        )

    def display(self, student: Student):
        """Display the student view."""
        self.current_student = student
        self.subject_controller.current_student = student

        def handle_enroll(e):
            if len(student.subjects) >= Student.MAX_SUBJECTS:
                self.display_error(f"Maximum subjects ({Student.MAX_SUBJECTS}) already enrolled!")
                return
            self.subject_controller.enrol_subject()
            self._refresh_subjects()

        def handle_remove(e):
            if not self.current_student.subjects:
                self.display_error("No subjects to remove!")
                return

            def handle_cancel(e):
                dlg.open = False
                self.page.update()

            def handle_remove_confirm(e):
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
            def handle_cancel(e):
                dlg.open = False
                self.page.update()

            def handle_change_confirm(e):
                dlg.open = False
                new_password = password_field.value
                if new_password:
                    if not PASSWORD_PATTERN.match(new_password):
                        self.display_error(
                            "Invalid password format! Must start with uppercase, "
                            "contain at least 5 letters followed by 3+ digits"
                        )
                        return

                    # Update password in current student object
                    self.current_student.password = new_password

                    # Save to database
                    if self.subject_controller.database.update_student(self.current_student):
                        self.display_success("Password changed successfully!")
                    else:
                        self.display_error("Failed to update password in database!")
                else:
                    self.display_error("Password cannot be empty!")
                self.page.update()

            password_field = ft.TextField(
                label="New Password",
                hint_text="Start with uppercase, 5+ letters, 3+ digits",
                password=True,
                can_reveal_password=True,
                width=300
            )

            dlg = ft.AlertDialog(
                title=ft.Text("Change Password"),
                content=ft.Column([
                    ft.Text("Password Requirements:"),
                    ft.Text("• Must start with an uppercase letter"),
                    ft.Text("• Must contain at least 5 letters"),
                    ft.Text("• Must end with 3 or more digits"),
                    ft.Text("Example: Password123"),
                    password_field
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
            # 清理当前学生状态
            self.current_student = None
            self.subject_controller.current_student = None

            # 返回登录页面
            self.app_view.navigate_to_login()

        # Create main content
        content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(f"Welcome, {student.name}!", size=30),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Text(f"Student ID: {student.id}", size=16),
                    alignment=ft.alignment.center,
                ),
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
                ft.Container(
                    content=ft.Text("Enrolled Subjects:", size=20),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=self.subjects_table,
                    alignment=ft.alignment.center,
                    padding=20,
                ),
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

        # Update main container content
        if hasattr(self.app_view, 'main_container'):
            self.app_view.main_container.content = ft.Container(
                content=content,
                expand=True,
                alignment=ft.alignment.center,
            )
        else:
            self.page.clean()
            self.page.add(content)

        self._refresh_subjects()
        self.page.update()

    def _refresh_subjects(self):
        """Refresh the subjects table."""
        self.subjects_table.rows.clear()

        for subject in self.current_student.subjects:
            self.subjects_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(subject.id)),
                        ft.DataCell(ft.Text(f"{subject.mark:.1f}")),
                        ft.DataCell(ft.Text(subject.grade)),
                    ]
                )
            )

        if self.current_student.subjects:
            avg_mark = self.current_student.get_average_mark()
            status = "PASS" if self.current_student.is_passing() else "FAIL"
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

        self.page.update()

    def display_enrolment_result(self, subject):
        """Display the result of subject enrollment."""

        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        content = ft.Column(
            controls=[
                ft.Text("Subject Enrollment Result", size=20),
                ft.Text(f"Subject ID: {subject.id}"),
                ft.Text(f"Mark: {subject.mark:.1f}"),
                ft.Text(f"Grade: {subject.grade}"),
            ],
            spacing=10
        )

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Enrollment Successful"),
            content=content,
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def display_error(self, message: str):
        """Display error message."""
        self.app_view.display_error(message)

    def display_success(self, message: str):
        """Display success message."""
        self.app_view.display_success(message)

    def get_input(self, prompt: str) -> str:
        """Get user input."""
        return self.app_view.get_input(prompt)

    def confirm_action(self, message: str) -> bool:
        """Get user confirmation."""
        return self.app_view.confirm_action(message)