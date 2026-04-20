import pandas as pd
import numpy as np
from pathlib import Path


class ExcelCleaner:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.original_df = None
        self.cleaned_df = None
        self.report = {}

    def load(self, sheet_name=0):
        self.original_df = pd.read_excel(self.filepath, sheet_name=sheet_name)
        self.cleaned_df = self.original_df.copy()
        print(f"Loaded: {self.filepath.name} | Rows: {len(self.cleaned_df)} | Cols: {len(self.cleaned_df.columns)}")
        return self

    def remove_duplicates(self):
        before = len(self.cleaned_df)
        self.cleaned_df = self.cleaned_df.drop_duplicates()
        removed = before - len(self.cleaned_df)
        self.report["duplicates_removed"] = removed
        print(f"Duplicates removed: {removed}")
        return self

    def fill_missing(self, strategy="auto"):
        missing_before = self.cleaned_df.isnull().sum().sum()
        for col in self.cleaned_df.columns:
            if self.cleaned_df[col].isnull().any():
                if strategy == "auto":
                    if pd.api.types.is_numeric_dtype(self.cleaned_df[col]):
                        self.cleaned_df[col] = self.cleaned_df[col].fillna(self.cleaned_df[col].median())
                    else:
                        mode = self.cleaned_df[col].mode()
                        self.cleaned_df[col] = self.cleaned_df[col].fillna(mode[0] if not mode.empty else "Unknown")
                elif strategy == "mean":
                    if pd.api.types.is_numeric_dtype(self.cleaned_df[col]):
                        self.cleaned_df[col] = self.cleaned_df[col].fillna(self.cleaned_df[col].mean())
                elif strategy == "drop":
                    self.cleaned_df = self.cleaned_df.dropna()
                    break
        missing_after = self.cleaned_df.isnull().sum().sum()
        self.report["missing_filled"] = int(missing_before - missing_after)
        print(f"Missing values filled: {self.report['missing_filled']}")
        return self

    def standardize_columns(self):
        original_cols = list(self.cleaned_df.columns)
        self.cleaned_df.columns = (
            self.cleaned_df.columns
            .str.strip()
            .str.lower()
            .str.replace(r"[^\w]", "_", regex=True)
            .str.replace(r"_+", "_", regex=True)
            .str.strip("_")
        )
        renamed = {o: n for o, n in zip(original_cols, self.cleaned_df.columns) if o != n}
        self.report["columns_renamed"] = renamed
        print(f"Columns standardized: {len(renamed)} renamed")
        return self

    def trim_whitespace(self):
        for col in self.cleaned_df.select_dtypes(include="object").columns:
            self.cleaned_df[col] = self.cleaned_df[col].str.strip()
        print("Whitespace trimmed from text columns")
        return self

    def fix_data_types(self):
        for col in self.cleaned_df.columns:
            if self.cleaned_df[col].dtype == object:
                converted = pd.to_numeric(self.cleaned_df[col], errors="ignore")
                if converted.dtype != object:
                    self.cleaned_df[col] = converted
        print("Data types inferred and fixed")
        return self

    def export(self, output_path: str = None):
        if output_path is None:
            stem = self.filepath.stem
            output_path = self.filepath.parent.parent / "output" / f"{stem}_cleaned.xlsx"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            self.cleaned_df.to_excel(writer, index=False, sheet_name="Cleaned Data")
            self._write_report_sheet(writer)

        print(f"Exported: {output_path}")
        return output_path

    def _write_report_sheet(self, writer):
        rows_removed = len(self.original_df) - len(self.cleaned_df)
        summary = {
            "Metric": [
                "Original Rows",
                "Final Rows",
                "Rows Removed",
                "Duplicates Removed",
                "Missing Values Filled",
                "Columns Renamed",
            ],
            "Value": [
                len(self.original_df),
                len(self.cleaned_df),
                rows_removed,
                self.report.get("duplicates_removed", 0),
                self.report.get("missing_filled", 0),
                len(self.report.get("columns_renamed", {})),
            ],
        }
        pd.DataFrame(summary).to_excel(writer, index=False, sheet_name="Cleaning Report")

    def summary(self):
        print("\n===== CLEANING SUMMARY =====")
        print(f"  Original rows : {len(self.original_df)}")
        print(f"  Final rows    : {len(self.cleaned_df)}")
        print(f"  Duplicates    : {self.report.get('duplicates_removed', 0)}")
        print(f"  Missing filled: {self.report.get('missing_filled', 0)}")
        print(f"  Cols renamed  : {len(self.report.get('columns_renamed', {}))}")
        print("============================\n")
        return self.report
