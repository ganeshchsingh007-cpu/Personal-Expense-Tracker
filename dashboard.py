
import customtkinter as ctk
from add_expense import open_add_expense
from balance import get_total_balance, get_total_income
from income import open_add_income
import sqlite3

def show_dashboard(user_id):
    open_expense_tracker(dashboard_app, user_id)

def open_expense_tracker(app=None, user_id=None,user_name=None):
    print("OPEN DASHBOARD CALLED", user_id)
    global dashboard_app
    
    conn = sqlite3.connect("expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id = ?",
        (user_id,)
    )
    total_expenses = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT amount, category, description
        FROM expenses
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    expenses = cursor.fetchall()
    conn.close()

    print(expenses)
    app = app or ctk.CTk()
    dashboard_app = app
    for widget in app.winfo_children():
        widget.destroy()

    # Sidebar
    sidebar = ctk.CTkFrame(
        app,
        width=220,
        corner_radius=0,
        fg_color="#172554"
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Sidebar heading
    ctk.CTkLabel(
        sidebar,
        text="EXPENSE TRACKER",
        font=("Arial", 18, "bold"),
        text_color="white"
    ).pack(pady=(30, 40))

    # Navigation buttons
    ctk.CTkButton(
        sidebar,
        text="🏠  Dashboard",
        anchor="w",
        fg_color="transparent",
        hover_color="#1E3A8A",
        text_color="white",
        command=lambda: open_expense_tracker(app,user_id,user_name)
    ).pack(fill="x", padx=12, pady=6)

    ctk.CTkButton(
        sidebar,
        text="➕  Add Expense",
        anchor="w",
        fg_color="transparent",
        hover_color="#1E3A8A",
        text_color="white",
        command=lambda: open_add_expense(main_frame, user_id,lambda:show_dashboard(user_id))
    ).pack(fill="x", padx=12, pady=6)

    ctk.CTkButton(
        sidebar,
        text="💰  Add Income",
        anchor="w",
        fg_color="transparent",
        hover_color="#1E3A8A",
        text_color="white",
        command=lambda: open_add_income(
            main_frame,
            user_id,
            lambda: show_dashboard(user_id)
        )
    ).pack(fill="x", padx=12, pady=6)

    ctk.CTkButton(
        sidebar,
        text="📋  Transactions",
        anchor="w",
        fg_color="transparent",
        hover_color="#1E3A8A",
        text_color="white"
    ).pack(fill="x", padx=12, pady=6)

    ctk.CTkButton(
        sidebar,
        text="👤  Account",
        anchor="w",
        fg_color="transparent",
        hover_color="#1E3A8A",
        text_color="white"
    ).pack(fill="x", padx=12, pady=6)

    # Main content area
    main_frame = ctk.CTkFrame(
        app,
        fg_color="#F1F5F9",
        corner_radius=0
    )
    main_frame.pack(side="left", fill="both", expand=True)

    ctk.CTkLabel(
        main_frame,
        text=f"Welcome, {user_name} 👋",
        font=("Arial", 26, "bold"),
        text_color="#0F172A"
    ).pack(anchor="w", padx=30, pady=(25, 5)),

    # Page heading
    ctk.CTkLabel(
        main_frame,
        text="Dashboard",
        font=("Arial", 28, "bold"),
        text_color="#1E293B"
    ).pack(anchor="w", padx=30, pady=(30, 10))

    ctk.CTkLabel(
        main_frame,
        text="Welcome back! Here's your financial overview.",
        font=("Arial", 14),
        text_color="#64748B"
    ).pack(anchor="w", padx=30, pady=(0, 25))

    # Summary cards
    cards_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )
    cards_frame.pack(fill="x", padx=20, pady=10)

    cards_frame.grid_columnconfigure(
        (0, 1, 2),
        weight=1
    )

    card_data = [
    ("Total Balance", f"₹{get_total_balance(user_id):,.2f}", "#2563EB"),
    ("Total Income", f"₹{get_total_income(user_id):,.2f}", "#16A34A"),
    ("Total Expenses", f"₹{total_expenses:,.2f}", "#DC2626")
    ]

    for index, (heading, amount, color) in enumerate(card_data):
        card = ctk.CTkFrame(
            cards_frame,
            fg_color="white",
            corner_radius=12,
            height=130
        )
        card.grid(
            row=0,
            column=index,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text=heading,
            font=("Arial", 15),
            text_color="#64748B"
        ).pack(anchor="w", padx=18, pady=(22, 8))

        amount_label = ctk.CTkLabel(
            card,
            text=amount,
            font=("Arial", 24, "bold"),
            text_color=color
        )

        amount_label.pack(anchor="w", padx=18)
        if heading == "Total Expenses":
            expense_label = amount_label
    # Recent transactions section
    def refresh_transactions():

        for widget in transactions_frame.winfo_children():
            widget.destroy()
        conn = sqlite3.connect("expense_tracker.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT amount, category, description, date_time
            FROM expenses
            WHERE user_id = ?
            ORDER BY id DESC
        """,(user_id,))
        
        expenses = cursor.fetchall()
        conn.close()  
        total_expenses = sum(amount for amount, category, description, date_time in expenses)
        expense_label.configure(text=f"₹{total_expenses:,.2f}")
        
        if expenses:
            for amount, category, description, date_time in expenses:
                transaction_text = (
                    f"{category}  |  ₹{amount:.2f}  |  {description or ''} | {date_time or 'Date unavailable'}"
                )

                ctk.CTkLabel(
                    transactions_frame,
                    text=transaction_text,
                    font=("Arial", 14),
                    text_color="#334155"
                ).pack(anchor="w", padx=20, pady=8)
        else:
            ctk.CTkLabel(
                transactions_frame,
                text="No transactions yet.",
                font=("Arial", 14),
                text_color="#64748B"
            ).pack(pady=40)  

        ctk.CTkLabel(
            transactions_frame,
            text="Recent Transactions",
        font=("Arial", 20, "bold"),
        text_color="#1E293B"
    ).pack(anchor="w", padx=20, pady=20)
    transactions_frame = ctk.CTkFrame(
        main_frame,
        fg_color="white",
        corner_radius=12
    )
    transactions_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )
    refresh_transactions()

    ctk.CTkLabel(
        transactions_frame,
        text="Recent Transactions",
        font=("Arial", 20, "bold"),
        text_color="#1E293B"
    ).pack(anchor="w", padx=20, pady=20)


    app.mainloop()


