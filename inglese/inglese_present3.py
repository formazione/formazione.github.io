
import tkinter as tk
from tkinter import ttk, messagebox

class FutureSimpleModule(tk.Toplevel):
    """A separate window for the Future Simple tense exercise."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Practice: Future Simple")
        self.geometry("600x550")
        self.configure(bg='#f4f4f4')
        self.resizable(False, False)

        # Make window modal
        self.grab_set()
        
        self.answers = ['will be', 'will travel', "won't tell", 'Will you help', 'will win']
        self.entries = []
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#f4f4f4', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        tk.Label(main_frame, text="Future Simple (will/won't)", font=('Arial', 18, 'bold'), bg='#f4f4f4', fg='#0056b3').pack(pady=(0, 15))

        # Rules Box
        rule_frame = tk.Frame(main_frame, bg='#e6f7ff', relief='solid', bd=1, padx=15, pady=10)
        rule_frame.pack(fill='x', pady=(0, 20))
        rules = "Used for predictions, spontaneous decisions, and promises.\nForm: will + base verb (e.g., I will go).\nNegative: won't + base verb (e.g., They won't come)."
        tk.Label(rule_frame, text="Grammar Rules", font=('Arial', 14, 'bold'), bg='#e6f7ff', fg='#0056b3').pack()
        tk.Label(rule_frame, text=rules, font=('Arial', 12), bg='#e6f7ff', fg='#333', justify='left').pack(pady=5)

        # Exercise Frame
        exercise_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=2, padx=15, pady=15)
        exercise_frame.pack(fill='both', expand=True)
        
        tk.Label(exercise_frame, text="Exercise: Complete the Sentences", font=('Arial', 14, 'bold'), bg='white', fg='#007bff').pack(pady=(0, 15))

        questions = [
            "I think the weather _______ (be) nice tomorrow.",
            "She _______ (travel) to Japan next year.",
            "Don't worry, I _______ (not, tell) anyone your secret.",
            "_______ (you, help) me with this heavy box?",
            "He _______ (win) the match. He's the best player."
        ]

        for i, q_text in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=6, anchor='w')
            tk.Label(q_frame, text=f"{i+1}. {q_text}", font=('Arial', 12), bg='white').pack(side='left')
            entry = tk.Entry(q_frame, font=('Arial', 12), width=15)
            entry.pack(side='left', padx=10)
            self.entries.append(entry)

        check_btn = tk.Button(exercise_frame, text="Check Answers", command=self.check_answers, bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        check_btn.pack(pady=15)

    def check_answers(self):
        all_correct = True
        for i, entry in enumerate(self.entries):
            user_answer = entry.get().strip().lower()
            correct_answer = self.answers[i].lower()
            if user_answer == correct_answer:
                entry.config(fg='green', bg='#e6ffe6')
            else:
                all_correct = False
                entry.config(fg='red', bg='#ffe6e6')
        
        if all_correct:
            messagebox.showinfo("Great Job!", "🎉 All answers are correct!", parent=self)
        else:
            messagebox.showwarning("Review Needed", "Some answers are incorrect. Please review the red boxes.", parent=self)


class EnglishLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive English Learning App")
        self.root.geometry("900x700")
        self.root.configure(bg='#f4f4f4')

        self.current_slide = 0
        self.answers = {
            'present_simple': ['wakes up', 'watch', 'studies', "don't eat", 'Do', 'rises', 'sleeps', "don't live"],
            'present_continuous': ['He is eating an apple.', 'She is running in the park.', 'They are talking.', 'It is sleeping.', 'She is cooking dinner.'],
            'past_simple': ['visited', 'went', "didn't finish", 'played', 'Did', 'bought', "didn't like", 'woke up'],
            'adjectives': ['blue', 'delicious', 'fast', 'happy', 'difficult', 'tall'],
            'prepositions': ['under', 'on', 'in', 'next to', 'on', 'under']
        }
        self.slides = ['Welcome', 'Present Simple', 'Present Continuous', 'Past Simple', 'Adjectives', 'Prepositions', 'Summary']
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

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_entries = []

    def show_slide(self):
        self.clear_content()
        slide_name = self.slides[self.current_slide]

        # Hide nav buttons on Welcome slide, show them otherwise
        if slide_name == 'Welcome':
            self.prev_btn.pack_forget()
            self.slide_label.pack_forget()
            self.next_btn.pack_forget()
        else:
            self.prev_btn.pack(side='left')
            self.slide_label.pack(side='left', expand=True)
            self.next_btn.pack(side='right')

        self.slide_label.config(text=f"Slide {self.current_slide + 1} of {len(self.slides)}: {slide_name}")
        self.prev_btn.config(state='normal' if self.current_slide > 1 else 'disabled') # Disable on first real slide
        self.next_btn.config(state='normal' if self.current_slide < len(self.slides) - 1 else 'disabled')

        slide_method = getattr(self, f"show_{slide_name.lower().replace(' ', '_')}_slide", None)
        if slide_method:
            slide_method()

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

    def create_exercise_frame(self, parent, title, questions, exercise_type):
        exercise_frame = tk.Frame(parent, bg='white', relief='ridge', bd=1, padx=15, pady=10)
        exercise_frame.pack(fill='x', pady=20, padx=10)
        tk.Label(exercise_frame, text=title, font=('Arial', 16, 'bold'), bg='white', fg='#007bff').pack(pady=(10, 15))
        for i, question_text in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=5, padx=15, anchor='w')
            tk.Label(q_frame, text=f"{i+1}. {question_text}", font=('Arial', 12), bg='white', fg='#333').pack(side='left')
            entry = tk.Entry(q_frame, font=('Arial', 12), width=20)
            entry.pack(side='left', padx=(10, 0))
            self.current_entries.append(entry)
        tk.Button(exercise_frame, text="Check Answers", command=lambda: self.check_answers(exercise_type), bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5).pack(pady=15)

    def show_welcome_slide(self):
        welcome_frame = tk.Frame(self.content_frame, bg='white')
        welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)
        tk.Label(welcome_frame, text="Welcome to English Learning! 🚀", font=('Arial', 22, 'bold'), bg='white', fg='#0056b3').pack(pady=(20, 10))
        tk.Label(welcome_frame, text="Choose your learning path:", font=('Arial', 14), bg='white').pack(pady=(0, 30))
        
        tk.Button(welcome_frame, text="Start Full Course", font=('Arial', 14, 'bold'), bg='#007bff', fg='white', padx=20, pady=10, command=self.next_slide).pack(pady=10)
        tk.Button(welcome_frame, text="Practice: Future Simple", font=('Arial', 14, 'bold'), bg='#5a6268', fg='white', padx=20, pady=10, command=self.open_future_module).pack(pady=10)

    def open_future_module(self):
        FutureSimpleModule(self.root)

    def create_rule_box(self, parent, title, content):
        rule_frame = tk.Frame(parent, bg='#e6f7ff', relief='solid', bd=1, padx=10, pady=5)
        rule_frame.pack(fill='x', pady=(10, 20), padx=10)
        tk.Label(rule_frame, text=title, font=('Arial', 16, 'bold'), bg='#e6f7ff', fg='#0056b3').pack(pady=(5, 5))
        tk.Label(rule_frame, text=content, font=('Arial', 12), bg='#e6f7ff', fg='#333', justify='left', wraplength=750).pack(pady=(0, 5), padx=15)

    def show_present_simple_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        self.create_rule_box(slide_frame, "Present Simple", "Used for habits and facts. Add -s/-es for he/she/it.")
        questions = ["Maria _______ (wake up) at 7 AM.", "My parents _______ (watch) TV.", "He _______ (study) English.", "We _______ (not, eat) meat.", "_______ (you, like) pizza?", "The sun _______ (rise) in the east.", "My cat _______ (sleep) a lot.", "They _______ (not, live) in Rome."]
        self.create_exercise_frame(slide_frame, "Complete the Sentences", questions, 'present_simple')

    def show_present_continuous_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        self.create_rule_box(slide_frame, "Present Continuous", "Used for actions happening now. Form: am/is/are + verb-ing.")
        questions = ["Un ragazzo mangia una mela. ->", "Una ragazza corre. ->", "Due amici parlano. ->", "Un cane dorme. ->", "Una mamma cucina. ->"]
        self.create_exercise_frame(slide_frame, "Describe What's Happening", questions, 'present_continuous')

    def show_past_simple_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        self.create_rule_box(slide_frame, "Past Simple", "Used for finished past actions. Add -ed or use irregular forms.")
        questions = ["Yesterday, I _______ (visit) my aunt.", "Last summer, we _______ (go) to the beach.", "She _______ (not, finish) her homework.", "My brother _______ (play) football.", "_______ (you, see) that movie?", "They _______ (buy) a new car.", "He _______ (not, like) the food.", "I _______ (wake up) late."]
        self.create_exercise_frame(slide_frame, "Complete the Sentences", questions, 'past_simple')

    def show_adjectives_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        self.create_rule_box(slide_frame, "Adjectives", "Words that describe nouns. They don't change for plurals.")
        tk.Label(slide_frame, text="Word Bank: happy, tall, blue, delicious, fast, difficult", font=('Arial', 12, 'italic'), bg='white').pack()
        questions = ["The sky is _______.", "The cake was very _______.", "My friend is a _______ runner.", "He is a _______ boy.", "This math problem is _______.", "My brother is very _______."]
        self.create_exercise_frame(slide_frame, "Choose the Best Adjective", questions, 'adjectives')

    def show_prepositions_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        self.create_rule_box(slide_frame, "Prepositions of Place", "Words that show location (in, on, under, next to).")
        questions = ["The cat is _______ the bed.", "The picture is _______ the wall.", "The toys are _______ the box.", "My pencil is _______ the book.", "The apples are _______ the table.", "The dog is sleeping _______ the tree."]
        self.create_exercise_frame(slide_frame, "Complete with Prepositions", questions, 'prepositions')

    def show_summary_slide(self):
        summary_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(summary_frame, text="🎉 Congratulations!", font=('Arial', 22, 'bold'), bg='white', fg='#0056b3').pack(pady=(20, 10))
        tk.Label(summary_frame, text="You have completed the full course.", font=('Arial', 14), bg='white', fg='#333').pack(pady=20)
        tk.Button(summary_frame, text="Restart Course", command=self.restart_course, bg='#dc3545', fg='white', font=('Arial', 14, 'bold'), pady=10).pack(pady=20)
        tk.Button(summary_frame, text="Practice Future Tense Again", command=self.open_future_module, bg='#5a6268', fg='white', font=('Arial', 12, 'bold'), pady=8).pack(pady=10)

    def check_answers(self, exercise_type):
        correct_answers = self.answers[exercise_type]
        all_correct = True
        for i, entry in enumerate(self.current_entries):
            user_answer = entry.get().strip().lower()
            correct_answer = correct_answers[i].lower()
            is_correct = (user_answer == correct_answer) or (exercise_type == 'prepositions' and i == 3 and user_answer in ['next to', 'beside']) or (exercise_type == 'present_continuous' and i == 3 and user_answer in ['it is sleeping.', 'the dog is sleeping.'])
            if is_correct:
                entry.config(fg='green', bg='#e6ffe6')
            else:
                all_correct = False
                entry.config(fg='red', bg='#ffe6e6')
        if all_correct:
            messagebox.showinfo("Great Job!", "🎉 All answers are correct!")
        else:
            messagebox.showwarning("Review Needed", "Some answers are incorrect. Please review the red boxes.")

    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.show_slide()

    def prev_slide(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.show_slide()

    def restart_course(self):
        if messagebox.askyesno("Restart Course", "Are you sure you want to return to the main menu?"):
            self.current_slide = 0
            self.show_slide()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnglishLearningApp(root)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
