import tkinter as tk
from tkinter import messagebox

class DoubleEntryApp:
    def __init__(self, master):
        self.master = master
        master.title("Double-Entry Exercise HTML Generator")

        # Data storage
        self.exercises = []
        self.current_accounts = []

        # --- Input Frames ---
        # Exercise Trace
        trace_frame = tk.Frame(master, padx=10, pady=5)
        trace_frame.pack(fill="x")
        tk.Label(trace_frame, text="Exercise Trace:", width=15, anchor="w").pack(side="left")
        self.trace_entry = tk.Entry(trace_frame)
        self.trace_entry.pack(fill="x", expand=True)

        # Account Details
        account_frame = tk.Frame(master, padx=10, pady=5)
        account_frame.pack(fill="x")
        tk.Label(account_frame, text="Account Title:", width=15, anchor="w").pack(side="left")
        self.title_entry = tk.Entry(account_frame)
        self.title_entry.pack(fill="x", expand=True)

        dare_avere_frame = tk.Frame(master, padx=10, pady=5)
        dare_avere_frame.pack(fill="x")
        tk.Label(dare_avere_frame, text="Debit (Dare):", width=15, anchor="w").pack(side="left")
        self.dare_entry = tk.Entry(dare_avere_frame)
        self.dare_entry.pack(side="left", fill="x", expand=True)
        tk.Label(dare_avere_frame, text="Credit (Avere):", width=15, anchor="e").pack(side="left")
        self.avere_entry = tk.Entry(dare_avere_frame)
        self.avere_entry.pack(side="left", fill="x", expand=True)

        # --- Buttons ---
        button_frame = tk.Frame(master, pady=10)
        button_frame.pack()
        tk.Button(button_frame, text="Add Account", command=self.add_account).pack(side="left", padx=5)
        tk.Button(button_frame, text="Add New Exercise", command=self.add_exercise).pack(side="left", padx=5)
        tk.Button(button_frame, text="Generate HTML", command=self.generate_html).pack(side="left", padx=5)

        # --- Output ---
        output_frame = tk.Frame(master, padx=10, pady=10)
        output_frame.pack(fill="both", expand=True)
        tk.Label(output_frame, text="Generated HTML:").pack(anchor="w")
        self.output_text = tk.Text(output_frame, wrap="word", height=15)
        self.output_text.pack(fill="both", expand=True)
        
    def add_account(self):
        title = self.title_entry.get()
        dare = self.dare_entry.get() or "0"
        avere = self.avere_entry.get() or "0"

        if not title:
            messagebox.showerror("Error", "Account title cannot be empty.")
            return

        self.current_accounts.append({"title": title, "dare": dare, "avere": avere})
        messagebox.showinfo("Success", f"Account '{title}' added.")
        self.title_entry.delete(0, tk.END)
        self.dare_entry.delete(0, tk.END)
        self.avere_entry.delete(0, tk.END)

    def add_exercise(self):
        trace = self.trace_entry.get()
        if not trace:
            messagebox.showerror("Error", "Exercise trace cannot be empty.")
            return
        if not self.current_accounts:
            messagebox.showerror("Error", "An exercise must have at least one account.")
            return

        self.exercises.append({"trace": trace, "accounts": self.current_accounts})
        self.current_accounts = []
        self.trace_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Exercise added.")
        
    def generate_html(self):
        if not self.exercises:
            messagebox.showerror("Error", "No exercises to generate HTML for.")
            return

        html_output = ""
        solution_string = ""
        dare_count = 1
        avere_count = 1
        js_input_string = ""

        for i, exercise in enumerate(self.exercises):
            html_output += f"<h3>Exercise {i+1}</h3>\n<p>{exercise['trace']}</p>\n"
            for account in exercise['accounts']:
                html_output += f"""<table border=1 style="width:300">
<td colspan=2><center>{account['title']}</center><tr>
<td  style="width:150">
<input type="text" id="dare{dare_count}" style="width:150" value=0></td><td style="width:150">
<input type="text" id="avere{avere_count}" style="width:150" value=0></td>
</table><br><br> """
                solution_string += f"{account['dare']} {account['avere']} | "
                js_input_string += f"dare{dare_count}.value + ' ' + avere{avere_count}.value + ' | ' + "
                dare_count += 1
                avere_count += 1

        solution_string = solution_string[:-2] + "'"
        js_input_string = js_input_string[:-6] + "|'"

        html_output += f"""<button onclick="if ({js_input_string}=='{solution_string}){{ver1.value='Correct'}}else{{ver1.value='Incorrect'}};console.log({js_input_string});console.log('{solution_string}');">Verify Answers</button><input id='ver1' type='text'>"""

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, html_output)

if __name__ == "__main__":
    root = tk.Tk()
    app = DoubleEntryApp(root)
    root.mainloop()