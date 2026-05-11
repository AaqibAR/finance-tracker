"""
categorizer.py
--------------
Assigns a category to each transaction based on keyword rules.
"""

CATEGORY_RULES = {
    "Groceries":      ["supermarket", "grocery", "groceries", "market"],
    "Transport":      ["uber", "grab", "fuel", "gas station", "taxi"],
    "Utilities":      ["electricity", "water bill", "internet", "mobile"],
    "Entertainment":  ["netflix", "spotify", "cinema", "youtube"],
    "Dining":         ["restaurant", "dinner", "coffee", "cafe"],
    "Health":         ["pharmacy", "clinic", "hospital", "gym"],
    "Shopping":       ["amazon", "purchase", "online", "shop"],
    "Education":      ["course", "book", "udemy", "class"],
    "Income":         ["salary", "freelance", "deposit"],
}

UNCATEGORIZED = "Uncategorized"


def categorize(description: str) -> str:
    """Return a category for a given transaction description."""
    desc_lower = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(kw in desc_lower for kw in keywords):
            return category
    return UNCATEGORIZED


def get_all_categories() -> list[str]:
    """Return all defined category names."""
    return list(CATEGORY_RULES.keys()) + [UNCATEGORIZED]