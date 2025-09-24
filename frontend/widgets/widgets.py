import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor


class AcademicTableWidget(QTableWidget):
    """
    Reusable table widget designed for academic scheduling systems.
    Features green header styling and customizable column configurations.
    """
    
    # Signals
    rowSelected = pyqtSignal(int, dict)  # row_index, row_data
    buttonClicked = pyqtSignal(str, int, dict)  # button_name, row_index, row_data
    
    def __init__(self, columns=None, button_configs=None, parent=None):
        super().__init__(parent)
        
        # Default columns if none provided
        if columns is None:
            columns = ['No.', 'Code', 'Title', 'Units', 'Section', 'Schedule', 'Room', 'Instructor', 'Type']
        
        self.columns = columns
        self.button_configs = button_configs or []  # List of button configurations
        self.row_buttons = {}  # Store button references by row
        
        # Add button columns to the column list if buttons are configured
        if self.button_configs:
            self.columns = self.columns + ['Actions']
        
        self.setup_table()
        self.setup_styling()
        self.setup_signals()
    
    def setup_table(self):
        """Initialize table structure and properties."""
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        
        # Table behavior settings
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        
        # Header settings
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # Auto-resize columns to content
        self.resizeColumnsToContents()
    
    def setup_styling(self):
        """Apply the green header styling to match the UI design."""
        # Set header stylesheet for green background
        header_style = """
            QHeaderView::section {
                background-color: #2d5a3d;
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                border: 1px solid #1e3a28;
                text-align: center;
            }
            QHeaderView::section:hover {
                background-color: #3d6a4d;
            }
        """
        
        # Set table stylesheet
        table_style = """
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
                selection-color: black;
                border: 1px solid #ddd;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
            }
        """
        
        self.setStyleSheet(header_style + table_style)
        
        # Set font
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
    
    def setup_signals(self):
        """Connect internal signals."""
        self.itemSelectionChanged.connect(self.on_selection_changed)
    
    def add_row(self, row_data, editable_columns=None):
        """
        Add a row to the table.
        
        Args:
            row_data (dict or list): Data for the row. If dict, keys should match column names.
            editable_columns (list): List of column indices that should be editable.
        """
        if editable_columns is None:
            editable_columns = []
        
        row_position = self.rowCount()
        self.insertRow(row_position)
        
        # Handle both dict and list input
        data_columns = self.columns[:-1] if self.button_configs else self.columns
        
        if isinstance(row_data, dict):
            for col_index, column_name in enumerate(data_columns):
                value = str(row_data.get(column_name, ''))
                item = QTableWidgetItem(value)
                
                # Set item as non-editable unless specified
                if col_index not in editable_columns:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                self.setItem(row_position, col_index, item)
        
        elif isinstance(row_data, list):
            for col_index, value in enumerate(row_data):
                if col_index < len(data_columns):
                    item = QTableWidgetItem(str(value))
                    
                    # Set item as non-editable unless specified
                    if col_index not in editable_columns:
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    self.setItem(row_position, col_index, item)
        
        # Add buttons if configured
        if self.button_configs:
            self.add_buttons_to_row(row_position)
        
        # Auto-resize after adding data
        self.resizeColumnsToContents()
    
    def add_buttons_to_row(self, row_index):
        """Add configured buttons to a specific row."""
        if not self.button_configs:
            return
        
        # Create a widget to hold the buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(2, 2, 2, 2)
        button_layout.setSpacing(2)
        
        row_buttons = []
        
        for button_config in self.button_configs:
            button = QPushButton(button_config.get('text', 'Button'))
            
            # Apply styling if provided
            if 'style' in button_config:
                button.setStyleSheet(button_config['style'])
            
            # Set size if provided
            if 'size' in button_config:
                size = button_config['size']
                button.setFixedSize(size[0], size[1])
            
            # Set tooltip if provided
            if 'tooltip' in button_config:
                button.setToolTip(button_config['tooltip'])
            
            # Connect button click with row data
            button_name = button_config.get('name', f"button_{len(row_buttons)}")
            button.clicked.connect(
                lambda checked, name=button_name, row=row_index: self.on_button_clicked(name, row)
            )
            
            button_layout.addWidget(button)
            row_buttons.append(button)
        
        # Store button references
        self.row_buttons[row_index] = row_buttons
        
        # Set the widget in the actions column
        actions_column = len(self.columns) - 1
        self.setCellWidget(row_index, actions_column, button_widget)
    
    def on_button_clicked(self, button_name, row_index):
        """Handle button clicks and emit signal with row data."""
        row_data = self.get_row_data(row_index)
        self.buttonClicked.emit(button_name, row_index, row_data)
    
    def add_multiple_rows(self, rows_data, editable_columns=None):
        """Add multiple rows at once."""
        for row_data in rows_data:
            self.add_row(row_data, editable_columns)
    
    def get_row_data(self, row_index):
        """Get data from a specific row as a dictionary (excluding button column)."""
        if row_index < 0 or row_index >= self.rowCount():
            return {}
        
        row_data = {}
        data_columns = self.columns[:-1] if self.button_configs else self.columns
        
        for col_index, column_name in enumerate(data_columns):
            item = self.item(row_index, col_index)
            row_data[column_name] = item.text() if item else ''
        
        return row_data
    
    def get_selected_row_data(self):
        """Get data from the currently selected row."""
        selected_rows = self.selectionModel().selectedRows()
        if selected_rows:
            row_index = selected_rows[0].row()
            return self.get_row_data(row_index)
        return {}
    
    def clear_table(self):
        """Clear all rows from the table."""
        self.row_buttons.clear()
        self.setRowCount(0)
    
    def on_selection_changed(self):
        """Handle row selection changes."""
        selected_rows = self.selectionModel().selectedRows()
        if selected_rows:
            row_index = selected_rows[0].row()
            row_data = self.get_row_data(row_index)
            self.rowSelected.emit(row_index, row_data)
    
    def set_column_widths(self, widths):
        """
        Set specific widths for columns.
        
        Args:
            widths (dict): Dictionary with column names as keys and widths as values.
        """
        for column_name, width in widths.items():
            if column_name in self.columns:
                col_index = self.columns.index(column_name)
                self.setColumnWidth(col_index, width)


class DemoWindow(QMainWindow):
    """Demo window showing both table configurations from the images."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Academic Table Widget Demo")
        self.setGeometry(100, 100, 1400, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create first table (Program Information - no buttons)
        self.create_program_table(layout)
        
        # Create second table (Course Schedule - with buttons)
        self.create_schedule_table(layout)
        
        # Add control buttons
        self.create_controls(layout)
    
    def create_program_table(self, layout):
        """Create the program information table."""
        # Table 1: Program Information
        program_columns = ['No.', 'Section', 'Program', 'Year', 'Type', 'Capacity', 'Remarks']
        self.program_table = AcademicTableWidget(program_columns)
        
        # Sample data for program table
        program_data = [
            ['2', 'B', 'BS Information Technology', '2', 'Lecture', '50', 'Regular'],
            ['2', 'B', 'BS Information Technology', '2', 'Lecture', '50', 'Regular']
        ]
        
        self.program_table.add_multiple_rows(program_data)
        
        # Set custom column widths
        program_widths = {
            'No.': 60,
            'Section': 80,
            'Program': 250,
            'Year': 60,
            'Type': 100,
            'Capacity': 80,
            'Remarks': 100
        }
        self.program_table.set_column_widths(program_widths)
        
        layout.addWidget(self.program_table)
    
    def create_schedule_table(self, layout):
        """Create the course schedule table with action buttons."""
        # Table 2: Course Schedule with buttons
        schedule_columns = ['No.', 'Code', 'Title', 'Units', 'Section', 'Schedule', 'Room', 'Instructor', 'Type']
        
        # Configure buttons for this table
        button_configs = [
            {
                'name': 'edit',
                'text': 'Edit',
                'style': '''
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 3px;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                ''',
                'size': (50, 25),
                'tooltip': 'Edit this course'
            },
            {
                'name': 'delete',
                'text': 'Delete',
                'style': '''
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 3px;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;
                    }
                ''',
                'size': (50, 25),
                'tooltip': 'Delete this course'
            },
            {
                'name': 'view',
                'text': 'View',
                'style': '''
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 3px;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                ''',
                'size': (50, 25),
                'tooltip': 'View course details'
            }
        ]
        
        self.schedule_table = AcademicTableWidget(schedule_columns, button_configs)
        
        # Sample data for schedule table
        schedule_data = [
            {
                'No.': '1',
                'Code': 'IT57',
                'Title': 'Fundamentals of Database',
                'Units': '3',
                'Section': '3A',
                'Schedule': 'TTH 7:00 - 7:30 AM',
                'Room': 'CISC Room 3',
                'Instructor': 'Juan Dela Cruz',
                'Type': 'Regular'
            },
            {
                'No.': '2',
                'Code': 'IT101',
                'Title': 'Programming Fundamentals',
                'Units': '3',
                'Section': '1A',
                'Schedule': 'MWF 8:00 - 9:00 AM',
                'Room': 'CISC Room 1',
                'Instructor': 'Maria Santos',
                'Type': 'Regular'
            }
        ]
        
        self.schedule_table.add_multiple_rows(schedule_data)
        
        # Set custom column widths
        schedule_widths = {
            'No.': 50,
            'Code': 80,
            'Title': 180,
            'Units': 60,
            'Section': 80,
            'Schedule': 150,
            'Room': 120,
            'Instructor': 130,
            'Type': 80,
            'Actions': 180
        }
        self.schedule_table.set_column_widths(schedule_widths)
        
        layout.addWidget(self.schedule_table)
        
        # Connect signals
        self.schedule_table.rowSelected.connect(self.on_row_selected)
        self.schedule_table.buttonClicked.connect(self.on_button_clicked)
    
    def create_controls(self, layout):
        """Create control buttons for demonstration."""
        controls_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Sample Row")
        add_btn.clicked.connect(self.add_sample_row)
        
        clear_btn = QPushButton("Clear Tables")
        clear_btn.clicked.connect(self.clear_tables)
        
        get_selection_btn = QPushButton("Get Selected Data")
        get_selection_btn.clicked.connect(self.get_selected_data)
        
        controls_layout.addWidget(add_btn)
        controls_layout.addWidget(clear_btn)
        controls_layout.addWidget(get_selection_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
    
    def add_sample_row(self):
        """Add a sample row to demonstrate functionality."""
        new_course = {
            'No.': str(self.schedule_table.rowCount() + 1),
            'Code': 'CS201',
            'Title': 'Data Structures',
            'Units': '3',
            'Section': '2B',
            'Schedule': 'TTH 10:00 - 11:30 AM',
            'Room': 'CISC Room 2',
            'Instructor': 'Dr. Jane Smith',
            'Type': 'Regular'
        }
        self.schedule_table.add_row(new_course)
    
    def clear_tables(self):
        """Clear both tables."""
        self.program_table.clear_table()
        self.schedule_table.clear_table()
    
    def get_selected_data(self):
        """Print selected row data."""
        data = self.schedule_table.get_selected_row_data()
        if data:
            print("Selected row data:")
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print("No row selected")
    
    def on_row_selected(self, row_index, row_data):
        """Handle row selection."""
        print(f"Row {row_index} selected: {row_data.get('Title', 'N/A')}")
    
    def on_button_clicked(self, button_name, row_index, row_data):
        """Handle button clicks in table rows."""
        course_title = row_data.get('Title', 'Unknown Course')
        course_code = row_data.get('Code', 'N/A')
        
        if button_name == 'edit':
            print(f"Edit button clicked for: {course_code} - {course_title}")
            # Here you could open an edit dialog
            
        elif button_name == 'delete':
            print(f"Delete button clicked for: {course_code} - {course_title}")
            # Here you could show a confirmation dialog and then delete the row
            # For demo, we'll actually delete the row
            self.schedule_table.removeRow(row_index)
            
        elif button_name == 'view':
            print(f"View button clicked for: {course_code} - {course_title}")
            # Here you could open a detailed view dialog
            print("Course Details:")
            for key, value in row_data.items():
                print(f"  {key}: {value}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = DemoWindow()
    window.show()
    
    sys.exit(app.exec())