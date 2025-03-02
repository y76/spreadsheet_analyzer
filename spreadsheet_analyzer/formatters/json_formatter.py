"""
JSON formatter for spreadsheet analysis output.
"""

import json
from .base import BaseFormatter
from .. import formatters


class JSONFormatter(BaseFormatter):
    """Formatter for JSON output."""
    
    def __init__(self):
        """Initialize the JSON formatter."""
        super().__init__()
        self.name = "JSON"
        self.extension = "json"
    
    def save(self, data, output_file, sheet_name=None):
        """
        Save the data to a JSON file.
        
        Args:
            data (dict): The data to save.
            output_file (str): Path to the output file.
            sheet_name (str, optional): Name of the sheet.
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# Register the formatter
formatters.register_formatter('json', JSONFormatter)
