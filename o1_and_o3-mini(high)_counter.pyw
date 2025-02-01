import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

# Configuration
FILE_NAME = "usage.json"
DAILY_LIMIT = 7

def load_usage():
    """Load the usage data from a JSON file and reset if the date has changed."""
    today = datetime.today().strftime("%Y-%m-%d")
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    # If the file does not exist or the date is different, reset counters
    if data.get("date") != today:
        data = {
            "date": today,
            "o1": DAILY_LIMIT,
            "o3": DAILY_LIMIT  # For o3-mini(high)
        }
        save_usage(data)
    return data

def save_usage(data):
    """Save the current usage data to a JSON file."""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_labels():
    """Update the labels to display the remaining uses for each model."""
    label_o1.config(text=f"o1: {data['o1']} uses remaining")
    label_o3.config(text=f"o3-mini(high): {data['o3']} uses remaining")

def use_model(model_key):
    """Decrease the usage count for the given model if possible."""
    if data[model_key] > 0:
        data[model_key] -= 1
        save_usage(data)
        update_labels()
    else:
        messagebox.showwarning("Warning", f"Daily usage limit exceeded for {model_key} model!")

def check_date():
    """Check the current date periodically and reset usage if needed."""
    global data
    current_date = datetime.today().strftime("%Y-%m-%d")
    if data.get("date") != current_date:
        data = {
            "date": current_date,
            "o1": DAILY_LIMIT,
            "o3": DAILY_LIMIT,
        }
        save_usage(data)
        update_labels()
    # Check again after 60 seconds (60000 milliseconds)
    root.after(60000, check_date)

# Setup the main window
root = tk.Tk()
root.title("AI Model Usage Manager")
root.geometry("500x400")  # Increased resolution

# Load the usage data from the JSON file
data = load_usage()

# UI for o1 model
label_o1 = tk.Label(root, text=f"o1: {data['o1']} uses remaining", font=("Arial", 18))
label_o1.pack(pady=20)
button_o1 = tk.Button(root, text="Use o1", font=("Arial", 16), command=lambda: use_model("o1"))
button_o1.pack(pady=10)

# UI for o3-mini(high) model
label_o3 = tk.Label(root, text=f"o3-mini(high): {data['o3']} uses remaining", font=("Arial", 18))
label_o3.pack(pady=20)
button_o3 = tk.Button(root, text="Use o3-mini(high)", font=("Arial", 16), command=lambda: use_model("o3"))
button_o3.pack(pady=10)

# Start the periodic date check
root.after(60000, check_date)

root.mainloop()