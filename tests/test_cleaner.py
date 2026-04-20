import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.cleaner import ExcelCleaner

FIXTURE = Path("tests/fixtures")
FIXTURE.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def messy_excel(tmp_path):
    df = pd.DataFrame({
        "  First Name  ": ["Alice", "Bob", "Alice", None, "Carol"],
        "Last Name": ["Smith", "Jones", "Smith", "Lee", None],
        "Age": [25, np.nan, 25, 30, 40],
        "Salary $": [50000, 60000, 50000, np.nan, 80000],
    })
    path = tmp_path / "test_messy.xlsx"
    df.to_excel(path, index=False)
    return path


def test_load(messy_excel):
    c = ExcelCleaner(messy_excel).load()
    assert c.original_df is not None
    assert len(c.cleaned_df) == 5


def test_remove_duplicates(messy_excel):
    c = ExcelCleaner(messy_excel).load().remove_duplicates()
    assert len(c.cleaned_df) < 5
    assert c.report["duplicates_removed"] == 1


def test_standardize_columns(messy_excel):
    c = ExcelCleaner(messy_excel).load().standardize_columns()
    for col in c.cleaned_df.columns:
        assert col == col.strip()
        assert col == col.lower()
        assert " " not in col


def test_fill_missing_auto(messy_excel):
    c = ExcelCleaner(messy_excel).load().fill_missing(strategy="auto")
    assert c.cleaned_df.isnull().sum().sum() == 0
    assert c.report["missing_filled"] > 0


def test_fill_missing_drop(messy_excel):
    c = ExcelCleaner(messy_excel).load().fill_missing(strategy="drop")
    assert c.cleaned_df.isnull().sum().sum() == 0


def test_export_creates_file(messy_excel, tmp_path):
    output = tmp_path / "cleaned.xlsx"
    ExcelCleaner(messy_excel).load().remove_duplicates().fill_missing().export(str(output))
    assert output.exists()
    df = pd.read_excel(output)
    assert len(df) > 0


def test_export_has_report_sheet(messy_excel, tmp_path):
    output = tmp_path / "cleaned.xlsx"
    ExcelCleaner(messy_excel).load().remove_duplicates().fill_missing().export(str(output))
    sheets = pd.ExcelFile(output).sheet_names
    assert "Cleaning Report" in sheets


def test_full_pipeline(messy_excel, tmp_path):
    output = tmp_path / "full_cleaned.xlsx"
    report = (
        ExcelCleaner(messy_excel)
        .load()
        .standardize_columns()
        .trim_whitespace()
        .fix_data_types()
        .remove_duplicates()
        .fill_missing()
        .export(str(output))
    )
    assert output.exists()
