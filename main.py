"""
main.py
-------
CLI entry point for Personal Finance Tracker.

Usage:
    python3 main.py --file data/transactions.csv
    python3 main.py --file data/transactions.csv --month 2024-01
    python3 main.py --file data/transactions.csv --top 10
    python3 main.py --file data/transactions.csv --no-charts
"""

import argparse
import sys

from finance_tracker.loader import load_transactions
from finance_tracker.analytics import (
    monthly_summary,
    category_breakdown,
    top_expenses,
    spending_trend,
)
from finance_tracker.reporter import (
    plot_monthly_summary,
    plot_category_pie,
    plot_spending_trend,
    print_summary_table,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="💰 Personal Finance Tracker — analyze your spending from CSV exports.",
    )
    parser.add_argument("--file", "-f", type=str, required=True,
                        help="Path to your transactions CSV file.")
    parser.add_argument("--month", "-m", type=str, default=None,
                        help="Filter to a specific month e.g. 2024-01.")
    parser.add_argument("--top", "-t", type=int, default=5,
                        help="Number of top expenses to display (default: 5).")
    parser.add_argument("--no-charts", action="store_true",
                        help="Skip chart generation.")
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"\n📂  Loading: {args.file}")
    try:
        df = load_transactions(args.file)
    except (FileNotFoundError, ValueError) as e:
        print(f"❌  Error: {e}")
        sys.exit(1)

    print(f"✅  Loaded {len(df)} transactions "
          f"({df['Date'].min().date()} → {df['Date'].max().date()})\n")

    summary = monthly_summary(df)
    print_summary_table(summary)

    cats = category_breakdown(df, month=args.month)
    label = f"for {args.month}" if args.month else "(all time)"
    print(f"📊  Category Breakdown {label}:")
    print(cats.to_string(index=False))
    print()

    tops = top_expenses(df, n=args.top, month=args.month)
    print(f"🔝  Top {args.top} Expenses {label}:")
    print(tops.to_string(index=False))
    print()

    if not args.no_charts:
        print("📈  Generating charts → reports/")
        plot_monthly_summary(summary)
        plot_category_pie(cats, month=args.month)
        plot_spending_trend(spending_trend(df))
        print("\n🎉  Done! Open reports/ to view your charts.\n")
    else:
        print("ℹ️   Charts skipped.\n")


if __name__ == "__main__":
    main()