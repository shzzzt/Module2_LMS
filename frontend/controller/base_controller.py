"""
Base Controller
Abstract base class for all controllers to ensure consistent structure
"""
from abc import ABC, abstractmethod
from PyQt6.QtCore import QObject, pyqtSignal


class BaseController(QObject, ABC):
    """
    Abstract base controller class that all specific controllers should inherit from.
    Provides common functionality and enforces consistent structure.
    """
    
    # Common signals that all controllers might need
    data_updated = pyqtSignal(object)  # Generic data update signal
    error_occurred = pyqtSignal(str)   # Error notification signal
    operation_completed = pyqtSignal(bool, str)  # Operation result signal (success, message)
    
    def __init__(self):
        super().__init__()
        self._initialize_services()
        
    @abstractmethod
    def _initialize_services(self):
        """
        Initialize required services for this controller.
        Must be implemented by each specific controller.
        """
        pass
    
    def handle_error(self, error_message: str, exception: Exception = None):
        """
        Common error handling method for all controllers
        """
        print(f"Controller Error: {error_message}")
        if exception:
            print(f"Exception details: {str(exception)}")
        
        self.error_occurred.emit(error_message)
    
    def emit_operation_result(self, success: bool, message: str = ""):
        """
        Emit operation completion signal with result
        """
        self.operation_completed.emit(success, message)
    
    def validate_required_data(self, data: dict, required_fields: list) -> bool:
        """
        Validate that required fields are present in data dictionary
        """
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            self.handle_error(error_msg)
            return False
        
        return True