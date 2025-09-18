from PyQt6 import uic
from PyQt6.QtWidgets import QFrame, QMenu, QWidget, QGridLayout, QScrollArea, QVBoxLayout, QLabel, QStackedWidget, QApplication, QTabWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction
import os

# Import the dynamic ClassroomStreamContent
from classroom_stream_content import ClassroomStreamContent
from classroom_classworks_content import ClassroomClassworksContent  # Import the new Classworks content

class ClassCard(QFrame):
    # Signals for controller communication
    card_clicked = pyqtSignal(dict)  # Emits class data when card is clicked
    restore_clicked = pyqtSignal(dict)  # Emits class data when restore is clicked
    delete_clicked = pyqtSignal(dict)  # Emits class data when delete is clicked
    
    def __init__(self, class_data, user_role="student"):
        super().__init__()
        
        # Store class data and user role
        self.class_data = class_data
        self.user_role = user_role
        
        # Load UI file
        self.load_ui()
        
        # Populate data
        self.populate_data()
        
        # Setup role-based visibility
        self.setup_role_based_ui()
        
        # Connect signals
        self.connect_signals()
    
    def load_ui(self):
        """Load the UI file created in Qt Designer"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, '../../../../../ui/Classroom/classroom_home.ui')
        uic.loadUi(ui_file, self)
    
    def populate_data(self):
        """Populate the UI elements with class data"""
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
        """Setup UI elements based on user role"""
        if self.user_role == "student":
            self.options_button.hide()
        else:
            self.options_button.show()
    
    def connect_signals(self):
        """Connect UI signals to methods"""
        self.options_button.clicked.connect(self.show_options_menu)
        self.mousePressEvent = self.card_clicked_event
    
    def show_options_menu(self):
        """Show options menu for admin/faculty"""
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
        """Handle card click event"""
        self.card_clicked.emit(self.class_data)
        super().mousePressEvent(event)
    
    def on_restore_clicked(self):
        """Handle restore button click"""
        self.restore_clicked.emit(self.class_data)
    
    def on_delete_clicked(self):
        """Handle delete button click"""
        self.delete_clicked.emit(self.class_data)

class ClassPage(QWidget):
    def __init__(self, class_data, user_role):
        super().__init__()
        self.class_data = class_data
        self.user_role = user_role
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add tabs
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

        # Stream tab
        stream_tab = ClassroomStreamContent(self.class_data)
        tab_widget.addTab(stream_tab, "Stream")

        # Classworks tab
        classworks_tab = ClassroomClassworksContent(self.class_data, self.user_role)
        tab_widget.addTab(classworks_tab, "Classworks")

        layout.addWidget(tab_widget)

class HomePage(QWidget):
    def __init__(self, user_role="student"):
        super().__init__()
        self.user_role = user_role
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the home page UI with class cards"""
        # Set the fixed size of the window
        self.setMinimumSize(940, 530)

        # Use QStackedWidget for navigation
        self.stacked_widget = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)

        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)

        # Page 1: Class cards home
        home_widget = QWidget()
        home_layout = QVBoxLayout(home_widget)
        home_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
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
        
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: white;  /* Ensure scroll area matches background */
            }
        """)
        
        # Container for cards
        cards_container = QWidget()
        cards_layout = QGridLayout(cards_container)
        cards_layout.setSpacing(20)
        
        # Sample class data
        sample_classes = [
            {
                "code": "ITSD81",
                "section": "BSIT 3C",
                "instructor": "Neil John Jomaya",
                "class_id": 1
            },
            {
                "code": "IT59",
                "section": "BSIT 3A",
                "instructor": "John Doe",
                "class_id": 2
            },
            {
                "code": "IT95",
                "section": "BSIT 3A",
                "instructor": "JInky",
                "class_id": 3
            }
        ]
        
        # Create and add class cards
        row, col = 0, 0
        max_cols = 2
        
        for class_data in sample_classes:
            card = ClassCard(class_data, self.user_role)
            card.card_clicked.connect(self.on_card_clicked)
            card.restore_clicked.connect(self.on_restore_clicked)
            card.delete_clicked.connect(self.on_delete_clicked)
            cards_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        scroll_area.setWidget(cards_container)
        home_layout.addWidget(scroll_area)
        
        self.stacked_widget.addWidget(home_widget)
    
    def on_card_clicked(self, class_data):
        """Handle card click - navigate to class page with tabs"""
        # Create the class page with tabs for Stream and Classworks
        class_page = ClassPage(class_data, self.user_role)
        self.stacked_widget.addWidget(class_page)
        self.stacked_widget.setCurrentWidget(class_page)
    
    def on_restore_clicked(self, class_data):
        """Handle restore click - to be connected to controller"""
        print(f"Restore clicked: {class_data}")
    
    def on_delete_clicked(self, class_data):
        """Handle delete button click"""
        print(f"Delete clicked: {class_data}")

# Test the widget
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    home_page = HomePage(user_role="student")
    home_page.show()
    sys.exit(app.exec())