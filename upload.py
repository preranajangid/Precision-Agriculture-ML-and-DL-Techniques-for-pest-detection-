import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from PIL import Image, ImageTk

# New Window for Uploading Image
def upload_image_window(user_id):
    upload_window = tk.Tk()
    upload_window.geometry("600x400")
    upload_window.title("Upload Image")
    upload_window.configure(background="skyblue")

    # Load the background image
    try:
        bg_image = Image.open("uploadjpg.jpg")  # Ensure upload.png is in the same directory
        bg_image = bg_image.resize((1700, 800))  # Resize to fit the window dimensions
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Background image could not be loaded: {e}")
        bg_photo = None

    # Create a label for the background image
    if bg_photo:
        bg_label = tk.Label(upload_window, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)  # Place it to cover the entire window

    def upload_image():
        # Select Image File
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg;.jpeg;*.png")])
        if not file_path:
            messagebox.showinfo("Error", "No file selected.")
            return

        try:
            # Read Image as Binary Data
            with open(file_path, 'rb') as file:
                blob_data = file.read()

            # Insert or Update the Image in Database
            conn = sqlite3.connect('resistration.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE registration SET image = ? WHERE rowid = ?", (blob_data, user_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Image uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            
            def display_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img

    # UI Components
    label = tk.Label(upload_window, text="Upload Your Image", font=("Sitka Text", 20, "bold"), bg="skyblue")
    label.pack(pady=20)

    upload_button = tk.Button(upload_window, text="Upload Image", font=("Sitka Text", 15), bg="#00b799", fg="black", command=upload_image)
    upload_button.pack(pady=20)

    upload_window.mainloop()

# For demonstration, replace '1' with the actual user ID fetched during login.
upload_image_window(1)
