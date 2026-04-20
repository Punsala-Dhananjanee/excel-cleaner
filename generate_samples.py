"""
Generates realistic messy Excel files for testing the cleaner.
Run: python generate_samples.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

rng = np.random.default_rng(42)
OUT = Path("sample_data")
OUT.mkdir(exist_ok=True)


def save(df, name):
    path = OUT / name
    df.to_excel(path, index=False)
    print(f"Generated: {path}")


# --- Sample 1: Customer Data (CRM export style) ---
n = 120
customers = pd.DataFrame({
    "  First Name  ": rng.choice(["Alice", "Bob", "Carol", "David", "Eve", None], n),
    "Last Name": rng.choice(["Smith", "Jones", "Lee", "Brown", np.nan], n),
    "Email Address": [f"user{i}@example.com" if rng.random() > 0.1 else None for i in range(n)],
    "Age": rng.integers(18, 70, n).astype(float),
    "Annual Salary": rng.integers(30000, 150000, n).astype(float),
    "Country": rng.choice(["USA", "UK", "Canada", "Australia", None, "USA", "UK"], n),
    "Customer Since": pd.date_range("2018-01-01", periods=n, freq="W"),
})
# Inject missing values
customers.loc[rng.choice(n, 15, replace=False), "Age"] = np.nan
customers.loc[rng.choice(n, 10, replace=False), "Annual Salary"] = np.nan
# Inject duplicates
customers = pd.concat([customers, customers.sample(10, random_state=1)], ignore_index=True)
save(customers, "customers_messy.xlsx")


# --- Sample 2: Sales Data ---
n = 200
sales = pd.DataFrame({
    "Order ID": [f"ORD-{i:04d}" for i in range(n)],
    "Product Name": rng.choice(["Widget A", "Widget B", "Gadget X", "  Gadget Y  ", None], n),
    "Quantity": rng.integers(1, 50, n).astype(float),
    "Unit Price": np.round(rng.uniform(5.0, 500.0, n), 2),
    "Discount %": rng.choice([0, 5, 10, 15, np.nan], n),
    "Region": rng.choice(["North", "South", "East", "West", None], n),
    "Sales Rep": rng.choice(["Tom", "Sara", "Mike", "Jen", np.nan], n),
})
sales.loc[rng.choice(n, 8, replace=False), "Quantity"] = np.nan
sales = pd.concat([sales, sales.sample(12, random_state=2)], ignore_index=True)
save(sales, "sales_messy.xlsx")


# --- Sample 3: Employee HR Data ---
n = 80
employees = pd.DataFrame({
    "EMP ID": [f"E{i:03d}" for i in range(n)],
    "Full Name": rng.choice(["John Doe", "Jane Smith", "Ali Hassan", "Maria Lopez", None], n),
    "Department": rng.choice(["Engineering", "Sales", "HR", "Finance", None], n),
    "Years of Experience": rng.integers(0, 30, n).astype(float),
    "Monthly Salary": np.round(rng.uniform(2000, 15000, n), 2),
    "Performance Score": rng.choice([1, 2, 3, 4, 5, np.nan], n),
    "Remote": rng.choice(["Yes", "No", None], n),
})
employees.loc[rng.choice(n, 6, replace=False), "Monthly Salary"] = np.nan
employees = pd.concat([employees, employees.sample(5, random_state=3)], ignore_index=True)
save(employees, "employees_messy.xlsx")

print("\nAll sample files created in ./sample_data/")
print("Use these with: python main.py sample_data/customers_messy.xlsx")
