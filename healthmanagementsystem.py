import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
def init_db():
    with sqlite3.connect('health_records.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS records
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      code TEXT NOT NULL UNIQUE,
                      details TEXT NOT NULL)''')
        conn.commit()

# Add a new health record
def add_record():
    name = name_entry.get().strip()
    code = code_entry.get().strip().lower()
    details = details_entry.get("1.0", tk.END).strip()
    
    if not name or not code or not details:
        messagebox.showerror("Input Error", "All fields are required!")
        return
    
    with sqlite3.connect('health_records.db') as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO records (name, code, details) VALUES (?, ?, ?)",
                      (name, code, details))
            conn.commit()
            messagebox.showinfo("Success", "Record added successfully!")
            clear_fields()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Code already exists.")

# Retrieve a health record by code
def get_record():
    code = search_entry.get().strip().lower()
    
    with sqlite3.connect('health_records.db') as conn:
        c = conn.cursor()
        c.execute("SELECT name, details FROM records WHERE code = ?", (code,))
        record = c.fetchone()
    
    if record:
        messagebox.showinfo("Record Found", f"Name: {record[0]}\nDetails: {record[1]}")
    else:
        messagebox.showerror("Not Found", "Record not found.")

# View all records
def view_all_records():
    with sqlite3.connect('health_records.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, code, details FROM records")
        records = c.fetchall()
    
    if records:
        record_text = "\n".join([f"ID: {r[0]}, Name: {r[1]}, Code: {r[2]}, Details: {r[3]}" for r in records])
        messagebox.showinfo("All Records", record_text)
    else:
        messagebox.showinfo("No Records", "No records found.")

# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    code_entry.delete(0, tk.END)
    details_entry.delete("1.0", tk.END)
    search_entry.delete(0, tk.END)

# Initialize database
init_db()

# GUI setup
root = tk.Tk()
root.title("Health Record Management System")
root.geometry("400x500")

tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Code:").pack()
code_entry = tk.Entry(root)
code_entry.pack()

tk.Label(root, text="Health Details:").pack()
details_entry = tk.Text(root, height=4, width=40)
details_entry.pack()

tk.Button(root, text="Add Record", command=add_record).pack(pady=5)

# Search Section
tk.Label(root, text="Search by Code:").pack()
search_entry = tk.Entry(root)
search_entry.pack()
tk.Button(root, text="Get Record", command=get_record).pack(pady=5)

# View All Records Button
tk.Button(root, text="View All Records", command=view_all_records).pack(pady=5)


#credits
tk.Label(root, text="Idea: Vedant Patil").pack()
tk.Label(root, text="Code: Vedant Bang").pack()

# Run the application
root.mainloop()
