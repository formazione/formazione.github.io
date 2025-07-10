import tkinter as tk
from tkinter import ttk, messagebox

class EnglishLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive English Learning App")
        self.root.geometry("900x700")
        self.root.configure(bg='#f4f4f4')

        # Current slide index
        self.current_slide = 0

        # Exercise answers (Corrected for single inputs)
        self.answers = {
            'present_simple': [
                'wakes up', 'watch', 'studies', "don't eat", 
                'Do', 'rises', 'sleeps', "don't live"
            ],
            'present_continuous': [
                'He is eating an apple.', 'She is running in the park.', 'They are talking.',
                'It is sleeping.', 'She is cooking dinner.'
            ],
            'past_simple': [
                'visited', 'went', "didn't finish", 'played',
                'Did', 'bought', "didn't like", 'woke up'
            ],
            'adjectives': [
                'blue', 'delicious', 'fast', 'happy', 'difficult', 'tall'
            ],
            'prepositions': [
                'under', 'on', 'in', 'next to', 'on', 'under'
            ]
        }

        self.slides = [
            'Welcome', 'Present Simple', 'Present Continuous',
            'Past Simple', 'Adjectives', 'Prepositions', 'Summary'
        ]
        
        # This will hold the entry widgets for the current slide
        self.current_entries = []

        self.create_widgets()
        self.show_slide()

    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#f4f4f4')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        self.title_label = tk.Label(self.main_frame, text="Interactive English Learning", 
                                    font=('Arial', 24, 'bold'), bg='#f4f4f4', fg='#0056b3')
        self.title_label.pack(pady=(0, 20))

        # Content frame
        self.content_frame = tk.Frame(self.main_frame, bg='white', relief='ridge', bd=2)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Navigation frame
        self.nav_frame = tk.Frame(self.main_frame, bg='#f4f4f4')
        self.nav_frame.pack(fill='x', pady=(10, 0))

        # Navigation buttons
        self.prev_btn = tk.Button(self.nav_frame, text="← Previous", 
                                  command=self.prev_slide, bg='#007bff', fg='white',
                                  font=('Arial', 12), padx=20, pady=5)
        self.prev_btn.pack(side='left')

        self.slide_label = tk.Label(self.nav_frame, text="", font=('Arial', 12), 
                                    bg='#f4f4f4', fg='#333')
        self.slide_label.pack(side='left', expand=True)

        self.next_btn = tk.Button(self.nav_frame, text="Next →", 
                                  command=self.next_slide, bg='#007bff', fg='white',
                                  font=('Arial', 12), padx=20, pady=5)
        self.next_btn.pack(side='right')

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_entries = [] # Clear entries list for the new slide

    def show_slide(self):
        self.clear_content()
        slide_name = self.slides[self.current_slide]

        self.slide_label.config(text=f"Slide {self.current_slide + 1} of {len(self.slides)}: {slide_name}")
        self.prev_btn.config(state='normal' if self.current_slide > 0 else 'disabled')
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

    def create_rule_box(self, parent, title, content):
        rule_frame = tk.Frame(parent, bg='#e6f7ff', relief='solid', bd=1)
        rule_frame.pack(fill='x', pady=(10, 20), padx=10)
        tk.Label(rule_frame, text=title, font=('Arial', 16, 'bold'), bg='#e6f7ff', fg='#0056b3').pack(pady=(10, 5))
        tk.Label(rule_frame, text=content, font=('Arial', 12), bg='#e6f7ff', fg='#333', justify='left', wraplength=750).pack(pady=(0, 10), padx=15)

    def create_exercise_frame(self, parent, title, questions, exercise_type):
        exercise_frame = tk.Frame(parent, bg='white', relief='ridge', bd=1)
        exercise_frame.pack(fill='x', pady=20, padx=10)
        tk.Label(exercise_frame, text=title, font=('Arial', 16, 'bold'), bg='white', fg='#007bff').pack(pady=(10, 15))
        
        for i, question_text in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=5, padx=15, anchor='w')
            
            label = tk.Label(q_frame, text=f"{i+1}. {question_text}", font=('Arial', 12), bg='white', fg='#333')
            label.pack(side='left')
            
            entry = tk.Entry(q_frame, font=('Arial', 12), width=20)
            entry.pack(side='left', padx=(10, 0))
            self.current_entries.append(entry)
            
        check_btn = tk.Button(exercise_frame, text="Check Answers", 
                              command=lambda: self.check_answers(exercise_type),
                              bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        check_btn.pack(pady=15)

    def show_welcome_slide(self):
        welcome_frame = tk.Frame(self.content_frame, bg='white')
        welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)
        tk.Label(welcome_frame, text="Welcome to English Learning! 🚀", font=('Arial', 20, 'bold'), bg='white', fg='#0056b3').pack(pady=(0, 20))
        intro_text = "Hello! This app will help you practice key English grammar points.\nClick 'Next' to start your learning journey."
        tk.Label(welcome_frame, text=intro_text, font=('Arial', 14), bg='white', fg='#333', justify='left').pack(pady=20)

    def show_present_simple_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(slide_frame, text="Present Simple: Routine and Habits", font=('Arial', 18, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 0))
        rules = "Used for habits, facts, and regular actions.\nAdd -s/-es for he/she/it (e.g., she works).\nUse do/don't for questions/negatives (e.g., Do you...?).\nUse does/doesn't for he/she/it (e.g., Does he...?)."
        self.create_rule_box(slide_frame, "Grammar Rules", rules)
        questions = [
            "Maria _______ (wake up) at 7 AM every day.", "My parents _______ (watch) TV in the evening.",
            "He _______ (study) English at school.", "We _______ (not, eat) meat.",
            "_______ (you, like) pizza?", "The sun _______ (rise) in the east.",
            "My cat _______ (sleep) a lot.", "They _______ (not, live) in Rome."
        ]
        self.create_exercise_frame(slide_frame, "Exercise: Complete the Sentences", questions, 'present_simple')
        
    def show_present_continuous_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(slide_frame, text="Present Continuous: Actions Happening Now", font=('Arial', 18, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 0))
        rules = "Used for actions happening right now.\nForm: am/is/are + verb-ing (e.g., I am reading)."
        self.create_rule_box(slide_frame, "Grammar Rules", rules)
        questions = [
            "Un ragazzo sta mangiando una mela. ->", "Una ragazza sta correndo nel parco. ->",
            "Due amici stanno parlando. ->", "Un cane sta dormendo. ->",
            "Una mamma sta cucinando la cena. ->"
        ]
        self.create_exercise_frame(slide_frame, "Exercise: Describe What's Happening", questions, 'present_continuous')

    def show_past_simple_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(slide_frame, text="Past Simple: Completed Actions", font=('Arial', 18, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 0))
        rules = "Used for actions that started and finished in the past.\nRegular verbs add -ed (e.g., played).\nIrregular verbs change (e.g., go -> went).\nUse did/didn't for questions/negatives (e.g., Did you go?)."
        self.create_rule_box(slide_frame, "Grammar Rules", rules)
        questions = [
            "Yesterday, I _______ (visit) my aunt.", "Last summer, we _______ (go) to the beach.",
            "She _______ (not, finish) her homework.", "My brother _______ (play) football with his friends.",
            "_______ (you, see) that movie?", "They _______ (buy) a new car last month.",
            "He _______ (not, like) the food.", "I _______ (wake up) late this morning."
        ]
        self.create_exercise_frame(slide_frame, "Exercise: Complete the Sentences", questions, 'past_simple')

    def show_adjectives_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(slide_frame, text="Adjectives: Describing Nouns", font=('Arial', 18, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 0))
        rules = "Adjectives describe nouns. They usually come before the noun (a big house) or after the verb 'to be' (the house is big).\nThey do not change for plural nouns (two big houses)."
        self.create_rule_box(slide_frame, "Grammar Rules", rules)
        tk.Label(slide_frame, text="Word Bank: happy, tall, blue, delicious, fast, difficult", font=('Arial', 12, 'italic'), bg='white').pack()
        questions = [
            "The sky is _______.", "The cake was very _______.",
            "My friend is a very _______ runner.", "He is a _______ boy because he got a new toy.",
            "This math problem is very _______.", "My brother is very _______; he can reach the top shelf."
        ]
        self.create_exercise_frame(slide_frame, "Exercise: Choose the Best Adjective", questions, 'adjectives')

    def show_prepositions_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(slide_frame, text="Prepositions of Place: Where Things Are", font=('Arial', 18, 'bold'), bg='white', fg='#0056b3').pack(pady=(10, 0))
        rules = "Prepositions tell us the location of something.\nExamples: in (inside), on (on a surface), under (below), next to (beside)."
        self.create_rule_box(slide_frame, "Grammar Rules", rules)
        questions = [
            "The cat is _______ the bed. (It's hiding underneath.)", "The picture is _______ the wall. (It's hanging there.)",
            "The toys are _______ the box. (They're inside.)", "My pencil is _______ the book. (It's right next to it.)",
            "The apples are _______ the table. (They're on the surface.)", "The dog is sleeping _______ the tree."
        ]
        self.create_exercise_frame(slide_frame, "Exercise: Complete with Prepositions", questions, 'prepositions')
        
    def show_summary_slide(self):
        summary_frame = self.create_scrollable_frame(self.content_frame)
        tk.Label(summary_frame, text="🎉 Congratulations! You've Completed the Course!", font=('Arial', 18, 'bold'), bg='white', fg='#0056b3').pack(pady=(20, 20))
        summary_text = "Great job! You have practiced several key grammar points.\nRemember, practice makes perfect!"
        tk.Label(summary_frame, text=summary_text, font=('Arial', 14), bg='white', fg='#333', justify='left').pack(pady=20)
        restart_btn = tk.Button(summary_frame, text="🔄 Restart Course", command=self.restart_course, bg='#dc3545', fg='white', font=('Arial', 14, 'bold'), pady=10, padx=20)
        restart_btn.pack(pady=30)
        
    def check_answers(self, exercise_type):
        correct_answers = self.answers[exercise_type]
        all_correct = True
        results = []

        for i, entry in enumerate(self.current_entries):
            user_answer = entry.get().strip().lower()
            correct_answer = correct_answers[i].lower()
            
            # Special handling for multiple correct options
            is_correct = False
            if exercise_type == 'prepositions' and i == 3: # next to / beside
                is_correct = user_answer in ['next to', 'beside']
            elif exercise_type == 'present_continuous' and i == 3: # it is sleeping / the dog is sleeping
                is_correct = user_answer in ['it is sleeping', 'the dog is sleeping', 'it is sleeping.', 'the dog is sleeping.']
            else:
                is_correct = (user_answer == correct_answer)

            if is_correct:
                entry.config(fg='green', bg='#e6ffe6')
                results.append(f"✓ Question {i+1}: Correct!")
            else:
                all_correct = False
                entry.config(fg='red', bg='#ffe6e6')
                results.append(f"✗ Question {i+1}: Incorrect. Correct answer: {correct_answers[i]}")

        if all_correct:
            messagebox.showinfo("Great Job!", "🎉 All answers are correct! Well done!")
        else:
            result_text = "\n".join(results)
            messagebox.showinfo("Results", "Some answers need review. Check the highlighted fields.\n\n" + result_text)
            
    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.show_slide()

    def prev_slide(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.show_slide()

    def restart_course(self):
        if messagebox.askyesno("Restart Course", "Are you sure you want to restart the course?"):
            self.current_slide = 0
            self.show_slide()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnglishLearningApp(root)
    root.eval('tk::PlaceWindow . center') # Center the window
    root.mainloop()