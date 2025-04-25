import tkinter as tk
from tkinter import ttk, LEFT, END
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk

root = tk.Tk()
root.configure(background="Green")

# Set window dimensions
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}")
root.title("Login Form")

username = tk.StringVar()
password = tk.StringVar()

# Load the background image
bg_image = Image.open("loginimage.jpeg")
bg_image = bg_image.resize((w, h), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Label widget for the background image
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


def registration():
    from subprocess import call
    call(["python", "registration1.py"])
    root.destroy()


def login():
    with sqlite3.connect('resistration.db') as db:
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS registration(
                        Fullname TEXT, 
                        address TEXT, 
                        username TEXT, 
                        Email TEXT, 
                        Phoneno TEXT,
                        Gender TEXT, 
                        age TEXT, 
                        password TEXT)""")
        db.commit()

        find_entry = "SELECT * FROM registration WHERE username = ? AND password = ?"
        c.execute(find_entry, [(username.get()), (password.get())])
        result = c.fetchall()

        if result:
            ms.showinfo("Message", "Login Successfully")
            root.destroy()
            from subprocess import call
            call(['python', 'GUI_Master_plant.py'])  # Open the camera.py file on successful login
        else:
            ms.showerror('Oops!', 'Username or Password did not match.')


# UI Components
title = tk.Label(root, text="Login Here", font=("Algerian", 30, "bold", "italic"), bd=5, bg="Green", fg="black")
title.place(x=650, y=100, width=250)

Login_frame = tk.Frame(root, bg="#2e4e3e")
Login_frame.place(x=490, y=220)

# Load images for login icons
bg_icon = ImageTk.PhotoImage(Image.open("L.jpg"))
user_icon = ImageTk.PhotoImage(Image.open("l1.png"))
pass_icon = ImageTk.PhotoImage(Image.open("p1.jpg"))

logolbl = tk.Label(Login_frame, image=bg_icon, bd=0).grid(row=0, columnspan=2, pady=20)

lbluser = tk.Label(Login_frame, text="Username", image=user_icon, compound=LEFT, font=("Times new roman", 20, "bold"),
                   bg="white")
lbluser.grid(row=1, column=0, padx=20, pady=10)
txtuser = tk.Entry(Login_frame, bd=5, textvariable=username, font=("", 15))
txtuser.grid(row=1, column=1, padx=20)

lblpass = tk.Label(Login_frame, text="Password", image=pass_icon, compound=LEFT, font=("Times new roman", 20, "bold"),
                   bg="white")
lblpass.grid(row=2, column=0, padx=50, pady=10)
txtpass = tk.Entry(Login_frame, bd=5, textvariable=password, show="*", font=("", 15))
txtpass.grid(row=2, column=1, padx=20)

btn_log = tk.Button(Login_frame, text="Login", command=login, width=15, font=("Times new roman", 14, "bold"),
                    bg="Green", fg="black")
btn_log.grid(row=3, column=1, pady=10)
btn_reg = tk.Button(Login_frame, text="Create Account", command=registration, width=15,
                    font=("Times new roman", 14, "bold"), bg="red", fg="black")
btn_reg.grid(row=3, column=0, pady=10)

root.mainloop()
