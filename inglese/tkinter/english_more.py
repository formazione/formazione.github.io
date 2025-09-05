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
import re
from morelessons import LESSON_DATA, COURSES # <-- IMPORT LESSON DATA

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
    # Clean text for TTS
    text_to_speak = text_to_speak.replace("_______", "blank")
    text_to_speak = re.sub(r'\(.*?\)', '', text_to_speak) # Remove text in parentheses

    def run_in_thread():
        # Each thread needs its own event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        audio_buffer = io.BytesIO()
        
        try:
            loop.run_until_complete(async_speak_generator(text_to_speak, audio_buffer))
            audio_buffer.seek(0)
            
            if audio_buffer.getbuffer().nbytes > 0:
                # Ensure mixer is not busy before loading new audio
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
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
        """Creates or updates database tables."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                absolute_score INTEGER NOT NULL DEFAULT 0
            )
        ''')
        # Use ALTER TABLE to safely add the new column to existing databases
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN absolute_score INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # Column already exists, ignore the error

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
        # Initialize user with a score of 0
        self.cursor.execute("INSERT INTO users (username, password_hash, absolute_score) VALUES (?, ?, 0)", (username, password_hash))
        self.conn.commit()
        return True, "Account created successfully."

    def verify_user(self, username, password):
        self.cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result and result[0] == self.hash_password(password)

    def update_score(self, username, points_to_add):
        """Adds points to a user's absolute score."""
        self.cursor.execute("UPDATE users SET absolute_score = absolute_score + ? WHERE username = ?", (points_to_add, username))
        self.conn.commit()

    def record_progress(self, username, lesson_key, score, total_questions):
        """Records a lesson attempt and updates the user's absolute score."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO progress (username, lesson_key, score, total_questions, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, lesson_key, score, total_questions, timestamp))
        self.conn.commit()
        # Update the absolute score with the points from this lesson
        self.update_score(username, score)

    def get_user_analytics(self, username):
        """Gathers all analytics data for a specific user."""
        # Get absolute score from the users table
        self.cursor.execute("SELECT absolute_score FROM users WHERE username = ?", (username,))
        user_data = self.cursor.fetchone()
        absolute_score = user_data[0] if user_data else 0

        # Get lesson progress from the progress table
        self.cursor.execute("SELECT lesson_key, score, total_questions FROM progress WHERE username = ?", (username,))
        records = self.cursor.fetchall()
        
        if not records:
            return {'total_tests': 0, 'average_score_percent': 0, 'lesson_stats': {}, 'absolute_score': absolute_score}

        total_tests = len(records)
        average_score_percent = sum((r[1] / r[2]) * 100 for r in records) / total_tests
        
        lesson_stats = {}
        for key, score, total in records:
            if key not in lesson_stats:
                lesson_stats[key] = {'attempts': 0, 'scores': []}
            lesson_stats[key]['attempts'] += 1
            lesson_stats[key]['scores'].append(score / total)
        
        for key, data in lesson_stats.items():
            data['best_score_percent'] = max(data['scores']) * 100
            data['average_score_percent'] = (sum(data['scores']) / len(data['scores'])) * 100
            
        return {'total_tests': total_tests, 'average_score_percent': average_score_percent, 'lesson_stats': lesson_stats, 'absolute_score': absolute_score}

    def get_leaderboard_data(self):
        """Gets user data ordered by absolute score for the leaderboard."""
        self.cursor.execute('''
            SELECT username, absolute_score
            FROM users
            ORDER BY absolute_score DESC
        ''')
        return self.cursor.fetchall()

db = Database()

# ===================================================================================
# 3. LESSON & RULES DATA (NOW IMPORTED FROM morelessons.py)
# ===================================================================================

RULES_DATA = {
    'general_grammar': {
        'title': 'Fundamental Grammar Rules',
        'rules_text': [
            "The Present Simple is used for habits, routines, and general truths.",
            "For 'he', 'she', and 'it', we add -s or -es to the verb in the Present Simple.",
            "The Present Continuous is for actions that are happening at the moment of speaking.",
            "Its structure is: Subject + am/is/are + Verb-ing.",
            "A gerund is a verb ending in -ing that functions as a noun.",
            "An infinitive is the base form of a verb, usually preceded by 'to'."
        ],
        'quiz': [
            {'question': "You use Present Simple for actions happening right now.", 'answer': False},
            {'question': "You add '-s' to verbs for 'they' in Present Simple.", 'answer': False},
            {'question': "Present Continuous uses the verb 'to be' and a verb ending in '-ing'.", 'answer': True},
            {'question': "A gerund can be the subject of a sentence.", 'answer': True}
        ]
    }
}

# ===================================================================================
# 4. GUI COMPONENTS
# ===================================================================================

class ResultsPopup(ctk.CTkToplevel):
    """A custom pop-up window to display exercise results and solutions."""
    def __init__(self, parent, score, total, lesson_data, on_close_callback=None):
        super().__init__(parent)
        self.title("Results")
        self.geometry("500x450")
        self.transient(parent)
        self.grab_set()

        self.lesson_data = lesson_data
        self.solutions_visible = False
        self.on_close_callback = on_close_callback
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        result_text = f"You scored {score}/{total}!"
        points_text = f"You earned {score} points! ✨"
        emoji = "🎉" if score == total else "👍" if score >= total / 2 else "🤔"
        ctk.CTkLabel(self.main_frame, text=f"{emoji} {result_text}", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(self.main_frame, text=points_text, font=ctk.CTkFont(size=16)).pack(pady=(0, 10))

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

        # Handle new word_bank type
        if self.lesson_data.get('type') == 'word_bank':
            answers = self.lesson_data['answers']
            solved_text = self.lesson_data['text']
            for ans in answers:
                solved_text = solved_text.replace("_______", f"**{ans}**", 1)
            
            # Display the solved text with highlighted answers
            solution_line = ctk.CTkFrame(self.solutions_frame, fg_color="transparent")
            solution_line.pack(fill="x", pady=4, anchor="w")
            
            parts = re.split(r'(\*\*.*?\*\*)', solved_text)
            current_line_frame = ctk.CTkFrame(solution_line, fg_color="transparent")
            current_line_frame.pack(fill="x", anchor="w")
            
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    label = ctk.CTkLabel(current_line_frame, text=part[2:-2], text_color="#5DADE2", font=ctk.CTkFont(weight="bold"))
                else:
                    label = ctk.CTkLabel(current_line_frame, text=part, anchor="w", wraplength=400, justify="left")
                label.pack(side="left")
            return

        # Handle existing question types
        questions = self.lesson_data['questions']
        for i, q_data in enumerate(questions):
            q_text = q_data['text']
            answer = q_data['answer']
            
            solution_line = ctk.CTkFrame(self.solutions_frame, fg_color="transparent")
            solution_line.pack(fill="x", pady=4, anchor="w")
            
            if q_data['type'] == 'fill_in':
                answer_parts = answer.split('|')
                solved_text = q_text
                for part in answer_parts:
                    solved_text = solved_text.replace("_______", f"**{part}**", 1)
                
                parts = re.split(r'(\*\*.*?\*\*)', solved_text)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        ctk.CTkLabel(solution_line, text=part[2:-2], text_color="#5DADE2", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=1)
                    else:
                        ctk.CTkLabel(solution_line, text=part, anchor="w").pack(side="left")
            
            elif q_data['type'] == 'multiple_choice':
                ctk.CTkLabel(solution_line, text=f"{i+1}. {q_text.replace('_______', '')}").pack(side="left")
                ctk.CTkLabel(solution_line, text=answer, text_color="#5DADE2", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)


class BaseExerciseWindow(ctk.CTkToplevel):
    """Base class for PracticeModule and CourseViewer to avoid code duplication."""
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username
        self.grab_set()
        self.transient(parent)
        self.question_widgets_info = []

    def create_word_bank_widget(self, parent, lesson_data):
        """Creates the special widget for word bank exercises."""
        # Display Word Bank
        word_bank_frame = ctk.CTkFrame(parent, border_width=1)
        word_bank_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(word_bank_frame, text="📖 Word Bank", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(5,0))
        words = ", ".join(lesson_data['word_bank'])
        ctk.CTkLabel(word_bank_frame, text=words, font=ctk.CTkFont(size=14, slant="italic"), wraplength=700).pack(pady=5, padx=10)
        
        # Display Text with Blanks
        text_frame = ctk.CTkFrame(parent, fg_color="transparent")
        text_frame.pack(fill="both", expand=True)

        text_with_blanks = lesson_data['text']
        parts = text_with_blanks.split("_______")
        entries = []

        # Use a Text widget for better layout control with mixed text and widgets
        text_widget = ctk.CTkTextbox(text_frame, wrap="word", fg_color="transparent", border_width=0, font=ctk.CTkFont(size=14))
        text_widget.pack(fill="both", expand=True)

        for i, part in enumerate(parts):
            text_widget.insert("end", part)
            if i < len(parts) - 1:
                entry = ctk.CTkEntry(text_widget, width=120, font=ctk.CTkFont(size=14))
                entries.append(entry)
                text_widget.window_create("end", window=entry, padx=5, pady=5)

        text_widget.configure(state="disabled") # Make the text non-editable
        self.question_widgets_info.append({'type': 'word_bank', 'widgets': entries, 'answers': lesson_data['answers']})

    def create_question_widget(self, parent, index, q_data):
        """Creates widgets for standard one-line questions."""
        q_frame = ctk.CTkFrame(parent, fg_color="transparent")
        q_frame.pack(fill="x", pady=8, padx=10)
        
        q_text = q_data['text']
        q_type = q_data.get('type', 'fill_in')
        q_answer = q_data['answer']

        hear_btn = ctk.CTkButton(q_frame, text="🔊", command=lambda t=q_text: speak(t), width=30)
        hear_btn.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(q_frame, text=f"{index+1}.").pack(side="left")

        interactive_frame = ctk.CTkFrame(q_frame, fg_color="transparent")
        interactive_frame.pack(side="left", padx=5, pady=2, fill="x", expand=True)

        if q_type == 'fill_in':
            parts = q_text.split("_______")
            entries = []
            ctk.CTkLabel(interactive_frame, text=parts[0]).pack(side="left")
            for i in range(len(parts) - 1):
                entry = ctk.CTkEntry(interactive_frame, width=150, font=ctk.CTkFont(size=14))
                entry.pack(side="left", padx=5)
                entries.append(entry)
                if len(parts) > i + 1:
                    ctk.CTkLabel(interactive_frame, text=parts[i+1]).pack(side="left")
            self.question_widgets_info.append({'type': 'fill_in', 'widgets': entries, 'answer': q_answer})
        
        elif q_type == 'multiple_choice':
            ctk.CTkLabel(interactive_frame, text=q_text.replace("_______", "")).pack(side="left")
            mc_frame = ctk.CTkFrame(interactive_frame, fg_color="transparent")
            mc_frame.pack(side="left", padx=10)
            var = tk.StringVar()
            for option in q_data['options']:
                rb = ctk.CTkRadioButton(mc_frame, text=option, variable=var, value=option)
                rb.pack(side="left", padx=5)
            self.question_widgets_info.append({'type': 'multiple_choice', 'variable': var, 'answer': q_answer, 'frame': mc_frame})

    def check_answers_logic(self):
        correct_count = 0
        for info in self.question_widgets_info:
            is_correct = False
            if info['type'] == 'fill_in':
                user_answers = [w.get().strip().lower() for w in info['widgets']]
                correct_answers = info['answer'].lower().split('|')
                if user_answers == correct_answers:
                    is_correct = True
                for widget in info['widgets']:
                    widget.configure(border_color="green" if is_correct else "red", state="disabled")

            elif info['type'] == 'multiple_choice':
                user_answer = info['variable'].get()
                if user_answer.lower() == info['answer'].lower():
                    is_correct = True
                for widget in info['frame'].winfo_children():
                    if isinstance(widget, ctk.CTkRadioButton):
                        if widget.cget('value') == info['answer']:
                            widget.configure(text_color="green")
                        widget.configure(state="disabled")
            
            elif info['type'] == 'word_bank':
                user_answers = [w.get().strip().lower() for w in info['widgets']]
                correct_answers = [a.lower() for a in info['answers']]
                # This type is all or nothing for the whole block
                if user_answers == correct_answers:
                    is_correct = True
                    correct_count += len(correct_answers) # Add points for all correct words
                # Visual feedback for each blank
                for i, widget in enumerate(info['widgets']):
                    if widget.get().strip().lower() == correct_answers[i]:
                         widget.configure(border_color="green", state="disabled")
                    else:
                         widget.configure(border_color="red", state="disabled")
                continue # Skip the single point addition below

            if is_correct:
                correct_count += 1
        
        return correct_count


class PracticeModule(BaseExerciseWindow):
    """A standalone window for practicing a single lesson."""
    def __init__(self, parent, lesson_key, username):
        super().__init__(parent, username)
        self.lesson_key = lesson_key
        
        self.title(f"Practice Mode")
        self.geometry("800x600")
        self.display_lesson(lesson_key)

    def display_lesson(self, lesson_key):
        self.lesson_data = LESSON_DATA[lesson_key]
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text=self.lesson_data['title'], font=ctk.CTkFont(size=22, weight="bold")).pack()
        ctk.CTkLabel(main_frame, text=self.lesson_data['subtitle'], font=ctk.CTkFont(size=14), text_color="gray").pack(pady=(0, 10))

        exercise_frame = ctk.CTkScrollableFrame(main_frame, label_text="✍️ Exercises")
        exercise_frame.pack(fill="both", expand=True, pady=10)

        # Check for lesson type and display accordingly
        if self.lesson_data.get('type') == 'word_bank':
            self.create_word_bank_widget(exercise_frame, self.lesson_data)
        else:
            # Display rules only for standard lessons
            rule_box = ctk.CTkFrame(main_frame, border_width=1)
            rule_box.pack(fill="x", pady=10, before=exercise_frame) # Place it before exercises
            ctk.CTkLabel(rule_box, text="📜 Grammar Rules", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
            ctk.CTkLabel(rule_box, text=self.lesson_data['rules'], wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(0, 10))

            for i, q_data in enumerate(self.lesson_data['questions']):
                self.create_question_widget(exercise_frame, i, q_data)

        self.check_btn = ctk.CTkButton(main_frame, text="Check Answers ✅", command=self.check_answers, height=40)
        self.check_btn.pack(pady=10)

    def check_answers(self):
        correct_count = self.check_answers_logic()
        
        if self.lesson_data.get('type') == 'word_bank':
            total_questions = len(self.lesson_data['answers'])
        else:
            total_questions = len(self.lesson_data['questions'])
        
        db.record_progress(self.username, self.lesson_key, correct_count, total_questions)
        self.check_btn.configure(state="disabled")
        
        ResultsPopup(self, correct_count, total_questions, self.lesson_data)


class CourseViewer(BaseExerciseWindow):
    """A window for progressing through a sequence of lessons."""
    def __init__(self, parent, course_name, lesson_keys, username):
        super().__init__(parent, username)
        self.lesson_keys = lesson_keys
        self.current_lesson_index = 0

        self.title(f"Course: {course_name}")
        self.geometry("800x650")

        self.lesson_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lesson_content_frame.pack(fill="both", expand=True)

        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", padx=20, pady=10)
        self.prev_btn = ctk.CTkButton(nav_frame, text="⬅️ Previous", command=self.prev_lesson)
        self.prev_btn.pack(side="left", padx=10)
        self.check_btn = ctk.CTkButton(nav_frame, text="Check Answers ✅", command=self.check_answers, height=40)
        self.check_btn.pack(side="left", expand=True, padx=10)
        self.next_btn = ctk.CTkButton(nav_frame, text="Next ➡️", command=self.next_lesson)
        self.next_btn.pack(side="right", padx=10)

        self.display_lesson()

    def display_lesson(self):
        for widget in self.lesson_content_frame.winfo_children():
            widget.destroy()
        
        self.question_widgets_info = []
        lesson_key = self.lesson_keys[self.current_lesson_index]
        self.current_lesson_data = LESSON_DATA[lesson_key]

        main_frame = ctk.CTkFrame(self.lesson_content_frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text=self.current_lesson_data['title'], font=ctk.CTkFont(size=22, weight="bold")).pack()
        ctk.CTkLabel(main_frame, text=f"Lesson {self.current_lesson_index + 1} of {len(self.lesson_keys)}", font=ctk.CTkFont(size=14), text_color="gray").pack()
        
        exercise_frame = ctk.CTkScrollableFrame(main_frame, label_text="✍️ Exercises")
        exercise_frame.pack(fill="both", expand=True, pady=10)

        if self.current_lesson_data.get('type') == 'word_bank':
            self.create_word_bank_widget(exercise_frame, self.current_lesson_data)
        else:
            rule_box = ctk.CTkFrame(main_frame, border_width=1)
            rule_box.pack(fill="x", pady=10, before=exercise_frame)
            ctk.CTkLabel(rule_box, text="📜 Grammar Rules", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
            ctk.CTkLabel(rule_box, text=self.current_lesson_data['rules'], wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(0, 10))
            for i, q_data in enumerate(self.current_lesson_data['questions']):
                self.create_question_widget(exercise_frame, i, q_data)

        self.update_nav_buttons()

    def check_answers(self):
        correct_count = self.check_answers_logic()
        
        if self.current_lesson_data.get('type') == 'word_bank':
            total_questions = len(self.current_lesson_data['answers'])
        else:
            total_questions = len(self.current_lesson_data['questions'])

        lesson_key = self.lesson_keys[self.current_lesson_index]
        
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
        self.prev_btn.configure(state="disabled" if self.current_lesson_index == 0 else "normal")
        
        if self.current_lesson_index == len(self.lesson_keys) - 1:
            self.next_btn.configure(text="Finish Course 🎉", command=self.destroy)
        else:
            self.next_btn.configure(text="Next ➡️", command=self.next_lesson)
        
        self.next_btn.configure(state="normal" if self.check_btn.cget("state") == "disabled" else "disabled")
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
        
        self.progress_tab = tab_view.add("📊 My Progress")
        self.leaderboard_tab = tab_view.add("🏆 Leaderboard")
        
        self.populate_progress_tab()
        self.populate_leaderboard_tab()

    def populate_progress_tab(self):
        analytics = db.get_user_analytics(self.username)
        
        header_frame = ctk.CTkFrame(self.progress_tab)
        header_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(header_frame, text=f"Total Points: {analytics['absolute_score']} ✨", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text=f"Total Tests Taken: {analytics['total_tests']}", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text=f"Average Score: {analytics['average_score_percent']:.2f}%", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)

        scroll_frame = ctk.CTkScrollableFrame(self.progress_tab, label_text="Per-Lesson Breakdown")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
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
            ctk.CTkLabel(row, text=f"{data['best_score_percent']:.2f}%").grid(row=0, column=2, padx=5, pady=5)
            ctk.CTkLabel(row, text=f"{data['average_score_percent']:.2f}%").grid(row=0, column=3, padx=5, pady=5)
            row.grid_columnconfigure((0,1,2,3), weight=1)

    def populate_leaderboard_tab(self):
        scroll_frame = ctk.CTkScrollableFrame(self.leaderboard_tab, label_text="Top Learners")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header = ctk.CTkFrame(scroll_frame)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Rank", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(header, text="User", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(header, text="Total Points", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5)
        header.grid_columnconfigure((0,1,2), weight=1)
        
        leaderboard_data = db.get_leaderboard_data()
        for i, (user, score) in enumerate(leaderboard_data, 1):
            row = ctk.CTkFrame(scroll_frame, fg_color=("gray81", "gray20"))
            row.pack(fill="x", pady=2, padx=2)
            rank_emoji = ""
            if i == 1: rank_emoji = "🥇 "
            elif i == 2: rank_emoji = "🥈 "
            elif i == 3: rank_emoji = "🥉 "
            ctk.CTkLabel(row, text=f"{rank_emoji}{i}").grid(row=0, column=0, padx=5)
            ctk.CTkLabel(row, text=user).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(row, text=f"{score} pts").grid(row=0, column=2, padx=5)
            row.grid_columnconfigure((0,1,2), weight=1)


class RulesWindow(ctk.CTkToplevel):
    """Window to display rules with TTS and a comprehension quiz."""
    def __init__(self, parent, username, rules_data):
        super().__init__(parent)
        self.username = username
        self.rules_data = rules_data
        self.quiz_vars = []
        
        self.title("Grammar Rules & Quiz")
        self.geometry("750x600")
        self.transient(parent)
        self.grab_set()

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Rules Display
        rules_frame = ctk.CTkScrollableFrame(main_frame, label_text=f"📜 {rules_data['title']}")
        rules_frame.pack(fill="both", expand=True, pady=(0, 10))

        for sentence in rules_data['rules_text']:
            line_frame = ctk.CTkFrame(rules_frame, fg_color="transparent")
            line_frame.pack(fill="x", pady=2, padx=5)
            speak_btn = ctk.CTkButton(line_frame, text="🔊", command=lambda s=sentence: speak(s), width=30)
            speak_btn.pack(side="left")
            ctk.CTkLabel(line_frame, text=sentence, wraplength=600, justify="left").pack(side="left", padx=10)

        # True/False Quiz
        quiz_frame = ctk.CTkScrollableFrame(main_frame, label_text="🧠 Rules Quiz (1 point per correct answer)")
        quiz_frame.pack(fill="both", expand=True, pady=(10, 0))

        for i, q_data in enumerate(rules_data['quiz']):
            q_frame = ctk.CTkFrame(quiz_frame)
            q_frame.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(q_frame, text=f"{i+1}. {q_data['question']}", wraplength=500, justify="left").pack(side="left", padx=10, fill="x", expand=True)
            
            var = tk.BooleanVar(self)
            self.quiz_vars.append({'var': var, 'answer': q_data['answer'], 'frame': q_frame})
            
            true_rb = ctk.CTkRadioButton(q_frame, text="True", variable=var, value=True)
            true_rb.pack(side="right", padx=10)
            false_rb = ctk.CTkRadioButton(q_frame, text="False", variable=var, value=False)
            false_rb.pack(side="right")

        self.submit_btn = ctk.CTkButton(main_frame, text="Submit Quiz & Earn Points", command=self.check_quiz, height=40)
        self.submit_btn.pack(pady=20)
        
        self.result_label = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=14))
        self.result_label.pack()

    def check_quiz(self):
        self.submit_btn.configure(state="disabled")
        score = 0
        for info in self.quiz_vars:
            var = info['var']
            correct_answer = info['answer']
            q_frame = info['frame']
            
            # Disable radio buttons after submitting
            for widget in q_frame.winfo_children():
                if isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(state="disabled")

            if var.get() == correct_answer:
                score += 1
                q_frame.configure(fg_color=("green", "#14422B")) # Show correct answer feedback
            else:
                q_frame.configure(fg_color=("red", "#421414")) # Show incorrect answer feedback
        
        if score > 0:
            db.update_score(self.username, score)

        self.result_label.configure(text=f"You answered {score}/{len(self.quiz_vars)} correctly and earned {score} points! ✨")
        
        # Add a close button after submission
        ctk.CTkButton(self, text="Close", command=self.destroy).pack(pady=10)


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
        
        ctk.CTkLabel(main_frame, text="Welcome Back!", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
        
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
        ctk.CTkLabel(header_frame, text="🚀 English Learning Hub", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")
        
        # Right-side buttons
        button_panel = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_panel.pack(side="right")
        ctk.CTkButton(button_panel, text="📜 Rules & Quiz", command=self.show_rules).pack(side="left", padx=5)
        ctk.CTkButton(button_panel, text="🏆 Analytics", command=self.show_analytics).pack(side="left", padx=5)
        
        tab_view = ctk.CTkTabview(self)
        tab_view.pack(fill="both", expand=True)
        
        self.course_tab = tab_view.add("📚 Courses")
        self.practice_tab = tab_view.add("✍️ Practice Topics")
        
        self.populate_course_tab()
        self.populate_practice_tab()

    def populate_course_tab(self):
        ctk.CTkLabel(self.course_tab, text="Select a course to begin a guided lesson series.", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(self.course_tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for course_name, lesson_keys in COURSES.items():
            if course_name == "All Topics" or not lesson_keys: continue
            
            course_frame = ctk.CTkFrame(scroll_frame, border_width=1)
            course_frame.pack(fill="x", pady=8, padx=5)
            
            ctk.CTkLabel(course_frame, text=course_name, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10,0))
            ctk.CTkLabel(course_frame, text=f"{len(lesson_keys)} lessons", text_color="gray").pack(anchor="w", padx=15)
            ctk.CTkButton(course_frame, text="Start Course 🚀", command=lambda cn=course_name, lk=lesson_keys: self.start_course(cn, lk)).pack(anchor="e", padx=15, pady=10)

    def populate_practice_tab(self):
        ctk.CTkLabel(self.practice_tab, text="Choose any topic for a quick practice session.", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(self.practice_tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for key, data in LESSON_DATA.items():
            lesson_frame = ctk.CTkFrame(scroll_frame)
            lesson_frame.pack(fill="x", pady=5, padx=5)
            
            info_frame = ctk.CTkFrame(lesson_frame, fg_color="transparent")
            info_frame.pack(side="left", padx=15, pady=10, fill="x", expand=True)
            ctk.CTkLabel(info_frame, text=data['title'], font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(info_frame, text=data['subtitle'], text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor="w")

            ctk.CTkButton(lesson_frame, text="Practice Now ✍️", command=lambda k=key: self.launch_practice_module(k), width=120).pack(side="right", padx=15, pady=10)

    def launch_practice_module(self, lesson_key):
        PracticeModule(self, lesson_key, self.username)
        
    def start_course(self, course_name, lesson_keys):
        if lesson_keys:
            CourseViewer(self, course_name, lesson_keys, self.username)
        else:
            print(f"Course '{course_name}' has no lessons.")

    def show_analytics(self):
        AnalyticsWindow(self, self.username)

    def show_rules(self):
        # For now, we only have one set of rules. This could be expanded later.
        RulesWindow(self, self.username, RULES_DATA['general_grammar'])

# ===================================================================================
# 5. APPLICATION LAUNCH
# ===================================================================================

if __name__ == "__main__":
    # Use a dummy root window to host the login modal
    root = ctk.CTk()
    root.withdraw()

    login = LoginWindow(root)
    root.wait_window(login) # Wait for the login window to close

    # If login was successful (username is set), launch the main app
    if login.username:
        app = EnglishLearningApp(login.username)
        app.mainloop()
    else:
        # If login was cancelled or failed, destroy the root window and exit
        root.destroy()
