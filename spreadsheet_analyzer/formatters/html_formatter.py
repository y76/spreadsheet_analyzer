"""
HTML formatter for spreadsheet analysis output.
"""

from .base import BaseFormatter
from .. import formatters


class HTMLFormatter(BaseFormatter):
    """Formatter for HTML output."""

    def __init__(self):
        """Initialize the HTML formatter."""
        super().__init__()
        self.name = "HTML"
        self.extension = "html"

    def save(self, data, output_file, sheet_name=None):
        """
        Save the data to an HTML file.

        Args:
            data (dict): The data to save.
            output_file (str): Path to the output file.
            sheet_name (str, optional): Name of the sheet.
        """
        # Process the data
        processed_data = self._process_data(data)

        # Generate HTML
        html = self._generate_html(sheet_name or "Unnamed Sheet", processed_data, list(data.keys()))

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

    def _process_data(self, data):
        """
        Process the data for HTML generation.

        Args:
            data (dict): The raw data.

        Returns:
            dict: Processed data.
        """
        processed = {}

        for column, values in data.items():
            # Calculate total count for percentages
            total_count = sum(item["count"] for item in values)

            # Add percentage to each value
            processed_values = []
            for value_data in values:
                percentage = (value_data["count"] / total_count) * 100 if total_count > 0 else 0
                processed_values.append({
                    "value": value_data["value"],
                    "count": value_data["count"],
                    "percentage": round(percentage, 2)
                })

            # Sort by count (descending)
            processed_values.sort(key=lambda x: x["count"], reverse=True)

            processed[column] = {
                "values": processed_values,
                "total_count": total_count,
                "unique_count": len(values)
            }

        return processed

    def _generate_html(self, sheet_name, data, column_names):
        """
        Generate HTML content.

        Args:
            sheet_name (str): Name of the sheet.
            data (dict): Processed data.
            column_names (list): List of column names.

        Returns:
            str: HTML content.
        """
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Sheet: {sheet_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .columns-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .column-button {{
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 0.3s;
        }}
        .column-button:hover {{
            background-color: #45a049;
        }}
        .column-button.active {{
            background-color: #007bff;
        }}
        .column-data {{
            display: none;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }}
        .column-data.active {{
            display: block;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            position: sticky;
            top: 0;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f1f1f1;
        }}
        .count {{
            font-weight: bold;
            color: #555;
            text-align: center;
        }}
        .search-container {{
            margin-bottom: 20px;
        }}
        #search-input {{
            padding: 10px;
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }}
        .summary {{
            margin-bottom: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        .summary p {{
            margin: 5px 0;
        }}
        .percentage-bar {{
            height: 20px;
            background-color: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 5px;
        }}
        .percentage-bar-fill {{
            height: 100%;
            background-color: #4CAF50;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Sheet: {sheet_name}</h1>

        <div class="summary">
            <h2>Summary</h2>
            <p>Total columns: <strong>{len(column_names)}</strong></p>
            <p>Columns: {", ".join(column_names)}</p>
        </div>

        <div class="search-container">
            <input type="text" id="search-input" placeholder="Search for columns...">
        </div>

        <div class="columns-container">
"""

        # Add buttons for each column
        for column in column_names:
            html += f'            <button class="column-button" data-column="{column}">{column}</button>\n'

        html += """        </div>

"""

        # Add data sections for each column
        for column, column_data in data.items():
            html += f"""        <div id="column-{column}" class="column-data">
            <h2>{column}</h2>
            <p>Unique values: <strong>{column_data["unique_count"]}</strong></p>
            <table>
                <tr>
                    <th>Value</th>
                    <th>Count</th>
                    <th>Percentage</th>
                </tr>
"""

            for value in column_data["values"]:
                html += f"""                <tr>
                    <td>{value["value"]}</td>
                    <td class="count">{value["count"]}</td>
                    <td>
                        {value["percentage"]}%
                        <div class="percentage-bar">
                            <div class="percentage-bar-fill" style="width: {value["percentage"]}%;"></div>
                        </div>
                    </td>
                </tr>
"""

            html += """            </table>
        </div>
"""

        html += """    </div>

    <script>
        // Function to show a specific column's data
        function showColumnData(columnName) {
            // Hide all column data sections
            document.querySelectorAll('.column-data').forEach(el => {
                el.classList.remove('active');
            });

            // Remove active class from all buttons
            document.querySelectorAll('.column-button').forEach(el => {
                el.classList.remove('active');
            });

            // Show the selected column's data
            const dataEl = document.getElementById('column-' + columnName);
            if (dataEl) {
                dataEl.classList.add('active');

                // Add active class to the button
                document.querySelector(`.column-button[data-column="${columnName}"]`).classList.add('active');
            }
        }

        // Add click handlers to all column buttons
        document.querySelectorAll('.column-button').forEach(button => {
            button.addEventListener('click', function() {
                const columnName = this.getAttribute('data-column');
                showColumnData(columnName);
            });
        });

        // Search functionality
        document.getElementById('search-input').addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();

            document.querySelectorAll('.column-button').forEach(button => {
                const columnName = button.getAttribute('data-column').toLowerCase();

                if (columnName.includes(searchTerm)) {
                    button.style.display = 'inline-block';
                } else {
                    button.style.display = 'none';
                }
            });
        });

        // Show the first column's data by default
        const firstColumn = document.querySelector('.column-button');
        if (firstColumn) {
            firstColumn.click();
        }
    </script>
</body>
</html>"""

        return html


# Register the formatter
formatters.register_formatter('html', HTMLFormatter)
