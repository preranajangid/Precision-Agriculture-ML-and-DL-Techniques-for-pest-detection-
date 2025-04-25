import sqlite3

# Connect to the database
conn = sqlite3.connect('resistration.db')
cursor = conn.cursor()

# Alter the table to add a new column
cursor.execute("ALTER TABLE registration ADD COLUMN image BLOB")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Column 'image' added successfully.")

CREATE TABLE registration (
    rowid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    image BLOB
);
