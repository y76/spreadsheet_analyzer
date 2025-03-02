"""
Text formatter for spreadsheet analysis output.
"""

from .base import BaseFormatter
from .. import formatters


class TextFormatter(BaseFormatter):
    """Formatter for plain text output."""
    
    def __init__(self):
        """Initialize the text formatter."""
        super().__init__()
        self.name = "Text"
        self.extension = "txt"
    
    def save(self, data, output_file, sheet_name=None):
        """
        Save the data to a text file.
        
        Args:
            data (dict): The data to save.
            output_file (str): Path to the output file.
            sheet_name (str, optional): Name of the sheet.
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            # Add sheet name as header if provided
            if sheet_name:
                f.write(f"Sheet: {sheet_name}\n")
                f.write("=" * (len(sheet_name) + 7) + "\n\n")
            
            # Write each column's data
            for column, values in data.items():
                f.write(f"{column}:\n")
                
                # Format values with counts
                formatted_values = []
                for value_data in values:
                    if value_data["count"] > 1:
                        formatted_values.append(f"({value_data['count']}) {value_data['value']}")
                    else:
                        formatted_values.append(value_data["value"])
                
                # Write the formatted values
                f.write(f"  {', '.join(formatted_values)}\n\n")


# Register the formatter
formatters.register_formatter('txt', TextFormatter)
