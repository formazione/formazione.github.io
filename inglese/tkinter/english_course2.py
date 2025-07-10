import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import os
from datetime import datetime

# ===================================================================================
# 1. DATABASE SETUP
# Manages users and their progress in a local SQLite database.
# ===================================================================================
class Database:
    def __init__(self, db_name="english_learning_app.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                lesson_key TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                timestamp DATETIME NOT NULL,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty."
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if self.cursor.fetchone():
            return False, "Username already exists."
        password_hash = self.hash_password(password)
        self.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        self.conn.commit()
        return True, "Account created successfully."

    def verify_user(self, username, password):
        self.cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        if result and result[0] == self.hash_password(password):
            return True
        return False

    def record_progress(self, username, lesson_key, score, total_questions):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO progress (username, lesson_key, score, total_questions, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, lesson_key, score, total_questions, timestamp))
        self.conn.commit()

    def get_user_analytics(self, username):
        self.cursor.execute("SELECT lesson_key, score, total_questions FROM progress WHERE username = ?", (username,))
        records = self.cursor.fetchall()
        
        if not records:
            return {'total_tests': 0, 'average_score': 0, 'lesson_stats': {}}

        total_tests = len(records)
        total_score_percentage = sum((r[1] / r[2]) * 100 for r in records)
        average_score = total_score_percentage / total_tests

        lesson_stats = {}
        for key, score, total in records:
            if key not in lesson_stats:
                lesson_stats[key] = {'attempts': 0, 'scores': []}
            lesson_stats[key]['attempts'] += 1
            lesson_stats[key]['scores'].append(score / total)

        for key, data in lesson_stats.items():
            data['best_score'] = max(data['scores']) * 100
            data['average_score'] = (sum(data['scores']) / len(data['scores'])) * 100
        
        return {'total_tests': total_tests, 'average_score': average_score, 'lesson_stats': lesson_stats}

# Initialize database globally
db = Database()

# ===================================================================================
# (Data dictionaries and PracticeModule remain the same as the previous version)
# ===================================================================================
LESSON_DATA = {
    'present_simple': {
        'title': "Present Simple", 'course': 'Present Tenses', 'subtitle': "Routine and Habits",
        'rules': "Used for habits and facts. Add -s/-es for he/she/it.",
        'questions': ["Maria _______ (wake up) at 7 AM.", "My parents _______ (watch) TV.", "He _______ (study) English.", "We _______ (not, eat) meat.", "_______ (you, like) pizza?"],
        'answers': ['wakes up', 'watch', 'studies', "don't eat", 'Do']
    },
    'present_continuous': {
        'title': "Present Continuous", 'course': 'Present Tenses', 'subtitle': "Actions Happening Now",
        'rules': "Used for actions happening right now. Form: am/is/are + verb-ing.",
        'questions': ["A boy _______ (eat) an apple.", "A girl _______ (run) in the park.", "Two friends _______ (talk).", "A dog _______ (sleep).", "A mother _______ (cook) dinner."],
        'answers': ['is eating', 'is running', 'are talking', 'is sleeping', 'is cooking']
    },
    'past_simple': {
        'title': "Past Simple", 'course': 'Past Tenses', 'subtitle': "Completed Actions",
        'rules': "Used for finished past actions. Add -ed or use irregular forms.",
        'questions': ["Yesterday, I _______ (visit) my aunt.", "Last summer, we _______ (go) to the beach.", "She _______ (not, finish) her homework.", "My brother _______ (play) football.", "_______ (you, see) that movie?"],
        'answers': ['visited', 'went', "didn't finish", 'played', 'Did']
    },
    'past_continuous': {
        'title': "Past Continuous", 'course': 'Past Tenses', 'subtitle': "Ongoing Past Actions",
        'rules': "Used for an action in progress at a specific past time. Form: was/were + verb-ing.",
        'questions': ["At 8 PM last night, I _______ (watch) TV.", "She _______ (read) when the phone rang.", "They _______ (not, play) football at 3 PM.", "What _______ (you, do) when I called?", "He was cooking while she _______ (work)."],
        'answers': ['was watching', 'was reading', "weren't playing", 'were you doing', 'was working']
    },
    'future_simple': {
        'title': "Future Simple", 'course': 'Future Tense', 'subtitle': "Predictions and Promises",
        'rules': "Used for predictions and promises. Form: will/won't + base verb.",
        'questions': ["I think it _______ (be) nice tomorrow.", "She _______ (travel) to Japan.", "I _______ (not, tell) anyone your secret.", "_______ (you, help) me with this?", "He _______ (win) the match."],
        'answers': ['will be', 'will travel', "won't tell", 'Will you help', 'will win']
    },
    'adjectives': {
        'title': "Adjectives", 'course': 'General Grammar', 'subtitle': "Describing Nouns",
        'rules': "Words that describe nouns. They don't change for plurals.",
        'questions': ["The sky is _______.", "The cake was _______.", "My friend is a _______ runner.", "This math problem is _______.", "My brother is very _______."],
        'answers': ['blue', 'delicious', 'fast', 'difficult', 'tall'],
        'word_bank': "Word Bank: happy, tall, blue, delicious, fast, difficult"
    }
}
COURSES = {
    "All Topics": list(LESSON_DATA.keys()), "Present Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Present Tenses'],
    "Past Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Past Tenses'], "Future Tense": [k for k, v in LESSON_DATA.items() if v['course'] == 'Future Tense'],
    "General Grammar": [k for k, v in LESSON_DATA.items() if v['course'] == 'General Grammar'],
}

class PracticeModule(tk.Toplevel):
    def __init__(self, parent, lesson_key, username):
        super().__init__(parent)
        self.username = username
        self.lesson_key = lesson_key
        self.lesson_data = LESSON_DATA[lesson_key]
        self.title(f"Practice: {self.lesson_data['title']}"); self.geometry("700x600"); self.configure(bg='#f4f4f4'); self.resizable(False, False); self.grab_set()
        self.entries = []
        self.create_widgets()
    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#f4f4f4', padx=20, pady=20); main_frame.pack(fill='both', expand=True)
        tk.Label(main_frame, text=self.lesson_data['title'], font=('Arial', 18, 'bold'), bg='#f4f4f4', fg='#0056b3').pack(pady=(0, 5))
        tk.Label(main_frame, text=self.lesson_data['subtitle'], font=('Arial', 12), bg='#f4f4f4', fg='#555').pack(pady=(0, 15))
        rule_frame = tk.Frame(main_frame, bg='#e6f7ff', relief='solid', bd=1, padx=15, pady=10); rule_frame.pack(fill='x', pady=(0, 20))
        tk.Label(rule_frame, text="Grammar Rules", font=('Arial', 14, 'bold'), bg='#e6f7ff', fg='#0056b3').pack()
        tk.Label(rule_frame, text=self.lesson_data['rules'], font=('Arial', 12), bg='#e6f7ff', fg='#333', justify='left').pack(pady=5)
        exercise_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=2, padx=15, pady=15); exercise_frame.pack(fill='both', expand=True)
        tk.Label(exercise_frame, text="Exercise: Complete the Sentences", font=('Arial', 14, 'bold'), bg='white', fg='#007bff').pack(pady=(0, 15))
        if 'word_bank' in self.lesson_data: tk.Label(exercise_frame, text=self.lesson_data['word_bank'], font=('Arial', 12, 'italic'), bg='white').pack()
        for i, q_text in enumerate(self.lesson_data['questions']):
            q_frame = tk.Frame(exercise_frame, bg='white'); q_frame.pack(fill='x', pady=6, anchor='w')
            tk.Label(q_frame, text=f"{i+1}. {q_text}", font=('Arial', 12), bg='white').pack(side='left')
            entry = tk.Entry(q_frame, font=('Arial', 12), width=20); entry.pack(side='left', padx=10)
            self.entries.append(entry)
        self.check_btn = tk.Button(exercise_frame, text="Check Answers", command=self.check_answers, bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        self.check_btn.pack(pady=15)
    def check_answers(self):
        correct_count = 0
        total_questions = len(self.entries)
        for i, entry in enumerate(self.entries):
            user_answer = entry.get().strip().lower(); correct_answer = self.lesson_data['answers'][i].lower()
            if user_answer == correct_answer: correct_count += 1; entry.config(fg='green', bg='#e6ffe6')
            else: entry.config(fg='red', bg='#ffe6e6')
        
        db.record_progress(self.username, self.lesson_key, correct_count, total_questions)
        self.check_btn.config(state='disabled')
        messagebox.showinfo("Score", f"You scored {correct_count}/{total_questions}.", parent=self)

# ===================================================================================
# 4. LOGIN AND ANALYTICS WINDOWS
# ===================================================================================
class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login or Register")
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", parent.destroy)
        self.configure(bg='#f4f4f4')
        self.grab_set()

        self.username = None

        tk.Label(self, text="Username:", font=('Arial', 12), bg='#f4f4f4').pack(pady=(20, 5))
        self.user_entry = tk.Entry(self, font=('Arial', 12))
        self.user_entry.pack(pady=5, padx=20, fill='x')
        tk.Label(self, text="Password:", font=('Arial', 12), bg='#f4f4f4').pack(pady=(10, 5))
        self.pass_entry = tk.Entry(self, font=('Arial', 12), show="*")
        self.pass_entry.pack(pady=5, padx=20, fill='x')

        btn_frame = tk.Frame(self, bg='#f4f4f4')
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Login", command=self.login, font=('Arial', 12, 'bold'), bg='#007bff', fg='white').pack(side='left', padx=10)
        tk.Button(btn_frame, text="Register", command=self.register, font=('Arial', 12, 'bold'), bg='#28a745', fg='white').pack(side='left', padx=10)

    def login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if db.verify_user(username, password):
            self.username = username
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.", parent=self)

    def register(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        success, message = db.create_user(username, password)
        if success:
            messagebox.showinfo("Success", message, parent=self)
        else:
            messagebox.showerror("Registration Failed", message, parent=self)

class AnalyticsWindow(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.title(f"Progress for {username}")
        self.geometry("800x600")
        self.configure(bg='#f4f4f4')
        self.grab_set()

        analytics = db.get_user_analytics(username)

        main_frame = tk.Frame(self, bg='#f4f4f4', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        # Overall stats
        stats_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=2)
        stats_frame.pack(pady=10, fill='x')
        tk.Label(stats_frame, text="Overall Performance", font=('Arial', 16, 'bold'), bg='white', fg='#0056b3').pack(pady=5)
        tk.Label(stats_frame, text=f"Total Tests Taken: {analytics['total_tests']}", font=('Arial', 12), bg='white').pack(pady=2)
        tk.Label(stats_frame, text=f"Lifetime Average Score: {analytics['average_score']:.2f}%", font=('Arial', 12), bg='white').pack(pady=2)

        # Detailed stats per lesson
        tk.Label(main_frame, text="Per-Lesson Breakdown", font=('Arial', 16, 'bold'), bg='#f4f4f4', fg='#0056b3').pack(pady=(20, 10))
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)
        
        cols = ('Lesson', 'Attempts', 'Best Score', 'Average Score')
        tree = ttk.Treeview(tree_frame, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=150)
        
        for key, data in sorted(analytics['lesson_stats'].items()):
            title = LESSON_DATA[key]['title']
            tree.insert("", "end", values=(title, data['attempts'], f"{data['best_score']:.2f}%", f"{data['average_score']:.2f}%"))
        
        tree.pack(fill='both', expand=True)
# ===================================================================================
# 5. MAIN APPLICATION
# ===================================================================================
class EnglishLearningApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Interactive English Learning App - Welcome, {username}!")
        self.root.geometry("900x700")
        self.root.configure(bg='#f4f4f4')
        self.slides = []
        self.current_slide_index = 0
        self.current_entries = []
        self.create_widgets()
        self.show_slide()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg='#f4f4f4'); self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.title_label = tk.Label(self.main_frame, text="Interactive English Learning", font=('Arial', 24, 'bold'), bg='#f4f4f4', fg='#0056b3'); self.title_label.pack(pady=(0, 20))
        self.content_frame = tk.Frame(self.main_frame, bg='white', relief='ridge', bd=2); self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.nav_frame = tk.Frame(self.main_frame, bg='#f4f4f4'); self.nav_frame.pack(fill='x', pady=(10, 0))
        self.prev_btn = tk.Button(self.nav_frame, text="← Previous", command=self.prev_slide, bg='#007bff', fg='white', font=('Arial', 12), padx=20, pady=5)
        self.slide_label = tk.Label(self.nav_frame, text="", font=('Arial', 12), bg='#f4f4f4', fg='#333')
        self.next_btn = tk.Button(self.nav_frame, text="Next →", command=self.next_slide, bg='#007bff', fg='white', font=('Arial', 12), padx=20, pady=5)

    def show_slide(self):
        self.current_entries = []
        for widget in self.content_frame.winfo_children(): widget.destroy()
        if not self.slides or self.current_slide_index >= len(self.slides): self.current_slide_index = 0; self.slides = ['Welcome']
        slide_key = self.slides[self.current_slide_index]
        is_lesson_mode = slide_key not in ['Welcome', 'Summary']
        if is_lesson_mode:
            self.prev_btn.pack(side='left'); self.slide_label.pack(side='left', expand=True); self.next_btn.pack(side='right')
            self.slide_label.config(text=f"Lesson {self.current_slide_index}/{len(self.slides)-2}: {LESSON_DATA[slide_key]['title']}")
            self.prev_btn.config(state='normal' if self.current_slide_index > 1 else 'disabled')
            self.next_btn.config(state='normal' if self.current_slide_index < len(self.slides) - 1 else 'disabled')
            self.show_lesson_slide(slide_key)
        else:
            self.prev_btn.pack_forget(); self.slide_label.pack_forget(); self.next_btn.pack_forget()
            if slide_key == 'Welcome': self.show_welcome_slide()
            elif slide_key == 'Summary': self.show_summary_slide()

    def show_welcome_slide(self):
        welcome_frame = tk.Frame(self.content_frame, bg='white', padx=20, pady=10); welcome_frame.pack(fill='both', expand=True)
        tk.Label(welcome_frame, text="Learning Dashboard 🚀", font=('Arial', 22, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 5))
        tk.Button(welcome_frame, text="View My Progress", font=('Arial', 12, 'bold'), bg='#6c757d', fg='white', command=lambda: AnalyticsWindow(self.root, self.username)).pack(pady=(5, 20))
        left_frame = tk.Frame(welcome_frame, bg='white'); left_frame.pack(side='left', fill='both', expand=True, padx=10)
        right_frame = tk.Frame(welcome_frame, bg='white'); right_frame.pack(side='right', fill='both', expand=True, padx=10)
        tk.Label(left_frame, text="1. Select a Course", font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0,5))
        self.course_listbox = tk.Listbox(left_frame, font=('Arial', 12), height=10, exportselection=False)
        for course_name in COURSES.keys(): self.course_listbox.insert(tk.END, course_name)
        self.course_listbox.pack(fill='both', expand=True)
        self.course_listbox.bind('<<ListboxSelect>>', self.update_practice_list)
        tk.Button(left_frame, text="Start Selected Course", font=('Arial', 12, 'bold'), bg='#007bff', fg='white', command=self.start_selected_course).pack(pady=10, fill='x')
        tk.Label(right_frame, text="2. Practice a Single Topic", font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0,5))
        tk.Label(right_frame, text="(Double-click to open)", font=('Arial', 10, 'italic'), bg='white').pack(anchor='w')
        self.practice_listbox = tk.Listbox(right_frame, font=('Arial', 12), height=10)
        self.practice_listbox.pack(fill='both', expand=True, pady=(0,10))
        self.practice_listbox.bind('<Double-1>', self.launch_practice_module)
        self.course_listbox.selection_set(0)
        self.update_practice_list()

    def update_practice_list(self, event=None):
        selection_indices = self.course_listbox.curselection()
        if not selection_indices: return
        selected_course_name = self.course_listbox.get(selection_indices[0])
        lesson_keys = COURSES[selected_course_name]
        self.practice_listbox.delete(0, tk.END)
        self.practice_list_keys = lesson_keys
        for key in lesson_keys: self.practice_listbox.insert(tk.END, LESSON_DATA[key]['title'])

    def start_selected_course(self):
        selection_indices = self.course_listbox.curselection()
        if not selection_indices: messagebox.showwarning("No Selection", "Please select a course to start."); return
        selected_course_name = self.course_listbox.get(selection_indices[0])
        lesson_keys = COURSES[selected_course_name]
        self.slides = ['Welcome'] + lesson_keys + ['Summary']
        self.current_slide_index = 1
        self.show_slide()
        
    def launch_practice_module(self, event=None):
        selection_indices = self.practice_listbox.curselection()
        if not selection_indices: return
        lesson_key = self.practice_list_keys[selection_indices[0]]
        PracticeModule(self.root, lesson_key, self.username)

    def show_lesson_slide(self, lesson_key):
        slide_frame = self.create_scrollable_frame(self.content_frame); lesson = LESSON_DATA[lesson_key]
        tk.Label(slide_frame, text=lesson['title'], font=('Arial', 18, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 0))
        tk.Label(slide_frame, text=lesson['subtitle'], font=('Arial', 12), bg='white', fg='#555').pack(pady=(0, 15))
        self.create_rule_box(slide_frame, "Grammar Rules", lesson['rules'])
        self.create_exercise_frame(slide_frame, "Exercise", lesson['questions'], lesson_key)
        
    def show_summary_slide(self):
        summary_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(summary_frame, text="🎉 Course Complete!", font=('Arial', 22, 'bold'), bg='white', fg='#0056b3').pack(pady=20)
        tk.Label(summary_frame, text="You have finished this set of lessons.", font=('Arial', 14), bg='white', fg='#333').pack(pady=20)
        tk.Button(summary_frame, text="Return to Main Menu", command=self.restart_course, bg='#dc3545', fg='white', font=('Arial', 14, 'bold'), pady=10).pack(pady=20)

    def create_scrollable_frame(self, parent):
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0); scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white'); scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw"); canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True); scrollbar.pack(side="right", fill="y")
        return scrollable_frame

    def create_rule_box(self, parent, title, content):
        rule_frame = tk.Frame(parent, bg='#e6f7ff', relief='solid', bd=1, padx=10, pady=5); rule_frame.pack(fill='x', pady=(10, 20), padx=10)
        tk.Label(rule_frame, text=title, font=('Arial', 16, 'bold'), bg='#e6f7ff', fg='#0056b3').pack(pady=5)
        tk.Label(rule_frame, text=content, font=('Arial', 12), bg='#e6f7ff', fg='#333', justify='left', wraplength=750).pack(pady=(0, 5), padx=15)

    def create_exercise_frame(self, parent, title, questions, lesson_key):
        exercise_frame = tk.Frame(parent, bg='white', relief='ridge', bd=1, padx=15, pady=10); exercise_frame.pack(fill='x', pady=20, padx=10)
        tk.Label(exercise_frame, text=title, font=('Arial', 16, 'bold'), bg='white', fg='#007bff').pack(pady=(10, 15))
        if 'word_bank' in LESSON_DATA[lesson_key]: tk.Label(exercise_frame, text=LESSON_DATA[lesson_key]['word_bank'], font=('Arial', 12, 'italic'), bg='white').pack()
        for i, q_text in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white'); q_frame.pack(fill='x', pady=5, padx=15, anchor='w')
            tk.Label(q_frame, text=f"{i+1}. {q_text}", font=('Arial', 12), bg='white', fg='#333').pack(side='left')
            entry = tk.Entry(q_frame, font=('Arial', 12), width=20); entry.pack(side='left', padx=(10, 0))
            self.current_entries.append(entry)
        self.check_btn = tk.Button(exercise_frame, text="Check Answers", command=lambda: self.check_answers(lesson_key), bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        self.check_btn.pack(pady=15)

    def check_answers(self, lesson_key):
        correct_answers = LESSON_DATA[lesson_key]['answers']; correct_count = 0
        total_questions = len(self.current_entries)
        for i, entry in enumerate(self.current_entries):
            user_answer = entry.get().strip().lower(); correct_answer = correct_answers[i].lower()
            if user_answer == correct_answer: correct_count += 1; entry.config(fg='green', bg='#e6ffe6')
            else: entry.config(fg='red', bg='#ffe6e6')
        
        db.record_progress(self.username, lesson_key, correct_count, total_questions)
        self.check_btn.config(state='disabled')
        messagebox.showinfo("Score", f"You scored {correct_count}/{total_questions}. Progress saved.")

    def next_slide(self):
        if self.current_slide_index < len(self.slides) - 1: self.current_slide_index += 1; self.show_slide()
    def prev_slide(self):
        if self.current_slide_index > 0: self.current_slide_index -= 1; self.show_slide()
    def restart_course(self):
        self.slides = []; self.current_slide_index = 0; self.show_slide()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # Hide the main window until login is successful
    
    login_window = LoginWindow(root)
    root.wait_window(login_window)

    if login_window.username:
        root.deiconify() # Show the main window
        app = EnglishLearningApp(root, login_window.username)
        root.eval('tk::PlaceWindow . center')
        root.mainloop()
    else:
        root.destroy()