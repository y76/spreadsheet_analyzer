from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spreadsheet-analyzer",
    version="0.1.0",
    author="",
    author_email="",
    description="A tool for analyzing spreadsheets and generating reports in various formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "spreadsheet_analyzer": ["templates/*.html"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "requests",
        "openpyxl",
        "jinja2",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "spreadsheet-analyzer=spreadsheet_analyzer.cli:main",
        ],
    },
)