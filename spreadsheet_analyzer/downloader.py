"""
Module for downloading spreadsheets from Google Sheets.
"""

import os
import requests
import pandas as pd
from io import BytesIO

from .config import GOOGLE_SHEETS_EXPORT_URL

class SpreadsheetDownloader:
    """Class for downloading spreadsheets from Google Sheets."""

    def __init__(self, output_dir=None):
        """
        Initialize the downloader.
        
        Args:
            output_dir (str, optional): Directory to save downloaded files. 
                                       Defaults to current directory.
        """
        self.output_dir = output_dir or os.getcwd()
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def download(self, sheet_id, output_file=None):
        """
        Download a Google Sheet as an Excel file.
        
        Args:
            sheet_id (str): The ID of the Google Sheet.
            output_file (str, optional): Path to save the downloaded file.
                                         Defaults to 'complete_spreadsheet.xlsx'.
        
        Returns:
            pandas.ExcelFile: The downloaded Excel file.
        
        Raises:
            ValueError: If download fails.
        """
        if not output_file:
            output_file = os.path.join(self.output_dir, 'complete_spreadsheet.xlsx')
        
        url = GOOGLE_SHEETS_EXPORT_URL.format(sheet_id)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Save the file
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            # Return as ExcelFile object
            excel_file = pd.ExcelFile(BytesIO(response.content))
            print(f"Spreadsheet successfully downloaded as '{output_file}'")
            print(f"Available sheets: {excel_file.sheet_names}")
            
            return excel_file
        
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to download spreadsheet: {e}")
