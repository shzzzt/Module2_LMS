"""
Refactored Classroom Home View
Now uses ClassroomController for all data operations
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QFrame, QMenu, QWidget, QGridLayout, QScrollArea, QVBoxLayout, QLabel, QStackedWidget, QApplication, QTabWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction
import os

from .classroom_stream_content import ClassroomStreamContent
from .classroom_classworks_content import ClassroomClassworksContent
from frontend.controller.classroom_controller import ClassroomController


class ClassCard(QFrame):
    card_clicked = pyqtSignal(dict)
    restore_clicked = pyqtSignal(dict)
    delete_clicked = pyqtSignal(dict)
    
    def __init__(self, class_data, user_role="student"):
        super().__init__()
        self.class_data = class_data
        self.user_role = user_role
        self.load_ui()
        self.populate_data()
        self.setup_role_based_ui()
        self.connect_signals()
    
    def load_ui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/classroom_home.ui')
        uic.loadUi(ui_file, self)
    
    def populate_data(self):
        code = self.class_data.get('code', 'CODE')
        self.course_code_label.setText(f"{code}")
        section = self.class_data.get('section', 'Section')
        self.course_code_section_label.setText(f"{section}")
        instructor = self.class_data.get('instructor', 'Instructor Name')
        self.instructor_label.setText(instructor)
        if instructor:
            initial = instructor[0].upper()
            self.profile_pic_label.setText(initial)
        recent_posts = self.class_data.get('recent_posts', 'No recent posts')
        self.recent_posts_label.setText(recent_posts)
    
    def setup_role_based_ui(self):
        if self.user_role == "student":
            self.options_button.hide()
        else:
            self.options_button.show()
    
    def connect_signals(self):
        self.options_button.clicked.connect(self.show_options_menu)
        self.mousePressEvent = self.card_clicked_event
    
    def show_options_menu(self):
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
        restore_action = QAction("Restore", self)
        delete_action = QAction("Delete", self)
        restore_action.triggered.connect(self.on_restore_clicked)
        delete_action.triggered.connect(self.on_delete_clicked)
        menu.addAction(restore_action)
        menu.addSeparator()
        menu.addAction(delete_action)
        button_pos = self.options_button.mapToGlobal(self.options_button.rect().bottomLeft())
        menu.exec(button_pos)
    
    def card_clicked_event(self, event):
        self.card_clicked.emit(self.class_data)
        super().mousePressEvent(event)
    
    def on_restore_clicked(self):
        self.restore_clicked.emit(self.class_data)
    
    def on_delete_clicked(self):
        self.delete_clicked.emit(self.class_data)


class ClassPage(QWidget):
    def __init__(self, class_data, user_role, controller):
        super().__init__()
        self.class_data = class_data
        self.user_role = user_role
        self.controller = controller  # Use shared controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        tab_widget = QTabWidget(self)
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: transparent;
                border-bottom: 2px solid transparent;
                padding: 8px 16px;
                font-size: 16px;
            }
            QTabBar::tab:selected {
                border-bottom: 2px solid #084924;
                font-weight: bold;
            }
        """)
        
        # Pass the shared controller to child tabs
        stream_tab = ClassroomStreamContent(self.class_data, self.user_role, self.controller)
        tab_widget.addTab(stream_tab, "Stream")
        
        classworks_tab = ClassroomClassworksContent(self.class_data, self.user_role, self.controller)
        tab_widget.addTab(classworks_tab, "Classworks")
        
        layout.addWidget(tab_widget)


class HomePage(QWidget):
    def __init__(self, user_role="student", user_id=None):
        super().__init__()
        self.user_role = user_role
        self.user_id = user_id or f"{user_role}_001"  # Default user ID
        
        # Initialize controller
        self.controller = ClassroomController()
        self.setup_controller_connections()
        self.setup_ui()
        
        # Load classes on startup
        self.load_classes()
        
    def setup_controller_connections(self):
        """Connect controller signals to view handlers"""
        self.controller.classes_updated.connect(self.on_classes_updated)
        self.controller.error_occurred.connect(self.on_error_occurred)
        
    def setup_ui(self):
        self.setMinimumSize(940, 530)
        self.stacked_widget = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setStyleSheet("QWidget { background-color: white; }")
        
        # Create home widget
        self.home_widget = QWidget()
        home_layout = QVBoxLayout(self.home_widget)
        home_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("My Classes")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }
        """)
        home_layout.addWidget(title)
        
        # Scroll area for class cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: white; }")
        
        # Container for class cards
        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(20)
        
        self.scroll_area.setWidget(self.cards_container)
        home_layout.addWidget(self.scroll_area)
        self.stacked_widget.addWidget(self.home_widget)
    
    def load_classes(self):
        """Load classes using controller"""
        self.controller.get_user_classes(self.user_role)
    
    def on_classes_updated(self, classes):
        """Handle classes updated signal from controller"""
        self.populate_class_cards(classes)
    
    def populate_class_cards(self, classes):
        """Populate the UI with class cards from controller data"""
        # Clear existing cards
        for i in reversed(range(self.cards_layout.count())):
            item = self.cards_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    self.cards_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Add class cards
        row, col = 0, 0
        max_cols = 2
        for class_data in classes:
            card = ClassCard(class_data, self.user_role)
            card.card_clicked.connect(self.on_card_clicked)
            card.restore_clicked.connect(self.on_restore_clicked)
            card.delete_clicked.connect(self.on_delete_clicked)
            self.cards_layout.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def on_card_clicked(self, class_data):
        """Handle class card click - create class page with shared controller"""
        class_page = ClassPage(class_data, self.user_role, self.controller)
        self.stacked_widget.addWidget(class_page)
        self.stacked_widget.setCurrentWidget(class_page)
    
    def on_restore_clicked(self, class_data):
        """Handle restore class using controller"""
        success = self.controller.restore_class(class_data)
        if success:
            print(f"Class {class_data.get('code')} restored successfully")
    
    def on_delete_clicked(self, class_data):
        """Handle delete class using controller"""
        success = self.controller.delete_class(class_data)
        if success:
            print(f"Class {class_data.get('code')} deleted successfully")
    
    def on_error_occurred(self, error_message):
        """Handle errors from controller"""
        print(f"Error: {error_message}")
        # You can show a proper error dialog here


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    home_page = HomePage(user_role="faculty", user_id="faculty_001")
    home_page.show()
    sys.exit(app.exec())