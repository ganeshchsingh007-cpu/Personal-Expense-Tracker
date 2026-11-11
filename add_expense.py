
import customtkinter as ctk
import sqlite3
from tkinter import messagebox

conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date_time TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    )
""")

conn.commit()
try:
    cursor.execute(
        "ALTER TABLE expenses ADD COLUMN user_id INTEGER"
    )
    conn.commit()
except sqlite3.OperationalError:
    pass
try:
    cursor.execute(
        "ALTER TABLE expenses ADD COLUMN date_time TEXT"
    )
    conn.commit()
except sqlite3.OperationalError:
    pass


def save_expense(user_id, refresh_callback=None):
    amount = amount_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    if not category.strip():
        print("Please enter a category!")
        return

    if not amount:
        print("Please enter an amount!")
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Please enter a valid number!")
        return

    if amount <= 0:
        print("Amount must be greater than zero!")
        return

    cursor.execute(
        """
        INSERT INTO expenses (user_id, amount, category, description, date_time)
        VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
        """,
        (user_id,amount, category, description)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Expense saved successfully!"
    )
    if refresh_callback:
        refresh_callback()
   
    

def open_add_expense(parent, user_id, refresh_callback=None):
    for widget in parent.winfo_children():
        widget.destroy()
    window = parent
    

    title = ctk.CTkLabel(
        window,
        text="Add New Expense",
        font=("Arial", 26, "bold"),
        text_color="#1E293B"
    )
    title.pack(anchor="w", padx=30, pady=25)
    # Expense amount
    global amount_entry
    amount_entry = ctk.CTkEntry(
        window,
        placeholder_text="Enter amount (₹)",
        width=400,
        height=40
    )
    amount_entry.pack(pady=12)

# Expense category
    global category_entry
    category_entry = ctk.CTkEntry(
        window,
        placeholder_text="Enter category (e.g. Food)",
        width=400,
        height=40
    )
    category_entry.pack(pady=12)

# Expense description
    global description_entry
    description_entry = ctk.CTkEntry(
        window,
        placeholder_text="Enter description",
        width=400,
        height=40
    )
    description_entry.pack(pady=12)
    save_button = ctk.CTkButton(
        window,
        text="Save Expense",
        width=400,
        height=40,
        fg_color="#2563EB",
        hover_color="#1D4ED8",
        command=lambda: save_expense(user_id,refresh_callback)
    )
    save_button.pack(pady=20)
    

    


