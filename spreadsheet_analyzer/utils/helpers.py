"""
Utility functions for the spreadsheet analyzer.
"""

import os
import re


def sanitize_filename(filename):
    """
    Sanitize a filename to ensure it's valid.
    
    Args:
        filename (str): The original filename.
    
    Returns:
        str: A sanitized filename.
    """
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[^\w\-\.]', '_', filename)
    
    # Ensure it doesn't start with a dot
    if sanitized.startswith('.'):
        sanitized = '_' + sanitized
    
    return sanitized


def ensure_directory(directory):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (str): Path to the directory.
    
    Returns:
        str: The directory path.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_file_extension(file_path):
    """
    Get the extension of a file.
    
    Args:
        file_path (str): Path to the file.
    
    Returns:
        str: The file extension.
    """
    return os.path.splitext(file_path)[1].lower()[1:]


def is_spreadsheet_file(file_path):
    """
    Check if a file is a spreadsheet.
    
    Args:
        file_path (str): Path to the file.
    
    Returns:
        bool: True if the file is a spreadsheet, False otherwise.
    """
    valid_extensions = ['xlsx', 'xls', 'csv']
    return get_file_extension(file_path) in valid_extensions
