
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import os
from datetime import datetime
import asyncio
import threading
import edge_tts
import platform
import time

# ===================================================================================
# 1. TTS (TEXT-TO-SPEECH) SETUP
# Added functions to convert text to speech using edge_tts and play it.
# ===================================================================================

# --- TTS Configuration ---
VOICE = "en-US-JennyNeural"
OUTPUT_FILE = "temp_english_exercise_audio.mp3"

async def async_speak_generator(text):
    """Asynchronously generates speech using edge_tts and saves it to a file."""
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(OUTPUT_FILE)
    except Exception as e:
        print(f"Error during TTS generation: {e}")

def play_audio():
    """Plays the generated audio file using a cross-platform command."""
    if not os.path.exists(OUTPUT_FILE):
        print(f"Audio file not found: {OUTPUT_FILE}")
        return
    
    system = platform.system()
    try:
        if system == "Windows":
            os.system(f'start /min "" "{OUTPUT_FILE}"')
        elif system == "Darwin":  # macOS
            os.system(f"afplay '{OUTPUT_FILE}'")
        else:  # Linux
            # Assumes 'mpg123' is installed. You can change this to another player like 'ffplay'.
            os.system(f"mpg123 -q '{OUTPUT_FILE}'")
    except Exception as e:
        print(f"Error playing audio: {e}")

def speak(text_to_speak):
    """
    Main function to handle TTS.
    It runs the async generator in a separate thread to avoid freezing the Tkinter GUI.
    """
    # Sanitize text for TTS
    text_to_speak = text_to_speak.replace("_______", "blank")

    def run_in_thread():
        # Each thread needs its own asyncio event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(async_speak_generator(text_to_speak))
            # Brief pause to ensure the file is ready before playback
            time.sleep(0.1)
            play_audio()
        finally:
            loop.close()

    # Start the TTS generation and playback in a daemon thread
    thread = threading.Thread(target=run_in_thread)
    thread.daemon = True
    thread.start()

# ===================================================================================
# 2. DATABASE SETUP
# (No changes from original)
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
        if not username or not password: return False, "Username and password cannot be empty."
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if self.cursor.fetchone(): return False, "Username already exists."
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
        if not records: return {'total_tests': 0, 'average_score': 0, 'lesson_stats': {}}
        total_tests = len(records)
        average_score = sum((r[1] / r[2]) * 100 for r in records) / total_tests
        lesson_stats = {}
        for key, score, total in records:
            if key not in lesson_stats: lesson_stats[key] = {'attempts': 0, 'scores': []}
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
# 3. LESSON DATA AND COURSES
# (No changes from original)
# ===================================================================================
LESSON_DATA = {
    # Existing lessons
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
    },
    'present_perfect': {
        'title': "Present Perfect", 'course': 'Perfect Tenses', 'subtitle': "Experience and Results",
        'rules': "Used for experiences and results that connect to now. Form: have/has + past participle.",
        'questions': ["I _______ (visit) Paris three times.", "She _______ (not, finish) her project yet.", "_______ (you, ever, see) a whale?", "We _______ (live) here for five years.", "He _______ (already, eat) lunch."],
        'answers': ['have visited', "hasn't finished", 'Have you ever seen', 'have lived', 'has already eaten']
    },
    'present_perfect_continuous': {
        'title': "Present Perfect Continuous", 'course': 'Perfect Tenses', 'subtitle': "Duration Until Now",
        'rules': "Used for actions that started in the past and continue to now. Form: have/has + been + verb-ing.",
        'questions': ["I _______ (study) English for two years.", "She _______ (wait) for an hour.", "They _______ (not, play) tennis lately.", "How long _______ (you, work) here?", "It _______ (rain) all morning."],
        'answers': ['have been studying', 'has been waiting', "haven't been playing", 'have you been working', 'has been raining']
    },
    'past_perfect': {
        'title': "Past Perfect", 'course': 'Perfect Tenses', 'subtitle': "Earlier Past Actions",
        'rules': "Used for actions completed before another past action. Form: had + past participle.",
        'questions': ["Before I arrived, they _______ (already, leave).", "She _______ (not, see) the movie before last night.", "After he _______ (finish) work, he went home.", "_______ (you, ever, visit) Italy before 2020?", "We _______ (just, sit) down when it started raining."],
        'answers': ['had already left', "hadn't seen", 'had finished', 'Had you ever visited', 'had just sat']
    },
    'future_continuous': {
        'title': "Future Continuous", 'course': 'Future Tense', 'subtitle': "Ongoing Future Actions",
        'rules': "Used for actions in progress at a specific future time. Form: will + be + verb-ing.",
        'questions': ["At 3 PM tomorrow, I _______ (work) in the office.", "She _______ (not, sleep) when you call.", "This time next week, we _______ (fly) to Tokyo.", "What _______ (you, do) at 8 PM tonight?", "They _______ (wait) for us at the airport."],
        'answers': ['will be working', "won't be sleeping", 'will be flying', 'will you be doing', 'will be waiting']
    },
    'going_to_future': {
        'title': "Going To Future", 'course': 'Future Tense', 'subtitle': "Plans and Intentions",
        'rules': "Used for plans and intentions. Form: am/is/are + going to + base verb.",
        'questions': ["I _______ (visit) my grandmother this weekend.", "She _______ (not, buy) a new car.", "_______ (you, study) abroad next year?", "We _______ (move) to a new house.", "It looks like it _______ (rain) soon."],
        'answers': ['am going to visit', "isn't going to buy", 'Are you going to study', 'are going to move', 'is going to rain']
    },
    'modal_verbs': {
        'title': "Modal Verbs", 'course': 'General Grammar', 'subtitle': "Ability, Permission, Obligation",
        'rules': "Can, could, should, must, might, may. Used to express ability, permission, advice, obligation.",
        'questions': ["You _______ drive without a license.", "_______ I borrow your pen?", "She _______ speak three languages.", "We _______ leave early today.", "You _______ see a doctor about that cough."],
        'answers': ["can't", 'May', 'can', 'might', 'should']
    },
    'conditionals_first': {
        'title': "First Conditional", 'course': 'Conditionals', 'subtitle': "Real Future Possibilities",
        'rules': "Used for real future possibilities. Form: If + present simple, will + base verb.",
        'questions': ["If it _______ (rain), we will stay home.", "She will pass the exam if she _______ (study) hard.", "If you _______ (not, hurry), you will miss the bus.", "Will you help me if I _______ (ask) nicely?", "If they _______ (arrive) early, we'll go to the park."],
        'answers': ['rains', 'studies', "don't hurry", 'ask', 'arrive']
    },
    'conditionals_second': {
        'title': "Second Conditional", 'course': 'Conditionals', 'subtitle': "Imaginary Present Situations",
        'rules': "Used for imaginary present situations. Form: If + past simple, would + base verb.",
        'questions': ["If I _______ (be) rich, I would travel the world.", "She would be happier if she _______ (have) more friends.", "If we _______ (live) in Japan, we would learn Japanese.", "Would you buy a car if you _______ (win) the lottery?", "If it _______ (not, be) so cold, we would go swimming."],
        'answers': ['were', 'had', 'lived', 'won', "weren't"]
    },
    'passive_voice': {
        'title': "Passive Voice", 'course': 'General Grammar', 'subtitle': "Focus on Action, Not Doer",
        'rules': "Used when the action is more important than who does it. Form: be + past participle.",
        'questions': ["The cake _______ (bake) by my mother.", "English _______ (speak) all over the world.", "The house _______ (build) in 1995.", "The homework _______ (not, finish) yet.", "_______ (the letter, send) yesterday?"],
        'answers': ['was baked', 'is spoken', 'was built', "hasn't been finished", 'Was the letter sent']
    },
    'articles': {
        'title': "Articles", 'course': 'General Grammar', 'subtitle': "A, An, and The",
        'rules': "A/an for general nouns (first mention), the for specific nouns (already mentioned or unique).",
        'questions': ["I saw _______ dog in the park. _______ dog was very friendly.", "She is _______ teacher at _______ local school.", "_______ sun is shining today.", "Would you like _______ apple or _______ orange?", "He plays _______ guitar very well."],
        'answers': ['a', 'The', 'a', 'the', 'The', 'an', 'an', 'the']
    },
    'prepositions_time': {
        'title': "Prepositions of Time", 'course': 'Prepositions', 'subtitle': "At, On, In for Time",
        'rules': "At for specific times, on for days/dates, in for months/years/seasons.",
        'questions': ["I wake up _______ 7 AM.", "My birthday is _______ December.", "We have a meeting _______ Monday.", "She was born _______ 1995.", "The flowers bloom _______ spring."],
        'answers': ['at', 'in', 'on', 'in', 'in']
    },
    'prepositions_place': {
        'title': "Prepositions of Place", 'course': 'Prepositions', 'subtitle': "At, On, In for Location",
        'rules': "At for specific points, on for surfaces, in for enclosed spaces.",
        'questions': ["The book is _______ the table.", "She lives _______ New York.", "The picture is _______ the wall.", "We met _______ the bus stop.", "The cat is _______ the box."],
        'answers': ['on', 'in', 'on', 'at', 'in']
    },
    'comparatives': {
        'title': "Comparatives", 'course': 'Comparisons', 'subtitle': "Comparing Two Things",
        'rules': "Add -er for short adjectives, more for long adjectives. Use than for comparison.",
        'questions': ["My sister is _______ (tall) than me.", "This book is _______ (interesting) than that one.", "Today is _______ (cold) than yesterday.", "Learning English is _______ (easy) than I thought.", "He runs _______ (fast) than his brother."],
        'answers': ['taller', 'more interesting', 'colder', 'easier', 'faster']
    },
    'superlatives': {
        'title': "Superlatives", 'course': 'Comparisons', 'subtitle': "The Best, Worst, Most",
        'rules': "Add -est for short adjectives, most for long adjectives. Use the before superlatives.",
        'questions': ["She is _______ (smart) student in the class.", "This is _______ (expensive) restaurant in town.", "Mount Everest is _______ (high) mountain in the world.", "Yesterday was _______ (bad) day of my life.", "He is _______ (good) player on the team."],
        'answers': ['the smartest', 'the most expensive', 'the highest', 'the worst', 'the best']
    },
    'question_words': {
        'title': "Question Words", 'course': 'General Grammar', 'subtitle': "Who, What, Where, When, Why, How",
        'rules': "Use question words to ask for specific information. Word order: Question word + auxiliary + subject + main verb.",
        'questions': ["_______ is your favorite color?", "_______ do you live?", "_______ did you go to bed last night?", "_______ is that man over there?", "_______ are you learning English?"],
        'answers': ['What', 'Where', 'When', 'Who', 'Why']
    },
    'adverbs': {
        'title': "Adverbs", 'course': 'General Grammar', 'subtitle': "Describing Actions",
        'rules': "Adverbs describe verbs, adjectives, or other adverbs. Often end in -ly.",
        'questions': ["She sings very _______.", "He drives _______.", "They worked _______ on the project.", "The baby sleeps _______.", "She speaks English _______."],
        'answers': ['beautifully', 'carefully', 'hard', 'peacefully', 'fluently'],
        'word_bank': "Word Bank: beautifully, carefully, hard, peacefully, fluently, quickly, slowly"
    },
    'reported_speech': {
        'title': "Reported Speech", 'course': 'Advanced Grammar', 'subtitle': "Reporting What Others Said",
        'rules': "When reporting speech, move tenses back: present → past, past → past perfect. Change pronouns and time expressions.",
        'questions': ["'I am tired,' she said. → She said she _______ tired.", "'We will come tomorrow,' they said. → They said they _______ the next day.", "'I have finished,' he said. → He said he _______ finished.", "'I can't swim,' she said. → She said she _______ swim.", "'I saw him yesterday,' Tom said. → Tom said he _______ him the day before."],
        'answers': ['was', 'would come', 'had', "couldn't", 'had seen']
    },
    'gerunds_infinitives': {
        'title': "Gerunds and Infinitives", 'course': 'Advanced Grammar', 'subtitle': "Verb Forms as Nouns",
        'rules': "Gerunds (verb-ing) and infinitives (to + verb) can act as nouns. Some verbs take gerunds, some take infinitives.",
        'questions': ["I enjoy _______ (read) books.", "She decided _______ (study) medicine.", "They finished _______ (work) at 6 PM.", "He wants _______ (learn) Spanish.", "We avoid _______ (drive) in heavy traffic."],
        'answers': ['reading', 'to study', 'working', 'to learn', 'driving']
    },

'gerunds_infinitives_2': {
    'title': "Gerunds and Infinitives",
    'course': 'Advanced Grammar',
    'subtitle': "Verb Forms as Nouns - Practice 2",
    'rules': "Use the correct form: gerund (-ing) or infinitive (to + verb), depending on the main verb.",
    'questions': [
        "He promised _______ (call) me later.",
        "They admitted _______ (cheat) during the test.",
        "I can’t afford _______ (buy) a new car.",
        "She suggested _______ (go) for a walk.",
        "We hope _______ (visit) Japan next year.",
        "I miss _______ (travel) with my friends.",
        "They agreed _______ (meet) at 8 PM.",
        "He kept _______ (talk) even after class ended.",
        "We plan _______ (move) to Canada.",
        "She avoided _______ (answer) the question."
    ],
    'answers': [
        'to call',
        'cheating',
        'to buy',
        'going',
        'to visit',
        'traveling',
        'to meet',
        'talking',
        'to move',
        'answering'
    ]
}


}
COURSES = {
    "All Topics": list(LESSON_DATA.keys()), 
    "Present Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Present Tenses'],
    "Past Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Past Tenses'], 
    "Future Tense": [k for k, v in LESSON_DATA.items() if v['course'] == 'Future Tense'],
    "General Grammar": [k for k, v in LESSON_DATA.items() if v['course'] == 'General Grammar'],
    "Perfect Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Perfect Tenses'],
    "Conditionals": [k for k, v in LESSON_DATA.items() if v['course'] == 'Conditionals'],
    "Prepositions": [k for k, v in LESSON_DATA.items() if v['course'] == 'Prepositions'],
    "Comparisons": [k for k, v in LESSON_DATA.items() if v['course'] == 'Comparisons'],
    "Advanced Grammar": [k for k, v in LESSON_DATA.items() if v['course'] == 'Advanced Grammar'],
}
# ===================================================================================
# 4. PRACTICE MODULE
# - Added "Hear" button for each question.
# - Updated check_answers to display all correct solutions after submission.
# ===================================================================================
class PracticeModule(tk.Toplevel):
    def __init__(self, parent, lesson_key, username):
        super().__init__(parent); self.username = username; self.lesson_key = lesson_key; self.lesson_data = LESSON_DATA[lesson_key]
        self.title(f"Practice: {self.lesson_data['title']}"); self.geometry("700x600"); self.configure(bg='#f4f4f4'); self.resizable(False, False); self.grab_set()
        self.entries = []; self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#f4f4f4', padx=20, pady=20); main_frame.pack(fill='both', expand=True)
        tk.Label(main_frame, text=self.lesson_data['title'], font=('Arial', 18, 'bold'), bg='#f4f4f4', fg='#0056b3').pack(pady=(0, 5))
        tk.Label(main_frame, text=self.lesson_data['subtitle'], font=('Arial', 12), bg='#f4f4f4', fg='#555').pack(pady=(0, 15))
        rule_frame = tk.Frame(main_frame, bg='#e6f7ff', relief='solid', bd=1, padx=15, pady=10); rule_frame.pack(fill='x', pady=(0, 20))
        tk.Label(rule_frame, text="Grammar Rules", font=('Arial', 14, 'bold'), bg='#e6f7ff', fg='#0056b3').pack()
        tk.Label(rule_frame, text=self.lesson_data['rules'], font=('Arial', 12), bg='#e6f7ff', fg='#333', justify='left', wraplength=600).pack(pady=5)
        
        exercise_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=2, padx=15, pady=15); exercise_frame.pack(fill='both', expand=True)
        tk.Label(exercise_frame, text="Exercise: Complete the Sentences", font=('Arial', 14, 'bold'), bg='white', fg='#007bff').pack(pady=(0, 15))
        if 'word_bank' in self.lesson_data: tk.Label(exercise_frame, text=self.lesson_data['word_bank'], font=('Arial', 12, 'italic'), bg='white').pack()
        
        for i, q_text in enumerate(self.lesson_data['questions']):
            q_frame = tk.Frame(exercise_frame, bg='white'); q_frame.pack(fill='x', pady=6, anchor='w')
            
            # --- NEW: Hear Button ---
            hear_btn = tk.Button(q_frame, text="🔊", command=lambda text=q_text: speak(text), bd=0, bg='white', activebackground='lightgrey', font=('Arial', 14))
            hear_btn.pack(side='left', padx=(0, 5))

            tk.Label(q_frame, text=f"{i+1}. {q_text}", font=('Arial', 12), bg='white').pack(side='left')
            entry = tk.Entry(q_frame, font=('Arial', 12), width=20); entry.pack(side='left', padx=10)
            self.entries.append(entry)
            
        # Pass exercise_frame to check_answers to allow it to add the solutions
        self.check_btn = tk.Button(exercise_frame, text="Check Answers", command=lambda f=exercise_frame: self.check_answers(f), bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        self.check_btn.pack(pady=15)

    def check_answers(self, parent_frame):
        correct_count = 0; total_questions = len(self.entries)
        for i, entry in enumerate(self.entries):
            user_answer = entry.get().strip().lower(); correct_answer = self.lesson_data['answers'][i].lower()
            if user_answer == correct_answer: correct_count += 1; entry.config(fg='green', bg='#e6ffe6', state='readonly')
            else: entry.config(fg='red', bg='#ffe6e6', state='readonly')
            
        db.record_progress(self.username, self.lesson_key, correct_count, total_questions)
        self.check_btn.config(state='disabled')
        messagebox.showinfo("Score", f"You scored {correct_count}/{total_questions}.", parent=self)

        # --- NEW: Show Solutions ---
        solutions_frame = tk.Frame(parent_frame, bg='white')
        solutions_frame.pack(fill='x', pady=(20, 10))
        tk.Label(solutions_frame, text="Correct Answers:", font=('Arial', 14, 'bold'), bg='white', fg='#28a745').pack(anchor='w')
        
        for i, answer in enumerate(self.lesson_data['answers']):
            q_text = self.lesson_data['questions'][i]
            # Use a Text widget for rich text (bolding the answer)
            solution_text = tk.Text(solutions_frame, height=1, font=('Arial', 12), bg='white', relief='flat', bd=0, wrap='word')
            
            # Create a tag for bolding text
            solution_text.tag_configure("bold", font=('Arial', 12, 'bold'), foreground='#007bff')
            
            parts = q_text.split("_______")
            solution_text.insert(tk.END, f"{i+1}. {parts[0]}")
            solution_text.insert(tk.END, answer, "bold")
            if len(parts) > 1:
                solution_text.insert(tk.END, parts[1])
            
            solution_text.config(state='disabled') # Make it read-only
            solution_text.pack(anchor='w', padx=15, pady=2, fill='x')

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent); self.title("Login or Register"); self.geometry("400x300"); self.protocol("WM_DELETE_WINDOW", parent.destroy)
        self.configure(bg='#f4f4f4'); self.grab_set(); self.username = None
        tk.Label(self, text="Username:", font=('Arial', 12), bg='#f4f4f4').pack(pady=(20, 5))
        self.user_entry = tk.Entry(self, font=('Arial', 12)); self.user_entry.pack(pady=5, padx=20, fill='x')
        tk.Label(self, text="Password:", font=('Arial', 12), bg='#f4f4f4').pack(pady=(10, 5))
        self.pass_entry = tk.Entry(self, font=('Arial', 12), show="*"); self.pass_entry.pack(pady=5, padx=20, fill='x')
        btn_frame = tk.Frame(self, bg='#f4f4f4'); btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Login", command=self.login, font=('Arial', 12, 'bold'), bg='#007bff', fg='white').pack(side='left', padx=10)
        tk.Button(btn_frame, text="Register", command=self.register, font=('Arial', 12, 'bold'), bg='#28a745', fg='white').pack(side='left', padx=10)
    def login(self):
        username = self.user_entry.get(); password = self.pass_entry.get()
        if db.verify_user(username, password): self.username = username; self.destroy()
        else: messagebox.showerror("Login Failed", "Invalid username or password.", parent=self)
    def register(self):
        username = self.user_entry.get(); password = self.pass_entry.get()
        success, message = db.create_user(username, password)
        if success: messagebox.showinfo("Success", message, parent=self)
        else: messagebox.showerror("Registration Failed", message, parent=self)

# ===================================================================================
# 5. ANALYTICS WINDOW
# (No changes from original)
# ===================================================================================
class AnalyticsWindow(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.title(f"Progress Dashboard for {username}")
        self.geometry("900x700")
        self.configure(bg='#f4f4f4')
        self.grab_set()

        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, padx=10, fill="both", expand=True)

        my_progress_tab = ttk.Frame(notebook, padding=10)
        leaderboard_tab = ttk.Frame(notebook, padding=10)

        notebook.add(my_progress_tab, text='My Progress')
        notebook.add(leaderboard_tab, text='🏆 Leaderboard')

        self.populate_my_progress_tab(my_progress_tab, username)
        self.populate_leaderboard_tab(leaderboard_tab)

    def populate_my_progress_tab(self, tab, username):
        analytics = db.get_user_analytics(username)
        stats_frame = tk.Frame(tab, bg='white', relief='ridge', bd=2)
        stats_frame.pack(pady=10, fill='x')
        tk.Label(stats_frame, text="My Overall Performance", font=('Arial', 16, 'bold'), bg='white', fg='#0056b3').pack(pady=5)
        tk.Label(stats_frame, text=f"Total Tests Taken: {analytics['total_tests']}", font=('Arial', 12), bg='white').pack(pady=2)
        tk.Label(stats_frame, text=f"My Lifetime Average Score: {analytics['average_score']:.2f}%", font=('Arial', 12), bg='white').pack(pady=2)

        tk.Label(tab, text="My Per-Lesson Breakdown", font=('Arial', 16, 'bold'), fg='#0056b3').pack(pady=(20, 10))
        tree_frame = tk.Frame(tab)
        tree_frame.pack(fill='both', expand=True)
        cols = ('Lesson', 'Attempts', 'Best Score', 'Average Score')
        tree = ttk.Treeview(tree_frame, columns=cols, show='headings')
        for col in cols: tree.heading(col, text=col); tree.column(col, anchor='center', width=150)
        for key, data in sorted(analytics['lesson_stats'].items()):
            title = LESSON_DATA[key]['title']
            tree.insert("", "end", values=(title, data['attempts'], f"{data['best_score']:.2f}%", f"{data['average_score']:.2f}%"))
        tree.pack(fill='both', expand=True)

    def populate_leaderboard_tab(self, tab):
        tk.Label(tab, text="Top Learners", font=('Arial', 16, 'bold'), fg='#0056b3').pack(pady=10)
        tree_frame = tk.Frame(tab)
        tree_frame.pack(fill='both', expand=True)
        cols = ('Rank', 'User', 'Average Score')
        tree = ttk.Treeview(tree_frame, columns=cols, show='headings')
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        tree.column("Rank", width=80, anchor='center')
        tree.column("User", anchor='center')
        tree.column("Average Score", anchor='center')

        for col in cols: tree.heading(col, text=col)
        
        leaderboard_data = db.get_leaderboard_data()
        for i, (user, avg_score) in enumerate(leaderboard_data, 1):
            rank_emoji = ""
            if i == 1: rank_emoji = "🥇 "
            elif i == 2: rank_emoji = "🥈 "
            elif i == 3: rank_emoji = "🥉 "
            tree.insert("", "end", values=(f"{rank_emoji}{i}", user, f"{avg_score:.2f}%"))
        
        tree.pack(fill='both', expand=True)

# ===================================================================================
# 6. MAIN APPLICATION
# - Added "Hear" button and solution display logic, mirroring the PracticeModule.
# ===================================================================================
class EnglishLearningApp:
    def __init__(self, root, username):
        self.root = root; self.username = username; self.root.title(f"Interactive English Learning App - Welcome, {username}!")
        self.root.geometry("900x700"); self.root.configure(bg='#f4f4f4'); self.slides = []; self.current_slide_index = 0; self.current_entries = []
        self.create_widgets(); self.show_slide()
    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg='#f4f4f4'); self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.title_label = tk.Label(self.main_frame, text="Interactive English Learning", font=('Arial', 24, 'bold'), bg='#f4f4f4', fg='#0056b3'); self.title_label.pack(pady=(0, 20))
        self.content_frame = tk.Frame(self.main_frame, bg='white', relief='ridge', bd=2); self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.nav_frame = tk.Frame(self.main_frame, bg='#f4f4f4'); self.nav_frame.pack(fill='x', pady=(10, 0))
        self.prev_btn = tk.Button(self.nav_frame, text="← Previous", command=self.prev_slide, bg='#007bff', fg='white', font=('Arial', 12), padx=20, pady=5)
        self.slide_label = tk.Label(self.nav_frame, text="", font=('Arial', 12), bg='#f4f4f4', fg='#333')
        self.next_btn = tk.Button(self.nav_frame, text="Next →", command=self.next_slide, bg='#007bff', fg='white', font=('Arial', 12), padx=20, pady=5)
    def show_slide(self):
        self.current_entries = []; [widget.destroy() for widget in self.content_frame.winfo_children()]
        if not self.slides or self.current_slide_index >= len(self.slides): self.current_slide_index = 0; self.slides = ['Welcome']
        slide_key = self.slides[self.current_slide_index]; is_lesson_mode = slide_key not in ['Welcome', 'Summary']
        if is_lesson_mode:
            self.prev_btn.pack(side='left'); self.slide_label.pack(side='left', expand=True); self.next_btn.pack(side='right')
            self.slide_label.config(text=f"Lesson {self.current_slide_index}/{len(self.slides)-2}: {LESSON_DATA[slide_key]['title']}")
            self.prev_btn.config(state='normal' if self.current_slide_index > 1 else 'disabled')
            self.next_btn.config(state='normal') # Always enable next button to allow skipping
            self.show_lesson_slide(slide_key)
        else:
            self.prev_btn.pack_forget(); self.slide_label.pack_forget(); self.next_btn.pack_forget()
            if slide_key == 'Welcome': self.show_welcome_slide()
            elif slide_key == 'Summary': self.show_summary_slide()
    def show_welcome_slide(self):
        welcome_frame = tk.Frame(self.content_frame, bg='white', padx=20, pady=10); welcome_frame.pack(fill='both', expand=True)
        tk.Label(welcome_frame, text="Learning Dashboard 🚀", font=('Arial', 22, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 5))
        tk.Button(welcome_frame, text="🏆 View Progress & Leaderboard", font=('Arial', 12, 'bold'), bg='#6c757d', fg='white', command=lambda: AnalyticsWindow(self.root, self.username)).pack(pady=(5, 20))
        left_frame = tk.Frame(welcome_frame, bg='white'); left_frame.pack(side='left', fill='both', expand=True, padx=10)
        right_frame = tk.Frame(welcome_frame, bg='white'); right_frame.pack(side='right', fill='both', expand=True, padx=10)
        tk.Label(left_frame, text="1. Select a Course", font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0,5))
        self.course_listbox = tk.Listbox(left_frame, font=('Arial', 12), height=10, exportselection=False)
        for course_name in COURSES.keys(): self.course_listbox.insert(tk.END, course_name)
        self.course_listbox.pack(fill='both', expand=True); self.course_listbox.bind('<<ListboxSelect>>', self.update_practice_list)
        tk.Button(left_frame, text="Start Selected Course", font=('Arial', 12, 'bold'), bg='#007bff', fg='white', command=self.start_selected_course).pack(pady=10, fill='x')
        tk.Label(right_frame, text="2. Practice a Single Topic", font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0,5))
        tk.Label(right_frame, text="(Double-click to open)", font=('Arial', 10, 'italic'), bg='white').pack(anchor='w')
        self.practice_listbox = tk.Listbox(right_frame, font=('Arial', 12), height=10)
        self.practice_listbox.pack(fill='both', expand=True, pady=(0,10)); self.practice_listbox.bind('<Double-1>', self.launch_practice_module)
        self.course_listbox.selection_set(0); self.update_practice_list()
    def update_practice_list(self, event=None):
        selection_indices = self.course_listbox.curselection()
        if not selection_indices: return
        selected_course_name = self.course_listbox.get(selection_indices[0]); lesson_keys = COURSES[selected_course_name]
        self.practice_listbox.delete(0, tk.END); self.practice_list_keys = lesson_keys
        for key in lesson_keys: self.practice_listbox.insert(tk.END, LESSON_DATA[key]['title'])
    def start_selected_course(self):
        selection_indices = self.course_listbox.curselection()
        if not selection_indices: messagebox.showwarning("No Selection", "Please select a course to start."); return
        selected_course_name = self.course_listbox.get(selection_indices[0]); lesson_keys = COURSES[selected_course_name]
        self.slides = ['Welcome'] + lesson_keys + ['Summary']; self.current_slide_index = 1; self.show_slide()
    def launch_practice_module(self, event=None):
        selection_indices = self.practice_listbox.curselection()
        if not selection_indices: return
        lesson_key = self.practice_list_keys[selection_indices[0]]; PracticeModule(self.root, lesson_key, self.username)
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
        canvas.pack(side="left", fill="both", expand=True); scrollbar.pack(side="right", fill="y"); return scrollable_frame
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
            
            # --- NEW: Hear Button ---
            hear_btn = tk.Button(q_frame, text="🔊", command=lambda text=q_text: speak(text), bd=0, bg='white', activebackground='lightgrey', font=('Arial', 14))
            hear_btn.pack(side='left', padx=(0, 5))

            tk.Label(q_frame, text=f"{i+1}. {q_text}", font=('Arial', 12), bg='white', fg='#333').pack(side='left')
            entry = tk.Entry(q_frame, font=('Arial', 12), width=20); entry.pack(side='left', padx=(10, 0))
            self.current_entries.append(entry)
            
        # Pass both lesson_key and exercise_frame to check_answers
        self.check_btn = tk.Button(exercise_frame, text="Check Answers", command=lambda lk=lesson_key, f=exercise_frame: self.check_answers(lk, f), bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        self.check_btn.pack(pady=15)

    def check_answers(self, lesson_key, parent_frame):
        correct_answers = LESSON_DATA[lesson_key]['answers']; correct_count = 0; total_questions = len(self.current_entries)
        for i, entry in enumerate(self.current_entries):
            user_answer = entry.get().strip().lower(); correct_answer = correct_answers[i].lower()
            if user_answer == correct_answer: correct_count += 1; entry.config(fg='green', bg='#e6ffe6', state='readonly')
            else: entry.config(fg='red', bg='#ffe6e6', state='readonly')
            
        db.record_progress(self.username, lesson_key, correct_count, total_questions)
        self.check_btn.config(state='disabled')
        messagebox.showinfo("Score", f"You scored {correct_count}/{total_questions}. Progress saved.")

        # --- NEW: Show Solutions ---
        solutions_frame = tk.Frame(parent_frame, bg='white')
        solutions_frame.pack(fill='x', pady=(20, 10))
        tk.Label(solutions_frame, text="Correct Answers:", font=('Arial', 14, 'bold'), bg='white', fg='#28a745').pack(anchor='w')
        
        questions = LESSON_DATA[lesson_key]['questions']
        answers = LESSON_DATA[lesson_key]['answers']

        for i, answer in enumerate(answers):
            q_text = questions[i]
            solution_text = tk.Text(solutions_frame, height=1, font=('Arial', 12), bg='white', relief='flat', bd=0, wrap='word')
            solution_text.tag_configure("bold", font=('Arial', 12, 'bold'), foreground='#007bff')
            
            parts = q_text.split("_______")
            solution_text.insert(tk.END, f"{i+1}. {parts[0]}")
            solution_text.insert(tk.END, answer, "bold")
            if len(parts) > 1:
                solution_text.insert(tk.END, parts[1])
            
            solution_text.config(state='disabled')
            solution_text.pack(anchor='w', padx=15, pady=2, fill='x')

    def next_slide(self):
        if self.current_slide_index < len(self.slides) - 1: self.current_slide_index += 1; self.show_slide()
    def prev_slide(self):
        if self.current_slide_index > 1: self.current_slide_index -= 1; self.show_slide()
    def restart_course(self):
        self.slides = []; self.current_slide_index = 0; self.show_slide()

if __name__ == "__main__":
    root = tk.Tk(); root.withdraw()
    login_window = LoginWindow(root); root.wait_window(login_window)
    if login_window.username:
        root.deiconify()
        app = EnglishLearningApp(root, login_window.username)
        root.eval('tk::PlaceWindow . center')

        # Clean up the temp audio file when the app closes
        def on_closing():
            if os.path.exists(OUTPUT_FILE):
                os.remove(OUTPUT_FILE)
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    else: 
        root.destroy()
