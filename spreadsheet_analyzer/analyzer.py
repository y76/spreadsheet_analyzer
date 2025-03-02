"""
Core module for analyzing spreadsheet data.
"""

import os
import pandas as pd
from collections import Counter
import importlib

from .downloader import SpreadsheetDownloader
from .config import DEFAULT_FORMATS
from .formatters import get_formatter


class SpreadsheetAnalyzer:
    """Main class for analyzing spreadsheets and generating reports."""
    
    def __init__(self, output_dir=None):
        """
        Initialize the spreadsheet analyzer.
        
        Args:
            output_dir (str, optional): Directory to save output files.
                                       Defaults to current directory.
        """
        self.output_dir = output_dir or os.getcwd()
        self.downloader = SpreadsheetDownloader(output_dir)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def download_and_analyze(self, sheet_id, formats=None, output_file=None):
        """
        Download a Google Sheet and analyze its contents.
        
        Args:
            sheet_id (str): The ID of the Google Sheet.
            formats (list, optional): List of output formats. 
                                     Defaults to DEFAULT_FORMATS.
            output_file (str, optional): Path to save the downloaded file.
        
        Returns:
            dict: Analysis results for all sheets.
        """
        # Download the spreadsheet
        excel_file = self.downloader.download(sheet_id, output_file)
        
        # Analyze the downloaded file
        return self.analyze_excel_file(excel_file, formats)
    
    def analyze_file(self, file_path, formats=None):
        """
        Analyze an existing spreadsheet file.
        
        Args:
            file_path (str): Path to the spreadsheet file.
            formats (list, optional): List of output formats.
                                     Defaults to DEFAULT_FORMATS.
        
        Returns:
            dict: Analysis results for all sheets.
        
        Raises:
            FileNotFoundError: If the file doesn't exist.
        """
        try:
            excel_file = pd.ExcelFile(file_path)
            print(f"Analyzing existing spreadsheet: {file_path}")
            print(f"Available sheets: {excel_file.sheet_names}")
            
            return self.analyze_excel_file(excel_file, formats)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Spreadsheet file not found: {file_path}")
    
    def analyze_excel_file(self, excel_file, formats=None):
        """
        Analyze an Excel file and generate reports.
        
        Args:
            excel_file (pandas.ExcelFile): The Excel file to analyze.
            formats (list, optional): List of output formats.
                                     Defaults to DEFAULT_FORMATS.
        
        Returns:
            dict: Analysis results for all sheets.
        """
        # Use default formats if none provided
        formats = formats or DEFAULT_FORMATS
        
        results = {}
        
        # Process each sheet
        for sheet_name in excel_file.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            
            try:
                # Read the sheet into a DataFrame
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                
                # Analyze the sheet
                sheet_results = self._analyze_dataframe(df)
                results[sheet_name] = sheet_results
                
                # Generate output files
                self._generate_outputs(sheet_results, sheet_name, formats)
                
            except Exception as e:
                print(f"Error processing sheet '{sheet_name}': {e}")
        
        print("All sheets have been processed successfully!")
        return results
    
    def _analyze_dataframe(self, df):
        """
        Analyze a DataFrame to extract column data.
        
        Args:
            df (pandas.DataFrame): The DataFrame to analyze.
        
        Returns:
            dict: Analysis results with column data.
        """
        column_data = {}
        
        for column in df.columns:
            # Filter out NaN values and convert all values to strings
            values = [str(val) for val in df[column].dropna()]
            
            # Count occurrences of each value
            value_counts = Counter(values)
            
            # Store as a list of dictionaries for flexibility
            column_data[column] = [{"value": val, "count": count} 
                                  for val, count in value_counts.items()]
        
        return column_data
    
    def _generate_outputs(self, column_data, sheet_name, formats):
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Clean up sheet name for filename (replace problematic characters)
        safe_sheet_name = sheet_name.replace('/', '_').replace('\\', '_')

        """
        Generate output files in the specified formats.
        
        Args:
            column_data (dict): The analyzed column data.
            sheet_name (str): Name of the sheet.
            formats (list): List of output formats.
        """
        for format_name in formats:
            try:
                # Get the formatter for this format
                formatter = get_formatter(format_name)
                if formatter:
                    output_file = os.path.join(self.output_dir, f"{safe_sheet_name}.{formatter.extension}")
                    formatter.save(column_data, output_file, sheet_name)
                    print(f"{formatter.name} data for sheet '{sheet_name}' saved to {output_file}")
                else:
                    print(f"Unknown output format: {format_name}")
            except Exception as e:
                print(f"Error generating {format_name} output for sheet '{sheet_name}': {e}")
