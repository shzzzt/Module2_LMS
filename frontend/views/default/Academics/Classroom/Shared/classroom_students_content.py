"""
Refactored Classroom Classworks Content View
Now uses ClassroomController for all data operations
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QToolButton, QVBoxLayout, QScrollArea, QSizePolicy, QSpacerItem, QMenu, QFrame, QStackedWidget, QComboBox
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
import os
from view_materials import ViewMaterial
from view_assessment import ViewAssessment


class ItemWidget(QWidget):
    def __init__(self, post_data, user_role, parent=None):
        super().__init__(parent)
        self.post_data = post_data
        self.user_role = user_role
        self.setup_ui()

    def setup_ui(self):
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
        # Use default icon
        icon_path = ":/icons/document.svg"
        icon_label.setPixmap(QPixmap(icon_path).scaled(38, 38, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setScaledContents(True)
        layout.addWidget(icon_label)

        # Title Label
        title_label = QLabel(self.post_data.get('title', 'Untitled'), self)
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
        date_text = f"Posted {self.post_data.get('date', '')}"
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
        self.menu_button = QPushButton("⋮", self)
        self.menu_button.setMinimumSize(24, 24)
        self.menu_button.setStyleSheet("""
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
        layout.addWidget(self.menu_button)
        
        if self.user_role in ["faculty", "admin"]:
            self.menu_button.clicked.connect(self.show_menu)

    def show_menu(self):
        """Show context menu for the button based on user role"""
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
        edit_action.triggered.connect(self.edit_item)
        delete_action.triggered.connect(self.delete_item)
        menu.addAction(edit_action)
        menu.addAction(delete_action)
        button_pos = self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft())
        menu.exec(button_pos)

    def edit_item(self):
        """Placeholder for editing the item"""
        print(f"Editing item: {self.post_data.get('title')}")

    def delete_item(self):
        """Placeholder for deleting the item"""
        print(f"Deleting item: {self.post_data.get('title')}")


class TopicFrame(QFrame):
    post_clicked = pyqtSignal(dict)

    def __init__(self, post_data, user_role, parent=None):
        super().__init__(parent)
        self.post_data = post_data
        self.user_role = user_role
        self.setObjectName(f"topicItemFrame_{id(self)}")
        self.setMinimumSize(800, 70)
        self.setMaximumHeight(70)
        self.setStyleSheet("""
            QFrame {
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
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(10, 5, 10, 5)

        # Use ItemWidget
        self.item_widget = ItemWidget(self.post_data, self.user_role, self)
        layout.addWidget(self.item_widget)

        # Make the entire frame clickable
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        """Emit signal when the frame is clicked"""
        if event.button() == Qt.MouseButton.LeftButton:
            print(f"Clicked: {self.post_data.get('title')}")
            self.post_clicked.emit(self.post_data)
        super().mousePressEvent(event)


class TopicWidget(QWidget):
    def __init__(self, topic_title, topic_posts, parent_content, user_role, parent=None):
        super().__init__(parent)
        self.parent_content = parent_content
        self.user_role = user_role
        self.title_label = None
        self.frames = []
        self.setup_ui(topic_title, topic_posts)

    def setup_ui(self, topic_title, topic_posts):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        # Topic Title
        self.title_label = QLabel(topic_title, self)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: 400;
                margin-left: 20px;
                margin-top: 20px;
                margin-bottom: -10px;
            }
        """)
        layout.addWidget(self.title_label)

        # Separator
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

        # Add item frames for posts in this topic
        for post in topic_posts:
            topic_frame = TopicFrame(post, self.user_role)
            self.frames.append(topic_frame)
            layout.addWidget(topic_frame)
            topic_frame.post_clicked.connect(self.parent_content.open_post_details)


class ClassroomClassworksContent(QWidget):
    def __init__(self, class_data, user_role, controller):
        super().__init__()
        self.class_data = class_data
        self.user_role = user_role
        self.controller = controller  # Use shared controller
        self.untitled_frames = []
        self.topic_widgets = []
        self.current_post_data = None
        self.material_view = None
        self.assessment_view = None
        self.material_index = None
        self.assessment_index = None
        self.main_content = None
        
        self.setup_controller_connections()
        self.load_ui()
        self.setup_role_based_ui()
        self.load_data()

    def setup_controller_connections(self):
        """Connect controller signals"""
        self.controller.posts_updated.connect(self.on_posts_updated)
        self.controller.error_occurred.connect(self.on_error_occurred)

    def load_ui(self):
        """Load the ClassroomClassworksContent UI file into a main content widget"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/classroom_classworks_content.ui')
        print(f"UI file path: {ui_file}")
        if not os.path.exists(ui_file):
            print("UI file not found")
            return
        self.main_content = QWidget()
        uic.loadUi(ui_file, self.main_content)
        
        # Assign references to main widgets
        self.filterComboBox = self.main_content.findChild(QComboBox, "filterComboBox")
        self.topicScrollArea = self.main_content.findChild(QScrollArea, "topicScrollArea")
        self.createButton = self.main_content.findChild(QToolButton, "createButton")
        
        if self.createButton:
            print("createButton found in UI file")
        else:
            print("ERROR: createButton not found in UI file")
        
        if self.filterComboBox:
            self.filterComboBox.currentTextChanged.connect(self.filter_posts)
        
        # Create stacked widget and main layout
        self.stackedWidget = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stackedWidget)
        
        # Add main content as index 0
        self.stackedWidget.addWidget(self.main_content)
        self.stackedWidget.setCurrentIndex(0)

    def setup_role_based_ui(self):
        """Setup UI elements based on user role"""
        if self.createButton:
            print(f"Setting up createButton for role: {self.user_role}")
            if self.user_role == "student":
                self.createButton.hide()
            else:
                self.createButton.show()
                self.createButton.setEnabled(True)
                self.createButton.clicked.connect(self.show_create_menu)
                print(f"createButton enabled: {self.createButton.isEnabled()}, visible: {self.createButton.isVisible()}")
        else:
            print("ERROR: Cannot setup createButton: not found")

    def show_create_menu(self):
        """Show menu for creating material, assessment, or topic"""
        print("Create button clicked - show_create_menu called")
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
        print(f"Menu execution position: {button_pos}")
        menu.exec(button_pos)

    def create_material(self):
        """Handle create material using controller"""
        print("Creating Material")
        # This would open a creation dialog, for now just placeholder
        material_data = {
            'title': 'New Material',
            'description': 'Material description',
            'instructor': self.class_data.get('instructor', 'Unknown'),
            'instructor_id': 'faculty_001'  # This should come from current user
        }
        class_id = self.class_data.get('class_id')
        if class_id:
            self.controller.create_material(class_id, material_data)

    def create_assessment(self):
        """Handle create assessment using controller"""
        print("Creating Assessment")
        assessment_data = {
            'title': 'New Assessment',
            'description': 'Assessment description',
            'instructor': self.class_data.get('instructor', 'Unknown'),
            'instructor_id': 'faculty_001',
            'points': 100
        }
        class_id = self.class_data.get('class_id')
        if class_id:
            self.controller.create_assessment(class_id, assessment_data)

    def create_topic(self):
        """Handle create topic using controller"""
        print("Creating Topic")
        topic_data = {
            'title': 'New Topic',
            'description': 'Topic description'
        }
        class_id = self.class_data.get('class_id')
        if class_id:
            self.controller.create_topic(class_id, topic_data)

    def load_data(self):
        """Load classworks data using controller"""
        class_id = self.class_data.get('class_id')
        if class_id:
            self.controller.get_classwork_posts(class_id)

    def on_posts_updated(self, posts):
        """Handle posts updated signal from controller"""
        self.populate_data(posts)

    def populate_data(self, posts):
        """Populate with posts from controller"""
        if not self.topicScrollArea:
            return
        
        # Get topics from controller
        class_id = self.class_data.get('class_id')
        topics = self.controller.classroom_service.get_class_topics(class_id) if class_id else []
        
        # Separate posts by topic
        untitled_posts = [p for p in posts if not p.get('topic_id')]
        topic_posts = {}
        for topic in topics:
            topic_id = topic.get('topic_id')
            topic_posts[topic_id] = {
                'info': topic,
                'posts': [p for p in posts if p.get('topic_id') == topic_id]
            }

        # Get the layout for adding topics
        scroll_widget = self.topicScrollArea.widget()
        if scroll_widget:
            topic_layout = scroll_widget.layout()
            if topic_layout:
                # Clear all existing widgets
                for i in reversed(range(topic_layout.count())):
                    item = topic_layout.itemAt(i)
                    if item:
                        widget = item.widget()
                        if widget:
                            topic_layout.removeWidget(widget)
                            widget.deleteLater()

                # Clear stored references
                self.untitled_frames.clear()
                self.topic_widgets.clear()

                # Populate filter combo box
                if self.filterComboBox:
                    self.filterComboBox.clear()
                    self.filterComboBox.addItem("All")
                    self.filterComboBox.addItem("Materials")
                    self.filterComboBox.addItem("Assessments")
                    for topic in topics:
                        self.filterComboBox.addItem(topic.get('title', 'Untitled Topic'))

                # Add untitled posts as standalone frames at the top
                for post in untitled_posts:
                    formatted_post = self.controller.post_service.format_post_for_display(post)
                    formatted_post['post_id'] = post.get('post_id')
                    topic_frame = TopicFrame(formatted_post, self.user_role)
                    self.untitled_frames.append(topic_frame)
                    topic_layout.addWidget(topic_frame)
                    topic_frame.post_clicked.connect(self.open_post_details)

                # Add topic-based posts
                for topic_id, topic_data in topic_posts.items():
                    if topic_data['posts']:  # Only show topics with posts
                        topic_info = topic_data['info']
                        formatted_posts = []
                        for post in topic_data['posts']:
                            formatted_post = self.controller.post_service.format_post_for_display(post)
                            formatted_post['post_id'] = post.get('post_id')
                            formatted_posts.append(formatted_post)
                        
                        topic_widget = TopicWidget(
                            topic_info.get('title', 'Untitled Topic'), 
                            formatted_posts, 
                            self, 
                            self.user_role
                        )
                        self.topic_widgets.append(topic_widget)
                        topic_layout.addWidget(topic_widget)

                # Add a spacer at the end for expansion
                spacer = QWidget()
                spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                topic_layout.addWidget(spacer)

    def filter_posts(self, filter_text):
        """Filter posts based on the selected combo box item"""
        if not filter_text:
            return

        # Show all by default
        for frame in self.untitled_frames:
            frame.setVisible(True)
        for widget in self.topic_widgets:
            widget.setVisible(True)
            for frame in widget.frames:
                frame.setVisible(True)

        # Apply filter
        if filter_text == "All":
            pass  # All are already visible
        elif filter_text == "Materials":
            for frame in self.untitled_frames:
                is_material = frame.post_data.get('type') == 'material'
                frame.setVisible(is_material)
            for widget in self.topic_widgets:
                has_materials = any(frame.post_data.get('type') == 'material' for frame in widget.frames)
                widget.setVisible(has_materials)
                for frame in widget.frames:
                    frame.setVisible(frame.post_data.get('type') == 'material')
        elif filter_text == "Assessments":
            for frame in self.untitled_frames:
                is_assessment = frame.post_data.get('type') == 'assessment'
                frame.setVisible(is_assessment)
            for widget in self.topic_widgets:
                has_assessments = any(frame.post_data.get('type') == 'assessment' for frame in widget.frames)
                widget.setVisible(has_assessments)
                for frame in widget.frames:
                    frame.setVisible(frame.post_data.get('type') == 'assessment')
        else:  # Topic filter
            for frame in self.untitled_frames:
                frame.setVisible(False)
            for widget in self.topic_widgets:
                widget.setVisible(widget.title_label.text() == filter_text)
                if widget.isVisible():
                    for frame in widget.frames:
                        frame.setVisible(True)

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
        print(f"Classworks Error: {error_message}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # This would normally be injected from parent
    from frontend.controller.classroom_controller import ClassroomController
    controller = ClassroomController()
    
    classworks_page = ClassroomClassworksContent({"class_id": 1}, "faculty", controller)
    classworks_page.setFixedSize(940, 530)
    classworks_page.show()
    sys.exit(app.exec())