import tkinter as tk
from tkinter import messagebox

# Function to calculate BMI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Input Error",
                "Weight and height must be positive numbers."
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

        result_label.config(
            text=f"Your BMI: {bmi:.2f}\nCategory: {category}",
            fg=color
        )

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numbers."
        )


# Create the main window
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x350")
root.resizable(False, False)

# Heading
heading = tk.Label(
    root,
    text="BMI CALCULATOR",
    font=("Arial", 20, "bold")
)
heading.pack(pady=20)

# Weight input
tk.Label(root, text="Weight (kg):").pack()
weight_entry = tk.Entry(root)
weight_entry.pack(pady=5)

# Height input
tk.Label(root, text="Height (meters):").pack()
height_entry = tk.Entry(root)
height_entry.pack(pady=5)

# Calculate button
calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    bg="lightblue",
    font=("Arial", 12)
)
calculate_button.pack(pady=15)

# Result
result_label = tk.Label(
    root,
    text="Enter your details",
    font=("Arial", 12, "bold")
)
result_label.pack(pady=10)

# Run the application
root.mainloop()