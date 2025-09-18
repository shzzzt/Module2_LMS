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
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            
            # Use > for expanded, < for collapsed
            indicator = ">" if column_info['expanded'] else "<"
            
            # Position at RIGHT side of header
            indicator_rect = rect.adjusted(rect.width() - 20, 0, -5, 0)
            painter.drawText(indicator_rect, Qt.AlignmentFlag.AlignCenter, indicator)
            
            painter.restore()


class CollapsibleGradesTable(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Track column states
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
        
        # Sample data
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

        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)

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
        
        # Initial structure
        self.build_initial_structure()

    def build_initial_structure(self):
        # Base columns
        columns = [
            {'name': 'No.', 'type': 'fixed', 'width': 50},
            {'name': 'Sort by Last Name', 'type': 'fixed', 'width': 200},
            {
                'name': 'Midterm Grade', 
                'type': 'expandable_main', 
                'width': 120, 
                'target': 'midterm'
            },
            {
                'name': 'Final Term Grade', 
                'type': 'expandable_main', 
                'width': 130, 
                'target': 'finalterm'
            },
            {'name': 'Final Grade', 'type': 'calculated', 'width': 100}
        ]

        # Set up initial table
        self.setColumnCount(len(columns))
        self.column_info = {i: col for i, col in enumerate(columns)}
        for i, col in enumerate(columns):
            self.setColumnWidth(i, col['width'])

        # Setup headers
        self.setup_expandable_headers(columns)

    def setup_expandable_headers(self, columns):
        labels = []
        for col in columns:
            if col['type'] in ['expandable_main', 'expandable_component']:
                is_expanded = False
                if col['type'] == 'expandable_main':
                    is_expanded = self.column_states.get(f"{col['target']}_expanded", False)
                elif col['type'] == 'expandable_component':
                    key = f"{col['component']}_{col['term']}_expanded"
                    is_expanded = self.column_states.get(key, False)
                
                indicator = " >" if is_expanded else " <"
                labels.append(col['name'] + indicator)
            else:
                labels.append(col['name'])
        self.setHeaderLabels(labels)

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
        clean_name = column_name.replace(" >", "").replace(" <", "")
        col_info = self.column_info.get(column_index, {})
        col_type = col_info.get('type', '')

        if col_type == 'expandable_main':
            target = col_info.get('target')
            if target:
                key = f"{target}_expanded"
                self.column_states[key] = not self.column_states.get(key, False)
                self.rebuild_table()

        elif col_type == 'expandable_component':
            term = col_info.get('term')
            component = col_info.get('component')
            if term and component:
                key = f"{component}_{term}_expanded"
                self.column_states[key] = not self.column_states.get(key, False)
                self.rebuild_table()

    def rebuild_table(self):
        saved_data = self.save_table_data()
        self.clear()
        self.build_column_structure()
        self.restore_table_data(saved_data)
        self.custom_header.update()

    def build_column_structure(self):
        # Start with base columns
        columns = [
            {'name': 'No.', 'type': 'fixed', 'width': 50},
            {'name': 'Sort by Last Name', 'type': 'fixed', 'width': 200}
        ]

        # Midterm section
        midterm_index = len(columns)
        columns.append({
            'name': 'Midterm Grade', 
            'type': 'expandable_main', 
            'width': 120, 
            'target': 'midterm'
        })

        if self.column_states.get('midterm_expanded', False):
            # Add components after Midterm Grade
            component_columns = []

            # Performance Task (always visible when midterm is expanded)
            pt_index = len(component_columns)
            component_columns.append({
                'name': 'Performance Task', 
                'type': 'expandable_component', 
                'width': 120, 
                'term': 'midterm', 
                'component': 'performance_task'
            })

            # Add PT components if PT is expanded
            if self.column_states.get('performance_task_midterm_expanded', False):
                for pt in self.sample_data['performance_tasks']:
                    component_columns.append({
                        'name': f'{pt} (M)', 
                        'type': 'grade_input', 
                        'width': 80, 
                        'term': 'midterm', 
                        'component': 'performance_task',
                        'format': 'score/max'
                    })

            # Quiz (always visible when midterm is expanded)
            quiz_index = len(component_columns)
            component_columns.append({
                'name': 'Quiz', 
                'type': 'expandable_component', 
                'width': 80, 
                'term': 'midterm', 
                'component': 'quiz'
            })

            # Add Quiz components if Quiz is expanded
            if self.column_states.get('quiz_midterm_expanded', False):
                for quiz in self.sample_data['quizzes']:
                    component_columns.append({
                        'name': f'{quiz} (M)', 
                        'type': 'grade_input', 
                        'width': 80, 
                        'term': 'midterm', 
                        'component': 'quiz',
                        'format': 'score/max'
                    })

            # Exam (always visible when midterm is expanded)
            exam_index = len(component_columns)
            component_columns.append({
                'name': 'Exam', 
                'type': 'expandable_component', 
                'width': 80, 
                'term': 'midterm', 
                'component': 'exam'
            })

            # Add Exam components if Exam is expanded
            if self.column_states.get('exam_midterm_expanded', False):
                for exam in self.sample_data['exams']:
                    component_columns.append({
                        'name': f'{exam} (M)', 
                        'type': 'grade_input', 
                        'width': 100, 
                        'term': 'midterm', 
                        'component': 'exam',
                        'format': 'score/max'
                    })

            # Insert component columns after Midterm Grade
            for i, col in enumerate(component_columns):
                columns.insert(midterm_index + 1 + i, col)

        # Final term section
        finalterm_index = len(columns)
        columns.append({
            'name': 'Final Term Grade', 
            'type': 'expandable_main', 
            'width': 130, 
            'target': 'finalterm'
        })

        if self.column_states.get('finalterm_expanded', False):
            component_columns = []

            # Performance Task (always visible when finalterm is expanded)
            pt_index = len(component_columns)
            component_columns.append({
                'name': 'Performance Task', 
                'type': 'expandable_component', 
                'width': 120, 
                'term': 'finalterm', 
                'component': 'performance_task'
            })

            # Add PT components if PT is expanded
            if self.column_states.get('performance_task_finalterm_expanded', False):
                for pt in self.sample_data['performance_tasks']:
                    component_columns.append({
                        'name': f'{pt} (F)', 
                        'type': 'grade_input', 
                        'width': 80, 
                        'term': 'finalterm', 
                        'component': 'performance_task',
                        'format': 'score/max'
                    })

            # Quiz (always visible when finalterm is expanded)
            quiz_index = len(component_columns)
            component_columns.append({
                'name': 'Quiz', 
                'type': 'expandable_component', 
                'width': 80, 
                'term': 'finalterm', 
                'component': 'quiz'
            })

            # Add Quiz components if Quiz is expanded
            if self.column_states.get('quiz_finalterm_expanded', False):
                for quiz in self.sample_data['quizzes']:
                    component_columns.append({
                        'name': f'{quiz} (F)', 
                        'type': 'grade_input', 
                        'width': 80, 
                        'term': 'finalterm', 
                        'component': 'quiz',
                        'format': 'score/max'
                    })

            # Exam (always visible when finalterm is expanded)
            exam_index = len(component_columns)
            component_columns.append({
                'name': 'Exam', 
                'type': 'expandable_component', 
                'width': 80, 
                'term': 'finalterm', 
                'component': 'exam'
            })

            # Add Exam components if Exam is expanded
            if self.column_states.get('exam_finalterm_expanded', False):
                for exam in self.sample_data['exams']:
                    component_columns.append({
                        'name': f'{exam} (F)', 
                        'type': 'grade_input', 
                        'width': 100, 
                        'term': 'finalterm', 
                        'component': 'exam',
                        'format': 'score/max'
                    })

            # Insert component columns after Final Term Grade
            for i, col in enumerate(component_columns):
                columns.insert(finalterm_index + 1 + i, col)

        # Final Grade
        columns.append({'name': 'Final Grade', 'type': 'calculated', 'width': 100})

        # Rebuild table
        self.setColumnCount(len(columns))
        self.column_info = {i: col for i, col in enumerate(columns)}
        for i, col in enumerate(columns):
            self.setColumnWidth(i, col['width'])

        self.setup_expandable_headers(columns)

    def save_table_data(self):
        data = []
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            row_data = {
                'no': item.text(0),
                'name': item.text(1),
                'grades': {}
            }
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
        for row_data in saved_data:
            self.add_student_row(row_data['name'], row_data['no'], row_data.get('grades', {}))

    def load_sample_data(self):
        students = [
            "Castro, Carlos Fidel",
            "Santos, Maria Elena",
            "Garcia, Juan Pablo",
            "Rodriguez, Ana Sofia"
        ]
        for i, name in enumerate(students, 1):
            self.add_student_row(name, str(i))

    def add_student_row(self, student_name, student_number, saved_grades=None):
        item = QTreeWidgetItem(self)
        item.setText(0, student_number)
        item.setText(1, student_name)
        item.setForeground(0, QColor("#000000"))
        item.setForeground(1, QColor("#000000"))

        for col_index in range(2, self.columnCount()):
            col_info = self.column_info.get(col_index, {})
            col_type = col_info.get('type', '')
            col_name = col_info.get('name', '')

            if col_type == 'grade_input':
                input_field = self.create_grade_input()
                if saved_grades:
                    saved_key = f"{col_index}_{col_name}"
                    if saved_key in saved_grades:
                        input_field.setText(saved_grades[saved_key])
                input_field.textChanged.connect(lambda: self.calculate_all_grades())
                self.setItemWidget(item, col_index, input_field)

            elif col_type in ['calculated', 'expandable_main', 'expandable_component']:
                label = self.create_grade_display()
                if saved_grades:
                    saved_key = f"{col_index}_{col_name}"
                    if saved_key in saved_grades:
                        label.setText(saved_grades[saved_key])
                self.setItemWidget(item, col_index, label)

        self.calculate_grades_for_student(item)

    def create_grade_input(self, value=""):
        input_field = QLineEdit()
        input_field.setText(value)
        input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_field.setPlaceholderText("e.g., 50/100")
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
        input_field.textChanged.connect(lambda: self.calculate_all_grades())
        return input_field

    def create_grade_display(self, value="0.00"):
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
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            self.calculate_grades_for_student(item)

    def calculate_grades_for_student(self, item):
        midterm_total = 0
        midterm_count = 0
        finalterm_total = 0
        finalterm_count = 0

        for col_index in range(self.columnCount()):
            col_info = self.column_info.get(col_index, {})
            widget = self.itemWidget(item, col_index)
            if col_info.get('type') == 'grade_input' and isinstance(widget, QLineEdit):
                try:
                    text = widget.text().strip()
                    if '/' in text:
                        parts = text.split('/', 1)
                        score = float(parts[0]) if parts[0] else 0
                        total = float(parts[1]) if parts[1] else 1
                        grade = score / total * 100
                    else:
                        grade = float(text) if text else 0
                    term = col_info.get('term', '')
                    if term == 'midterm':
                        midterm_total += grade
                        midterm_count += 1
                    elif term == 'finalterm':
                        finalterm_total += grade
                        finalterm_count += 1
                except ValueError:
                    continue

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
        info_label = QLabel("💡 Click column headers with < to expand/collapse")
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