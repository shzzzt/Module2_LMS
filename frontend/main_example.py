# main.py
import sys
from PyQt6.QtWidgets import QApplication
from .controller.section_controller import SectionController

def main():
    app = QApplication(sys.argv)
    controller = SectionController()
    controller.view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
