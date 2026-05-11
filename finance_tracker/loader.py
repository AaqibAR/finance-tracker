"""
loader.py
---------
Reads transaction CSV files and returns a clean, categorized DataFrame.

Expected CSV columns: Date, Description, Amount, Type
"""

import pandas as pd
from pathlib import Path
from finance_tracker.categorizer import categorize


def load_transactions(filepath: str | Path) -> pd.DataFrame:
    """
    Load a CSV of transactions, parse dates, and auto-categorize.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(path)

    # Validate required columns
    required_cols = {"Date", "Description", "Amount", "Type"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    # Parse and sort by date
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # Auto-categorize transactions
    df["Category"] = df["Description"].apply(categorize)

    # Add month label for grouping
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    return df


def get_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """Return only expense rows (negative amounts)."""
    return df[df["Amount"] < 0].copy()


def get_income(df: pd.DataFrame) -> pd.DataFrame:
    """Return only income rows (positive amounts)."""
    return df[df["Amount"] > 0].copy()