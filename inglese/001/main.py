import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame
from datetime import datetime

LOG_FILE = "exercise_log.txt"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_exercises():
    """
    Returns a list of HTML files in the 'exercizes' directory.
    """
    exercizes_dir = resource_path("exercizes")
    if os.path.isdir(exercizes_dir):
        return [f for f in os.listdir(exercizes_dir) if f.endswith(".html")]
    return []

def update_log(exercise_name):
    """
    Updates the log file with the exercise open count and date.
    """
    log_data = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    name, count, date = parts
                    log_data[name] = {"count": int(count), "date": date}

    if exercise_name in log_data:
        log_data[exercise_name]["count"] += 1
        log_data[exercise_name]["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        log_data[exercise_name] = {"count": 1, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    with open(LOG_FILE, "w") as f:
        for name, data in log_data.items():
            f.write(f"{name},{data['count']},{data['date']}\n")

def open_exercise(event):
    """
    Opens the selected exercise in a new window and updates the log.
    """
    widget = event.widget
    selection = widget.curselection()
    if selection:
        exercise_name = widget.get(selection[0])
        exercizes_dir = resource_path("exercizes")
        filepath = os.path.join(exercizes_dir, exercise_name)

        # Create a new window to display the exercise
        exercise_window = tk.Toplevel()
        exercise_window.title(exercise_name)
        
        frame = HtmlFrame(exercise_window)
        # Use pathlib to create a proper file URI
        frame.load_file(Path(filepath).as_uri())
        frame.pack(fill="both", expand=True)

        update_log(exercise_name)

def main():
    """
    Creates the main GUI window.
    """
    root = tk.Tk()
    root.title("English exercizes")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    exercises = get_exercises()

    if not exercises:
        ttk.Label(main_frame, text="No exercises found in the 'exercizes' directory.").grid(row=0, column=0)
    else:
        listbox = tk.Listbox(main_frame, height=10, width=50)
        listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))

        for exercise in exercises:
            listbox.insert(tk.END, exercise)

        listbox.bind("<Double-1>", open_exercise)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        listbox['yscrollcommand'] = scrollbar.set

    root.mainloop()

if __name__ == "__main__":
    main()