import argparse
from src.cleaner import ExcelCleaner


def main():
    parser = argparse.ArgumentParser(description="Excel Data Cleaning Tool")
    parser.add_argument("file", help="Path to Excel file (.xlsx)")
    parser.add_argument("--sheet", default=0, help="Sheet name or index (default: 0)")
    parser.add_argument("--fill-strategy", choices=["auto", "mean", "drop"], default="auto")
    parser.add_argument("--output", default=None, help="Output file path")
    parser.add_argument("--no-dedup", action="store_true", help="Skip duplicate removal")
    parser.add_argument("--no-fill", action="store_true", help="Skip missing value fill")
    parser.add_argument("--no-standardize", action="store_true", help="Skip column standardization")

    args = parser.parse_args()

    cleaner = ExcelCleaner(args.file).load(sheet_name=args.sheet)

    if not args.no_standardize:
        cleaner.standardize_columns()

    cleaner.trim_whitespace().fix_data_types()

    if not args.no_dedup:
        cleaner.remove_duplicates()

    if not args.no_fill:
        cleaner.fill_missing(strategy=args.fill_strategy)

    cleaner.export(args.output)
    cleaner.summary()


if __name__ == "__main__":
    main()
