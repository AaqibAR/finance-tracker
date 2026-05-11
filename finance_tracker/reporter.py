"""
reporter.py
-----------
Generates visual charts and saves them to the reports/ folder.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

COLORS = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52",
    "#8172B3", "#937860", "#DA8BC3", "#8C8C8C",
    "#CCB974", "#64B5CD",
]

plt.rcParams.update({
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor":   "#FAFAFA",
    "axes.grid":        True,
    "grid.alpha":       0.4,
    "font.family":      "sans-serif",
})


def plot_monthly_summary(summary_df: pd.DataFrame) -> None:
    """Bar chart comparing monthly income vs expenses with net savings line."""
    fig, ax = plt.subplots(figsize=(10, 5))
    months = summary_df["Month"]
    x = range(len(months))
    width = 0.35

    ax.bar([i - width / 2 for i in x], summary_df["Income"],   width, label="Income",   color="#55A868")
    ax.bar([i + width / 2 for i in x], summary_df["Expenses"], width, label="Expenses", color="#C44E52")
    ax.plot(x, summary_df["Net"], marker="o", color="#4C72B0", linewidth=2, label="Net Savings")

    ax.set_xticks(list(x))
    ax.set_xticklabels(months, rotation=30, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_title("Monthly Income vs Expenses", fontsize=14, fontweight="bold")
    ax.legend()
    fig.tight_layout()

    out = REPORTS_DIR / "monthly_summary.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  ✅  Saved: {out}")


def plot_category_pie(category_df: pd.DataFrame, month: str | None = None) -> None:
    """Pie chart of spending by category."""
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = category_df["Category"]
    sizes  = category_df["Total"]

    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        colors=COLORS[:len(labels)],
        startangle=140,
        pctdistance=0.82,
    )

    title = f"Spending by Category — {month}" if month else "Spending by Category (All Time)"
    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    fig.tight_layout()

    slug = f"_{month}" if month else ""
    out  = REPORTS_DIR / f"category_pie{slug}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  ✅  Saved: {out}")


def plot_spending_trend(trend_df: pd.DataFrame) -> None:
    """Line chart of daily spending over time."""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.fill_between(trend_df["Date"], trend_df["DailySpend"], alpha=0.25, color="#4C72B0")
    ax.plot(trend_df["Date"], trend_df["DailySpend"], color="#4C72B0", linewidth=1.5)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_title("Daily Spending Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount Spent ($)")
    fig.tight_layout()

    out = REPORTS_DIR / "spending_trend.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  ✅  Saved: {out}")


def print_summary_table(summary_df: pd.DataFrame) -> None:
    """Pretty-print the monthly summary to console."""
    print("\n" + "=" * 58)
    print(f"  {'Month':<12} {'Income':>9} {'Expenses':>10} {'Net':>9} {'Savings%':>9}")
    print("=" * 58)
    for _, row in summary_df.iterrows():
        net_str = f"${row['Net']:>8,.2f}"
        color   = "\033[92m" if row["Net"] >= 0 else "\033[91m"
        reset   = "\033[0m"
        print(
            f"  {row['Month']:<12} "
            f"${row['Income']:>8,.2f} "
            f"${row['Expenses']:>8,.2f} "
            f"{color}{net_str}{reset} "
            f"{row['Savings Rate (%)']:>7.1f}%"
        )
    print("=" * 58 + "\n")