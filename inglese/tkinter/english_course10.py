import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3
import hashlib
from datetime import datetime
import asyncio
import threading
import edge_tts
import io
import pygame

# ===================================================================================
# 1. APP CONFIGURATION & INITIALIZATION
# ===================================================================================

# --- Pygame Mixer Initialization ---
pygame.mixer.init()

# --- Customtkinter Theme ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- TTS Configuration ---
VOICE = "en-US-JennyNeural"

# ===================================================================================
# 2. CORE MODULES (TTS & DATABASE)
# ===================================================================================

async def async_speak_generator(text: str, audio_buffer: io.BytesIO):
    """
    Asynchronously generates speech using edge_tts and writes the audio
    data to an in-memory buffer.
    """
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
    except Exception as e:
        print(f"Error during TTS generation: {e}")

def speak(text_to_speak: str):
    """
    Handles TTS by generating audio into a buffer and playing it with pygame.mixer.
    Runs in a separate thread to keep the GUI responsive.
    """
    text_to_speak = text_to_speak.replace("_______", "blank")

    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        audio_buffer = io.BytesIO()
        
        try:
            loop.run_until_complete(async_speak_generator(text_to_speak, audio_buffer))
            audio_buffer.seek(0)
            
            if audio_buffer.getbuffer().nbytes > 0:
                pygame.mixer.music.load(audio_buffer)
                pygame.mixer.music.play()
        except Exception as e:
            print(f"An error occurred in the speech thread: {e}")
        finally:
            loop.close()

    thread = threading.Thread(target=run_in_thread)
    thread.daemon = True
    thread.start()

class Database:
    """Handles all database operations for users and progress."""
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
        return result and result[0] == self.hash_password(password)

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
        average_score = sum((r[1] / r[2]) * 100 for r in records) / total_tests
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

    def get_leaderboard_data(self):
        self.cursor.execute('''
            SELECT
                username,
                AVG(CAST(score AS REAL) / total_questions) * 100 AS average_score
            FROM progress
            GROUP BY username
            ORDER BY average_score DESC
        ''')
        return self.cursor.fetchall()

db = Database()

# ===================================================================================
# 3. LESSON DATA
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
    'present_perfect': {
        'title': "Present Perfect", 'course': 'Perfect Tenses', 'subtitle': "Experience and Results",
        'rules': "Used for experiences and results that connect to now. Form: have/has + past participle.",
        'questions': ["I _______ (visit) Paris three times.", "She _______ (not, finish) her project yet.", "_______ (you, ever, see) a whale?", "We _______ (live) here for five years.", "He _______ (already, eat) lunch."],
        'answers': ['have visited', "hasn't finished", 'Have you ever seen', 'have lived', 'has already eaten']
    },
    'gerunds_infinitives': {
        'title': "Gerunds and Infinitives", 'course': 'Advanced Grammar', 'subtitle': "Verb Forms as Nouns",
        'rules': "Gerunds (verb-ing) and infinitives (to + verb) can act as nouns.",
        'questions': ["I enjoy _______ (read) books.", "She decided _______ (study) medicine.", "They finished _______ (work) at 6 PM.", "He wants _______ (learn) Spanish.", "We avoid _______ (drive) in heavy traffic."],
        'answers': ['reading', 'to study', 'working', 'to learn', 'driving']
    },
}
COURSES = {
    "All Topics": list(LESSON_DATA.keys()),
    "Present Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Present Tenses'],
    "Perfect Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Perfect Tenses'],
    "Advanced Grammar": [k for k, v in LESSON_DATA.items() if v['course'] == 'Advanced Grammar'],
}

# ===================================================================================
# 4. GUI COMPONENTS
# ===================================================================================

class ResultsPopup(ctk.CTkToplevel):
    """A custom pop-up window to display exercise results and solutions."""
    def __init__(self, parent, score, total, lesson_data, on_close_callback=None):
        super().__init__(parent)
        self.title("Results")
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()

        self.lesson_data = lesson_data
        self.solutions_visible = False
        self.on_close_callback = on_close_callback
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        result_text = f"You scored {score}/{total}!"
        emoji = "🎉" if score == total else "👍" if score >= total / 2 else "🤔"
        ctk.CTkLabel(self.main_frame, text=f"{emoji} {result_text}", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)
        self.solutions_btn = ctk.CTkButton(self.button_frame, text="Show Solutions", command=self.toggle_solutions)
        self.solutions_btn.pack(side="left", padx=10)
        ctk.CTkButton(self.button_frame, text="Close", command=self.close_window).pack(side="left", padx=10)

        self.solutions_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Correct Answers")

    def close_window(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def toggle_solutions(self):
        if not self.solutions_visible:
            self.populate_solutions()
            self.solutions_frame.pack(fill="both", expand=True, pady=(10, 0))
            self.solutions_btn.configure(text="Hide Solutions")
            self.solutions_visible = True
        else:
            self.solutions_frame.pack_forget()
            self.solutions_btn.configure(text="Show Solutions")
            self.solutions_visible = False

    def populate_solutions(self):
        for widget in self.solutions_frame.winfo_children():
            widget.destroy()

        questions = self.lesson_data['questions']
        answers = self.lesson_data['answers']

        for i, answer in enumerate(answers):
            q_text = questions[i]
            parts = q_text.split("_______")
            
            solution_line = ctk.CTkFrame(self.solutions_frame, fg_color="transparent")
            solution_line.pack(fill="x", pady=4)
            
            ctk.CTkLabel(solution_line, text=f"{i+1}. {parts[0]}", anchor="w").pack(side="left")
            ctk.CTkLabel(solution_line, text=answer, text_color="#5DADE2", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)
            if len(parts) > 1:
                ctk.CTkLabel(solution_line, text=parts[1], anchor="w").pack(side="left")

class PracticeModule(ctk.CTkToplevel):
    """A standalone window for practicing a single lesson."""
    def __init__(self, parent, lesson_key, username):
        super().__init__(parent)
        self.username = username
        self.lesson_key = lesson_key
        
        self.title(f"Practice Mode")
        self.geometry("800x600")
        self.transient(parent)
        self.grab_set()

        self.entries = []
        self.display_lesson(lesson_key)

    def display_lesson(self, lesson_key):
        self.lesson_data = LESSON_DATA[lesson_key]
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text=self.lesson_data['title'], font=ctk.CTkFont(size=22, weight="bold")).pack()
        ctk.CTkLabel(main_frame, text=self.lesson_data['subtitle'], font=ctk.CTkFont(size=14), text_color="gray").pack(pady=(0, 10))

        rule_box = ctk.CTkFrame(main_frame, border_width=1)
        rule_box.pack(fill="x", pady=10)
        ctk.CTkLabel(rule_box, text="📜 Grammar Rules", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        ctk.CTkLabel(rule_box, text=self.lesson_data['rules'], wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(0, 10))
        
        exercise_frame = ctk.CTkScrollableFrame(main_frame, label_text="Exercises")
        exercise_frame.pack(fill="both", expand=True, pady=10)

        if 'word_bank' in self.lesson_data:
            ctk.CTkLabel(exercise_frame, text=f"Word Bank: {self.lesson_data['word_bank']}", font=ctk.CTkFont(slant="italic")).pack(anchor="w", padx=10, pady=5)

        for i, q_text in enumerate(self.lesson_data['questions']):
            self.create_question_widget(exercise_frame, i, q_text)

        self.check_btn = ctk.CTkButton(main_frame, text="Check Answers", command=self.check_answers, height=40)
        self.check_btn.pack(pady=10)
        
    def create_question_widget(self, parent, index, q_text):
        q_frame = ctk.CTkFrame(parent, fg_color="transparent")
        q_frame.pack(fill="x", pady=8, padx=10)
        
        parts = q_text.split("_______")
        
        hear_btn = ctk.CTkButton(q_frame, text="🔊", command=lambda t=q_text: speak(t), width=30)
        hear_btn.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(q_frame, text=f"{index+1}. {parts[0]}").pack(side="left")
        entry = ctk.CTkEntry(q_frame, width=150, font=ctk.CTkFont(size=14))
        entry.pack(side="left", padx=5)
        self.entries.append(entry)
        if len(parts) > 1:
            ctk.CTkLabel(q_frame, text=parts[1]).pack(side="left")

    def check_answers(self):
        correct_count = 0
        total_questions = len(self.entries)
        
        for i, entry in enumerate(self.entries):
            user_answer = entry.get().strip().lower()
            correct_answer = self.lesson_data['answers'][i].lower()
            
            if user_answer == correct_answer:
                correct_count += 1
                entry.configure(border_color="green")
            else:
                entry.configure(border_color="red")
            entry.configure(state="disabled")

        db.record_progress(self.username, self.lesson_key, correct_count, total_questions)
        self.check_btn.configure(state="disabled")
        
        ResultsPopup(self, correct_count, total_questions, self.lesson_data)


class CourseViewer(ctk.CTkToplevel):
    """A window for progressing through a sequence of lessons."""
    def __init__(self, parent, course_name, lesson_keys, username):
        super().__init__(parent)
        self.username = username
        self.lesson_keys = lesson_keys
        self.current_lesson_index = 0

        self.title(f"Course: {course_name}")
        self.geometry("800x650")
        self.transient(parent)
        self.grab_set()

        # Main frame to hold lesson content, gets cleared and rebuilt
        self.lesson_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lesson_content_frame.pack(fill="both", expand=True)

        # Navigation frame at the bottom
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", padx=20, pady=10)
        self.prev_btn = ctk.CTkButton(nav_frame, text="Previous Lesson", command=self.prev_lesson)
        self.prev_btn.pack(side="left", padx=10)
        self.check_btn = ctk.CTkButton(nav_frame, text="Check Answers", command=self.check_answers, height=40)
        self.check_btn.pack(side="left", expand=True, padx=10)
        self.next_btn = ctk.CTkButton(nav_frame, text="Next Lesson", command=self.next_lesson)
        self.next_btn.pack(side="right", padx=10)

        self.display_lesson()

    def display_lesson(self):
        # Clear previous lesson content
        for widget in self.lesson_content_frame.winfo_children():
            widget.destroy()
        
        self.entries = []
        lesson_key = self.lesson_keys[self.current_lesson_index]
        self.current_lesson_data = LESSON_DATA[lesson_key]

        # Create widgets for the current lesson
        main_frame = ctk.CTkFrame(self.lesson_content_frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text=self.current_lesson_data['title'], font=ctk.CTkFont(size=22, weight="bold")).pack()
        ctk.CTkLabel(main_frame, text=f"Lesson {self.current_lesson_index + 1} of {len(self.lesson_keys)}", font=ctk.CTkFont(size=14), text_color="gray").pack()

        rule_box = ctk.CTkFrame(main_frame, border_width=1)
        rule_box.pack(fill="x", pady=10)
        ctk.CTkLabel(rule_box, text="📜 Grammar Rules", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        ctk.CTkLabel(rule_box, text=self.current_lesson_data['rules'], wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(0, 10))
        
        exercise_frame = ctk.CTkScrollableFrame(main_frame, label_text="Exercises")
        exercise_frame.pack(fill="both", expand=True, pady=10)

        for i, q_text in enumerate(self.current_lesson_data['questions']):
            self.create_question_widget(exercise_frame, i, q_text)

        self.update_nav_buttons()

    def create_question_widget(self, parent, index, q_text):
        q_frame = ctk.CTkFrame(parent, fg_color="transparent")
        q_frame.pack(fill="x", pady=8, padx=10)
        parts = q_text.split("_______")
        hear_btn = ctk.CTkButton(q_frame, text="🔊", command=lambda t=q_text: speak(t), width=30)
        hear_btn.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(q_frame, text=f"{index+1}. {parts[0]}").pack(side="left")
        entry = ctk.CTkEntry(q_frame, width=150, font=ctk.CTkFont(size=14))
        entry.pack(side="left", padx=5)
        self.entries.append(entry)
        if len(parts) > 1:
            ctk.CTkLabel(q_frame, text=parts[1]).pack(side="left")

    def check_answers(self):
        correct_count = 0
        total_questions = len(self.entries)
        lesson_key = self.lesson_keys[self.current_lesson_index]
        
        for i, entry in enumerate(self.entries):
            user_answer = entry.get().strip().lower()
            correct_answer = self.current_lesson_data['answers'][i].lower()
            if user_answer == correct_answer:
                correct_count += 1
                entry.configure(border_color="green")
            else:
                entry.configure(border_color="red")
            entry.configure(state="disabled")

        db.record_progress(self.username, lesson_key, correct_count, total_questions)
        self.check_btn.configure(state="disabled")
        
        ResultsPopup(self, correct_count, total_questions, self.current_lesson_data, on_close_callback=self.update_nav_buttons)

    def next_lesson(self):
        if self.current_lesson_index < len(self.lesson_keys) - 1:
            self.current_lesson_index += 1
            self.display_lesson()

    def prev_lesson(self):
        if self.current_lesson_index > 0:
            self.current_lesson_index -= 1
            self.display_lesson()

    def update_nav_buttons(self):
        # Enable/disable Previous button
        if self.current_lesson_index == 0:
            self.prev_btn.configure(state="disabled")
        else:
            self.prev_btn.configure(state="normal")

        # Enable/disable Next button
        if self.current_lesson_index == len(self.lesson_keys) - 1:
            self.next_btn.configure(text="Finish Course", command=self.destroy)
        else:
            self.next_btn.configure(text="Next Lesson", command=self.next_lesson)
        
        # Next button is only available after checking answers
        if self.check_btn.cget("state") == "disabled":
             self.next_btn.configure(state="normal")
        else:
             self.next_btn.configure(state="disabled")
        
        # Re-enable check button for new lesson
        self.check_btn.configure(state="normal")


class AnalyticsWindow(ctk.CTkToplevel):
    """A window to display user progress and the leaderboard."""
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username
        self.title("Analytics Dashboard")
        self.geometry("800x600")
        self.transient(parent)
        self.grab_set()

        tab_view = ctk.CTkTabview(self)
        tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.progress_tab = tab_view.add("My Progress")
        self.leaderboard_tab = tab_view.add("Leaderboard")
        
        self.populate_progress_tab()
        self.populate_leaderboard_tab()

    def populate_progress_tab(self):
        analytics = db.get_user_analytics(self.username)
        
        header_frame = ctk.CTkFrame(self.progress_tab)
        header_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(header_frame, text=f"Total Tests Taken: {analytics['total_tests']}", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text=f"Average Score: {analytics['average_score']:.2f}%", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10)

        scroll_frame = ctk.CTkScrollableFrame(self.progress_tab, label_text="Per-Lesson Breakdown")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table Header
        header = ctk.CTkFrame(scroll_frame)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Lesson", font=ctk.CTkFont(weight="bold"), width=250).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(header, text="Attempts", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(header, text="Best Score", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkLabel(header, text="Average Score", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5, pady=5)
        header.grid_columnconfigure((0,1,2,3), weight=1)

        for key, data in sorted(analytics['lesson_stats'].items()):
            row = ctk.CTkFrame(scroll_frame, fg_color=("gray81", "gray20"))
            row.pack(fill="x", pady=2, padx=2)
            title = LESSON_DATA[key]['title']
            ctk.CTkLabel(row, text=title, width=250).grid(row=0, column=0, padx=5, pady=5)
            ctk.CTkLabel(row, text=data['attempts']).grid(row=0, column=1, padx=5, pady=5)
            ctk.CTkLabel(row, text=f"{data['best_score']:.2f}%").grid(row=0, column=2, padx=5, pady=5)
            ctk.CTkLabel(row, text=f"{data['average_score']:.2f}%").grid(row=0, column=3, padx=5, pady=5)
            row.grid_columnconfigure((0,1,2,3), weight=1)

    def populate_leaderboard_tab(self):
        scroll_frame = ctk.CTkScrollableFrame(self.leaderboard_tab, label_text="Top Learners")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header = ctk.CTkFrame(scroll_frame)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Rank", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0)
        ctk.CTkLabel(header, text="User", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1)
        ctk.CTkLabel(header, text="Average Score", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2)
        header.grid_columnconfigure((0,1,2), weight=1)
        
        leaderboard_data = db.get_leaderboard_data()
        for i, (user, avg_score) in enumerate(leaderboard_data, 1):
            row = ctk.CTkFrame(scroll_frame, fg_color=("gray81", "gray20"))
            row.pack(fill="x", pady=2, padx=2)
            rank_emoji = ""
            if i == 1: rank_emoji = "🥇 "
            elif i == 2: rank_emoji = "🥈 "
            elif i == 3: rank_emoji = "🥉 "
            ctk.CTkLabel(row, text=f"{rank_emoji}{i}").grid(row=0, column=0)
            ctk.CTkLabel(row, text=user).grid(row=0, column=1)
            ctk.CTkLabel(row, text=f"{avg_score:.2f}%").grid(row=0, column=2)
            row.grid_columnconfigure((0,1,2), weight=1)


class LoginWindow(ctk.CTkToplevel):
    """Modal window for user login and registration."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login")
        self.geometry("400x350")
        self.transient(parent)
        self.grab_set()
        
        self.username = None
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(main_frame, text="Welcome!", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
        
        self.user_entry = ctk.CTkEntry(main_frame, placeholder_text="Username", width=250, height=35)
        self.user_entry.pack(pady=10)
        
        self.pass_entry = ctk.CTkEntry(main_frame, placeholder_text="Password", show="*", width=250, height=35)
        self.pass_entry.pack(pady=10)
        
        self.error_label = ctk.CTkLabel(main_frame, text="", text_color="red")
        self.error_label.pack()
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Login", command=self.login, width=120, height=35).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Register", command=self.register, fg_color="#5A5A5A", hover_color="#6E6E6E", width=120, height=35).pack(side="left", padx=5)

    def login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if db.verify_user(username, password):
            self.username = username
            self.destroy()
        else:
            self.error_label.configure(text="Invalid username or password.")

    def register(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        success, message = db.create_user(username, password)
        if success:
            self.error_label.configure(text=message, text_color="green")
        else:
            self.error_label.configure(text=message, text_color="red")


class EnglishLearningApp(ctk.CTk):
    """The main application window."""
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"English Learning Hub - Welcome, {username}!")
        self.geometry("900x700")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header_frame, text="English Learning Hub", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")
        ctk.CTkButton(header_frame, text="🏆 Analytics", command=self.show_analytics).pack(side="right")
        
        tab_view = ctk.CTkTabview(main_frame)
        tab_view.pack(fill="both", expand=True)
        
        self.course_tab = tab_view.add("📚 Courses")
        self.practice_tab = tab_view.add("✍️ Practice All Topics")
        
        self.populate_course_tab()
        self.populate_practice_tab()

    def populate_course_tab(self):
        ctk.CTkLabel(self.course_tab, text="Select a course to begin a guided lesson series.", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(self.course_tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for course_name, lesson_keys in COURSES.items():
            if course_name == "All Topics": continue
            
            course_frame = ctk.CTkFrame(scroll_frame, border_width=1)
            course_frame.pack(fill="x", pady=8, padx=5)
            
            ctk.CTkLabel(course_frame, text=course_name, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10,0))
            ctk.CTkLabel(course_frame, text=f"{len(lesson_keys)} lessons", text_color="gray").pack(anchor="w", padx=15)
            ctk.CTkButton(course_frame, text="Start Course", command=lambda cn=course_name, lk=lesson_keys: self.start_course(cn, lk)).pack(anchor="e", padx=15, pady=10)

    def populate_practice_tab(self):
        ctk.CTkLabel(self.practice_tab, text="Choose any topic for a quick practice session.", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(self.practice_tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for key, data in LESSON_DATA.items():
            lesson_frame = ctk.CTkFrame(scroll_frame)
            lesson_frame.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(lesson_frame, text=data['title'], font=ctk.CTkFont(size=14)).pack(side="left", padx=15, pady=10)
            ctk.CTkButton(lesson_frame, text="Practice", command=lambda k=key: self.launch_practice_module(k), width=100).pack(side="right", padx=15, pady=10)

    def launch_practice_module(self, lesson_key):
        PracticeModule(self, lesson_key, self.username)
        
    def start_course(self, course_name, lesson_keys):
        if lesson_keys:
            CourseViewer(self, course_name, lesson_keys, self.username)
        else:
            # This would ideally be a custom message box
            print(f"Course '{course_name}' has no lessons.")

    def show_analytics(self):
        AnalyticsWindow(self, self.username)

# ===================================================================================
# 5. APPLICATION LAUNCH
# ===================================================================================

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()

    login = LoginWindow(root)
    root.wait_window(login)

    if login.username:
        app = EnglishLearningApp(login.username)
        app.mainloop()
    else:
        root.destroy()
