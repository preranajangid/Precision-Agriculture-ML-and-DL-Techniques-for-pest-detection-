import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import sqlite3
import os

# Database setup and connection
db = sqlite3.connect('resistration.db')
cursor = db.cursor()

# Creating users table if not already exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    image BLOB
)
""")
db.commit()

# Simulated login function to get the user ID (this would be replaced by your actual login mechanism)
def login(username, password):
    """Authenticate user and get their ID."""
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        return user[0]  # Return the user ID
    else:
        return None  # User not found

# Simulated login (replace with actual login mechanism)
# For example, after the user logs in, get the user ID
logged_in_user_id = login("testuser", "testpassword")  # Replace with actual login process

if logged_in_user_id:
    print(f"Logged in as user ID: {logged_in_user_id}")
else:
    print("Invalid credentials!")

def save_image_to_database(image_path):
    """Save the selected or captured image to the database for the logged-in user."""
    if logged_in_user_id is None:
        messagebox.showerror("Error", "No user logged in")
        return

    with open(image_path, 'rb') as file:
        img_blob = file.read()
    with sqlite3.connect('resistration.db') as db:
        cursor = db.cursor()
        cursor.execute("UPDATE users SET image = ? WHERE id = ?", (img_blob, logged_in_user_id))
        db.commit()
    messagebox.showinfo("Success", "Image saved to the database!")

def upload_from_storage():
    """Upload an image from storage and save it to the database."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp;*.tiff")]
    )
    if file_path:
        display_image(file_path)
        save_image_to_database(file_path)

def capture_from_camera():
    """Capture an image from the camera and save it to the database."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Unable to access the camera")
        return
    ret, frame = cap.read()
    if ret:
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        cap.release()
        display_image(image_path)
        save_image_to_database(image_path)
        os.remove(image_path)  # Remove the temporary file
    else:
        messagebox.showerror("Error", "Failed to capture image")
        cap.release()

def display_image(image_path):
    """Display the selected or captured image in the Tkinter GUI."""
    img = Image.open(image_path)
    img.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img  # Keep a reference to avoid garbage collection

# Create the main window
root = tk.Tk()
root.title("Photo Uploader")
root.geometry("500x500")

# Create buttons for uploading and capturing images
btn_upload = tk.Button(root, text="Upload from Storage", command=upload_from_storage)
btn_upload.pack(pady=10)

btn_camera = tk.Button(root, text="Capture from Camera", command=capture_from_camera)
btn_camera.pack(pady=10)

# Create a label to display the image
image_label = tk.Label(root)
image_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()