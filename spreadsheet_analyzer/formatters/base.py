"""
Base formatter class for output generation.
"""

from abc import ABC, abstractmethod


class BaseFormatter(ABC):
    """
    Abstract base class for formatters.
    
    All formatters should inherit from this class and implement
    the required methods.
    """
    
    def __init__(self):
        """Initialize the formatter."""
        self.name = "Base"
        self.extension = "out"
    
    @abstractmethod
    def save(self, data, output_file, sheet_name=None):
        """
        Save the data to an output file.
        
        Args:
            data (dict): The data to save.
            output_file (str): Path to the output file.
            sheet_name (str, optional): Name of the sheet.
        
        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Formatter must implement save() method")
