"""
analytics.py
------------
Computes summaries, breakdowns, and insights from transaction data.
"""

import pandas as pd


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a month-by-month summary of income, expenses and net savings.
    """
    income = (
        df[df["Amount"] > 0]
        .groupby("Month")["Amount"]
        .sum()
        .rename("Income")
    )
    expenses = (
        df[df["Amount"] < 0]
        .groupby("Month")["Amount"]
        .sum()
        .abs()
        .rename("Expenses")
    )
    summary = pd.concat([income, expenses], axis=1).fillna(0)
    summary["Net"] = summary["Income"] - summary["Expenses"]
    summary["Savings Rate (%)"] = (
        (summary["Net"] / summary["Income"].replace(0, float("nan"))) * 100
    ).round(1)
    return summary.reset_index()


def category_breakdown(df: pd.DataFrame, month: str | None = None) -> pd.DataFrame:
    """
    Return spending by category, optionally filtered to one month.
    """
    data = df[df["Amount"] < 0].copy()
    if month:
        data = data[data["Month"] == month]

    grouped = (
        data.groupby("Category")["Amount"]
        .agg(Total="sum", Count="count")
        .reset_index()
    )
    grouped["Total"] = grouped["Total"].abs()
    total = grouped["Total"].sum()
    grouped["% of Expenses"] = (grouped["Total"] / total * 100).round(1)
    return grouped.sort_values("Total", ascending=False).reset_index(drop=True)


def top_expenses(df: pd.DataFrame, n: int = 5, month: str | None = None) -> pd.DataFrame:
    """
    Return the top N largest individual expense transactions.
    """
    data = df[df["Amount"] < 0].copy()
    if month:
        data = data[data["Month"] == month]
    data["Amount"] = data["Amount"].abs()
    return data.nlargest(n, "Amount")[["Date", "Description", "Category", "Amount"]].reset_index(drop=True)


def spending_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return daily spending totals for trend visualization.
    """
    daily = (
        df[df["Amount"] < 0]
        .groupby("Date")["Amount"]
        .sum()
        .abs()
        .reset_index()
        .rename(columns={"Amount": "DailySpend"})
    )
    return daily