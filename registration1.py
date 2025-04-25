import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import re
import random
import os

window = tk.Tk()
window.geometry("1700x1200")
window.title("REGISTRATION FORM")
window.configure(background="skyblue")

# Load and set the background image
bg_image = Image.open("pests.webp")
bg_image = bg_image.resize((1700, 1200), Image.LANCZOS)  # Resize to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Set the background image using a Label
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

Fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
Email = tk.StringVar()
Phoneno = tk.IntVar()
var = tk.IntVar()
age = tk.IntVar()
password = tk.StringVar()
password1 = tk.StringVar()

value = random.randint(1, 1000)
print(value)

# Database setup
db = sqlite3.connect('resistration.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS registration"
               "(Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT,Gender TEXT,age TEXT , password TEXT)")
db.commit()

# Password validation function
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 6:
        print('length should be at least 6')
        val = False

    if len(passwd) > 20:
        print('length should not be greater than 20')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return val

# Insert function
def insert():
    fname = Fullname.get()
    addr = address.get()
    un = username.get()
    email = Email.get()
    mobile = Phoneno.get()
    gender = var.get()
    time = age.get()
    pwd = password.get()
    cnpwd = password1.get()

    with sqlite3.connect('resistration.db') as db:
        c = db.cursor()

    find_user = ('SELECT * FROM registration WHERE username = ?')
    c.execute(find_user, [(username.get())])

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        a = True
    else:
        a = False

    if (fname.isdigit() or (fname == "")):
        ms.showinfo("Message", "please enter valid name")
    elif (addr == ""):
        ms.showinfo("Message", "Please Enter Address")
    elif (email == "") or (a == False):
        ms.showinfo("Message", "Please Enter valid email")
    elif ((len(str(mobile))) < 10 or len(str((mobile))) > 10):
        ms.showinfo("Message", "Please Enter 10 digit mobile number")
    elif ((time > 100) or (time == 0)):
        ms.showinfo("Message", "Please Enter valid age")
    elif (c.fetchall()):
        ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
    elif (pwd == ""):
        ms.showinfo("Message", "Please Enter valid password")
    elif (var == False):
        ms.showinfo("Message", "Please Enter gender")
    elif (pwd == "") or (password_check(pwd)) != True:
        ms.showinfo("Message", "Password must contain at least 1 uppercase letter, 1 symbol, and 1 number")
    elif (pwd != cnpwd):
        ms.showinfo("Message", "Password and Confirm Password must be the same")
    else:
        conn = sqlite3.connect('resistration.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO registration(Fullname, address, username, Email, Phoneno, Gender, age , password) VALUES(?,?,?,?,?,?,?,?)',
                (fname, addr, un, email, mobile, gender, time, pwd))

            conn.commit()
            db.close()
            ms.showinfo('Success!', 'Account Created Successfully !')
            from subprocess import call
            call(["python", "Login.py"])
            window.destroy()

form_frame = tk.Frame(window, bg="#fae9e1", bd=0, relief="ridge")
form_frame.place(x=820, y=120, width=650, height=600)

# Form UI
l1 = tk.Label(window, text="Join Us!!!!", font=("Sitka text", 30, "bold"), bg="#fae9e1", fg="black")
l1.place(x=1030, y=50) 

l2 = tk.Label(window, text="Full Name :", width=16, font=("Sitka text", 13,  "bold"), bg="#CDC1FF")
l2.place(x=940, y=150)
t1 = tk.Entry(window, textvar=Fullname, width=20, font=('', 15))
t1.place(x=1150, y=150)

l3 = tk.Label(window, text="Address :", width=16, font=("Sitka text", 13, "bold"), bg="#CDC1FF")
l3.place(x=940, y=200)
t2 = tk.Entry(window, textvar=address, width=20, font=('', 15))
t2.place(x=1150, y=200)

l5 = tk.Label(window, text="E-mail :",width=16, font=("Sitka text", 13,  "bold"), bg="#CDC1FF")
l5.place(x=940, y=250)
t4 = tk.Entry(window, textvar=Email, width=20, font=('', 15))
t4.place(x=1150, y=250)

l6 = tk.Label(window, text="Phone number :",width=16, font=("Sitka text", 13, "bold"), bg="#CDC1FF")
l6.place(x=940, y=300)
t5 = tk.Entry(window, textvar=Phoneno, width=20, font=('', 15))
t5.place(x=1150, y=300)

l7 = tk.Label(window, text="Gender :", width=16, font=("Sitka text", 13, "bold"), bg="#CDC1FF")
l7.place(x=940, y=350)
tk.Radiobutton(window, text="Male", padx=5, width=5, bg="snow", font=("bold", 15), variable=var, value=1).place(x=1150, y=350)
tk.Radiobutton(window, text="Female", padx=20, width=4, bg="snow", font=("bold", 15), variable=var, value=2).place(x=1260, y=350)

l8 = tk.Label(window, text="Age :",width=16, font=("Sitka text", 13,  "bold"), bg="#CDC1FF")
l8.place(x=940, y=400)
t6 = tk.Entry(window, textvar=age, width=20, font=('', 15))
t6.place(x=1150, y=400)

l4 = tk.Label(window, text="User Name :", width=16, font=("Sitka text", 13, "bold"), bg="#CDC1FF")
l4.place(x=940, y=450)
t3 = tk.Entry(window, textvar=username, width=20, font=('', 15))
t3.place(x=1150, y=450)

l9 = tk.Label(window, text="Password :", width=16, font=("Sitka text", 13, "bold"), bg="#CDC1FF")
l9.place(x=940, y=500)
t9 = tk.Entry(window, textvar=password, width=20, font=('', 15), show="*")
t9.place(x=1150, y=500)

l10 = tk.Label(window, text="Confirm Password:", width=16, font=("Sitka text", 13, "bold"), bg="#CDC1FF")
l10.place(x=940, y=550)
t10 = tk.Entry(window, textvar=password1, width=20, font=('', 15), show="*")
t10.place(x=1150, y=550)

btn = tk.Button(window, text="Register", bg="#fae9e1", font=("Sitka text", 20), fg="black", width=9, height=1, command=insert)
btn.place(x=1040, y=620)

window.mainloop()