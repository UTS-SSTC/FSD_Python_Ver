from typing import Dict, List

import flet as ft

from src.controllers.admin_controller import AdminController
from src.models.student import Student
from src.views.base_view import BaseView


class AdminView(BaseView):
    """
    Admin view for managing students and viewing statistics.
    This class provides a GUI interface for administrative functions such as:
    - Viewing all students and their details
    - Grouping students by grades
    - Partitioning students by pass/fail status
    - Removing students from the system
    - Clearing the entire database
    """

    def __init__(self, app_view):
        """
        Initialize the admin view with necessary components.

        Args:
            app_view: The main application view instance for navigation and shared functionality
        """
        self.app_view = app_view
        self.page = app_view.page
        self.admin_controller = AdminController(self)

        # Initialize the data table for displaying student information
        # Each column represents different aspects of student data
        self.student_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Average")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Subjects")),
            ],
            column_spacing=20,
            heading_row_height=40,
            data_row_min_height=100,
            data_row_max_height=200,
            horizontal_margin=20,
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            rows=[]
        )

    def _get_mark_color(self, mark: float) -> str:
        """
        Determine the color to display for a given mark based on grade thresholds.

        Args:
            mark (float): The numerical mark to evaluate

        Returns:
            str: Color code for the mark:
                - Green for >= 85 (HD)
                - Blue for >= 75 (D)
                - Orange for >= 65 (C)
                - Orange_700 for >= 50 (P)
                - Red for < 50 (Z/Fail)
        """
        if mark >= 85:
            return ft.colors.GREEN
        elif mark >= 75:
            return ft.colors.BLUE
        elif mark >= 65:
            return ft.colors.ORANGE
        elif mark >= 50:
            return ft.colors.ORANGE_700
        return ft.colors.RED

    def _get_grade_color(self, grade: str) -> str:
        """
        Get the display color for a given grade letter.

        Args:
            grade (str): The grade letter (HD, D, C, P, Z)

        Returns:
            str: Corresponding color code for the grade
        """
        grade_colors = {
            'HD': ft.colors.GREEN,
            'D': ft.colors.BLUE,
            'C': ft.colors.ORANGE,
            'P': ft.colors.ORANGE_700,
            'Z': ft.colors.RED
        }
        return grade_colors.get(grade, ft.colors.BLACK)

    def display(self, data=None):
        """
        Display the main admin interface with all controls and tables.
        Creates a dashboard layout with buttons for various administrative actions
        and a table to display student data.

        Args:
            data: Optional data to display (not used in current implementation)
        """

        # Event handler for showing all students
        def handle_show_students(e):
            """Load and display all students in the system"""
            self.page.show_loading = True
            self.page.update()
            try:
                students = self.admin_controller.database.load_all_students()
                self.display_all_students(students)
            finally:
                self.page.show_loading = False
                self.page.update()

        # Event handler for grouping students by grade
        def handle_group_students(e):
            """Group and display students by their average grade"""
            self.page.show_loading = True
            self.page.update()
            try:
                self.admin_controller.group_students()
            finally:
                self.page.show_loading = False
                self.page.update()

        # Event handler for partitioning students by pass/fail status
        def handle_partition_students(e):
            """Partition and display students by pass/fail status"""
            self.page.show_loading = True
            self.page.update()
            try:
                self.admin_controller.partition_students()
            finally:
                self.page.show_loading = False
                self.page.update()

        # Event handler for removing a student
        def handle_remove_student(e):
            """Show dialog for removing a student by ID"""

            def handle_remove_confirm(e):
                """Process the student removal after confirmation"""
                nonlocal student_id_field
                dialog.open = False
                self.page.update()

                student_id = student_id_field.value
                if student_id:
                    self.page.show_loading = True
                    self.page.update()
                    try:
                        if self.admin_controller.database.remove_student(student_id):
                            self.display_success(f"Student {student_id} removed successfully!")
                            handle_show_students(None)
                        else:
                            self.display_error(f"Student {student_id} not found!")
                    finally:
                        self.page.show_loading = False
                        self.page.update()

            def handle_remove_cancel(e):
                """Cancel the remove operation"""
                dialog.open = False
                self.page.update()

            # Create and show the remove student dialog
            student_id_field = ft.TextField(
                label="Student ID",
                hint_text="Enter student ID to remove",
                width=300
            )

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Remove Student"),
                content=ft.Column([
                    ft.Text("Please enter the ID of the student to remove:"),
                    student_id_field,
                ], tight=True),
                actions=[
                    ft.TextButton("Cancel", on_click=handle_remove_cancel),
                    ft.TextButton("Remove", on_click=handle_remove_confirm),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        # Event handler for clearing the database
        def handle_clear_database(e):
            """Show confirmation dialog for clearing the entire database"""

            def handle_clear_confirm(e):
                """Process the database clear after confirmation"""
                dialog.open = False
                self.page.update()

                self.page.show_loading = True
                self.page.update()
                try:
                    self.admin_controller.database.clear_all()
                    self.display_success("Database cleared successfully!")
                    self.student_list.rows.clear()
                    self.page.update()
                except Exception as ex:
                    self.display_error(f"Error clearing database: {str(ex)}")
                finally:
                    self.page.show_loading = False
                    self.page.update()

            def handle_clear_cancel(e):
                """Cancel the clear operation"""
                dialog.open = False
                self.page.update()

            # Create and show the clear database confirmation dialog
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Clear Database"),
                content=ft.Text(
                    "Are you sure you want to clear all data? This action cannot be undone!"
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=handle_clear_cancel),
                    ft.TextButton(
                        "Clear All",
                        on_click=handle_clear_confirm,
                        style=ft.ButtonStyle(
                            color={"": ft.colors.RED}
                        )
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        # Event handler for navigating back to login
        def handle_back(e):
            """Return to the login screen"""
            self.app_view.navigate_to_login()

        # Create all the action buttons
        show_button = ft.ElevatedButton(
            text="Show All Students",
            on_click=handle_show_students
        )
        group_button = ft.ElevatedButton(
            text="Group by Grade",
            on_click=handle_group_students
        )
        partition_button = ft.ElevatedButton(
            text="Partition Pass/Fail",
            on_click=handle_partition_students
        )
        remove_button = ft.ElevatedButton(
            text="Remove Student",
            on_click=handle_remove_student
        )
        clear_button = ft.ElevatedButton(
            text="Clear Database",
            color=ft.colors.RED,
            on_click=handle_clear_database
        )
        back_button = ft.TextButton(
            text="Back to Login",
            on_click=handle_back
        )

        # Configure the data table with proper column settings
        self.student_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID"), numeric=False),
                ft.DataColumn(ft.Text("Name"), numeric=False),
                ft.DataColumn(ft.Text("Email"), numeric=False),
                ft.DataColumn(ft.Text("Average"), numeric=True),
                ft.DataColumn(ft.Text("Status"), numeric=False),
                ft.DataColumn(ft.Text("Subjects"), numeric=False),
            ],
            column_spacing=20,
            heading_row_height=40,
            data_row_min_height=100,
            data_row_max_height=200,
            horizontal_margin=20,
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            rows=[],
        )

        # Create a scrollable container for the data table
        table_container = ft.Container(
            content=self.student_list,
            padding=ft.padding.all(20),
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            expand=True,
            alignment=ft.alignment.center,
        )

        # Create a container for the action buttons
        button_row = ft.Container(
            content=ft.Row(
                controls=[
                    show_button,
                    group_button,
                    partition_button,
                    remove_button,
                    clear_button,
                ],
                wrap=True,
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=20),
        )

        # Create the main content column with title, buttons, and table
        main_column = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Admin Dashboard",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=20),
                ),
                button_row,
                ft.Container(
                    content=ft.Column(
                        controls=[table_container],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=back_button,
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=20),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        # Create the main container with fixed width
        main_content = ft.Container(
            content=main_column,
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.all(20),
            width=1200,
        )

        # Update the page content
        if hasattr(self.app_view, 'main_container'):
            self.app_view.main_container.content = main_content
        else:
            self.page.clean()
            self.page.add(main_content)

        self.page.update()

    def display_all_students(self, students: List[Student]):
        """
        Display all students in the data table with formatted cells and styling.

        Args:
            students (List[Student]): List of students to display
        """
        self.student_list.rows.clear()

        if not students:
            self.display_error("No students found")
            return

        try:
            for student in students:
                avg_mark = student.get_average_mark()
                is_passing = student.is_passing()

                # Create a data row for each student with formatted cells
                self.student_list.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(student.id),
                                    padding=ft.padding.all(5),
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(student.name),
                                    padding=ft.padding.all(5),
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(student.email),
                                    padding=ft.padding.all(5),
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(
                                        f"{avg_mark:.1f}",
                                        color=self._get_mark_color(avg_mark),
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    padding=ft.padding.all(5),
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(
                                        "PASS" if is_passing else "FAIL",
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    bgcolor=ft.colors.GREEN if is_passing else ft.colors.RED,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                    border_radius=3,
                                    alignment=ft.alignment.center,
                                )
                            ),
                            ft.DataCell(self._format_subject_details(student)),
                        ]
                    )
                )

        except Exception as e:
            self.display_error(f"Error displaying students: {str(e)}")
        finally:
            self.page.update()

    def _format_subject_details(self, student: Student) -> ft.Container:
        """
        Create a formatted container displaying detailed subject information for a student.

        This method creates a visually structured layout showing each subject's details
        including ID, mark, and grade, with appropriate styling and color coding.

        Args:
            student (Student): The student whose subject details are to be displayed

        Returns:
            ft.Container: A formatted container with all subject information, scrollable
                         if there are many subjects
        """
        subject_rows = []

        if student.subjects:
            for subject in subject.subjects:
                # Create a container for each subject with header and details
                subject_info = ft.Container(
                    content=ft.Column([
                        # Subject ID header with background
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    f"Subject {subject.id}",
                                    weight=ft.FontWeight.BOLD,
                                    size=14
                                ),
                                bgcolor=ft.colors.BLUE_GREY_50,
                                padding=5,
                                border_radius=3
                            )
                        ]),
                        # Mark and Grade information row
                        ft.Row([
                            # Mark container with color coding
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Mark: "),
                                    ft.Text(
                                        f"{subject.mark:.1f}",
                                        color=self._get_mark_color(subject.mark),
                                        weight=ft.FontWeight.BOLD
                                    )
                                ]),
                                padding=5
                            ),
                            # Grade container with color coding
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Grade: "),
                                    ft.Text(
                                        subject.grade,
                                        color=self._get_grade_color(subject.grade),
                                        weight=ft.FontWeight.BOLD
                                    )
                                ]),
                                padding=5
                            )
                        ])
                    ]),
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=5,
                    margin=ft.margin.only(bottom=5),
                    padding=5
                )
                subject_rows.append(subject_info)
        else:
            # Display message when no subjects are enrolled
            subject_rows.append(
                ft.Container(
                    content=ft.Text(
                        "No subjects enrolled",
                        italic=True,
                        color=ft.colors.GREY_700
                    ),
                    padding=10
                )
            )

        # Return a scrollable container with all subject information
        return ft.Container(
            content=ft.Column(
                controls=subject_rows,
                spacing=5,
                scroll=ft.ScrollMode.AUTO
            ),
            width=300
        )

    def display_grade_groups(self, grade_groups: Dict[str, List[Student]]):
        """
        Display students grouped by their average grades in a modal dialog.

        Creates a scrollable dialog showing students organized by grade categories
        (HD, D, C, P, Z) with detailed information for each student.

        Args:
            grade_groups (Dict[str, List[Student]]): Dictionary mapping grade
                categories to lists of students in that grade range
        """
        dialog = None

        def close_dialog(e):
            """Close the grade groups dialog"""
            dialog.open = False
            self.page.update()

        # Create main content container for the dialog
        content = ft.Column(
            controls=[ft.Text("Students Grouped by Average Grade", size=20)],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=400
        )

        try:
            # Display grades in descending order
            grade_order = ['HD', 'D', 'C', 'P', 'Z']

            for grade in grade_order:
                if grade in grade_groups and grade_groups[grade]:
                    # Create header for each grade category
                    content.controls.append(
                        ft.Container(
                            content=ft.Text(
                                f"Grade {grade}",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            ),
                            bgcolor=ft.colors.BLUE_GREY_100,
                            padding=10,
                            border_radius=5
                        )
                    )

                    # Add detailed information for each student in this grade group
                    for student in grade_groups[grade]:
                        student_info = ft.Container(
                            content=ft.Column([
                                ft.Text(f"ID: {student.id}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Name: {student.name}"),
                                ft.Text(f"Email: {student.email}"),
                                ft.Text(f"Average Mark: {student.get_average_mark():.1f}"),
                                ft.Text("Subjects:", weight=ft.FontWeight.BOLD),
                                # List all subjects with their marks and grades
                                ft.Column([
                                    ft.Text(
                                        f"  Subject {subject.id}: Mark = {subject.mark:.1f}, Grade = {subject.grade}"
                                    ) for subject in student.subjects
                                ], spacing=2)
                            ]),
                            padding=10,
                            border=ft.border.all(1, ft.colors.GREY_400),
                            border_radius=5,
                            margin=ft.margin.only(bottom=10)
                        )
                        content.controls.append(student_info)

            # Create and display the dialog
            dialog = ft.AlertDialog(
                title=ft.Text("Grade Groups"),
                content=content,
                actions=[
                    ft.TextButton("Close", on_click=close_dialog)
                ],
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        except Exception as e:
            self.display_error(f"Error displaying grade groups: {str(e)}")

    def display_partitioned_students(self, passing: List[Student], failing: List[Student]):
        """
        Display students partitioned into passing and failing groups.

        Creates a modal dialog showing two sections: passing and failing students,
        with detailed information for each student and color coding for visual distinction.

        Args:
            passing (List[Student]): List of students with passing average marks (≥50)
            failing (List[Student]): List of students with failing average marks (<50)
        """
        dialog = None

        def close_dialog(e):
            """Close the partition dialog"""
            dialog.open = False
            self.page.update()

        # Create main content container
        content = ft.Column(
            controls=[ft.Text("Students by Pass/Fail Status", size=20)],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=400
        )

        try:
            def create_student_container(student: Student, status: str):
                """
                Create a formatted container for student information.

                Args:
                    student (Student): Student to display
                    status (str): "Passing" or "Failing"

                Returns:
                    ft.Container: Formatted container with student details
                """
                return ft.Container(
                    content=ft.Column([
                        ft.Text(f"ID: {student.id}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"Name: {student.name}"),
                        ft.Text(f"Email: {student.email}"),
                        ft.Text(
                            f"Average Mark: {student.get_average_mark():.1f}",
                            color=ft.colors.GREEN if status == "Passing" else ft.colors.RED
                        ),
                        ft.Text("Subjects:", weight=ft.FontWeight.BOLD),
                        ft.Column([
                            ft.Text(
                                f"  Subject {subject.id}: Mark = {subject.mark:.1f}, Grade = {subject.grade}"
                            ) for subject in student.subjects
                        ], spacing=2)
                    ]),
                    padding=10,
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=5,
                    margin=ft.margin.only(bottom=10)
                )

            # Add passing students section with green background
            content.controls.append(
                ft.Container(
                    content=ft.Text("Passing Students", size=18, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.GREEN_100,
                    padding=10,
                    border_radius=5
                )
            )
            for student in passing:
                content.controls.append(create_student_container(student, "Passing"))

            # Add failing students section with red background
            content.controls.append(
                ft.Container(
                    content=ft.Text("Failing Students", size=18, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.RED_100,
                    padding=10,
                    border_radius=5
                )
            )
            for student in failing:
                content.controls.append(create_student_container(student, "Failing"))

            # Create and display the dialog
            dialog = ft.AlertDialog(
                title=ft.Text("Pass/Fail Partition"),
                content=content,
                actions=[
                    ft.TextButton("Close", on_click=close_dialog)
                ],
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        except Exception as e:
            self.display_error(f"Error displaying partitioned students: {str(e)}")

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
            str: User input string
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
