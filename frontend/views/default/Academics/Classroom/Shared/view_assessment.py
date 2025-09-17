from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QMenu
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt
import os

class ViewAssessment(QWidget):
    def __init__(self, assessment_data, parent=None):
        super().__init__(parent)
        self.assessment_data = assessment_data  # e.g., {"title": "Assessment Title", "instructor": "Carlos Fidel Castro", "date": "August 18, 2025", "description": "...", "attachment": "assessment.pdf", "score": "10"}
        self.load_ui()
        self.populate_data()

    def load_ui(self):
        """Load the ViewAssessment UI file"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/view_assessment.ui')
        uic.loadUi(ui_file, self)

    def populate_data(self):
        """Populate the UI with assessment data"""
        self.title_label.setText(self.assessment_data.get("title", "Assessment Title"))
        self.instructor_label.setText(self.assessment_data.get("instructor", "Carlos Fidel Castro"))
        self.date_label.setText("• " + self.assessment_data.get("date", "August 18, 2025"))
        self.descriptionEdit.setText(self.assessment_data.get("description", "This is the assessment description..."))
        attachment = self.assessment_data.get("attachment", "assessment.pdf")
        self.attachmentName.setText(attachment.split('.')[0])  # Filename without extension
        self.attachmentType.setText("." + attachment.split('.')[-1])  # File type
        self.score_label.setText(self.assessment_data.get("score", "10") + " points")
        self.backButton.mousePressEvent = self.go_back  # Back button click
        self.attachmentFrame.mousePressEvent = self.preview_attachment
        self.menuButton.clicked.connect(self.show_menu)
        self.pushButton.clicked.connect(self.send_comment)

        ## Ensure backButton icon is displayed (it's a QLabel with pixmap in UI)
        self.backButton.setScaledContents(True)
        pixmap = QPixmap(":/icons/back2.png")
        if pixmap.isNull():
            print("Warning: back2.png not found or invalid in resources!")
            self.backButton.setText("< Back")  # Fallback to text if icon fails
        else:
            self.backButton.setPixmap(pixmap)
            print("back2.png loaded successfully")

        self.backButton.mousePressEvent = self.go_back
        self.attachmentFrame.mousePressEvent = self.preview_attachment
        self.menuButton.clicked.connect(self.show_menu)
        self.pushButton.clicked.connect(self.send_comment)

    def go_back(self, event):
        """Handle back button click to return to stream"""
        self.close()

    def preview_attachment(self, event):
        """Handle click to preview attachment"""
        attachment = self.assessment_data.get("attachment", "assessment.pdf")
        print(f"Previewing {attachment}...")  # Replace with actual preview logic

    def show_menu(self):
        """Show options menu"""
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
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)
        menu.addAction(edit_action)
        menu.addAction(delete_action)
        button_pos = self.menuButton.mapToGlobal(self.menuButton.rect().bottomLeft())
        menu.exec(button_pos)

    def send_comment(self):
        """Handle send button click for comments (placeholder)"""
        comment = self.commentBox.toPlainText().strip()
        if comment:
            print(f"Sending comment: {comment}")  # Replace with actual comment submission logic
            self.commentBox.clear()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    assessment_data = {
        "title": "Quiz 1",
        "instructor": "Carlos Fidel Castro",
        "date": "August 18, 2025",
        "description": "Please ensure that the task is completed according to the requirements...",
        "attachment": "quiz1.pdf",
        "score": "10"
    }
    view_assessment = ViewAssessment(assessment_data)
    view_assessment.setFixedSize(1030, 634)
    view_assessment.show()
    sys.exit(app.exec())