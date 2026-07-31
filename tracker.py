from database import (
    init_db, add_expense_db, get_all_expenses_db,
    delete_expense_db, update_expense_db, get_expenses_by_category_db,
    search_expenses_by_keyword_db, get_expenses_by_date_range_db,
    get_monthly_summary_db, get_budget_db, set_budget_db
)
from utils import log_action, write_history
from reports import export_to_csv, generate_category_chart, generate_pie_chart

class ExpenseTracker:
    def __init__(self):
        init_db()

    def add_expense(self, date, category, amount, description):
        exp_id = add_expense_db(date, category, amount, description)
        log_action(f"Added expense ID {exp_id}: ${amount:.2f} [{category}]")
        write_history("Added Expense",
                      f"ID: {exp_id}  |  {category}  |  ${amount:.2f}  |  \"{description}\"")
        return exp_id

    def get_expenses(self):
        write_history("Viewed All Expenses")
        return get_all_expenses_db()

    def delete_expense(self, exp_id):
        success = delete_expense_db(exp_id)
        if success:
            log_action(f"Deleted expense ID {exp_id}")
            write_history("Deleted Expense", f"ID: {exp_id}")
        return success

    def export_csv(self):
        path = export_to_csv()
        log_action(f"Exported data to {path}")
        write_history("Exported CSV", f"File: {path}")
        return path

    def generate_chart(self):
        path = generate_category_chart()
        if path:
            log_action(f"Generated bar chart at {path}")
            write_history("Generated Bar Chart", f"Saved to: {path}")
        return path

    def generate_pie_chart(self):
        """Generates a pie chart of spending by category."""
        path = generate_pie_chart()
        if path:
            log_action(f"Generated pie chart at {path}")
            write_history("Generated Pie Chart", f"Saved to: {path}")
        return path

    def update_expense(self, exp_id, amount, category, description):
        success = update_expense_db(exp_id, amount, category, description)
        if success:
            log_action(f"Updated expense ID {exp_id}: ${amount:.2f} [{category}]")
            write_history("Edited Expense",
                          f"ID: {exp_id}  |  {category}  |  ${amount:.2f}  |  \"{description}\"")
        return success

    def get_category_expenses(self, category):
        write_history("Filtered by Category", f"Category: {category}")
        return get_expenses_by_category_db(category)

    def search_by_keyword(self, keyword):
        """Returns expenses whose description contains the keyword."""
        write_history("Searched by Keyword", f"Keyword: \"{keyword}\"")
        return search_expenses_by_keyword_db(keyword)

    def get_expenses_by_date_range(self, start_date, end_date):
        """Returns expenses between start_date and end_date (YYYY-MM-DD)."""
        write_history("Filtered by Date Range", f"{start_date}  →  {end_date}")
        return get_expenses_by_date_range_db(start_date, end_date)

    def get_monthly_summary(self):
        """Returns a list of (month, total) tuples."""
        write_history("Viewed Monthly Summary")
        return get_monthly_summary_db()

    def get_spending_summary(self):
        """Returns (total, average, max_expense) across all expenses."""
        write_history("Viewed Spending Stats")
        expenses = get_all_expenses_db()
        if not expenses:
            return None
        amounts = [e[3] for e in expenses]
        total = sum(amounts)
        average = total / len(amounts)
        max_exp = max(expenses, key=lambda e: e[3])
        return total, average, max_exp

    def get_budget(self):
        """Returns the monthly budget limit, or None if not set."""
        return get_budget_db()

    def set_budget(self, limit):
        """Sets the monthly budget limit."""
        set_budget_db(limit)
        log_action(f"Monthly budget set to ${limit:.2f}")
        write_history("Set Monthly Budget", f"Limit: ${limit:.2f}")

    def check_budget_status(self):
        """Returns (budget, current_month_total, is_over) or None if no budget set."""
        import datetime
        budget = get_budget_db()
        if budget is None:
            return None
        current_month = datetime.datetime.now().strftime("%Y-%m")
        monthly_data = get_monthly_summary_db()
        spent = next((total for month, total in monthly_data if month == current_month), 0.0)
        return budget, spent, spent > budget
