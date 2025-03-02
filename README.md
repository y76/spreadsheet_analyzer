# Spreadsheet Analyzer

A powerful tool for analyzing spreadsheet data and generating reports in various formats.

## Features

- Download spreadsheets directly from Google Sheets
- Analyze columns and values across multiple sheets
- Generate reports in multiple formats:
  - Interactive HTML with clickable column navigation
  - JSON for machine-readable data
  - CSV for spreadsheet integration
  - XML for structured data exchange
  - Text for simple viewing

## Installation

```bash
# Install from source
git clone https://github.com/y76/spreadsheet-analyzer.git
cd spreadsheet-analyzer
pip install -e .

# Or directly from PyPI (when published)
pip install spreadsheet-analyzer
```

## Usage

### Command Line

```bash
# Basic usage
spreadsheet-analyzer --sheet-id YOUR_SHEET_ID

# Specify output formats
spreadsheet-analyzer --sheet-id YOUR_SHEET_ID --formats json,csv,html

# Download the spreadsheet
spreadsheet-analyzer --sheet-id YOUR_SHEET_ID --download

# Use a local file
spreadsheet-analyzer --file path/to/spreadsheet.xlsx

# Get help
spreadsheet-analyzer --help
```

### Python API

```python
from spreadsheet_analyzer import SpreadsheetAnalyzer

# Initialize the analyzer
analyzer = SpreadsheetAnalyzer()

# Download and analyze a Google Sheet
analyzer.download_and_analyze("YOUR_SHEET_ID", formats=["html", "json"])

# Or analyze a local file
analyzer.analyze_file("path/to/spreadsheet.xlsx", formats=["html", "json"])
```

## Output Examples

### Interactive HTML

The HTML output provides an interactive interface where you can:
- Click on column buttons to view detailed information
- Search for specific columns
- View value counts and percentages
- Sort data by frequency
![Screenshot_20250302_140603](https://github.com/user-attachments/assets/0e5fcebc-15dc-4444-89d6-00a44af64a68)

### JSON

JSON output is structured for easy integration with other applications:

```json
{
  "ColumnName": [
    {"value": "Value1", "count": 5},
    {"value": "Value2", "count": 3}
  ]
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
