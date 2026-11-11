
import customtkinter as ctk
import sqlite3
import hashlib
import secrets
from dashboard import open_expense_tracker

conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

conn.commit()


def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_password):
    salt_hex, hash_hex = stored_password.split(":")

    salt = bytes.fromhex(salt_hex)
    saved_hash = bytes.fromhex(hash_hex)

    entered_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return secrets.compare_digest(
        entered_hash,
        saved_hash
    )


def login_user():
    email = login_email_entry.get().strip()
    password = login_password_entry.get()

    if not email or not password:
        login_message.configure(
            text="Please enter your email/phone and password.",
            text_color="red"
        )
        return

    cursor.execute(
        "SELECT id,name, password FROM users WHERE email = ?",
        (email,)
    )
    result = cursor.fetchone()

    if result and verify_password(password, result[2]):
        login_message.configure(
            text="Login successful!",
            text_color="green"
        )
        user_id = result[0]
        user_name = result[1]
        root.destroy()
        open_expense_tracker(user_id=user_id,user_name=user_name)
    else:
        login_message.configure(
            text="Invalid email/phone or password.",
            text_color="red"
        )



root = ctk.CTk()
root.title("Expense Tracker | Login")
root.geometry("900x600")
root.resizable(False, False)

# Main background
root.configure(fg_color="#F1F5F9")

# Login card
login_card = ctk.CTkFrame(
    root,
    width=380,
    height=440,
    corner_radius=20,
    fg_color="white"
)
login_card.place(relx=0.5, rely=0.5, anchor="center")

# Heading
ctk.CTkLabel(
    login_card,
    text="Welcome Back",
    font=("Arial", 28, "bold"),
    text_color="#0F172A"
).pack(pady=(35, 5))

ctk.CTkLabel(
    login_card,
    text="Sign in to manage your expenses",
    font=("Arial", 13),
    text_color="#64748B"
).pack(pady=(0, 25))

# Email
login_email_entry = ctk.CTkEntry(
    login_card,
    width=300,
    height=42,
    corner_radius=10,
    placeholder_text="Email address or Phone Number"
)
login_email_entry.pack(pady=10)

# Password
# Password
# Password
password_frame = ctk.CTkFrame(
    login_card,
    fg_color="transparent"
)
password_frame.pack(pady=10)

login_password_entry = ctk.CTkEntry(
    password_frame,
    width=300,
    height=42,
    corner_radius=10,
    placeholder_text="Password",
    show="*"
)
login_password_entry.pack()

def toggle_login_password():
    if login_password_entry.cget("show") == "*":
        login_password_entry.configure(show="")
        login_eye_button.configure(text="🙈")
    else:
        login_password_entry.configure(show="*")
        login_eye_button.configure(text="👁")

login_eye_button = ctk.CTkButton(
    password_frame,
    text="👁",
    width=30,
    height=30,
    fg_color="transparent",
    hover_color="#E2E8F0",
    text_color="#475569",
    command=toggle_login_password
)

login_eye_button.place(relx=0.91, rely=0.5, anchor="center")

def toggle_login_password():
    if login_password_entry.cget("show") == "*":
        login_password_entry.configure(show="")
        login_eye_button.configure(text="🙈")
    else:
        login_password_entry.configure(show="*")
        login_eye_button.configure(text="👁")


login_eye_button = ctk.CTkButton(
    login_card,
    text="👁",
    width=35,
    height=30,
    fg_color="transparent",
    hover_color="#E2E8F0",
    text_color="#475569",
    command=toggle_login_password
)
login_eye_button.place(x=305, y=145)


login_message = ctk.CTkLabel(
    login_card,
    text="",
    text_color="red",
    font=("Arial", 12)
)
login_message.pack(pady=5)



def register_user():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get()

    if not name or not email or not password:
        register_message.configure(
            text="Please fill in all fields.",
            text_color="red"
        )
        return

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hash_password(password))
        )
        conn.commit()

        register_message.configure(
            text="Account created successfully!",
            text_color="green"
        )
        name_entry.delete(0,"end")
        email_entry.delete(0,"end")
        password_entry.delete(0,"end")
        root.after(1200, show_login)
        
        
    except sqlite3.IntegrityError:
        register_message.configure(
            text="This email or phone is already registered.",
            text_color="red"
        )



def show_register():
    login_card.place_forget()

    register_card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )


def show_login():
    register_card.place_forget()

    login_card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )


register_card = ctk.CTkFrame(
    root,
    width=380,
    height=480,
    corner_radius=20,
    fg_color="white"
)

register_card.pack_propagate(False)

# Password
# Password
register_password_frame = ctk.CTkFrame(
    register_card,
    fg_color="transparent"
)
register_password_frame.pack(pady=8)

password_entry = ctk.CTkEntry(
    register_password_frame,
    width=300,
    height=42,
    corner_radius=10,
    placeholder_text="Password",
    show="*"
)
password_entry.pack()

def toggle_register_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        register_eye_button.configure(text="🙈")
    else:
        password_entry.configure(show="*")
        register_eye_button.configure(text="👁")

register_eye_button = ctk.CTkButton(
    register_password_frame,
    text="👁",
    width=30,
    height=30,
    fg_color="transparent",
    hover_color="#E2E8F0",
    text_color="#475569",
    command=toggle_register_password
)

register_eye_button.place(relx=0.91, rely=0.5, anchor="center")

def toggle_register_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        register_eye_button.configure(text="🙈")
    else:
        password_entry.configure(show="*")
        register_eye_button.configure(text="👁")


register_eye_button = ctk.CTkButton(
    register_card,
    text="👁",
    width=35,
    height=30,
    fg_color="transparent",
    hover_color="#E2E8F0",
    text_color="#475569",
    command=toggle_register_password
)
register_eye_button.place(x=305, y=126)

name_entry = ctk.CTkEntry(
    register_card,
    width=300,
    height=42,
    placeholder_text="Full name"
)
name_entry.pack(pady=8)

email_entry = ctk.CTkEntry(
    register_card,
    width=300,
    height=42,
    placeholder_text="Email or phone number"
)
email_entry.pack(pady=8)

password_entry = ctk.CTkEntry(
    register_card,
    width=300,
    height=42,
    placeholder_text="Password",
    show="*"
)
password_entry.pack(pady=8)


register_message = ctk.CTkLabel(
    register_card,
    text="",
    text_color="red",
    font=("Arial", 12)
)
register_message.pack(pady=5)


ctk.CTkButton(
    register_card,
    text="Create Account",
    width=300,
    height=42,
    command=register_user
).pack(pady=(20, 10))

ctk.CTkButton(
    register_card,
    text="Back to Login",
    width=300,
    height=38,
    fg_color="transparent",
    text_color="#2563EB",
    hover_color="#DBEAFE",
    command=show_login
).pack()


# Login button

login_button = ctk.CTkButton(
    login_card,
    text="Login",
    width=300,
    height=42,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    command=login_user
)
login_button.pack(pady=(20, 15))


ctk.CTkLabel(
    login_card,
    text="Don't have an account?",
    font=("Arial", 12),
    text_color="#64748B"
).pack(pady=(5, 0))

ctk.CTkButton(
    login_card,
    text="Create Account",
    width=300,
    height=38,
    corner_radius=10,
    fg_color="transparent",
    text_color="#2563EB",
    hover_color="#DBEAFE",
    command=show_register
).pack(pady=5)


root.mainloop()

