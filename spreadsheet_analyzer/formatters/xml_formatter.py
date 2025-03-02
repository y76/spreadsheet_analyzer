"""
XML formatter for spreadsheet analysis output.
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as md
from .base import BaseFormatter
from .. import formatters


class XMLFormatter(BaseFormatter):
    """Formatter for XML output."""
    
    def __init__(self):
        """Initialize the XML formatter."""
        super().__init__()
        self.name = "XML"
        self.extension = "xml"
    
    def save(self, data, output_file, sheet_name=None):
        """
        Save the data to an XML file.
        
        Args:
            data (dict): The data to save.
            output_file (str): Path to the output file.
            sheet_name (str, optional): Name of the sheet.
        """
        # Create root element
        root = ET.Element("spreadsheet")
        if sheet_name:
            root.set("sheet", sheet_name)
        
        # Add columns
        for column, values in data.items():
            column_elem = ET.SubElement(root, "column")
            column_elem.set("name", column)
            
            # Add values
            for value_data in values:
                value_elem = ET.SubElement(column_elem, "value")
                value_elem.set("text", value_data["value"])
                value_elem.set("count", str(value_data["count"]))
        
        # Convert to string with pretty formatting
        xml_string = ET.tostring(root, encoding='utf-8')
        xml_pretty = md.parseString(xml_string).toprettyxml(indent="  ")
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_pretty)


# Register the formatter
formatters.register_formatter('xml', XMLFormatter)
