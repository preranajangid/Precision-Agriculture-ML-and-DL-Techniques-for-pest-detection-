import tkinter as tk
from tkinter import ttk, messagebox as ms
import sqlite3

# --- MAIN WINDOW SETUP ---
root = tk.Tk()
root.title("Agri Pest Detection - Registration")
root.geometry("600x600")
root.configure(bg="#f5f5f5")
root.resizable(True, True)

# Variables for form fields
fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
email = tk.StringVar()
phoneno = tk.StringVar()
gender = tk.StringVar()
age = tk.StringVar()
password = tk.StringVar()
confirm_password = tk.StringVar()

# --- STYLE SETUP ---
style = ttk.Style()
style.theme_use('clam')

style.configure("TFrame", background="#ffffff")
style.configure("TLabel", background="#ffffff", font=("Segoe UI", 12))
style.configure("TEntry", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 12), padding=6)
style.map("TButton",
          background=[('active', '#4CAF50'), ('!active', '#388E3C')],
          foreground=[('active', 'white'), ('!active', 'white')])

# --- FUNCTIONS ---

def register_user():
    # Validate required fields
    if not (fullname.get() and address.get() and username.get() and email.get() and phoneno.get() and gender.get() and age.get() and password.get() and confirm_password.get()):
        ms.showerror("Error", "All fields are required.")
        return

    if password.get() != confirm_password.get():
        ms.showerror("Error", "Passwords do not match.")
        return

    with sqlite3.connect('resistration.db') as db:
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS registration
                     (Fullname TEXT, address TEXT, username TEXT UNIQUE, Email TEXT, 
                      Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)""")
        db.commit()

        # Check if username already exists
        c.execute('SELECT * FROM registration WHERE username = ?', (username.get(),))
        if c.fetchone():
            ms.showerror("Error", "Username already exists. Choose a different username.")
            return

        # Insert user data
        c.execute('INSERT INTO registration (Fullname, address, username, Email, Phoneno, Gender, age, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                  (fullname.get(), address.get(), username.get(), email.get(), phoneno.get(), gender.get(), age.get(), password.get()))
        db.commit()

        ms.showinfo("Success", "Registration Successful! Please login.")
        root.destroy()
        from subprocess import call
        call(["python", "login.py"])

def back_to_login():
    root.destroy()
    from subprocess import call
    call(["python", "login.py"])

# --- MAIN FRAME ---
main_frame = ttk.Frame(root, padding="40 30 40 30", style="TFrame")
main_frame.place(relx=0.5, rely=0.5, anchor='center')

# --- TITLE ---
title_label = ttk.Label(main_frame, text="🌿 Agri Pest Detection", font=("Segoe UI", 20, "bold"), foreground="#2E7D32", background="#ffffff")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# --- FORM FIELDS ---

labels = ["Full Name:", "Address:", "Username:", "Email:", "Phone No:", "Gender:", "Age:", "Password:", "Confirm Password:"]
variables = [fullname, address, username, email, phoneno, gender, age, password, confirm_password]
widgets = []

for i, (label_text, var) in enumerate(zip(labels, variables), start=1):
    ttk.Label(main_frame, text=label_text).grid(row=i, column=0, sticky='w', pady=8)
    if label_text == "Gender:":
        gender_combo = ttk.Combobox(main_frame, textvariable=gender, values=["Male", "Female", "Other"], state="readonly", width=19, font=("Segoe UI", 12))
        gender_combo.grid(row=i, column=1, pady=8)
        gender_combo.current(0)
        widgets.append(gender_combo)
    elif "Password" in label_text:
        entry = ttk.Entry(main_frame, textvariable=var, show='*', width=30)
        entry.grid(row=i, column=1, pady=8)
        widgets.append(entry)
    else:
        entry = ttk.Entry(main_frame, textvariable=var, width=30)
        entry.grid(row=i, column=1, pady=8)
        widgets.append(entry)

# --- BUTTONS ---
register_button = ttk.Button(main_frame, text="Register", command=register_user)
register_button.grid(row=len(labels)+1, column=1, sticky='e', pady=20, padx=5)

back_button = ttk.Button(main_frame, text="Back to Login", command=back_to_login)
back_button.grid(row=len(labels)+1, column=0, sticky='w', pady=20, padx=5)

# --- FOOTER ---
footer_label = ttk.Label(root, text="© 2025 Precision Agriculture Team", background="#f5f5f5", font=("Segoe UI", 10))
footer_label.pack(side='bottom', pady=10)

root.mainloop()
