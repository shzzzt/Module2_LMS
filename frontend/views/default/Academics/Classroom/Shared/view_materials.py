from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QMenu
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
import os

class ViewMaterial(QWidget):
    back_clicked = pyqtSignal()  # Signal to return to main page

    def __init__(self, material_data, user_role, parent=None):
        super().__init__(parent)
        self.material_data = material_data
        self.user_role = user_role  # Store user role (e.g., "student", "faculty", "admin")
        self.load_ui()
        self.populate_data()

    def load_ui(self):
        """Load the ViewMaterial UI file"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/view_material.ui')
        uic.loadUi(ui_file, self)

    def populate_data(self):
        """Populate the UI with material data"""
        self.title_label.setText(self.material_data.get("title", "Desktop Project Guidelines"))
        self.instructor_label.setText(self.material_data.get("instructor", "Carlos Fidel Castro"))
        self.date_label.setText("• " + self.material_data.get("date", "August 18, 2025"))
        self.descriptionEdit.setText(self.material_data.get("description", "This is the material description..."))
        attachment = self.material_data.get("attachment", "Desktop Project Guidelines.pdf")
        self.attachmentName.setText(attachment.split('.')[0])  # Filename without extension
        self.attachmentType.setText("." + attachment.split('.')[-1])  # File type
        self.backButton.mousePressEvent = self.go_back  # Back button click
        self.attachmentFrame.mousePressEvent = self.preview_attachment
        self.menuButton.clicked.connect(self.show_menu)
        self.pushButton.clicked.connect(self.send_comment)

        # Ensure descriptionEdit is read-only (already set in UI file, but confirm)
        self.descriptionEdit.setReadOnly(True)

        # Ensure backButton icon is displayed (it's a QLabel with pixmap in UI)
        self.backButton.setScaledContents(True)
        pixmap = QPixmap(":/icons/back2.png")
        if pixmap.isNull():
            print("Warning: back2.png not found or invalid in resources!")
            self.backButton.setText("< Back")  # Fallback to text if icon fails
        else:
            self.backButton.setPixmap(pixmap)
            print("back2.png loaded successfully")

    def go_back(self, event):
        """Handle back button click to emit back_clicked signal"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.back_clicked.emit()

    def preview_attachment(self, event):
        """Handle click to preview attachment"""
        if event.button() == Qt.MouseButton.LeftButton:
            attachment = self.material_data.get("attachment", "Desktop Project Guidelines.pdf")
            print(f"Previewing {attachment}...")  # Replace with actual preview logic

    def show_menu(self):
        """Show options menu based on user role"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 4px 0px;
            }
            QMenu::item {
                padding: 8px 16px;
                font-size: 13px;
            }
            QMenu::item:selected {
                background-color: #f5f5f5;
            }
        """)
        if self.user_role in ["faculty", "admin"]:
            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)
            menu.addAction(edit_action)
            menu.addAction(delete_action)
        # Optionally, add other actions for all roles here (e.g., "View Details")
        button_pos = self.menuButton.mapToGlobal(self.menuButton.rect().bottomLeft())
        menu.exec(button_pos)

    def send_comment(self):
        """Handle send button click for comments (placeholder)"""
        comment = self.commentBox.toPlainText().strip()
        if comment:
            print(f"Sending comment: {comment}")  # Replace with actual comment submission logic
            self.commentBox.clear()

    def update_data(self, material_data):
        """Update the widget with new material data"""
        self.material_data = material_data
        self.populate_data()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    material_data = {
        "title": "Desktop Project Guidelines",
        "instructor": "Carlos Fidel Castro",
        "date": "August 18, 2025",
        "description": "Please ensure that the task is completed according to the requirements provided, keeping everything consistent and aligned throughout the process. Make sure to follow the necessary steps as outlined, review your work before finalizing, and confirm that it meets the expected standards. Always double-check that the format is correct, the details are accurate, and the output follows the general guidelines. Be mindful of maintaining a clear structure, avoid unnecessary errors, and ensure that the submission is properly prepared before turning it in.",
        "attachment": "Desktop project guidelines.pdf"
    }
    view_material = ViewMaterial(material_data, "faculty")
    view_material.setFixedSize(1030, 634)
    view_material.show()
    sys.exit(app.exec())