import sys
from pathlib import Path


def setup_environment():
    """Set up the environment for the application."""
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Database file will be created in project root
    return project_root  # 直接返回项目根目录


def main():
    """Main entry point for the CLI application."""
    try:
        data_dir = setup_environment()

        # Import after environment setup
        from src.controllers.university_controller import UniversityController
        from src.models.database import Database

        # Set database file path relative to src directory
        Database.DEFAULT_PATH = "students.data"  # 文件将直接在 src 目录下创建

        # Run application
        controller = UniversityController()
        controller.run()

        return 0
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
