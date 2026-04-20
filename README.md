# 🧹 Excel Data Cleaning Tool

A Python CLI tool to automatically clean and standardize messy Excel files.

## Features

| Feature | Description |
|---|---|
| 🗑️ Remove Duplicates | Detects and removes exact duplicate rows |
| 🔧 Fill Missing Values | Auto-fills numeric (median) and text (mode) columns |
| 📝 Standardize Columns | Lowercases, strips spaces, replaces special chars |
| ✂️ Trim Whitespace | Cleans leading/trailing spaces in text cells |
| 🔍 Fix Data Types | Converts numeric strings to proper numbers |
| 📊 Cleaning Report | Exports a summary sheet alongside cleaned data |

## Project Structure

```
excel-cleaner/
├── src/
│   └── cleaner.py          # Core ExcelCleaner class
├── tests/
│   └── test_cleaner.py     # Pytest test suite
├── sample_data/            # Messy test Excel files
├── output/                 # Cleaned output files
├── main.py                 # CLI entry point
├── generate_samples.py     # Script to create test data
└── requirements.txt
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/excel-cleaner.git
cd excel-cleaner
pip install -r requirements.txt
```

## Usage

### Basic
```bash
python main.py sample_data/customers_messy.xlsx
```

### With options
```bash
# Choose fill strategy
python main.py sample_data/sales_messy.xlsx --fill-strategy mean

# Specify output path
python main.py sample_data/employees_messy.xlsx --output output/employees_clean.xlsx

# Skip specific steps
python main.py data.xlsx --no-dedup --no-fill

# Specific sheet
python main.py data.xlsx --sheet "Sheet2"
```

### In Python
```python
from src.cleaner import ExcelCleaner

report = (
    ExcelCleaner("data.xlsx")
    .load()
    .standardize_columns()
    .trim_whitespace()
    .fix_data_types()
    .remove_duplicates()
    .fill_missing(strategy="auto")
    .export("output/clean.xlsx")
)
```

## Generate Test Data

```bash
python generate_samples.py
```

Creates three messy Excel files in `sample_data/`:
- `customers_messy.xlsx` — CRM-style data with nulls & duplicates
- `sales_messy.xlsx` — Sales records with missing prices & regions
- `employees_messy.xlsx` — HR data with mixed types

## Run Tests

```bash
pytest tests/ -v
```

## Where to Find Real Test Excel Files

| Source | URL | Notes |
|---|---|---|
| Kaggle Datasets | kaggle.com/datasets | Search "messy data" or "raw data" |
| UCI ML Repository | archive.ics.uci.edu | Classic datasets |
| data.gov | data.gov | US government open data |
| Our World in Data | ourworldindata.org | Download as CSV → open in Excel |
| StatLib | lib.stat.cmu.edu/datasets | Academic datasets |

## Output Format

The tool exports two sheets:
- **Cleaned Data** — The processed dataset
- **Cleaning Report** — Summary of all changes made

## License

MIT
