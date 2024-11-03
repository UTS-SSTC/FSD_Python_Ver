# FSD Python Implementation

> A complete implementation of the FSD assignment with fully functional CLI & GUI interfaces.

## Architecture Overview

This project follows the MVC (Model-View-Controller) architectural pattern:

- **Models** (Shared between CLI & GUI)
  - Student: Manages student data and enrollment logic
  - Subject: Handles subject information and grading
  - Database: Provides data persistence using file storage
- **Controllers** (Shared between CLI & GUI)

  - UniversityController: Manages main system navigation
  - StudentController: Handles student registration and authentication
  - SubjectController: Controls subject enrollment operations
  - AdminController: Manages administrative functions

- **Views** (Separate implementations)
  - CLI: Traditional command-line interface
  - GUI: Modern graphical interface using Flet UI framework

## Technical Requirements

- **IDE**: PyCharm (>=2024.2)
- **Python**: 3.11.9
- **Key Dependencies**:
  - Flet: Modern UI framework for Python

## Installation & Setup

1. Clone the repository:

```bash
git clone [repository is not public]
cd fsd-python
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

The application provides two interface options:

### CLI Version

```bash
python cli_main.py
```

### GUI Version

```bash
python flet_main.py
```

## Features

1. **Student Management**

   - Registration with email validation
   - Secure login system
   - Password management
   - Subject enrollment (max 4 subjects)

2. **Admin Functions**

   - View all students
   - Group students by grade
   - Partition students (Pass/Fail)
   - Remove students
   - Clear database

3. **Data Persistence**
   - File-based storage using students.data
   - CRUD operations for student records
   - Automatic file creation and management

## Development Guidelines

1. **Code Style**

   - Follow PEP 8 guidelines
   - Use type hints where applicable
   - Document classes and complex functions

2. **Git Commit Convention**

   - Follow [gitmoji](https://gitmoji.dev/) convention
   - Format: `<emoji> <description>`

3. **Pull Requests**
   - Create feature branches
   - Provide clear descriptions
   - Reference related issues

## Project Structure

```
src/
├── controllers/     # Application logic
├── models/         # Data models
├── views/          # User interfaces
│   ├── cli/       # Command line views
│   └── flet_ui/   # GUI views
├── core/           # Core utilities
├── cli_main.py    # CLI entry point
└── flet_main.py   # GUI entry point
```

## Common Issues & Solutions

1. **Database File Location**

   - The students.data file is created in the project root
   - Ensure write permissions in the directory

2. **GUI Display Issues**

   - Check Flet version compatibility
   - Verify screen resolution settings

3. **Virtual Environment**
   - Always use the project's virtual environment
   - Ensure all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of an academic assignment and should be used accordingly.

## Support

For issues and questions:

1. Check existing issues in the repository
2. Create a new issue with detailed description
3. Use appropriate labels
