"""
Package for output formatters.
"""

from .base import BaseFormatter

# Map of format names to formatter classes
_formatters = {}

def register_formatter(format_name, formatter_class):
    """
    Register a formatter class for a specific format.
    
    Args:
        format_name (str): The name of the format.
        formatter_class (BaseFormatter): The formatter class.
    """
    _formatters[format_name] = formatter_class


def get_formatter(format_name):
    """
    Get a formatter instance for a specific format.
    
    Args:
        format_name (str): The name of the format.
    
    Returns:
        BaseFormatter: An instance of the formatter.
    """
    formatter_class = _formatters.get(format_name)
    if formatter_class:
        return formatter_class()
    return None


# Import formatters to register them
try:
    from .json_formatter import JSONFormatter
    from .csv_formatter import CSVFormatter
    from .xml_formatter import XMLFormatter
    from .text_formatter import TextFormatter
    from .html_formatter import HTMLFormatter
except ImportError as e:
    print(f"Warning: Not all formatters could be imported: {e}")
