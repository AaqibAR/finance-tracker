# 💰 Personal Finance Tracker

A Python CLI tool to analyze personal finances from bank CSV exports.
Automatically categorizes transactions, generates monthly summaries,
and produces visual charts — all from your terminal.

---

## Features

- 📥 Load transactions from any CSV export
- 🏷️ Auto-categorize spending (groceries, transport, utilities, etc.)
- 📊 Monthly income vs expenses breakdown with savings rate
- 🥧 Category spending pie chart
- 📈 Daily spending trend chart
- 🔝 Top N biggest expense finder
- ✅ Unit tested with pytest

---

## Getting Started

### 1. Clone and install dependencies

```bash
git clone https://github.com/AaqibAR/finance-tracker.git
cd finance-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add your transactions CSV

Your CSV needs these columns:

| Column      | Format     | Example               |
|-------------|------------|-----------------------|
| Date        | YYYY-MM-DD | 2024-01-15            |
| Description | Text       | Supermarket Groceries |
| Amount      | +/-        | -45.50 or 2500.00     |
| Type        | text       | expense or income     |

### 3. Run the tracker

```bash
# Full analysis with charts
python3 main.py --file data/transactions.csv

# Filter to a specific month
python3 main.py --file data/transactions.csv --month 2024-01

# Show top 10 biggest expenses
python3 main.py --file data/transactions.csv --top 10

# Terminal only, no charts
python3 main.py --file data/transactions.csv --no-charts
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Tech Stack

- `pandas` — data loading and transformation
- `matplotlib` — chart generation
- `argparse` — CLI interface
- `pytest` — unit testing

---

## License

MIT