import customtkinter as ctk
import sqlite3
from tkinter import messagebox


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

def save_income(user_id, refresh_callback=None):
    amount = amount_entry.get()
    description = description_entry.get()

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
        INSERT INTO income (user_id, amount, description)
        VALUES (?, ?, ?)
        """,
        (user_id, amount, description)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Income saved successfully!"
    )

    if refresh_callback:
        refresh_callback()


def open_add_income(parent, user_id, refresh_callback=None):
    for widget in parent.winfo_children():
        widget.destroy()

    window = parent

    title = ctk.CTkLabel(
        window,
        text="Add New Income",
        font=("Arial", 26, "bold"),
        text_color="#1E293B"
    )
    title.pack(anchor="w", padx=30, pady=25)

    global amount_entry
    amount_entry = ctk.CTkEntry(
        window,
        placeholder_text="Enter amount (₹)",
        width=400,
        height=40
    )
    amount_entry.pack(pady=12)

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
        text="Save Income",
        width=400,
        height=40,
        fg_color="#16A34A",
        hover_color="#15803D",
        command=lambda: save_income(user_id, refresh_callback)
    )
    save_button.pack(pady=20)