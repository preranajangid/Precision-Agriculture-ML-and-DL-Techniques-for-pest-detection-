import tkinter as tk
from tkinter import ttk, messagebox as ms
import sqlite3

# --- MAIN WINDOW SETUP ---
root = tk.Tk()
root.title("Agri Pest Detection - Login")
root.geometry("600x480")
root.configure(bg="#f5f5f5")
root.resizable(True, True)

username = tk.StringVar()
password = tk.StringVar()

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

def registration():
    from subprocess import call
    call(["python", "registration.py"])
    root.destroy()

def login():
    with sqlite3.connect('resistration.db') as db:
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS registration
                     (Fullname TEXT, address TEXT, username TEXT, Email TEXT, 
                      Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)""")
        db.commit()
        c.execute('SELECT * FROM registration WHERE username = ? AND password = ?', 
                  (username.get(), password.get()))
        result = c.fetchall()

        if result:
            ms.showinfo("Success", "Login Successful!")
            root.destroy()
            from subprocess import call
            call(['python', 'GUI_Master_plant.py'])
        else:
            ms.showerror('Error', 'Invalid Username or Password.')

def forgot_password():
    def reset_password():
        user = fp_username.get()
        mail = fp_email.get()
        new_pass = fp_new_password.get()

        if not user or not mail or not new_pass:
            ms.showerror("Error", "All fields are required.")
            return

        with sqlite3.connect('resistration.db') as db:
            c = db.cursor()
            c.execute('SELECT * FROM registration WHERE username = ? AND Email = ?', (user, mail))
            result = c.fetchone()

            if result:
                c.execute('UPDATE registration SET password = ? WHERE username = ?', (new_pass, user))
                db.commit()
                ms.showinfo('Success', 'Password updated successfully!')
                fp_window.destroy()
            else:
                ms.showerror('Error', 'User not found or email does not match.')

    # Popup window
    fp_window = tk.Toplevel(root)
    fp_window.title("Reset Password")
    fp_window.geometry("400x300")
    fp_window.configure(bg="#f5f5f5")
    fp_window.resizable(False, False)

    # Frame for styling consistency
    fp_frame = ttk.Frame(fp_window, padding="20 20 20 20", style="TFrame")
    fp_frame.pack(expand=True, fill='both')

    fp_username = tk.StringVar()
    fp_email = tk.StringVar()
    fp_new_password = tk.StringVar()

    ttk.Label(fp_frame, text="Username:").pack(anchor='w', pady=(0,5))
    ttk.Entry(fp_frame, textvariable=fp_username, width=30).pack(pady=(0,10))

    ttk.Label(fp_frame, text="Registered Email:").pack(anchor='w', pady=(0,5))
    ttk.Entry(fp_frame, textvariable=fp_email, width=30).pack(pady=(0,10))

    ttk.Label(fp_frame, text="New Password:").pack(anchor='w', pady=(0,5))
    ttk.Entry(fp_frame, textvariable=fp_new_password, width=30, show='*').pack(pady=(0,20))

    ttk.Button(fp_frame, text="Reset Password", command=reset_password).pack()

# --- MAIN FRAME ---
main_frame = ttk.Frame(root, padding="40 30 40 30", style="TFrame")
main_frame.place(relx=0.5, rely=0.5, anchor='center')

# --- TITLE ---
title_label = ttk.Label(main_frame, text="🌿 Agri Pest Detection", font=("Segoe UI", 20, "bold"), foreground="#2E7D32", background="#ffffff")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# --- USERNAME ---
username_label = ttk.Label(main_frame, text="Username:")
username_label.grid(row=1, column=0, sticky='w', pady=10)
username_entry = ttk.Entry(main_frame, textvariable=username, width=30)
username_entry.grid(row=1, column=1, pady=10)

# --- PASSWORD ---
password_label = ttk.Label(main_frame, text="Password:")
password_label.grid(row=2, column=0, sticky='w', pady=10)
password_entry = ttk.Entry(main_frame, textvariable=password, width=30, show="*")
password_entry.grid(row=2, column=1, pady=10)

# --- BUTTONS ---
login_button = ttk.Button(main_frame, text="Login", command=login)
login_button.grid(row=3, column=1, sticky='e', pady=20, padx=5)

register_button = ttk.Button(main_frame, text="Create Account", command=registration)
register_button.grid(row=3, column=0, sticky='w', pady=20, padx=5)

forget_button = ttk.Button(main_frame, text="Forgot Password?", command=forgot_password)
forget_button.grid(row=4, column=0, columnspan=2, pady=5)

# --- FOOTER ---
footer_label = ttk.Label(root, text="© 2025 Precision Agriculture Team", background="#f5f5f5", font=("Segoe UI", 10))
footer_label.pack(side='bottom', pady=10)

root.mainloop()
