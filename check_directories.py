 
import os

# Required directories
directories = [
    "spreadsheet_analyzer",
    "spreadsheet_analyzer/formatters",
    "spreadsheet_analyzer/utils",
    "spreadsheet_analyzer/templates",
    "tests"
]

# Required files (with empty content if they don't exist)
init_files = [
    "spreadsheet_analyzer/__init__.py",
    "spreadsheet_analyzer/formatters/__init__.py",
    "spreadsheet_analyzer/utils/__init__.py",
    "tests/__init__.py"
]

print("Checking and creating directories and init files...")

# Create directories
for directory in directories:
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)
    else:
        print(f"Directory exists: {directory}")

# Create __init__.py files
for init_file in init_files:
    if not os.path.exists(init_file):
        print(f"Creating file: {init_file}")
        with open(init_file, 'w') as f:
            f.write('"""Package initialization."""\n')
    else:
        print(f"File exists: {init_file}")

print("Done!")
