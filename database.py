import sqlite3
import os
from config import DB_PATH

def get_connection():
    """Ensures database directory exists and returns a connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Creates the expenses and budget tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budget (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                monthly_limit REAL NOT NULL
            )
        """)
        conn.commit()

def add_expense_db(date, category, amount, description):
    """Inserts a new expense and returns the assigned ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        """, (date, category, amount, description))
        conn.commit()
        return cursor.lastrowid

def get_all_expenses_db():
    """Retrieves all expenses ordered by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, category, amount, description FROM expenses ORDER BY id ASC")
        return cursor.fetchall()

def delete_expense_db(expense_id):
    """Deletes an expense by ID if it exists."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
        if not cursor.fetchone():
            return False
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        return True

def update_expense_db(expense_id, amount, category, description):
    """Updates an existing expense record by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
        if not cursor.fetchone():
            return False
            
        cursor.execute("""
            UPDATE expenses 
            SET amount = ?, category = ?, description = ?
            WHERE id = ?
        """, (amount, category, description, expense_id))
        conn.commit()
        return True

def get_expenses_by_category_db(category):
    """Retrieves expenses filtered by a specific category."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, date, category, amount, description 
            FROM expenses 
            WHERE category = ? COLLATE NOCASE 
            ORDER BY id ASC
        """, (category,))
        return cursor.fetchall()


def search_expenses_by_keyword_db(keyword):
    """Searches expenses where the description contains the given keyword."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, date, category, amount, description
            FROM expenses
            WHERE description LIKE ? COLLATE NOCASE
            ORDER BY id ASC
        """, (f"%{keyword}%",))
        return cursor.fetchall()


def get_expenses_by_date_range_db(start_date, end_date):
    """Retrieves expenses between start_date and end_date (DD-MM-YYYY).
    Converts to YYYY-MM-DD internally for correct string comparison.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        # Reorder date stored as DD-MM-YYYY to YYYY-MM-DD for BETWEEN comparison
        cursor.execute("""
            SELECT id, date, category, amount, description
            FROM expenses
            WHERE (
                substr(date,7,4) || '-' || substr(date,4,2) || '-' || substr(date,1,2)
            ) BETWEEN ? AND ?
            ORDER BY
                substr(date,7,4), substr(date,4,2), substr(date,1,2) ASC
        """, (start_date, end_date))
        return cursor.fetchall()


def get_monthly_summary_db():
    """Returns total spending grouped by month (YYYY-MM) for correct ordering.
    Dates stored as DD-MM-YYYY; year and month extracted via substrings.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                substr(date,7,4) || '-' || substr(date,4,2) AS month,
                SUM(amount) AS total
            FROM expenses
            GROUP BY month
            ORDER BY month ASC
        """)
        return cursor.fetchall()


def get_budget_db():
    """Returns the current monthly budget limit, or None if not set."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT monthly_limit FROM budget WHERE id = 1")
        row = cursor.fetchone()
        return row[0] if row else None


def set_budget_db(limit):
    """Inserts or updates the monthly budget limit."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO budget (id, monthly_limit) VALUES (1, ?)
            ON CONFLICT(id) DO UPDATE SET monthly_limit = excluded.monthly_limit
        """, (limit,))
        conn.commit()