"""
Configuration settings for the spreadsheet analyzer.
"""

import os
from pathlib import Path

# Default output directory
DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), "spreadsheet_analysis")

# Default output formats
DEFAULT_FORMATS = ["json", "csv", "html"]

# Available formatters
AVAILABLE_FORMATS = {
    "json": "JSON format (machine-readable)",
    "csv": "CSV format (spreadsheet-compatible)",
    "xml": "XML format (structured data)",
    "txt": "Text format (simple view)",
    "html": "Interactive HTML (visual interface)"
}

# Google Sheets export URL format
GOOGLE_SHEETS_EXPORT_URL = "https://docs.google.com/spreadsheets/d/{}/export?format=xlsx"

# Get the package directory for template loading
PACKAGE_DIR = Path(__file__).parent
TEMPLATES_DIR = PACKAGE_DIR / "templates"
