"""
tests/test_finance_tracker.py
-----------------------------
Unit tests for core modules.
Run with: pytest tests/
"""

import pytest
import pandas as pd
from pathlib import Path

from finance_tracker.categorizer import categorize, get_all_categories
from finance_tracker.loader import load_transactions, get_expenses, get_income
from finance_tracker.analytics import monthly_summary, category_breakdown, top_expenses

SAMPLE_CSV = Path(__file__).parent.parent / "data" / "transactions.csv"


# ── Categorizer ───────────────────────────────────────────────────────────────

class TestCategorizer:
    def test_known_keywords(self):
        assert categorize("Supermarket Groceries") == "Groceries"
        assert categorize("Netflix Subscription")  == "Entertainment"
        assert categorize("Uber Ride")             == "Transport"
        assert categorize("Salary Deposit")        == "Income"

    def test_case_insensitive(self):
        assert categorize("SUPERMARKET") == "Groceries"
        assert categorize("netflix")     == "Entertainment"

    def test_unknown_returns_uncategorized(self):
        assert categorize("Random Unknown Merchant XYZ") == "Uncategorized"

    def test_get_all_categories_returns_list(self):
        cats = get_all_categories()
        assert isinstance(cats, list)
        assert "Groceries" in cats
        assert "Uncategorized" in cats


# ── Loader ────────────────────────────────────────────────────────────────────

class TestLoader:
    @pytest.fixture
    def df(self):
        return load_transactions(SAMPLE_CSV)

    def test_loads_without_error(self, df):
        assert len(df) > 0

    def test_has_required_columns(self, df):
        for col in ["Date", "Description", "Amount", "Type", "Category", "Month"]:
            assert col in df.columns

    def test_dates_are_sorted(self, df):
        assert df["Date"].is_monotonic_increasing

    def test_category_column_populated(self, df):
        assert df["Category"].notna().all()

    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            load_transactions("nonexistent_file.csv")

    def test_get_expenses_all_negative(self, df):
        expenses = get_expenses(df)
        assert (expenses["Amount"] < 0).all()

    def test_get_income_all_positive(self, df):
        income = get_income(df)
        assert (income["Amount"] > 0).all()


# ── Analytics ─────────────────────────────────────────────────────────────────

class TestAnalytics:
    @pytest.fixture
    def df(self):
        return load_transactions(SAMPLE_CSV)

    def test_monthly_summary_has_correct_columns(self, df):
        summary = monthly_summary(df)
        for col in ["Month", "Income", "Expenses", "Net", "Savings Rate (%)"]:
            assert col in summary.columns

    def test_monthly_summary_net_is_income_minus_expenses(self, df):
        summary = monthly_summary(df)
        for _, row in summary.iterrows():
            assert abs(row["Net"] - (row["Income"] - row["Expenses"])) < 0.01

    def test_category_breakdown_sorted_by_total(self, df):
        cats = category_breakdown(df)
        assert cats["Total"].is_monotonic_decreasing

    def test_top_expenses_count(self, df):
        tops = top_expenses(df, n=3)
        assert len(tops) == 3

    def test_top_expenses_are_largest(self, df):
        tops = top_expenses(df, n=5)
        assert tops["Amount"].is_monotonic_decreasing