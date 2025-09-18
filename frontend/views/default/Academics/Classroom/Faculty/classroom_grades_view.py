from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, QMainWindow, 
    QLabel, QPushButton, QHeaderView, QSpacerItem, QSizePolicy, 
    QFrame, QComboBox, QTreeWidget, QTreeWidgetItem, QLineEdit,
    QMenu, QCheckBox, QToolButton
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QFont, QIcon, QAction
import sys


class CustomHeaderView(QHeaderView):
    # Custom header that can detect clicks and show visual indicators
    expand_clicked = pyqtSignal(int, str)  # column_index, column_name
    
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.expandable_columns = {}  # {column_index: {'name': str, 'expanded': bool}}
        
    def set_expandable_column(self, column_index, column_name, is_expanded=False):
        # Mark a column as expandable
        self.expandable_columns[column_index] = {
            'name': column_name,
            'expanded': is_expanded
        }
        self.update()
        
    def mousePressEvent(self, event):
        # Handle mouse clicks on header sections
        if event.button() == Qt.MouseButton.LeftButton:
            index = self.logicalIndexAt(event.pos())
            if index in self.expandable_columns:
                column_info = self.expandable_columns[index]
                column_info['expanded'] = not column_info['expanded']
                self.expand_clicked.emit(index, column_info['name'])
                self.update()
                return
        super().mousePressEvent(event)
        
    def paintSection(self, painter, rect, logicalIndex):
        # Custom painting for expandable columns
        super().paintSection(painter, rect, logicalIndex)
        
        if logicalIndex in self.expandable_columns:
            column_info = self.expandable_columns[logicalIndex]
            
            # Draw expand/collapse indicator
            painter.save()
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))  # Larger font
            
            indicator = "▼" if column_info['expanded'] else "▶"
            
            # Position the indicator at the RIGHT side of the header
            indicator_rect = rect.adjusted(rect.width() - 20, 0, -5, 0)
            painter.drawText(indicator_rect, Qt.AlignmentFlag.AlignCenter, indicator)
            
            painter.restore()


class CollapsibleGradesTable(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Track column states and structure
        self.column_states = {
            'midterm_expanded': False,
            'finalterm_expanded': False,
            'performance_task_midterm_expanded': False,
            'quiz_midterm_expanded': False,
            'exam_midterm_expanded': False,
            'performance_task_finalterm_expanded': False,
            'quiz_finalterm_expanded': False,
            'exam_finalterm_expanded': False,
        }
        
        # Sample data for different activities
        self.sample_data = {
            'performance_tasks': ['PT1', 'PT2', 'PT3'],
            'quizzes': ['Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4'],
            'exams': ['Prelim Exam', 'Final Exam']
        }
        
        self.setup_table()
        self.load_sample_data()
        
    def setup_table(self):
        self.custom_header = CustomHeaderView(Qt.Orientation.Horizontal, self)
        self.setHeader(self.custom_header)
        self.custom_header.expand_clicked.connect(self.on_header_expand_clicked)
        
        # Also connect to section clicked for additional handling
        self.custom_header.sectionClicked.connect(self.on_section_clicked)
        
        # Setup the initial table structure
        self.build_column_structure()

        self.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                alternate-background-color: #F8F9FA;
                border: none;
                font-family: 'Inter';
                gridline-color: #E0E0E0;
                color: #000000;
            }
            QTreeWidget::item {
                padding: 8px 4px;
                border-bottom: 1px solid #E0E0E0;
                min-height: 35px;
                color: #000000;
            }
            QTreeWidget::item:selected {
                background-color: #E8F5E8;
                color: #000000;
            }
            QTreeWidget::item:hover {
                background-color: #F0F8F0;
                color: #000000;
            }
        """)
        
        # Configure table appearance
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        
        # Header styling
        self.custom_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #084924;
                color: white;
                padding: 8px 4px;
                font-weight: bold;
                font-size: 11px;
                border: none;
                border-right: 1px solid #0A5A2A;
                min-height: 40px;
                text-align: left;
            }
            QHeaderView::section:hover {
                background-color: #0A5A2A;
                cursor: pointer;
            }
        """)
        
    def build_column_structure(self):
        # Build column structure based on current states
        columns = []
        self.column_info = {}  # Track column types and purposes
        
        # Base columns
        columns.extend([
            {'name': 'No.', 'type': 'fixed', 'width': 50},
            {'name': 'Sort by Last Name', 'type': 'fixed', 'width': 200}
        ])
        
        # Midterm section
        if self.column_states['midterm_expanded']:
            # Add component columns
            if self.column_states['performance_task_midterm_expanded']:
                for pt in self.sample_data['performance_tasks']:
                    columns.append({
                        'name': f'{pt} (M)', 
                        'type': 'grade_input', 
                        'width': 80, 
                        'term': 'midterm', 
                        'component': 'performance_task'
                    })
            else:
                columns.append({
                    'name': 'Performance Task', 
                    'type': 'expandable_component', 
                    'width': 120, 
                    'term': 'midterm', 
                    'component': 'performance_task'
                })
            
            if self.column_states['quiz_midterm_expanded']:
                for quiz in self.sample_data['quizzes']:
                    columns.append({
                        'name': f'{quiz} (M)', 
                        'type': 'grade_input', 
                        'width': 80, 
                        'term': 'midterm', 
                        'component': 'quiz'
                    })
            else:
                columns.append({
                    'name': 'Quiz', 
                    'type': 'expandable_component', 
                    'width': 80, 
                    'term': 'midterm', 
                    'component': 'quiz'
                })
            
            if self.column_states['exam_midterm_expanded']:
                for exam in self.sample_data['exams']:
                    columns.append({
                        'name': f'{exam} (M)', 
                        'type': 'grade_input', 
                        'width': 100, 
                        'term': 'midterm', 
                        'component': 'exam'
                    })
            else:
                columns.append({
                    'name': 'Exam', 
                    'type': 'expandable_component', 
                    'width': 80, 
                    'term': 'midterm', 
                    'component': 'exam'
                })
                
            columns.append({'name': 'Midterm Grade', 'type': 'calculated', 'width': 100})
        else:
            columns.append({
                'name': 'Midterm Grade', 
                'type': 'expandable_main', 
                'width': 120, 
                'target': 'midterm'
            })
        
        # Final term section
        if self.column_states['finalterm_expanded']:
            if self.column_states['performance_task_finalterm_expanded']:
                for pt in self.sample_data['performance_tasks']:
                    columns.append({
                        'name': f'{pt} (F)', 
                        'type': 'grade_input', 
                        'width': 80, 
                        'term': 'finalterm', 
                        'component': 'performance_task'
                    })
            else:
                columns.append({
                    'name': 'Performance Task', 
                    'type': 'expandable_component', 
                    'width': 120, 
                    'term': 'finalterm', 
                    'component': 'performance_task'
                })
            
            if self.column_states['quiz_finalterm_expanded']:
                for quiz in self.sample_data['quizzes']:
                    columns.append({
                        'name': f'{quiz} (F)', 
                        'type': 'grade_input', 
                        'width': 80, 
                        'term': 'finalterm', 
                        'component': 'quiz'
                    })
            else:
                columns.append({
                    'name': 'Quiz', 
                    'type': 'expandable_component', 
                    'width': 80, 
                    'term': 'finalterm', 
                    'component': 'quiz'
                })
            
            if self.column_states['exam_finalterm_expanded']:
                for exam in self.sample_data['exams']:
                    columns.append({
                        'name': f'{exam} (F)', 
                        'type': 'grade_input', 
                        'width': 100, 
                        'term': 'finalterm', 
                        'component': 'exam'
                    })
            else:
                columns.append({
                    'name': 'Exam', 
                    'type': 'expandable_component', 
                    'width': 80, 
                    'term': 'finalterm', 
                    'component': 'exam'
                })
                
            columns.append({'name': 'Final Term Grade', 'type': 'calculated', 'width': 120})
        else:
            columns.append({
                'name': 'Final Term Grade', 
                'type': 'expandable_main', 
                'width': 130, 
                'target': 'finalterm'
            })
        
        # Final grade
        columns.append({'name': 'Final Grade', 'type': 'calculated', 'width': 100})
        
        # Set up the table
        self.setColumnCount(len(columns))
        self.column_info = {i: col for i, col in enumerate(columns)}
        
        # Set column widths
        for i, col in enumerate(columns):
            self.setColumnWidth(i, col['width'])
        
        # Setup headers with expand indicators
        self.setup_expandable_headers(columns)
        
    def setup_expandable_headers(self, columns):
        # Set basic header labels with indicators
        labels = []
        for col in columns:
            if col['type'] in ['expandable_main', 'expandable_component']:
                is_expanded = False
                
                if col['type'] == 'expandable_main':
                    is_expanded = self.column_states.get(f"{col['target']}_expanded", False)
                elif col['type'] == 'expandable_component':
                    key = f"{col['component']}_{col['term']}_expanded"
                    is_expanded = self.column_states.get(key, False)
                
                # Add indicator to the label text itself as fallback
                indicator = " ▼" if is_expanded else " ▶"
                labels.append(col['name'] + indicator)
            else:
                labels.append(col['name'])
        
        self.setHeaderLabels(labels)
        
        # Mark expandable columns in custom header
        for i, col in enumerate(columns):
            if col['type'] in ['expandable_main', 'expandable_component']:
                is_expanded = False
                
                if col['type'] == 'expandable_main':
                    is_expanded = self.column_states.get(f"{col['target']}_expanded", False)
                elif col['type'] == 'expandable_component':
                    key = f"{col['component']}_{col['term']}_expanded"
                    is_expanded = self.column_states.get(key, False)
                
                self.custom_header.set_expandable_column(i, col['name'], is_expanded)
    
    def on_header_expand_clicked(self, column_index, column_name):
        # Handle header expansion clicks
        # Remove the indicator from column name for comparison
        clean_column_name = column_name.replace(" ▶", "").replace(" ▼", "")
        print(f"Header clicked: {clean_column_name} at index {column_index}")  # Debug print
        print(f"Current column states: {self.column_states}")  # Debug print
        
        col_info = self.column_info.get(column_index, {})
        col_type = col_info.get('type', '')
        
        print(f"Column type: {col_type}")  # Debug print
        
        if col_type == 'expandable_main':
            target = col_info.get('target')
            if target:
                key = f"{target}_expanded"
                old_state = self.column_states[key]
                self.column_states[key] = not self.column_states[key]
                print(f"Toggling {key}: {old_state} -> {self.column_states[key]}")  # Debug print
                self.rebuild_table()
                
        elif col_type == 'expandable_component':
            term = col_info.get('term')
            component = col_info.get('component')
            if term and component:
                key = f"{component}_{term}_expanded"
                old_state = self.column_states[key]
                self.column_states[key] = not self.column_states[key]
                print(f"Toggling {key}: {old_state} -> {self.column_states[key]}")  # Debug print
                self.rebuild_table()
        
        print(f"Updated column states: {self.column_states}")  # Debug print
    
    def on_section_clicked(self, logical_index):
        # Additional handler for section clicks
        print(f"Section clicked at index: {logical_index}")
        
        # Get the header text
        header_item = self.headerItem()
        if header_item:
            header_text = header_item.text(logical_index)
            print(f"Header text: {header_text}")
            
            # Check if this is an expandable column based on header text
            if "▶" in header_text or "▼" in header_text:
                clean_name = header_text.replace(" ▶", "").replace(" ▼", "")
                print(f"Expandable column detected: {clean_name}")
                
                # Find the matching column info
                col_info = self.column_info.get(logical_index, {})
                col_type = col_info.get('type', '')
                
                if col_type == 'expandable_main':
                    target = col_info.get('target')
                    if target:
                        key = f"{target}_expanded"
                        self.column_states[key] = not self.column_states[key]
                        print(f"Direct toggle {key}: {self.column_states[key]}")
                        self.rebuild_table()
                        
                elif col_type == 'expandable_component':
                    term = col_info.get('term')
                    component = col_info.get('component')
                    if term and component:
                        key = f"{component}_{term}_expanded"
                        self.column_states[key] = not self.column_states[key]
                        print(f"Direct toggle {key}: {self.column_states[key]}")
                        self.rebuild_table()
    
    def rebuild_table(self):
        # Rebuild table structure while preserving data
        print("Rebuilding table...")  # Debug print
        print(f"States before rebuild: {self.column_states}")  # Debug print
        
        # Save current data
        saved_data = self.save_table_data()
        
        # Clear and rebuild
        self.clear()
        self.build_column_structure()
        
        # Restore data
        self.restore_table_data(saved_data)
        
        print(f"Table rebuilt with {self.columnCount()} columns")  # Debug print
        print(f"States after rebuild: {self.column_states}")  # Debug print
        
        # Force update of header indicators
        self.custom_header.update()
    
    def save_table_data(self):
        # Save current table data
        data = []
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            row_data = {
                'no': item.text(0),
                'name': item.text(1),
                'grades': {}
            }
            
            # Save all grade inputs
            for col in range(self.columnCount()):
                widget = self.itemWidget(item, col)
                if isinstance(widget, QLineEdit):
                    col_info = self.column_info.get(col, {})
                    key = f"{col}_{col_info.get('name', '')}"
                    row_data['grades'][key] = widget.text()
                elif isinstance(widget, QLabel):
                    col_info = self.column_info.get(col, {})
                    key = f"{col}_{col_info.get('name', '')}"
                    row_data['grades'][key] = widget.text()
                    
            data.append(row_data)
        return data
    
    def restore_table_data(self, saved_data):
        # Restore table data after rebuild
        for row_data in saved_data:
            self.add_student_row(row_data['name'], row_data['no'], row_data.get('grades', {}))
    
    def load_sample_data(self):
        # Load sample student data
        sample_students = [
            "Castro, Carlos Fidel",
            "Santos, Maria Elena", 
            "Garcia, Juan Pablo",
            "Rodriguez, Ana Sofia"
        ]
        
        for i, student_name in enumerate(sample_students, 1):
            self.add_student_row(student_name, str(i))
    
    def add_student_row(self, student_name, student_number, saved_grades=None):
        # Add a student row with appropriate widgets
        item = QTreeWidgetItem(self)
        
        # Set basic info with black text color
        item.setText(0, student_number)
        item.setText(1, student_name)
        
        # Set text color to black for basic columns
        item.setForeground(0, QColor("#000000"))
        item.setForeground(1, QColor("#000000"))
        
        # Add widgets for each column
        for col_index in range(2, self.columnCount()):
            col_info = self.column_info.get(col_index, {})
            col_type = col_info.get('type', '')
            col_name = col_info.get('name', '')
            
            if col_type == 'grade_input':
                # Individual grade input
                grade_input = self.create_grade_input()
                
                # Restore saved data if available
                if saved_grades:
                    saved_key = f"{col_index}_{col_name}"
                    if saved_key in saved_grades:
                        grade_input.setText(saved_grades[saved_key])
                
                self.setItemWidget(item, col_index, grade_input)
                
            elif col_type in ['calculated', 'expandable_main']:
                # Calculated grade display
                grade_display = self.create_grade_display()
                
                # Restore saved data if available
                if saved_grades:
                    saved_key = f"{col_index}_{col_name}"
                    if saved_key in saved_grades:
                        grade_display.setText(saved_grades[saved_key])
                
                self.setItemWidget(item, col_index, grade_display)
                
            elif col_type == 'expandable_component':
                # Component summary (calculated from individual activities)
                component_display = self.create_grade_display()
                self.setItemWidget(item, col_index, component_display)
        
        # Calculate initial grades
        self.calculate_grades_for_student(item)
    
    def create_grade_input(self, value=""):
        # Create a grade input field
        input_field = QLineEdit()
        input_field.setText(value)
        input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_field.setPlaceholderText("0-100")
        input_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 3px;
                padding: 6px;
                background-color: white;
                font-size: 11px;
                color: #000000;
            }
            QLineEdit:focus {
                border: 2px solid #084924;
                background-color: #F9FFF9;
                color: #000000;
            }
            QLineEdit:hover {
                border: 1px solid #084924;
                color: #000000;
            }
        """)
        
        # Connect to calculation
        input_field.textChanged.connect(lambda: self.calculate_all_grades())
        
        return input_field
    
    def create_grade_display(self, value="0.00"):
        # Create a grade display label
        label = QLabel(value)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-weight: bold;
                font-size: 11px;
                padding: 6px;
                background-color: #F8F9FA;
                border-radius: 3px;
                border: 1px solid #E0E0E0;
            }
        """)
        return label
    
    def calculate_all_grades(self):
        # Calculate grades for all students
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            self.calculate_grades_for_student(item)
    
    def calculate_grades_for_student(self, item):
        # Calculate grades for a specific student
        # This is where to implement grade calcu
        
        midterm_total = 0
        midterm_count = 0
        finalterm_total = 0
        finalterm_count = 0
        
        # Calculate component and term grades
        for col_index in range(self.columnCount()):
            col_info = self.column_info.get(col_index, {})
            widget = self.itemWidget(item, col_index)
            
            if col_info.get('type') == 'grade_input' and isinstance(widget, QLineEdit):
                try:
                    grade = float(widget.text()) if widget.text() else 0
                    term = col_info.get('term', '')
                    
                    if term == 'midterm':
                        midterm_total += grade
                        midterm_count += 1
                    elif term == 'finalterm':
                        finalterm_total += grade
                        finalterm_count += 1
                        
                except ValueError:
                    continue
        
        # Update calculated displays
        for col_index in range(self.columnCount()):
            col_info = self.column_info.get(col_index, {})
            widget = self.itemWidget(item, col_index)
            
            if isinstance(widget, QLabel):
                col_name = col_info.get('name', '')
                
                if 'Midterm Grade' in col_name:
                    avg = midterm_total / midterm_count if midterm_count > 0 else 0
                    widget.setText(f"{avg:.2f}")
                elif 'Final Term Grade' in col_name:
                    avg = finalterm_total / finalterm_count if finalterm_count > 0 else 0
                    widget.setText(f"{avg:.2f}")
                elif 'Final Grade' in col_name:
                    midterm_avg = midterm_total / midterm_count if midterm_count > 0 else 0
                    finalterm_avg = finalterm_total / finalterm_count if finalterm_count > 0 else 0
                    final_grade = (midterm_avg * 1/3) + (finalterm_avg * 2/3)
                    widget.setText(f"{final_grade:.2f}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Classroom Grades")
        self.setAutoFillBackground(True)
        self.setFixedSize(QSize(1400, 700))
        
        # Main container
        container = QWidget()
        container.setAutoFillBackground(True)
        pal = container.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor("white"))
        container.setPalette(pal)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Rubrics dropdown
        self.rubrics_combo = QComboBox()
        self.rubrics_combo.addItems([
            "Overall Lecture",
            "Performance Task",
            "Quiz", 
            "Exam"
        ])
        self.rubrics_combo.setFixedWidth(150)
        self.rubrics_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
                font-size: 12px;
                color: #084924;
                background-color: white;
                font-weight: bold;
            }
            QComboBox:focus {
                border: 2px solid #084924;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #084924;
                selection-background-color: #E8F5E8;
            }
        """)
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # Info label
        info_label = QLabel("💡 Click column headers with ▶ to expand/collapse")
        info_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 11px;
                font-style: italic;
            }
        """)
        
        # Grading System label
        grading_label = QLabel("Grading System")
        grading_label.setStyleSheet("""
            QLabel {
                background-color: #FDC601;
                color: white;
                border-radius: 3px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        
        # Download button
        download_button = QPushButton("📥 Download")
        download_button.setStyleSheet("""
            QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0A5A2A;
            }
        """)
        
        # Add to header
        header_layout.addWidget(self.rubrics_combo)
        header_layout.addItem(spacer)
        header_layout.addWidget(info_label)
        header_layout.addWidget(grading_label)
        header_layout.addWidget(download_button)
        
        # Create grades table
        self.grades_table = CollapsibleGradesTable()
        
        # Add to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.grades_table)
        
        container.setLayout(main_layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()