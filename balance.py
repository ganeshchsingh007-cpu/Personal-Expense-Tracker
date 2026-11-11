import sqlite3



conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL NOT NULL,
        description TEXT,
        date_time TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    )
""")

conn.commit()
conn.close()


def get_total_balance(user_id):
    conn = sqlite3.connect("expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id = ?",
        (user_id,)
    )
    total_expenses = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE user_id = ?",
        (user_id,)
    )

    total_income = cursor.fetchone()[0] or 0

    conn.close()

    return total_income - total_expenses

    
def get_total_income(user_id):
    conn = sqlite3.connect("expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE user_id = ?",
        (user_id,)
    )

    total_income = cursor.fetchone()[0] or 0

    conn.close()

    return total_income