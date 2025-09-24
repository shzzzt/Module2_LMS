import sys
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QApplication, QFileDialog, QScrollArea, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from frontend.widgets.labeled_section import LabeledSection

class UploadClassMaterialPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_files = []  # Store selected file paths
        self.initializeUI()

    def initializeUI(self):
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #084924;
            }
            LabeledSection {
                border: none;               
            }
        """)

        self.__layout = QVBoxLayout(self)
        self.__layout.setSpacing(20)
        self.__layout.setContentsMargins(30, 25, 30, 25)
        self.setup_widgets()

    def setup_widgets(self):
        # Title section
        title_input = QLineEdit()
        title_input.setPlaceholderText("Enter title")
        title_input.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #0066cc;
                border-width: 2px;
            }
        """)
        self.__layout.addWidget(LabeledSection("Title", title_input, "*Required"))

        # Instructions section
        instructions_input = QTextEdit()
        instructions_input.setStyleSheet("""
            QTextEdit {
                padding: 15px;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QTextEdit:focus {
                border-color: #0066cc;
                border-width: 2px;
            }
        """)
        instructions_input.setMinimumHeight(100)
        instructions_input.setMaximumHeight(120)
        self.__layout.addWidget(LabeledSection("Instructions", instructions_input, "(Optional)"))

        # Upload section
        self.setup_upload_section()

    def setup_upload_section(self):
        # Main upload container
        upload_container = QFrame()
        upload_container.setStyleSheet("QFrame { border: none; }")
        upload_layout = QVBoxLayout(upload_container)
        upload_layout.setSpacing(10)
        upload_layout.setContentsMargins(0, 0, 0, 0)

        # Dashed border container for drag & drop and files
        self.upload_frame = QFrame()
        self.upload_frame.setStyleSheet("""
            QFrame {
                border: 2px dashed #999;
                border-radius: 8px;
                background-color: #fafafa;
            }
        """)
        self.upload_frame.setMinimumHeight(160)
        
        # Main content layout inside dashed border
        self.upload_content_layout = QVBoxLayout(self.upload_frame)
        self.upload_content_layout.setContentsMargins(20, 15, 20, 15)
        self.upload_content_layout.setSpacing(10)
        
        # Initial drag & drop content
        self.setup_drag_drop_content()
        
        # Scrollable area for selected files (initially hidden)
        self.setup_files_scroll_area()

        upload_layout.addWidget(self.upload_frame)

        # Upload Now button
        self.upload_now_btn = QPushButton("Upload Now")
        self.upload_now_btn.setStyleSheet("""
            QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #777;
            }
            QPushButton:pressed {
                background-color: #666;
            }
        """)
        self.upload_now_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        upload_layout.addWidget(self.upload_now_btn)

        self.__layout.addWidget(LabeledSection("Upload File", upload_container))

        self.upload_now_btn.clicked.connect(self.open_file_dialog)
    
    def setup_drag_drop_content(self):
        # Container for drag & drop elements
        self.drag_drop_container = QWidget()
        drag_drop_layout = QVBoxLayout(self.drag_drop_container)
        drag_drop_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drag_drop_layout.setSpacing(8)
        drag_drop_layout.setContentsMargins(0, 0, 0, 0)
        
        # File icon (using a more document-like appearance)
        file_icon = QLabel("📄")
        file_icon.setStyleSheet("font-size: 40px; border: none; color: #28a745;")
        file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        drag_label = QLabel("Drag n Drop here")
        drag_label.setStyleSheet("font-size: 16px; color: #333; border: none; font-weight: normal;")
        drag_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        or_label = QLabel("Or")
        or_label.setStyleSheet("font-size: 14px; color: #666; border: none;")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        browse_label = QLabel("Browse")
        browse_label.setStyleSheet("font-size: 16px; color: #333; border: none; font-weight: normal;")
        browse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        for widget in (file_icon, drag_label, or_label, browse_label):
            drag_drop_layout.addWidget(widget)
        
        self.upload_content_layout.addWidget(self.drag_drop_container)
        
    def setup_files_scroll_area(self):
        # Scroll area for selected files
        self.files_scroll_area = QScrollArea()
        self.files_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        self.files_scroll_area.setWidgetResizable(True)
        self.files_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.files_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.files_scroll_area.setMaximumHeight(250)
        self.files_scroll_area.hide()
        
        # Widget to contain the files in grid layout
        self.files_widget = QWidget()
        # Import QGridLayout
        from PyQt6.QtWidgets import QGridLayout
        self.files_grid_layout = QGridLayout(self.files_widget)
        self.files_grid_layout.setSpacing(10)
        self.files_grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.files_scroll_area.setWidget(self.files_widget)
        self.upload_content_layout.addWidget(self.files_scroll_area)

    def open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Documents (*.docx *.pdf *.txt *.doc)")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                # Add new files to the list (avoid duplicates)
                for filename in filenames:
                    if filename not in self.selected_files:
                        self.selected_files.append(filename)
                
                self.update_files_display()

    def update_files_display(self):
        # Clear existing file widgets
        for i in reversed(range(self.files_grid_layout.count())):
            child = self.files_grid_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        if self.selected_files:
            # Hide drag & drop content and show files
            self.drag_drop_container.hide()
            self.files_scroll_area.show()
            
            # Add files in a 2-column grid layout
            for index, file_path in enumerate(self.selected_files):
                file_widget = self.create_file_widget(file_path)
                row = index // 2
                col = index % 2
                self.files_grid_layout.addWidget(file_widget, row, col)
            
        else:
            # Show drag & drop content and hide files
            self.files_scroll_area.hide()
            self.drag_drop_container.show()

    def create_file_widget(self, file_path):
        # Extract filename from path
        import os
        filename = os.path.basename(file_path)
        
        # Create container for the file item
        file_container = QFrame()
        file_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px;
            }
            QFrame:hover {
                border-color: #ccc;
            }
        """)
        file_container.setMinimumHeight(55)
        file_container.setMaximumHeight(55)
        
        file_layout = QHBoxLayout(file_container)
        file_layout.setContentsMargins(10, 8, 10, 8)
        file_layout.setSpacing(12)
        
        # File icon
        file_icon = QLabel("📄")
        file_icon.setStyleSheet("font-size: 16px; border: none; color: #28a745;")
        file_icon.setFixedSize(20, 20)
        file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # File name label with word wrapping
        file_label = QLabel(filename)
        file_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333;
                border: none;
                line-height: 1.3;
                font-weight: 500;
                padding: 2px 0px;
            }
        """)
        file_label.setWordWrap(True)
        file_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        file_label.setToolTip(file_path)  # Show full path on hover
        
        # Remove button
        remove_btn = QPushButton("✕")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        remove_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        remove_btn.setToolTip("Remove file")
        
        # Connect remove button to remove function
        remove_btn.clicked.connect(lambda: self.remove_file(file_path))
        
        # Add widgets to layout
        file_layout.addWidget(file_icon)
        file_layout.addWidget(file_label, 1)  # Stretch factor 1 to take remaining space
        file_layout.addWidget(remove_btn)
        
        return file_container

    def remove_file(self, file_path):
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            self.update_files_display()

    def get_selected_files(self):
        """Return list of selected file paths"""
        return self.selected_files.copy()

    def clear_selected_files(self):
        """Clear all selected files"""
        self.selected_files.clear()
        self.update_files_display()