"""
Refactored Classroom Stream Content View
Now uses ClassroomController for all data operations
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QScrollArea, QFrame, QSizePolicy, QSpacerItem, QStackedWidget
from PyQt6.QtGui import QPixmap, QPainter, QRegion
from PyQt6.QtCore import Qt, QSize, pyqtSignal
import os
from .view_materials import ViewMaterial
from .view_assessment import ViewAssessment


class PostWidget(QFrame):
    post_clicked = pyqtSignal(dict)  # Signal to emit post data when clicked

    def __init__(self, post_data, parent=None):
        super().__init__(parent)
        self.post_data = post_data
        self.setup_ui()

    def setup_ui(self):
        # Apply frame styling matching postTemplate
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #084924;
            }
            QFrame:hover {
                border: 1px solid #e9ecef;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
        """)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)

        # Icon Label (circular)
        icon_label = QLabel(self)
        icon_label.setMaximumSize(50, 50)
        icon_label.setMinimumSize(50, 50)
        icon_label.setStyleSheet("""
            QLabel {
                background-color: #084924;
                border-radius: 25px;
                border: 2px solid white;
                overflow: hidden;
            }
        """)
        
        # Use a default icon path or derive from post type
        icon_path = ":/icons/document.svg"
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            region = QRegion(QSize(50, 50), QRegion.Ellipse)
            icon_label.setMask(region)
            icon_label.setPixmap(scaled_pixmap)
        icon_label.setScaledContents(True)
        layout.addWidget(icon_label)

        # Title and Date Layout
        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(self.post_data.get('title', 'Untitled'), self)
        title_label.setStyleSheet("font-size: 18px; border: none;")
        title_layout.addWidget(title_label)

        date_label = QLabel(self.post_data.get('date', ''), self)
        date_label.setStyleSheet("font-size: 14px; border: none;")
        date_label.setWordWrap(True)
        title_layout.addWidget(date_label)

        layout.addLayout(title_layout)

        # Menu Button
        menu_button = QPushButton("⋮", self)
        menu_button.setMaximumSize(32, 32)
        menu_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #6c757d;
                font-size: 32px;
                font-weight: bold;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                color: #495057;
            }
            QPushButton:pressed {
                background-color: #e9ecef;
            }
        """)
        layout.addWidget(menu_button)

        # Make the entire widget clickable
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        """Emit signal when the widget is clicked"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.post_clicked.emit(self.post_data)
        super().mousePressEvent(event)


class ClassroomStreamContent(QWidget):
    def __init__(self, class_data, user_role, controller):
        super().__init__()
        self.class_data = class_data
        self.user_role = user_role
        self.controller = controller  # Use shared controller
        self.current_post_data = None
        self.material_view = None
        self.assessment_view = None
        self.material_index = None
        self.assessment_index = None
        self.main_content = None
        
        self.setup_controller_connections()
        self.load_ui()
        self.load_posts()

    def setup_controller_connections(self):
        """Connect controller signals"""
        self.controller.posts_updated.connect(self.on_posts_updated)
        self.controller.error_occurred.connect(self.on_error_occurred)

    def load_ui(self):
        """Load the ClassroomStreamContent UI file into a main content widget"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/stream_post.ui')
        self.main_content = QWidget()
        uic.loadUi(ui_file, self.main_content)

        # Create stacked widget and main layout
        self.stackedWidget = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stackedWidget)

        # Add main content as index 0
        self.stackedWidget.addWidget(self.main_content)
        self.stackedWidget.setCurrentIndex(0)

        # Populate static header data
        self.populate_header_data()

    def populate_header_data(self):
        """Populate header with class information"""
        course_code_label = self.main_content.findChild(QLabel, "courseCode_label")
        course_title_label = self.main_content.findChild(QLabel, "courseTitle_label")
        course_section_label = self.main_content.findChild(QLabel, "courseSection_label")
        
        if course_code_label:
            course_code_label.setText(self.class_data.get("code", "ITSD81"))
        if course_title_label:
            course_title_label.setText(self.class_data.get("title", "DESKTOP APPLICATION DEVELOPMENT LECTURE"))
        if course_section_label:
            section_text = f"{self.class_data.get('section', 'BSIT-3C')}\n{self.class_data.get('schedule', 'MONDAY - 1:00 - 4:00 PM')}"
            course_section_label.setText(section_text)

    def load_posts(self):
        """Load posts using controller"""
        class_id = self.class_data.get('class_id')
        if class_id:
            self.controller.get_stream_posts(class_id)

    def on_posts_updated(self, posts):
        """Handle posts updated signal from controller"""
        self.populate_posts(posts)

    def populate_posts(self, posts):
        """Populate the stream with posts from controller"""
        # Get the layout for adding posts
        stream_container = self.main_content.findChild(QWidget, "stream_item_container")
        if not stream_container:
            return
            
        post_layout = stream_container.findChild(QVBoxLayout, "stream_items_layout")
        if not post_layout:
            return

        # Clear existing widgets
        for i in reversed(range(post_layout.count())):
            item = post_layout.itemAt(i)
            if item:
                widget_to_remove = item.widget()
                if widget_to_remove:
                    post_layout.removeWidget(widget_to_remove)
                    widget_to_remove.deleteLater()

        # Add posts dynamically to stream_items_layout
        for post in posts:
            # Format post data for display
            formatted_post = self.controller.post_service.format_post_for_display(post)
            formatted_post['post_id'] = post.get('post_id')  # Keep ID for navigation
            
            post_widget = PostWidget(formatted_post)
            post_layout.addWidget(post_widget)
            post_widget.post_clicked.connect(self.open_post_details)

        # Ensure spacer at the end for scrolling
        if post_layout.count() > 0 and not isinstance(post_layout.itemAt(post_layout.count() - 1).spacerItem(), QSpacerItem):
            spacer = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            post_layout.addItem(spacer)

    def open_post_details(self, post_data):
        """Switch to the appropriate page in the stacked widget with post details"""
        self.current_post_data = post_data

        # Initialize or update ViewMaterial page
        if post_data["type"] == "material":
            if self.material_view is None:
                self.material_view = ViewMaterial(post_data, self.user_role, self.controller)
                self.material_view.back_clicked.connect(self.back_to_main)
                self.material_index = self.stackedWidget.addWidget(self.material_view)
            else:
                self.material_view.update_data(post_data)
            self.stackedWidget.setCurrentIndex(self.material_index)

        # Initialize or update ViewAssessment page
        elif post_data["type"] == "assessment":
            if self.assessment_view is None:
                self.assessment_view = ViewAssessment(post_data, self.user_role, self.controller)
                self.assessment_view.back_clicked.connect(self.back_to_main)
                self.assessment_index = self.stackedWidget.addWidget(self.assessment_view)
            else:
                self.assessment_view.update_data(post_data)
            self.stackedWidget.setCurrentIndex(self.assessment_index)

    def back_to_main(self):
        """Switch back to the main content page (index 0)"""
        self.stackedWidget.setCurrentIndex(0)

    def on_error_occurred(self, error_message):
        """Handle errors from controller"""
        print(f"Stream Error: {error_message}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    sample_class_data = {
        "class_id": 1,
        "code": "ITSD81",
        "section": "BSIT-2C",
        "schedule": "MONDAY - 1:00 - 4:00 PM",
        "instructor": "Dr. Maria Santos"
    }
    
    # This would normally be injected from parent
    from frontend.controller.classroom_controller import ClassroomController
    controller = ClassroomController()
    
    stream_page = ClassroomStreamContent(sample_class_data, "faculty", controller)
    stream_page.setFixedSize(932, 454)
    stream_page.show()
    sys.exit(app.exec())