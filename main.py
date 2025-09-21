# In main.py
import sys
import os

# Ensure project root is in path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from frontend.views.default.Academics.Classroom.Shared.classroom_home import HomePage

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    home_page = HomePage(user_role="faculty")
    home_page.show()
    sys.exit(app.exec())