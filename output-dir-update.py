import os

# First, let's modify the analyzer.py file to ensure output directory is used consistently
def update_analyzer_py():
    file_path = "spreadsheet_analyzer/analyzer.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the _generate_outputs method
    method_start = content.find("def _generate_outputs(self, column_data, sheet_name, formats):")
    if method_start == -1:
        print("Could not find _generate_outputs method in analyzer.py")
        return

    # Find the body of the method
    body_start = content.find(":", method_start) + 1

    # Insert the directory creation code after the method definition
    output_dir_code = """
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Clean up sheet name for filename (replace problematic characters)
        safe_sheet_name = sheet_name.replace('/', '_').replace('\\\\', '_')
"""

    # Construct the modified content
    modified_content = content[:body_start] + output_dir_code + content[body_start:]

    # Replace output_file path construction
    modified_content = modified_content.replace(
        "output_file = os.path.join(self.output_dir, f\"{sheet_name}.{formatter.extension}\")",
        "output_file = os.path.join(self.output_dir, f\"{safe_sheet_name}.{formatter.extension}\")"
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)

    print(f"Updated {file_path}")

# Next, let's update the CLI to make the output directory more prominent
def update_cli_py():
    file_path = "spreadsheet_analyzer/cli.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Make the output-dir option more prominent and add a default value
    modified_content = content.replace(
        "@click.option('--output-dir', default=None, help='Directory to save output files')",
        "@click.option('--output-dir', default='output', help='Directory to save output files (default: \"output\")')"
    )

    # Find the line where analyzer is created
    analyzer_line = content.find("analyzer = SpreadsheetAnalyzer(output_dir)")
    if analyzer_line == -1:
        print("Could not find SpreadsheetAnalyzer initialization in cli.py")
        return

    # Insert output directory message before analyzer initialization
    output_dir_message = """    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        click.echo(f"Output files will be saved to: {os.path.abspath(output_dir)}")

    """

    # Construct the modified content
    line_start = content.rfind("\n", 0, analyzer_line) + 1
    modified_content = content[:line_start] + output_dir_message + content[line_start:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)

    print(f"Updated {file_path}")

# Execute the updates
try:
    update_analyzer_py()
    update_cli_py()

    print("\nFiles updated successfully. Now the program will save all output files to the specified output directory.")
    print("You can specify the output directory using the --output-dir parameter:")
    print("spreadsheet-analyzer --sheet-id 1HxbYPplFDEn61vhx8N6P6zHU2Cp4aXEV --output-dir my_analysis")
    print("\nBy default, files will be saved to the 'output' directory in the current working directory.")
except Exception as e:
    print(f"Error updating files: {e}")
