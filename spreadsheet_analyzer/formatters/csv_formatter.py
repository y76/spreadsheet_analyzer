"""
CSV formatter for spreadsheet analysis output.
"""

import csv
from .base import BaseFormatter
from .. import formatters


class CSVFormatter(BaseFormatter):
    """Formatter for CSV output."""
    
    def __init__(self):
        """Initialize the CSV formatter."""
        super().__init__()
        self.name = "CSV"
        self.extension = "csv"
    
    def save(self, data, output_file, sheet_name=None):
        """
        Save the data to a CSV file.
        
        Args:
            data (dict): The data to save.
            output_file (str): Path to the output file.
            sheet_name (str, optional): Name of the sheet.
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header row
            writer.writerow(["Column", "Value", "Count"])
            
            # Write data rows
            for column, values in data.items():
                for value_data in values:
                    writer.writerow([
                        column, 
                        value_data["value"], 
                        value_data["count"]
                    ])


# Register the formatter
formatters.register_formatter('csv', CSVFormatter)
