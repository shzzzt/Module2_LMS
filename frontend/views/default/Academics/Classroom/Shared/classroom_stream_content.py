from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QScrollArea, QFrame, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QPixmap, QPainter, QRegion
from PyQt6.QtCore import Qt, QSize, pyqtSignal
import os
from view_materials import ViewMaterial
from view_assessment import ViewAssessment

class PostWidget(QFrame):  # Inherit from QFrame to apply the frame styling
    post_clicked = pyqtSignal(dict)  # Signal to emit post data when clicked

    def __init__(self, icon_path, title_text, date_text, post_type="material", parent=None):
        super().__init__(parent)
        self.post_type = post_type
        self.title_text = title_text  # Store title for mousePressEvent
        self.date_text = date_text   # Store date for mousePressEvent
        self.setup_ui(icon_path, title_text, date_text)

    def setup_ui(self, icon_path, title_text, date_text):
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
        layout.setContentsMargins(10, 10, 10, 10)  # Padding to match design

        # Icon Label (matches icon_label, forced to be circular)
        icon_label = QLabel(self)
        icon_label.setMaximumSize(50, 50)
        icon_label.setMinimumSize(50, 50)  # Ensure square size for circular mask
        icon_label.setStyleSheet("""
            QLabel {
                background-color: #084924;
                border-radius: 25px;  /* Half of 50px for a perfect circle */
                border: 2px solid white;
                overflow: hidden;
            }
        """)
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            region = QRegion(QSize(50, 50), QRegion.Ellipse)
            icon_label.setMask(region)
            icon_label.setPixmap(scaled_pixmap)
        icon_label.setScaledContents(True)
        layout.addWidget(icon_label)

        # Title and Date Layout (matches verticalLayout_3)
        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(title_text, self)
        title_label.setStyleSheet("font-size: 18px; border: none;")
        title_layout.addWidget(title_label)

        date_label = QLabel(date_text, self)
        date_label.setStyleSheet("font-size: 14px; border: none;")
        date_label.setWordWrap(True)
        title_layout.addWidget(date_label)

        layout.addLayout(title_layout)

        # Menu Button (matches menu_button)
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
            post_data = {
                "type": self.post_type,
                "title": self.title_text,
                "instructor": "Carlos Fidel Castro",
                "date": self.date_text,
                "description": f"Details for {self.title_text}",
                "attachment": f"{self.title_text.lower().replace(' ', '_')}.pdf",
                "score": "10" if self.post_type == "assessment" else None
            }
            self.post_clicked.emit(post_data)
        super().mousePressEvent(event)

class ClassroomStreamContent(QWidget):
    def __init__(self, class_data):
        super().__init__()
        self.class_data = class_data
        self.load_ui()
        self.populate_data()

    def load_ui(self):
        """Load the ClassroomStreamContent UI file"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/stream_post.ui')
        uic.loadUi(ui_file, self)

    def populate_data(self):
        """Populate with hardcoded data based on class_data and add multiple posts"""
        # Hardcoded header data (using class_data where possible)
        self.courseCode_label.setText(self.class_data.get("code", "ITSD81"))
        self.courseTitle_label.setText("DESKTOP APPLICATION DEVELOPMENT LECTURE")
        self.courseSection_label.setText(self.class_data.get("section", "BSIT-2C\nMONDAY - 1:00 - 4:00 PM"))

        # Get the layout for adding posts (stream_items_layout inside stream_item_container)
        stream_container = self.findChild(QWidget, "stream_item_container")
        if stream_container:
            post_layout = stream_container.findChild(QVBoxLayout, "stream_items_layout")
            if post_layout:
                # Clear existing widgets (e.g., postTemplate)
                for i in reversed(range(post_layout.count())):
                    item = post_layout.itemAt(i)
                    if item:
                        widget_to_remove = item.widget()
                        if widget_to_remove:
                            post_layout.removeWidget(widget_to_remove)
                            widget_to_remove.deleteLater()

                # Hardcoded multiple posts (recyclable structure)
                posts_data = [
                    (":/icons/document.svg", "Desktop Project Guidelines", "Aug 18", "material"),
                    (":/icons/document.svg", "Midterm Exam", "Sep 15", "assessment"),
                    (":/icons/document.svg", "Project Deadline Extended", "Sep 14", "material"),
                    (":/icons/document.svg", "Practice Test", "Sep 10", "assessment"),
                    (":/icons/document.svg", "Testing", "Sep 10", "material")
                ]

                # Add posts dynamically to stream_items_layout
                for icon_path, title, date, post_type in posts_data:
                    post_widget = PostWidget(icon_path, title, date, post_type)
                    post_layout.addWidget(post_widget)
                    # Connect the post_clicked signal to open the details view
                    post_widget.post_clicked.connect(self.open_post_details)

                # Ensure spacer at the end for scrolling (if not already present)
                if post_layout.count() > 0 and not isinstance(post_layout.itemAt(post_layout.count() - 1).spacerItem(), QSpacerItem):
                    spacer = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                    post_layout.addItem(spacer)

    def open_post_details(self, post_data):
        """Open the appropriate view based on post type"""
        if post_data["type"] == "material":
            view = ViewMaterial(post_data)  # Remove parent to make it a top-level window
        elif post_data["type"] == "assessment":
            view = ViewAssessment(post_data)  # Remove parent
        # Adjust size to fit content and avoid clipping
        view.setMinimumSize(1030, 634)  # Use minimum size to allow resizing
        view.adjustSize()  # Let Qt adjust based on content
        view.show()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    sample_class_data = {
        "code": "ITSD81",
        "section": "BSIT-2C\nMONDAY - 1:00 - 4:00 PM",
        "instructor": "Dr. Maria Santos"
    }
    stream_page = ClassroomStreamContent(sample_class_data)
    stream_page.setFixedSize(932, 454)  # Match new UI geometry
    stream_page.show()
    sys.exit(app.exec())