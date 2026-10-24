import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Create database and table
def create_table():
    with sqlite3.connect("bmi_records.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                weight REAL,
                height REAL,
                bmi REAL,
                category TEXT
            )
        """)

        columns = [
            row[1] for row in
            conn.execute("PRAGMA table_info(bmi_records)")
        ]

        if "record_date" not in columns:
            conn.execute("""
                ALTER TABLE bmi_records
                ADD COLUMN record_date TEXT
            """)

# Calculate BMI and save record
def calculate_bmi():
    username = name_entry.get().strip()

    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if not username:
            messagebox.showerror("Error", "Enter your name.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Error", "Weight and height must be positive."
            )
            return

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            color = "orange"
        elif bmi < 25:
            category = "Normal"
            color = "green"
        elif bmi < 30:
            category = "Overweight"
            color = "orange"
        else:
            category = "Obese"
            color = "red"

        # Save BMI in SQLite
        with sqlite3.connect("bmi_records.db") as conn:
            conn.execute("""
                INSERT INTO bmi_records
                (username, weight, height, bmi, category, record_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                username, weight, height, bmi, category,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            fg=color
        )

        messagebox.showinfo("Success", "BMI record saved!")

    except ValueError:
        messagebox.showerror(
            "Error", "Please enter valid numbers."
        )
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))

def show_history():
    try:
        with sqlite3.connect("bmi_records.db") as conn:
            records = conn.execute("""
                SELECT username, weight, height, bmi,
                       category, record_date
                FROM bmi_records
                ORDER BY id DESC
            """).fetchall()

        if not records:
            messagebox.showinfo(
                "History", "No BMI records found."
            )
            return

        history_text = "SAVED BMI RECORDS\n\n"

        for record in records:
            history_text += (
                f"Name: {record[0]}\n"
                f"Weight: {record[1]} kg\n"
                f"Height: {record[2]} m\n"
                f"BMI: {record[3]:.2f}\n"
                f"Category: {record[4]}\n"
                f"Date: {record[5] or 'Not available'}\n"
                "----------------------\n"
            )

        messagebox.showinfo("BMI History", history_text)

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))

def show_graph():
    username = name_entry.get().strip()

    if not username:
        messagebox.showerror("Error", "Enter your name first.")
        return

    try:
        with sqlite3.connect("bmi_records.db") as conn:
            records = conn.execute("""
                SELECT record_date, bmi
                FROM bmi_records
                WHERE username = ?
                ORDER BY id
            """, (username,)).fetchall()

        if not records:
            messagebox.showinfo("History", "No records found.")
            return

        dates = [
            row[0] or f"Record {i + 1}"
            for i, row in enumerate(records)
        ]
        values = [row[1] for row in records]

        plt.figure(figsize=(8, 4))
        plt.plot(dates, values, marker="o")
        plt.title(f"BMI Trend for {username}")
        plt.xlabel("Date / Record")
        plt.ylabel("BMI")
        plt.xticks(rotation=30)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))        

# Create window
create_table()

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x400")

tk.Label(
    root, text="BMI CALCULATOR",
    font=("Arial", 20, "bold")
).pack(pady=15)

tk.Label(root, text="User Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Weight (kg):").pack()
weight_entry = tk.Entry(root)
weight_entry.pack(pady=5)

tk.Label(root, text="Height (meters):").pack()
height_entry = tk.Entry(root)
height_entry.pack(pady=5)



result_label = tk.Label(
    root, text="Enter your details",
    font=("Arial", 12, "bold")
)
result_label.pack(pady=10)


# Calculate BMI button
tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi
).pack(pady=10)

# Show History button
tk.Button(
    root,
    text="Show History",
    command=show_history
).pack(pady=5)

# View BMI Graph button
tk.Button(
    root,
    text="View BMI Graph",
    command=show_graph
).pack(pady=5)

root.mainloop()