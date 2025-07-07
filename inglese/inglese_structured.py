""" I have restructured the entire application to be data-driven and highly modular. This new architecture makes adding new lessons incredibly easy—you only need to add the lesson's content to a central data structure, and the application will automatically generate the corresponding slides and practice modules.

Here is the new, fully refactored code.

-----

### Key Architectural Changes

1.  **Centralized `LESSON_DATA`**:

      * All lesson content (titles, rules, questions, answers) is now stored in a single dictionary called `LESSON_DATA`.
      * **To add a new lesson, you just need to add a new entry to this dictionary.**

2.  **Generic `PracticeModule` Class**:

      * The old, specific `FutureSimpleModule` has been replaced by a single, reusable `PracticeModule` class.
      * This class is now generic and can create a practice window for *any* lesson by simply loading the relevant data from `LESSON_DATA`.

3.  **Dynamic Main Menu**:

      * The welcome screen now automatically creates a "Practice" button for every lesson defined in `LESSON_DATA`. When you add a new lesson to the data, a button for it will appear on the menu automatically.

4.  **Dynamic Slide Generation**:

      * The old, repetitive `show_present_simple_slide()`, `show_past_simple_slide()`, etc., methods have been removed.
      * They are replaced by a single, smart method, `show_lesson_slide()`, which generates the content for any lesson slide dynamically based on the `LESSON_DATA`.

To prove how easy it is, I have already added a new lesson for the **"Past Continuous"** tense to the `LESSON_DATA`. You will see it automatically appear in the app as both a slide in the full course and as a button on the main menu.

-----

### Complete, Refactored Python Code

"""
import tkinter as tk
from tkinter import ttk, messagebox

# ===================================================================================
# CENTRALIZED LESSON DATA
# To add a new lesson, simply add a new entry to this dictionary.
# The application will automatically generate the slides and practice modules.
# ===================================================================================
LESSON_DATA = {
    'present_simple': {
        'title': "Present Simple",
        'subtitle': "Routine and Habits",
        'rules': "Used for habits, facts, and regular actions.\nAdd -s/-es for he/she/it (e.g., she works).\nUse do/don't for questions/negatives (e.g., Do you...?).\nUse does/doesn't for he/she/it (e.g., Does he...?).",
        'questions': [
            "Maria _______ (wake up) at 7 AM every day.", "My parents _______ (watch) TV in the evening.",
            "He _______ (study) English at school.", "We _______ (not, eat) meat.",
            "_______ (you, like) pizza?", "The sun _______ (rise) in the east.",
            "My cat _______ (sleep) a lot.", "They _______ (not, live) in Rome."
        ],
        'answers': ['wakes up', 'watch', 'studies', "don't eat", 'Do', 'rises', 'sleeps', "don't live"]
    },
    'present_continuous': {
        'title': "Present Continuous",
        'subtitle': "Actions Happening Now",
        'rules': "Used for actions happening right now.\nForm: am/is/are + verb-ing (e.g., I am reading).",
        'questions': [
            "Un ragazzo sta mangiando una mela. ->", "Una ragazza sta correndo nel parco. ->",
            "Due amici stanno parlando. ->", "Un cane sta dormendo. ->",
            "Una mamma sta cucinando la cena. ->"
        ],
        'answers': ['He is eating an apple.', 'She is running in the park.', 'They are talking.', 'It is sleeping.', 'She is cooking dinner.']
    },
    'past_simple': {
        'title': "Past Simple",
        'subtitle': "Completed Actions",
        'rules': "Used for actions that started and finished in the past.\nRegular verbs add -ed (e.g., played).\nIrregular verbs change (e.g., go -> went).\nUse did/didn't for questions/negatives (e.g., Did you go?).",
        'questions': [
            "Yesterday, I _______ (visit) my aunt.", "Last summer, we _______ (go) to the beach.",
            "She _______ (not, finish) her homework.", "My brother _______ (play) football with his friends.",
            "_______ (you, see) that movie?", "They _______ (buy) a new car last month.",
            "He _______ (not, like) the food.", "I _______ (wake up) late this morning."
        ],
        'answers': ['visited', 'went', "didn't finish", 'played', 'Did', 'bought', "didn't like", 'woke up']
    },
    'future_simple': {
        'title': "Future Simple",
        'subtitle': "Predictions and Promises",
        'rules': "Used for predictions, spontaneous decisions, and promises.\nForm: will + base verb (e.g., I will go).\nNegative: won't + base verb (e.g., They won't come).",
        'questions': [
            "I think the weather _______ (be) nice tomorrow.", "She _______ (travel) to Japan next year.",
            "Don't worry, I _______ (not, tell) anyone your secret.", "_______ (you, help) me with this heavy box?",
            "He _______ (win) the match. He's the best player."
        ],
        'answers': ['will be', 'will travel', "won't tell", 'Will you help', 'will win']
    },
    'past_continuous': {
        'title': "Past Continuous",
        'subtitle': "Ongoing Past Actions",
        'rules': "Used for an action that was in progress at a specific time in the past.\nForm: was/were + verb-ing (e.g., I was studying).",
        'questions': [
            "At 8 PM last night, I _______ (watch) TV.",
            "She _______ (read) when the phone rang.",
            "They _______ (not, play) football at 3 PM.",
            "What _______ (you, do) when I called?",
            "He was cooking while she _______ (work)."
        ],
        'answers': ['was watching', 'was reading', "weren't playing", 'were you doing', 'was working']
    },
    'adjectives': {
        'title': "Adjectives",
        'subtitle': "Describing Nouns",
        'rules': "Adjectives describe nouns. They usually come before the noun (a big house) or after the verb 'to be' (the house is big).\nThey do not change for plural nouns (two big houses).",
        'questions': [
            "The sky is _______.", "The cake was very _______.",
            "My friend is a very _______ runner.", "He is a _______ boy because he got a new toy.",
            "This math problem is very _______.", "My brother is very _______; he can reach the top shelf."
        ],

        'answers': ['blue', 'delicious', 'fast', 'happy', 'difficult', 'tall'],
        'word_bank': "Word Bank: happy, tall, blue, delicious, fast, difficult"
    },
    'prepositions': {
        'title': "Prepositions",
        'subtitle': "Where Things Are",
        'rules': "Prepositions of place tell us where something is located.\nExamples: in (inside), on (on a surface), under (below), next to (beside).",
        'questions': [
            "The cat is _______ the bed. (It's hiding underneath.)", "The picture is _______ the wall. (It's hanging there.)",
            "The toys are _______ the box. (They're inside.)", "My pencil is _______ the book. (It's right next to it.)",
            "The apples are _______ the table. (They're on the surface.)", "The dog is sleeping _______ the tree."
        ],
        'answers': ['under', 'on', 'in', 'next to', 'on', 'under']
    }
}

# ===================================================================================
# GENERIC PRACTICE MODULE
# This single class can create a practice window for ANY lesson.
# ===================================================================================
class PracticeModule(tk.Toplevel):
    def __init__(self, parent, lesson_key):
        super().__init__(parent)
        self.lesson_data = LESSON_DATA[lesson_key]
        self.title(f"Practice: {self.lesson_data['title']}")
        self.geometry("700x600")
        self.configure(bg='#f4f4f4')
        self.resizable(False, False)
        self.grab_set()

        self.entries = []
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#f4f4f4', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        tk.Label(main_frame, text=self.lesson_data['title'], font=('Arial', 18, 'bold'), bg='#f4f4f4', fg='#0056b3').pack(pady=(0, 5))
        tk.Label(main_frame, text=self.lesson_data['subtitle'], font=('Arial', 12), bg='#f4f4f4', fg='#555').pack(pady=(0, 15))

        rule_frame = tk.Frame(main_frame, bg='#e6f7ff', relief='solid', bd=1, padx=15, pady=10)
        rule_frame.pack(fill='x', pady=(0, 20))
        tk.Label(rule_frame, text="Grammar Rules", font=('Arial', 14, 'bold'), bg='#e6f7ff', fg='#0056b3').pack()
        tk.Label(rule_frame, text=self.lesson_data['rules'], font=('Arial', 12), bg='#e6f7ff', fg='#333', justify='left').pack(pady=5)

        exercise_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=2, padx=15, pady=15)
        exercise_frame.pack(fill='both', expand=True)
        tk.Label(exercise_frame, text="Exercise: Complete the Sentences", font=('Arial', 14, 'bold'), bg='white', fg='#007bff').pack(pady=(0, 15))
        
        if 'word_bank' in self.lesson_data:
            tk.Label(exercise_frame, text=self.lesson_data['word_bank'], font=('Arial', 12, 'italic'), bg='white').pack()

        for i, q_text in enumerate(self.lesson_data['questions']):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=6, anchor='w')
            tk.Label(q_frame, text=f"{i+1}. {q_text}", font=('Arial', 12), bg='white').pack(side='left')
            entry = tk.Entry(q_frame, font=('Arial', 12), width=20)
            entry.pack(side='left', padx=10)
            self.entries.append(entry)

        tk.Button(exercise_frame, text="Check Answers", command=self.check_answers, bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5).pack(pady=15)

    def check_answers(self):
        all_correct = True
        for i, entry in enumerate(self.entries):
            user_answer = entry.get().strip().lower()
            correct_answer = self.lesson_data['answers'][i].lower()
            if user_answer == correct_answer:
                entry.config(fg='green', bg='#e6ffe6')
            else:
                all_correct = False
                entry.config(fg='red', bg='#ffe6e6')
        
        if all_correct:
            messagebox.showinfo("Great Job!", "🎉 All answers are correct!", parent=self)
        else:
            messagebox.showwarning("Review Needed", "Some answers are incorrect. Please review the red boxes.", parent=self)

# ===================================================================================
# MAIN APPLICATION
# This class now dynamically loads lessons from the central data structure.
# ===================================================================================
class EnglishLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive English Learning App")
        self.root.geometry("900x700")
        self.root.configure(bg='#f4f4f4')

        self.lesson_keys = list(LESSON_DATA.keys())
        self.slides = ['Welcome'] + self.lesson_keys + ['Summary']
        self.current_slide_index = 0
        self.current_entries = []

        self.create_widgets()
        self.show_slide()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg='#f4f4f4')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.title_label = tk.Label(self.main_frame, text="Interactive English Learning", font=('Arial', 24, 'bold'), bg='#f4f4f4', fg='#0056b3')
        self.title_label.pack(pady=(0, 20))
        self.content_frame = tk.Frame(self.main_frame, bg='white', relief='ridge', bd=2)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.nav_frame = tk.Frame(self.main_frame, bg='#f4f4f4')
        self.nav_frame.pack(fill='x', pady=(10, 0))
        self.prev_btn = tk.Button(self.nav_frame, text="← Previous", command=self.prev_slide, bg='#007bff', fg='white', font=('Arial', 12), padx=20, pady=5)
        self.slide_label = tk.Label(self.nav_frame, text="", font=('Arial', 12), bg='#f4f4f4', fg='#333')
        self.next_btn = tk.Button(self.nav_frame, text="Next →", command=self.next_slide, bg='#007bff', fg='white', font=('Arial', 12), padx=20, pady=5)

    def show_slide(self):
        self.current_entries = []
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        slide_name = self.slides[self.current_slide_index]
        
        is_welcome_or_summary = slide_name in ['Welcome', 'Summary']
        if is_welcome_or_summary:
            self.prev_btn.pack_forget()
            self.slide_label.pack_forget()
            self.next_btn.pack_forget()
        else:
            self.prev_btn.pack(side='left')
            self.slide_label.pack(side='left', expand=True)
            self.next_btn.pack(side='right')

        self.slide_label.config(text=f"Slide {self.current_slide_index + 1}/{len(self.slides)}: {slide_name.replace('_', ' ').title()}")
        self.prev_btn.config(state='normal' if self.current_slide_index > 1 else 'disabled')
        self.next_btn.config(state='normal' if self.current_slide_index < len(self.slides) - 1 else 'disabled')

        if slide_name == 'Welcome':
            self.show_welcome_slide()
        elif slide_name == 'Summary':
            self.show_summary_slide()
        else: # It's a lesson slide
            self.show_lesson_slide(slide_name)

    def show_welcome_slide(self):
        welcome_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(welcome_frame, text="Welcome to English Learning! 🚀", font=('Arial', 22, 'bold'), bg='white', fg='#0056b3').pack(pady=(20, 10))
        tk.Label(welcome_frame, text="Choose your learning path:", font=('Arial', 14), bg='white').pack(pady=(0, 20))
        tk.Button(welcome_frame, text="Start Full Course", font=('Arial', 14, 'bold'), bg='#007bff', fg='white', padx=20, pady=10, command=self.next_slide).pack(pady=10)
        
        tk.Label(welcome_frame, text="Or, practice a specific topic:", font=('Arial', 14), bg='white').pack(pady=(20, 10))
        for key in self.lesson_keys:
            title = LESSON_DATA[key]['title']
            tk.Button(welcome_frame, text=f"Practice: {title}", font=('Arial', 12, 'bold'), bg='#5a6268', fg='white', padx=15, pady=8, command=lambda k=key: PracticeModule(self.root, k)).pack(pady=5)

    def show_lesson_slide(self, lesson_key):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        lesson = LESSON_DATA[lesson_key]
        
        tk.Label(slide_frame, text=lesson['title'], font=('Arial', 18, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 0))
        tk.Label(slide_frame, text=lesson['subtitle'], font=('Arial', 12), bg='white', fg='#555').pack(pady=(0, 15))
        
        self.create_rule_box(slide_frame, "Grammar Rules", lesson['rules'])
        self.create_exercise_frame(slide_frame, "Exercise: Complete the Sentences", lesson['questions'], lesson_key)

    def show_summary_slide(self):
        summary_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(summary_frame, text="🎉 Congratulations!", font=('Arial', 22, 'bold'), bg='white', fg='#0056b3').pack(pady=(20, 10))
        tk.Label(summary_frame, text="You have completed the full course.", font=('Arial', 14), bg='white', fg='#333').pack(pady=20)
        tk.Button(summary_frame, text="Return to Main Menu", command=self.restart_course, bg='#dc3545', fg='white', font=('Arial', 14, 'bold'), pady=10).pack(pady=20)

    def create_scrollable_frame(self, parent):
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return scrollable_frame

    def create_rule_box(self, parent, title, content):
        rule_frame = tk.Frame(parent, bg='#e6f7ff', relief='solid', bd=1, padx=10, pady=5)
        rule_frame.pack(fill='x', pady=(10, 20), padx=10)
        tk.Label(rule_frame, text=title, font=('Arial', 16, 'bold'), bg='#e6f7ff', fg='#0056b3').pack(pady=(5, 5))
        tk.Label(rule_frame, text=content, font=('Arial', 12), bg='#e6f7ff', fg='#333', justify='left', wraplength=750).pack(pady=(0, 5), padx=15)

    def create_exercise_frame(self, parent, title, questions, lesson_key):
        exercise_frame = tk.Frame(parent, bg='white', relief='ridge', bd=1, padx=15, pady=10)
        exercise_frame.pack(fill='x', pady=20, padx=10)
        tk.Label(exercise_frame, text=title, font=('Arial', 16, 'bold'), bg='white', fg='#007bff').pack(pady=(10, 15))
        
        if 'word_bank' in LESSON_DATA[lesson_key]:
            tk.Label(exercise_frame, text=LESSON_DATA[lesson_key]['word_bank'], font=('Arial', 12, 'italic'), bg='white').pack()

        for i, question_text in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=5, padx=15, anchor='w')
            tk.Label(q_frame, text=f"{i+1}. {question_text}", font=('Arial', 12), bg='white', fg='#333').pack(side='left')
            entry = tk.Entry(q_frame, font=('Arial', 12), width=20)
            entry.pack(side='left', padx=(10, 0))
            self.current_entries.append(entry)
        tk.Button(exercise_frame, text="Check Answers", command=lambda: self.check_answers(lesson_key), bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5).pack(pady=15)

    def check_answers(self, lesson_key):
        correct_answers = LESSON_DATA[lesson_key]['answers']
        all_correct = True
        for i, entry in enumerate(self.current_entries):
            user_answer = entry.get().strip().lower()
            correct_answer = correct_answers[i].lower()
            if user_answer == correct_answer:
                entry.config(fg='green', bg='#e6ffe6')
            else:
                all_correct = False
                entry.config(fg='red', bg='#ffe6e6')
        if all_correct:
            messagebox.showinfo("Great Job!", "🎉 All answers are correct!")
        else:
            messagebox.showwarning("Review Needed", "Some answers are incorrect. Please review the red boxes.")

    def next_slide(self):
        if self.current_slide_index < len(self.slides) - 1:
            self.current_slide_index += 1
            self.show_slide()

    def prev_slide(self):
        if self.current_slide_index > 0:
            self.current_slide_index -= 1
            self.show_slide()

    def restart_course(self):
        self.current_slide_index = 0
        self.show_slide()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnglishLearningApp(root)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
