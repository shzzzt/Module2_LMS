"""
Refactored View Material
Now uses ClassroomController for all data operations
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QMenu, QScrollArea, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
import os


class ViewMaterial(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self, material_data, user_role, controller, parent=None):
        super().__init__(parent)
        self.material_data = material_data
        self.user_role = user_role
        self.controller = controller  # Use shared controller
        
        # Extract post_id from material_data if available
        self.post_id = material_data.get('post_id')
        
        self.setup_controller_connections()
        self.load_ui()
        self.populate_data()

    def setup_controller_connections(self):
        """Connect controller signals"""
        self.controller.post_details_updated.connect(self.on_post_details_updated)
        self.controller.error_occurred.connect(self.on_error_occurred)

    def load_ui(self):
        """Load the ViewMaterial UI file and wrap it in a scroll area"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/view_material.ui')
        
        # Load the UI into a temporary widget
        ui_widget = QWidget()
        uic.loadUi(ui_file, ui_widget)
        
        # Create a scroll area and set the UI widget as its content
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(ui_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        # Set up the main layout to include the scroll area
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll_area)
        
        # Assign references to UI elements from the loaded widget
        self.title_label = ui_widget.findChild(QWidget, "title_label") or ui_widget.findChild(QLabel, "title_label")
        self.instructor_label = ui_widget.findChild(QWidget, "instructor_label") or ui_widget.findChild(QLabel, "instructor_label")
        self.date_label = ui_widget.findChild(QWidget, "date_label") or ui_widget.findChild(QLabel, "date_label")
        self.descriptionEdit = ui_widget.findChild(QWidget, "descriptionEdit") or ui_widget.findChild(QTextEdit, "descriptionEdit")
        self.attachmentName = ui_widget.findChild(QWidget, "attachmentName") or ui_widget.findChild(QLabel, "attachmentName")
        self.attachmentType = ui_widget.findChild(QWidget, "attachmentType") or ui_widget.findChild(QLabel, "attachmentType")
        self.backButton = ui_widget.findChild(QWidget, "backButton") or ui_widget.findChild(QLabel, "backButton")
        self.attachmentFrame = ui_widget.findChild(QWidget, "attachmentFrame") or ui_widget.findChild(QFrame, "attachmentFrame")
        self.menuButton = ui_widget.findChild(QWidget, "menuButton") or ui_widget.findChild(QPushButton, "menuButton")
        self.commentBox = ui_widget.findChild(QWidget, "commentBox") or ui_widget.findChild(QTextEdit, "commentBox")
        self.pushButton = ui_widget.findChild(QWidget, "pushButton") or ui_widget.findChild(QPushButton, "pushButton")

    def populate_data(self):
        """Populate the UI with material data"""
        if self.title_label:
            self.title_label.setText(self.material_data.get("title", "Desktop Project Guidelines"))
        if self.instructor_label:
            self.instructor_label.setText(self.material_data.get("instructor", "Carlos Fidel Castro"))
        if self.date_label:
            self.date_label.setText("• " + self.material_data.get("date", "August 18, 2025"))
        if self.descriptionEdit:
            self.descriptionEdit.setText(self.material_data.get("description", "This is the material description..."))
            self.descriptionEdit.setReadOnly(True)
        
        attachment = self.material_data.get("attachment", "Desktop Project Guidelines.pdf")
        if self.attachmentName and attachment:
            self.attachmentName.setText(attachment.split('.')[0])
        if self.attachmentType and attachment:
            self.attachmentType.setText("." + attachment.split('.')[-1])
        
        if self.backButton:
            self.backButton.mousePressEvent = self.go_back
        if self.attachmentFrame:
            self.attachmentFrame.mousePressEvent = self.preview_attachment
        if self.menuButton:
            self.menuButton.clicked.connect(self.show_menu)
        if self.pushButton:
            self.pushButton.clicked.connect(self.send_comment)

        # Ensure backButton icon is displayed
        if self.backButton:
            self.backButton.setScaledContents(True)
            pixmap = QPixmap(":/icons/back2.png")
            if pixmap.isNull():
                print("Warning: back2.png not found or invalid in resources!")
                self.backButton.setText("< Back")
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
            edit_action.triggered.connect(self.edit_material)
            delete_action.triggered.connect(self.delete_material)
            menu.addAction(edit_action)
            menu.addAction(delete_action)
        
        if self.menuButton:
            button_pos = self.menuButton.mapToGlobal(self.menuButton.rect().bottomLeft())
            menu.exec(button_pos)

    def edit_material(self):
        """Handle edit material using controller"""
        if self.post_id:
            print(f"Editing material with ID: {self.post_id}")
            # This would open an edit dialog, for now just placeholder
            updated_data = {
                'title': f"Updated {self.material_data.get('title', 'Material')}",
                'description': 'Updated description'
            }
            success = self.controller.edit_post(self.post_id, updated_data)
            if success:
                print("Material updated successfully")

    def delete_material(self):
        """Handle delete material using controller"""
        if self.post_id:
            print(f"Deleting material with ID: {self.post_id}")
            success = self.controller.delete_post(self.post_id)
            if success:
                print("Material deleted successfully")
                self.back_clicked.emit()  # Go back after deletion

    def send_comment(self):
        """Handle send button click for comments using controller"""
        if self.commentBox and self.post_id:
            comment = self.commentBox.toPlainText().strip()
            if comment:
                print(f"Sending comment: {comment}")
                # This should get the current user ID from session/auth
                user_id = "current_user_001"  # Placeholder
                user_name = "Current User"  # Placeholder
                
                comment_id = self.controller.add_comment(self.post_id, comment, user_id, user_name)
                if comment_id:
                    print("Comment added successfully")
                    self.commentBox.clear()

    def update_data(self, material_data):
        """Update the widget with new material data"""
        self.material_data = material_data
        self.post_id = material_data.get('post_id')
        self.populate_data()

    def on_post_details_updated(self, post_details):
        """Handle post details updated from controller"""
        if post_details.get('post_id') == self.post_id:
            formatted_data = self.controller.post_service.format_post_for_display(post_details)
            formatted_data['post_id'] = post_details.get('post_id')
            self.update_data(formatted_data)

    def on_error_occurred(self, error_message):
        """Handle errors from controller"""
        print(f"View Material Error: {error_message}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    material_data = {
        "post_id": 1,
        "title": "Desktop Project Guidelines",
        "instructor": "Carlos Fidel Castro",
        "date": "August 18, 2025",
        "description": "Please ensure that the task is completed according to the requirements provided, keeping everything consistent and aligned throughout the process. Make sure to follow the necessary steps as outlined, review your work before finalizing, and confirm that it meets the expected standards. Always double-check that the format is correct, the details are accurate, and the output follows the general guidelines. Be mindful of maintaining a clear structure, avoid unnecessary errors, and ensure that the submission is properly prepared before turning it in.",
        "attachment": "Desktop project guidelines.pdf"
    }
    
    # Mock controller for testing
    class MockController:
        def __init__(self):
            self.post_details_updated = lambda x: None
            self.error_occurred = lambda x: None
        
        def edit_post(self, post_id, data):
            return True
        
        def delete_post(self, post_id):
            return True
        
        def add_comment(self, post_id, comment, user_id, user_name):
            return 1
    
    controller = MockController()
    view_material = ViewMaterial(material_data, "faculty", controller)
    view_material.setFixedSize(940, 530)
    view_material.show()
    sys.exit(app.exec())