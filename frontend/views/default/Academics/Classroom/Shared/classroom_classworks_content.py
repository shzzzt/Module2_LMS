from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QScrollArea, QSizePolicy, QSpacerItem, QMenu, QFrame
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt
import os

class ItemWidget(QWidget):
    def __init__(self, icon_path, title_text, date_text, parent=None):
        super().__init__(parent)
        self.setup_ui(icon_path, title_text, date_text)

    def setup_ui(self, icon_path, title_text, date_text):
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Icon Label
        icon_label = QLabel(self)
        icon_label.setMinimumSize(32, 32)
        icon_label.setMaximumSize(38, 38)
        icon_label.setStyleSheet("""
            QLabel {
                background-color: #084924;
                border-radius: 19px;
                border: 2px solid white;
                overflow: hidden;
            }
        """)
        icon_label.setPixmap(QPixmap(icon_path).scaled(38, 38, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setScaledContents(True)
        layout.addWidget(icon_label)

        # Title Label
        title_label = QLabel(title_text, self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 400;
                color: #24292f;
                border: none;
                background: transparent;
            }
        """)
        layout.addWidget(title_label)

        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer)

        # Date Label
        date_label = QLabel(date_text, self)
        date_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #656d76;
                border: none;
                background: transparent;
            }
        """)
        date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(date_label)

        # Menu Button
        menu_button = QPushButton("⋮", self)
        menu_button.setMinimumSize(24, 24)
        menu_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                font-size: 34px;
                color: #656d76;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
            }
        """)
        layout.addWidget(menu_button)

class TopicFrame(QFrame):
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.setObjectName("topicItemFrame")  # Match UI frame name for styling
        self.setMinimumSize(800, 70)
        self.setMaximumHeight(70)  # Limit height per item
        self.setStyleSheet("""
            QFrame#topicItemFrame {
                background-color: white;
                border: 1px solid #084924;
                border-radius: 20px;
                margin-left: 20px;
            }
            QFrame:hover {
                background-color: #F8F9FA;
                border-color: #D0D7DE;
            }
        """)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setup_ui(item_data)

    def setup_ui(self, item_data):
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(10, 5, 10, 5)  # Match UI margins

        icon_path, title, date = item_data
        # Icon Label
        icon_label = QLabel(self)
        icon_label.setMinimumSize(32, 32)
        icon_label.setMaximumSize(38, 38)
        icon_label.setStyleSheet("""
            QLabel {
                background-color: #084924;
                border-radius: 19px;
                border: 2px solid white;
                overflow: hidden;
            }
        """)
        icon_label.setPixmap(QPixmap(icon_path).scaled(38, 38, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setScaledContents(True)
        layout.addWidget(icon_label)

        # Title Label
        title_label = QLabel(title, self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 400;
                color: #24292f;
                border: none;
                background: transparent;
            }
        """)
        layout.addWidget(title_label)

        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer)

        # Date Label
        date_label = QLabel(date, self)
        date_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #656d76;
                border: none;
                background: transparent;
            }
        """)
        date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(date_label)

        # Menu Button
        menu_button = QPushButton("⋮", self)
        menu_button.setMinimumSize(24, 24)
        menu_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                font-size: 34px;
                color: #656d76;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
            }
        """)
        layout.addWidget(menu_button)

class TopicWidget(QWidget):
    def __init__(self, topic_title, items_data, parent=None):
        super().__init__(parent)
        self.setup_ui(topic_title, items_data)

    def setup_ui(self, topic_title, items_data):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margin, handled by frame

        # Topic Title (match topicTitle from UI)
        title_label = QLabel(topic_title, self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: 400;
                margin-left: 20px;
                margin-top: 20px;
                margin-bottom: -10px;
            }
        """)
        layout.addWidget(title_label)

        # Separator (mimic UI separator)
        separator = QFrame(self)
        separator.setMinimumSize(800, 1)
        separator.setMaximumHeight(1)
        separator.setStyleSheet("""
            QFrame {
                border: 1px solid #A9A9A9;
                background-color: transparent;
                margin-left: 20px;
            }
        """)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        # Add item frames
        for item_data in items_data:
            topic_frame = TopicFrame(item_data)
            layout.addWidget(topic_frame)

class ClassroomClassworksContent(QWidget):
    def __init__(self, class_data, user_role):
        super().__init__()
        self.class_data = class_data
        self.user_role = user_role
        self.load_ui()
        self.setup_role_based_ui()
        self.populate_data()

    def load_ui(self):
        """Load the ClassroomClassworksContent UI file"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/classroom_classworks_content.ui')
        uic.loadUi(ui_file, self)

    def setup_role_based_ui(self):
        """Setup UI elements based on user role"""
        if self.user_role == "student":
            self.createButton.hide()
        else:
            self.createButton.show()
            self.createButton.clicked.connect(self.show_create_menu)

    def show_create_menu(self):
        """Show menu for creating material, assessment, or topic"""
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
        
        material_action = QAction("Material", self)
        assessment_action = QAction("Assessment", self)
        topic_action = QAction("Topic", self)
        
        material_action.triggered.connect(self.create_material)
        assessment_action.triggered.connect(self.create_assessment)
        topic_action.triggered.connect(self.create_topic)
        
        menu.addAction(material_action)
        menu.addAction(assessment_action)
        menu.addAction(topic_action)
        
        button_pos = self.createButton.mapToGlobal(self.createButton.rect().bottomLeft())
        menu.exec(button_pos)

    def create_material(self):
        """Handle create material (placeholder)"""
        print("Creating Material")

    def create_assessment(self):
        """Handle create assessment (placeholder)"""
        print("Creating Assessment")

    def create_topic(self):
        """Handle create topic (placeholder)"""
        print("Creating Topic")

    def populate_data(self):
        """Populate with hardcoded data and add multiple topics with items"""
        # Hardcoded topics and items
        topics_data = [
            ("Lecture: Topic 1", [
                (":/icons/document.svg", "Desktop Project Guidelines", "Posted Aug 18"),
                (":/icons/document.svg", "Chapter 2: Basics", "Posted Aug 25")
            ]),
            ("Lecture: Topic 2", [
                (":/icons/document.svg", "Chapter 3: Advanced Concepts", "Posted Sep 1"),
                (":/icons/document.svg", "Chapter 4: Practical Applications", "Posted Sep 8")
            ])
        ]

        # Get the layout for adding topics (topicListLayout in topicScrollArea widget)
        scroll_widget = self.topicScrollArea.widget()
        if scroll_widget:
            topic_layout = scroll_widget.layout()  # topicListLayout
            if topic_layout:
                # Clear only dynamic widgets, preserve topicTitle and separator
                for i in reversed(range(topic_layout.count())):
                    widget = topic_layout.itemAt(i).widget()
                    if widget and widget.objectName() not in ["topicTitle", "separator", "topicItemFrame", "topicItemFrame_2"]:
                        topic_layout.removeWidget(widget)
                        widget.deleteLater()

                # Add topics and items dynamically below the static header
                for topic_title, items_data in topics_data:
                    topic_widget = TopicWidget(topic_title, items_data)
                    topic_layout.addWidget(topic_widget)

                # Add a spacer at the end for expansion
                spacer = QWidget()
                spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                topic_layout.addWidget(spacer)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    classworks_page = ClassroomClassworksContent({"class_id": 1}, "faculty")  # Example with faculty role
    classworks_page.setFixedSize(940, 530)
    classworks_page.show()
    sys.exit(app.exec())