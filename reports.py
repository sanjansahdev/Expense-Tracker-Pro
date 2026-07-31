import csv
import os
import matplotlib.pyplot as plt
from config import EXPORTS_DIR, CHARTS_DIR
from database import get_all_expenses_db

def export_to_csv():
    """Exports all database records to a CSV file."""
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    file_path = os.path.join(EXPORTS_DIR, "expenses.csv")
    expenses = get_all_expenses_db()

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
        writer.writerows(expenses)
    return file_path

def generate_category_chart():
    """Generates a bar chart breakdown of expenses by category."""
    os.makedirs(CHARTS_DIR, exist_ok=True)
    expenses = get_all_expenses_db()
    if not expenses:
        return None

    totals = {}
    for exp in expenses:
        cat = exp[2]
        amt = exp[3]
        totals[cat] = totals.get(cat, 0) + amt

    categories = list(totals.keys())
    amounts = list(totals.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount ($)")
    plt.tight_layout()

    chart_path = os.path.join(CHARTS_DIR, "category_bar.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def generate_pie_chart():
    """Generates a pie chart breakdown of expenses by category."""
    os.makedirs(CHARTS_DIR, exist_ok=True)
    expenses = get_all_expenses_db()
    if not expenses:
        return None

    totals = {}
    for exp in expenses:
        cat = exp[2]
        amt = exp[3]
        totals[cat] = totals.get(cat, 0) + amt

    categories = list(totals.keys())
    amounts = list(totals.values())

    plt.figure(figsize=(7, 7))
    plt.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.2}
    )
    plt.title("Spending Distribution by Category", pad=15)
    plt.tight_layout()

    chart_path = os.path.join(CHARTS_DIR, "category_pie.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path