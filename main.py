from PyQt6.QtWidgets import QWidget, QPushButton, QTabWidget, QVBoxLayout, QHBoxLayout,QButtonGroup,QMainWindow, QStackedWidget, QApplication
from PyQt6.QtCore import pyqtSignal
from frontend.views.default.Academics.Classroom.Shared.post_details import PostDetails
from frontend.views.default.Academics.Classroom.Shared.classroom_home import ClassroomHome
from frontend.views.default.Academics.Classroom.Shared.classroom_stream import ClassroomStream
from frontend.views.default.Academics.Classroom.Shared.classroom_classworks import ClassroomClassworks
from frontend.services.classroom_service import ClassroomService
from frontend.services.stream_service import StreamService
from frontend.services.classwork_service import ClassworkService
from frontend.controller.classroom_controller import ClassroomController
from frontend.controller.stream_controller import StreamController
from frontend.controller.classwork_controller import ClassworkController

# main.py - Fix the ClassroomView class
class ClassroomView(QWidget):
    back_clicked = pyqtSignal()
    post_selected = pyqtSignal(dict)  # This should emit the post data

    def __init__(self, cls, user_role, parent=None):
        super().__init__(parent)
        self.cls = cls
        self.user_role = user_role
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(self)
        
        header_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton { border: none; background: transparent; padding: 5px; font-size: 16px; }
            QPushButton:hover { text-decoration: underline; }
        """)
        back_button.clicked.connect(self.back_clicked.emit)
        header_layout.addWidget(back_button)
        header_layout.addStretch()
        lecture_btn = QPushButton("LECTURE")
        lecture_btn.setStyleSheet("""
            QPushButton { background-color: #084924; color: white; border-radius: 5px; padding: 5px 10px; }
            QPushButton:checked { background-color: #1B5E20; }
        """)
        lecture_btn.setCheckable(True)
        lecture_btn.setChecked(True)
        lab_btn = QPushButton("LABORATORY")
        lab_btn.setStyleSheet("""
            QPushButton { background-color: #084924; color: white; border-radius: 5px; padding: 5px 10px; }
            QPushButton:checked { background-color: #1B5E20; }
        """)
        lab_btn.setCheckable(True)
        group = QButtonGroup()
        group.addButton(lecture_btn)
        group.addButton(lab_btn)
        header_layout.addWidget(lecture_btn)
        header_layout.addWidget(lab_btn)
        layout.addLayout(header_layout)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background-color: white; }
            QTabBar::tab {
                background: white;
                padding: 10px 20px;
                font-size: 14px;
                font-family: "Poppins", Arial, sans-serif;
                text-transform: uppercase;
                border: none;
            }
            QTabBar::tab:selected {
                border-bottom: 4px solid #FFD700;
                color: black;
            }
        """)
        
        stream_service = StreamService("data/classroom_data.json")
        classwork_service = ClassworkService("data/classroom_data.json")
        stream_controller = StreamController(stream_service)
        classwork_controller = ClassworkController(classwork_service)
        
        self.stream_view = ClassroomStream(self.cls, stream_controller)
        self.classworks_view = ClassroomClassworks(self.cls, self.user_role, classwork_controller)
        students_view = QWidget()
        attendance_view = QWidget()
        grades_view = QWidget()
        
        tabs.addTab(self.stream_view, "STREAM")
        tabs.addTab(self.classworks_view, "CLASSWORKS")
        tabs.addTab(students_view, "STUDENTS")
        tabs.addTab(attendance_view, "ATTENDANCE")
        tabs.addTab(grades_view, "GRADES")
        
        # FIX: Connect the signals properly - remove .emit from the connection
        self.stream_view.post_selected.connect(self.post_selected)
        self.classworks_view.post_selected.connect(self.post_selected)
        
        layout.addWidget(tabs)

    def clear(self):
        self.stream_view.clear()
        self.classworks_view.clear()

# In your MainWindow class - fix the post navigation
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Classroom App")
        self.setMinimumSize(940, 530)
        self.setStyleSheet("background-color: white;")
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.classroom_controller = ClassroomController()
        
        self.home_view = ClassroomHome(user_role="faculty")
        self.home_view.class_selected.connect(self.show_classroom)
        self.stacked_widget.addWidget(self.home_view)
        
        self.current_classroom_view = None
        self.current_post_view = None

    def show_classroom(self, cls):
        print(f"Showing classroom: {cls['title']}")
        
        if self.current_classroom_view:
            self.stacked_widget.removeWidget(self.current_classroom_view)
            self.current_classroom_view.deleteLater()
        
        self.current_classroom_view = ClassroomView(cls, user_role="faculty")
        self.current_classroom_view.back_clicked.connect(self.show_home)
        self.current_classroom_view.post_selected.connect(self.show_post)
        self.stacked_widget.addWidget(self.current_classroom_view)
        self.stacked_widget.setCurrentWidget(self.current_classroom_view)

    def show_post(self, post):
        print(f"Showing post: {post['title']}")
        
        if self.current_post_view:
            self.stacked_widget.removeWidget(self.current_post_view)
            self.current_post_view.deleteLater()
        
        self.current_post_view = PostDetails(post)
        self.current_post_view.back_clicked.connect(self.return_to_classroom)
        self.stacked_widget.addWidget(self.current_post_view)
        self.stacked_widget.setCurrentWidget(self.current_post_view)

    def return_to_classroom(self):
        print("Returning to classroom")
        if self.current_post_view:
            self.stacked_widget.removeWidget(self.current_post_view)
            self.current_post_view.deleteLater()
            self.current_post_view = None
        self.stacked_widget.setCurrentWidget(self.current_classroom_view)

    def show_home(self):
        print("Showing home")
        if self.current_classroom_view:
            self.stacked_widget.removeWidget(self.current_classroom_view)
            self.current_classroom_view.deleteLater()
            self.current_classroom_view = None
        self.stacked_widget.setCurrentWidget(self.home_view)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())