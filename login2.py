def login():
    username_input = username.get()
    password_input = password.get()

    conn = sqlite3.connect('resistration.db')
    cursor = conn.cursor()

    # Fetch user details
    cursor.execute("SELECT rowid FROM registration WHERE username = ? AND password = ?", (username_input, password_input))
    result = cursor.fetchone()

    if result:
        user_id = result[0]  # Extract user ID
        ms.showinfo("Success", "Login Successful!")
        conn.close()

        # Open the upload image window
        upload_image_window(user_id)
        window.destroy()
    else:
        ms.showerror("Error", "Invalid Username or Password")
        conn.close()