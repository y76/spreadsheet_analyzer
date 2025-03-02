"""
Command-line interface for the spreadsheet analyzer.
"""

import os
import sys
import click
from .analyzer import SpreadsheetAnalyzer
from .config import DEFAULT_FORMATS, AVAILABLE_FORMATS


@click.command()
@click.option('--sheet-id', help='Google Sheet ID to analyze')
@click.option('--file', help='Local spreadsheet file to analyze')
@click.option('--output-dir', default='output', help='Directory to save output files (default: "output")')
@click.option('--formats', default=','.join(DEFAULT_FORMATS),
              help='Comma-separated list of output formats')
@click.option('--download', is_flag=True, help='Force download even if file exists')
@click.option('--list-formats', is_flag=True, help='List available output formats')
def main(sheet_id, file, output_dir, formats, download, list_formats):
    """Analyze spreadsheets and generate reports in various formats."""

    # Show available formats and exit
    if list_formats:
        click.echo("Available output formats:")
        for fmt, description in AVAILABLE_FORMATS.items():
            click.echo(f"  {fmt:5} - {description}")
        return

    # Parse formats
    format_list = [f.strip() for f in formats.split(',')]

    # Validate formats
    invalid_formats = [f for f in format_list if f not in AVAILABLE_FORMATS]
    if invalid_formats:
        click.echo(f"Error: Invalid format(s): {', '.join(invalid_formats)}")
        click.echo("Use --list-formats to see available formats")
        return

    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        click.echo(f"Output files will be saved to: {os.path.abspath(output_dir)}")

    # Create analyzer
    analyzer = SpreadsheetAnalyzer(output_dir)

    try:
        # Check if we have a sheet ID or file
        if sheet_id:
            # Get file path for potential existing file
            file_path = os.path.join(analyzer.output_dir, 'complete_spreadsheet.xlsx')

            # Check if download is needed
            if download or not os.path.exists(file_path):
                click.echo(f"Downloading spreadsheet with ID: {sheet_id}")
                analyzer.download_and_analyze(sheet_id, format_list)
            else:
                click.echo(f"Using existing spreadsheet (use --download to force refresh)")
                analyzer.analyze_file(file_path, format_list)

        elif file:
            # Analyze local file
            click.echo(f"Analyzing local file: {file}")
            analyzer.analyze_file(file, format_list)

        else:
            # No input source
            click.echo("Error: Please provide either --sheet-id or --file")
            click.echo("Use --help for more information")

    except Exception as e:
        click.echo(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
