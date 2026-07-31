from datetime import datetime
from tracker import ExpenseTracker
from utils import print_banner, write_history


# ─── Helpers ─────────────────────────────────────────────────────────────────

def print_expense_table(expenses):
    """Print a formatted table of expense rows."""
    print(f"{'ID':<5} | {'Date':<12} | {'Category':<15} | {'Amount':<10} | {'Description'}")
    print("-" * 70)
    for exp in expenses:
        print(f"{exp[0]:<5} | {exp[1]:<12} | {exp[2]:<15} | ${exp[3]:<9.2f} | {exp[4]}")
    print()


def validate_date(date_str):
    """Return True if the date string matches DD-MM-YYYY format."""
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def to_db_date(date_str):
    """Convert DD-MM-YYYY user input to YYYY-MM-DD for database storage/query."""
    return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")


# Preset category list
CATEGORIES = [
    "Food",
    "Shopping",
    "Travel",
    "Bills",
    "Entertainment",
    "Education",
    "Health",
    "Salary",
    "Investment",
    "Rent",
]


def select_category():
    """Show a numbered category menu and return the chosen category string.
    Returns None if the user cancels (empty input on custom category).
    """
    print("\n  Select a Category:")
    print("  " + "-" * 30)
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"  {i:>2}. {cat}")
    print(f"  {len(CATEGORIES) + 1:>2}. Other (enter your own)")
    print("  " + "-" * 30)

    while True:
        pick = input(f"  Choose (1-{len(CATEGORIES) + 1}): ").strip()
        if pick.isdigit():
            idx = int(pick)
            if 1 <= idx <= len(CATEGORIES):
                return CATEGORIES[idx - 1]
            elif idx == len(CATEGORIES) + 1:
                custom = input("  Enter your custom category: ").strip()
                if custom:
                    return custom
                else:
                    print("  Category cannot be empty. Please try again.")
        else:
            print(f"  Invalid choice. Enter a number between 1 and {len(CATEGORIES) + 1}.")


# ─── Help ─────────────────────────────────────────────────────────────────────

def print_help():
    """Display the full how-to-use guide."""
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║               HOW TO USE THIS APPLICATION               ║
  ╠══════════════════════════════════════════════════════════╣
  ║                                                          ║
  ║  ADDING AN EXPENSE                                       ║
  ║    1 → Pick a category from the list                    ║
  ║    2 → Type a short description (e.g. "Lunch at KFC")   ║
  ║    3 → Enter the amount (e.g. 12.50)                    ║
  ║                                                          ║
  ║  VIEWING & SEARCHING                                     ║
  ║    • Option 2  → See every expense you've logged        ║
  ║    • Option 5  → Filter by a specific category          ║
  ║    • Option 6  → Search by a keyword in descriptions    ║
  ║    • Option 7  → View expenses between two dates        ║
  ║                                                          ║
  ║  REPORTS & INSIGHTS                                      ║
  ║    • Option 8  → Monthly spending totals                ║
  ║    • Option 9  → Overall stats (total, avg, highest)    ║
  ║    • Option 11 → Export all data to CSV (/exports)      ║
  ║    • Option 12 → Bar chart  (saved to /charts)          ║
  ║    • Option 13 → Pie chart  (saved to /charts)          ║
  ║                                                          ║
  ║  BUDGET                                                  ║
  ║    • Option 10 → Set your monthly budget limit          ║
  ║    • A warning shows automatically if you overspend     ║
  ║                                                          ║
  ║  EDITING & DELETING                                      ║
  ║    • Option 3  → Edit any expense by its ID             ║
  ║    • Option 4  → Delete an expense (asks confirmation)  ║
  ║                                                          ║
  ║  TIP: Every expense gets a unique ID shown in the table ║
  ║       Use that ID to edit or delete it later.           ║
  ║                                                          ║
  ║  Type  'help'  or select  15  anytime to see this guide ║
  ╚══════════════════════════════════════════════════════════╝
    """)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    tracker = ExpenseTracker()

    while True:
        print_banner()

        # ── Budget status alert ──────────────────────────────────────────────
        budget_status = tracker.check_budget_status()
        if budget_status:
            budget, spent, is_over = budget_status
            current_month = datetime.now().strftime("%B %Y")
            if is_over:
                print(f" ⚠  BUDGET ALERT: You've spent ${spent:.2f} of your "
                      f"${budget:.2f} budget for {current_month}!\n")
            else:
                remaining = budget - spent
                print(f" 💰 Budget ({current_month}): ${spent:.2f} spent / "
                      f"${budget:.2f} limit  →  ${remaining:.2f} remaining\n")

        # ── Menu ─────────────────────────────────────────────────────────────
        print(" 1.  Add Expense")
        print(" 2.  View All Expenses")
        print(" 3.  Edit an Expense")
        print(" 4.  Delete Expense")
        print(" 5.  Filter by Category")
        print(" 6.  Search by Keyword")
        print(" 7.  Filter by Date Range")
        print(" 8.  Monthly Summary")
        print(" 9.  Spending Summary (Stats)")
        print("10.  Set / View Monthly Budget")
        print("11.  Export to CSV")
        print("12.  Generate Bar Chart")
        print("13.  Generate Pie Chart")
        print("14.  Exit")
        print("15.  Help  (or type 'help')\n")

        choice = input("Select an option (1-15): ").strip().lower()

        # ── 1. Add Expense ───────────────────────────────────────────────────
        if choice == "1":
            category = select_category()

            description = input("\n  Enter description: ").strip()

            try:
                amount = float(input("  Enter amount ($): "))
            except ValueError:
                print("\n Error: Please enter a valid numerical amount.\n")
                continue

            date_str = datetime.now().strftime("%d-%m-%Y")

            exp_id = tracker.add_expense(date_str, category, amount, description)
            print(f"\n ✔ Expense added with ID {exp_id}!\n")

        # ── 2. View All ──────────────────────────────────────────────────────
        elif choice == "2":
            expenses = tracker.get_expenses()
            print("\n--- All Expenses ---")
            if not expenses:
                print("No expenses recorded yet.\n")
            else:
                print_expense_table(expenses)

        # ── 3. Edit ──────────────────────────────────────────────────────────
        elif choice == "3":
            expenses = tracker.get_expenses()
            if not expenses:
                print("\n No expenses recorded yet.\n")
                continue

            print("\n--- All Expenses ---")
            print_expense_table(expenses)

            try:
                exp_id = int(input("Enter the ID of the expense to edit: "))
            except ValueError:
                print("\n Error: Please enter a valid ID number.\n")
                continue

            # Find the existing record
            existing = next((e for e in expenses if e[0] == exp_id), None)
            if existing is None:
                print(f"\n Error: Expense ID {exp_id} not found.\n")
                continue

            cur_date, cur_cat, cur_amount, cur_desc = existing[1], existing[2], existing[3], existing[4]
            # Category
            change_cat = input("\n  Change category? (y/n): ").strip().lower()
            if change_cat == "y":
                new_category = select_category()
            else:
                new_category = cur_cat

            # Description
            change_desc = input("  Change description? (y/n): ").strip().lower()
            if change_desc == "y":
                new_desc = input("  Enter new description: ").strip() or cur_desc
            else:
                new_desc = cur_desc

            # Amount
            change_amt = input("  Change amount? (y/n): ").strip().lower()
            if change_amt == "y":
                try:
                    new_amount = float(input("  Enter new amount ($): ").strip())
                except ValueError:
                    print("\n Error: Please enter a valid numerical amount.\n")
                    continue
            else:
                new_amount = cur_amount

            if tracker.update_expense(exp_id, new_amount, new_category, new_desc):
                print(f"\n ✔ Expense ID {exp_id} updated successfully!\n")
            else:
                print(f"\n Error: Could not update Expense ID {exp_id}.\n")

        # ── 4. Delete ────────────────────────────────────────────────────────
        elif choice == "4":
            expenses = tracker.get_expenses()
            if not expenses:
                print("\n No expenses recorded yet.\n")
                continue

            print("\n--- All Expenses ---")
            print_expense_table(expenses)

            try:
                exp_id = int(input("Enter the ID of the expense to delete: "))
            except ValueError:
                print("\n Error: Please enter a valid ID number.\n")
                continue

            confirm = input(f"Are you sure you want to delete expense ID {exp_id}? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("\n Deletion cancelled.\n")
                continue

            if tracker.delete_expense(exp_id):
                print(f"\n ✔ Expense ID {exp_id} deleted successfully.\n")
            else:
                print(f"\n Error: Expense ID {exp_id} not found.\n")

        # ── 5. Filter by Category ────────────────────────────────────────────
        elif choice == "5":
            search_cat = select_category()
            filtered = tracker.get_category_expenses(search_cat)

            print(f"\n--- Expenses for '{search_cat}' ---")
            if not filtered:
                print("No expenses found for that category.\n")
            else:
                print_expense_table(filtered)
                total = sum(e[3] for e in filtered)
                print(f" Category Total: ${total:.2f}\n")

        # ── 6. Search by Keyword ─────────────────────────────────────────────
        elif choice == "6":
            keyword = input("Enter keyword to search in descriptions: ").strip()
            results = tracker.search_by_keyword(keyword)

            print(f"\n--- Search Results for '{keyword}' ---")
            if not results:
                print("No expenses matched that keyword.\n")
            else:
                print_expense_table(results)
                print(f" {len(results)} result(s) found.\n")

        # ── 7. Filter by Date Range ──────────────────────────────────────────
        elif choice == "7":
            start = input("Enter start date (DD-MM-YYYY): ").strip()
            end = input("Enter end date   (DD-MM-YYYY): ").strip()

            if not validate_date(start) or not validate_date(end):
                print("\n Error: Invalid date format. Use DD-MM-YYYY.\n")
                continue
            if to_db_date(start) > to_db_date(end):
                print("\n Error: Start date must be on or before end date.\n")
                continue

            results = tracker.get_expenses_by_date_range(to_db_date(start), to_db_date(end))
            print(f"\n--- Expenses from {start} to {end} ---")
            if not results:
                print("No expenses found in that date range.\n")
            else:
                print_expense_table(results)
                total = sum(e[3] for e in results)
                print(f" Period Total: ${total:.2f}\n")

        # ── 8. Monthly Summary ───────────────────────────────────────────────
        elif choice == "8":
            summary = tracker.get_monthly_summary()
            print("\n--- Monthly Spending Summary ---")
            if not summary:
                print("No expenses recorded yet.\n")
            else:
                print(f"{'Month':<12} | {'Total Spent':>12}")
                print("-" * 27)
                grand_total = 0.0
                for month, total in summary:
                    print(f"{month:<12} | ${total:>11.2f}")
                    grand_total += total
                print("-" * 27)
                print(f"{'Grand Total':<12} | ${grand_total:>11.2f}\n")

        # ── 9. Spending Summary (Stats) ──────────────────────────────────────
        elif choice == "9":
            stats = tracker.get_spending_summary()
            print("\n--- Spending Summary ---")
            if stats is None:
                print("No expenses recorded yet.\n")
            else:
                total, average, max_exp = stats
                print(f"  Total Spent  : ${total:.2f}")
                print(f"  Average/Entry: ${average:.2f}")
                print(f"  Largest Entry: ${max_exp[3]:.2f}  →  {max_exp[4]} "
                      f"[{max_exp[2]}] on {max_exp[1]}\n")

        # ── 10. Set / View Budget ────────────────────────────────────────────
        elif choice == "10":
            current = tracker.get_budget()
            if current is not None:
                print(f"\n Current monthly budget: ${current:.2f}")
            else:
                print("\n No monthly budget set yet.")

            action = input(" Enter new budget amount (or press Enter to keep current): ").strip()
            if action == "":
                print()
                continue
            try:
                new_limit = float(action)
                if new_limit <= 0:
                    raise ValueError
            except ValueError:
                print("\n Error: Please enter a positive number.\n")
                continue

            tracker.set_budget(new_limit)
            print(f"\n ✔ Monthly budget set to ${new_limit:.2f}\n")

        # ── 11. Export to CSV ────────────────────────────────────────────────
        elif choice == "11":
            path = tracker.export_csv()
            print(f"\n ✔ CSV exported successfully to: {path}\n")

        # ── 12. Bar Chart ────────────────────────────────────────────────────
        elif choice == "12":
            path = tracker.generate_chart()
            if path:
                print(f"\n ✔ Bar chart generated at: {path}\n")
            else:
                print("\n Error: Add some expenses before generating a chart.\n")

        # ── 13. Pie Chart ────────────────────────────────────────────────────
        elif choice == "13":
            path = tracker.generate_pie_chart()
            if path:
                print(f"\n ✔ Pie chart generated at: {path}\n")
            else:
                print("\n Error: Add some expenses before generating a chart.\n")

        # ── 14. Exit ─────────────────────────────────────────────────────────
        elif choice == "14":
            write_history("App Exited", "User exited the application")
            print("\n Goodbye! 👋\n")
            break

        # ── 15. Help ─────────────────────────────────────────────────────────
        elif choice in ("15", "help"):
            print_help()

        else:
            print("\n Invalid choice. Please select 1-15 or type 'help'.\n")


if __name__ == "__main__":
    main()