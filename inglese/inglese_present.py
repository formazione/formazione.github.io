
import tkinter as tk
from tkinter import ttk, messagebox
import random

class EnglishLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive English Learning App")
        self.root.geometry("900x700")
        self.root.configure(bg='#f4f4f4')

        # Current slide index
        self.current_slide = 0

        # Exercise answers
        self.answers = {
            'present_simple': {
                0: 'wakes up',
                1: 'watch',
                2: 'studies',
                3: "don't eat",
                4: 'Do',
                5: 'rises',
                6: 'sleeps',
                7: "don't live"
            },
            'present_continuous': {
                0: 'He is eating an apple.',
                1: 'She is running in the park.',
                2: 'They are talking.',
                3: 'It is sleeping.',
                4: 'She is cooking dinner.'
            },
            'past_simple': {
                0: 'visited',
                1: 'went',
                2: "didn't finish",
                3: 'played',
                4: 'Did',
                5: 'bought',
                6: "didn't like",
                7: 'woke up'
            },
            'adjectives': {
                0: 'blue',
                1: 'delicious',
                2: 'fast',
                3: 'happy',
                4: 'difficult',
                5: 'tall'
            },
            'prepositions': {
                0: 'under',
                1: 'on',
                2: 'in',
                3: 'next to',
                4: 'on',
                5: 'under'
            }
        }

        self.user_answers = {}
        self.slides = [
            'Welcome',
            'Present Simple',
            'Present Continuous',
            'Past Simple',
            'Adjectives',
            'Prepositions',
            'Summary'
        ]

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

    def show_slide(self):
        self.clear_content()
        slide_name = self.slides[self.current_slide]

        # Update navigation
        self.slide_label.config(text=f"Slide {self.current_slide + 1} of {len(self.slides)}: {slide_name}")
        self.prev_btn.config(state='normal' if self.current_slide > 0 else 'disabled')
        self.next_btn.config(state='normal' if self.current_slide < len(self.slides) - 1 else 'disabled')

        # Show appropriate slide content
        if slide_name == 'Welcome':
            self.show_welcome_slide()
        elif slide_name == 'Present Simple':
            self.show_present_simple_slide()
        elif slide_name == 'Present Continuous':
            self.show_present_continuous_slide()
        elif slide_name == 'Past Simple':
            self.show_past_simple_slide()
        elif slide_name == 'Adjectives':
            self.show_adjectives_slide()
        elif slide_name == 'Prepositions':
            self.show_prepositions_slide()
        elif slide_name == 'Summary':
            self.show_summary_slide()

    def create_scrollable_frame(self, parent):
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return scrollable_frame

    def show_welcome_slide(self):
        welcome_frame = tk.Frame(self.content_frame, bg='white')
        welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title = tk.Label(welcome_frame, text="Welcome to English Learning!", 
                         font=('Arial', 20, 'bold'), bg='white', fg='#0056b3')
        title.pack(pady=(0, 20))

        intro_text = """Hello! Welcome to our interactive English learning app!

This app will help you learn and practice:
• Present Simple tense
• Present Continuous tense
• Past Simple tense
• Adjectives
• Prepositions of place

Each section includes:
✓ Clear explanations of grammar rules
✓ Examples to help you understand
✓ Interactive exercises to practice
✓ Instant feedback on your answers

Take your time and don't worry about making mistakes - 
that's how we learn! Click 'Next' to start your learning journey."""

        intro_label = tk.Label(welcome_frame, text=intro_text, font=('Arial', 14), 
                               bg='white', fg='#333', justify='left')
        intro_label.pack(pady=20)

        # Tips box
        tips_frame = tk.Frame(welcome_frame, bg='#fff3cd', relief='solid', bd=1)
        tips_frame.pack(fill='x', pady=20)

        tips_title = tk.Label(tips_frame, text="💡 Learning Tips:", 
                              font=('Arial', 14, 'bold'), bg='#fff3cd', fg='#856404')
        tips_title.pack(pady=(10, 5))

        tips_text = """• Read the rules carefully before starting exercises
• Don't rush - take time to understand each concept
• Practice makes perfect - try the exercises multiple times
• Celebrate your progress, no matter how small!"""

        tips_label = tk.Label(tips_frame, text=tips_text, font=('Arial', 12), 
                              bg='#fff3cd', fg='#856404', justify='left')
        tips_label.pack(pady=(0, 10))

    def create_rule_box(self, parent, title, content):
        rule_frame = tk.Frame(parent, bg='#e6f7ff', relief='solid', bd=1)
        rule_frame.pack(fill='x', pady=(0, 20), padx=10)

        rule_title = tk.Label(rule_frame, text=title, font=('Arial', 16, 'bold'), 
                              bg='#e6f7ff', fg='#0056b3')
        rule_title.pack(pady=(10, 5))

        rule_text = tk.Label(rule_frame, text=content, font=('Arial', 12), 
                             bg='#e6f7ff', fg='#333', justify='left', wraplength=750)
        rule_text.pack(pady=(0, 10), padx=15)

    def show_present_simple_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)

        # Title
        title = tk.Label(slide_frame, text="Present Simple: Routine and Habits", 
                         font=('Arial', 18, 'bold'), bg='white', fg='#0056b3')
        title.pack(pady=(10, 20))

        # Rules
        rules_content = """The Present Simple is used for actions that happen regularly, habits, facts, and general truths.

Rules:
• For most verbs, use the base form (play, eat, work)
• For he, she, it, and singular nouns, add -s or -es (plays, eats, works, goes, washes)
• For questions, use do or does (for he/she/it) before the subject
• For negative sentences, use don't or doesn't (for he/she/it) before the verb

Examples:
• I play tennis every Saturday.
• She reads a book every night.
• They don't like coffee.
• Does he go to school by bus?"""

        self.create_rule_box(slide_frame, "Grammar Rules", rules_content)

        # Exercise
        exercise_frame = tk.Frame(slide_frame, bg='white', relief='ridge', bd=1)
        exercise_frame.pack(fill='x', pady=20, padx=10)

        exercise_title = tk.Label(exercise_frame, text="Exercise: Complete the Sentences", 
                                  font=('Arial', 16, 'bold'), bg='white', fg='#007bff')
        exercise_title.pack(pady=(10, 15))

        # Exercise questions
        questions = [
            "Maria _______ (wake up) at 7 AM every day.",
            "My parents _______ (watch) TV in the evening.",
            "He _______ (study) English at school.",
            "We _______ (not, eat) meat.",
            "_______ you _______ (like) pizza?",
            "The sun _______ (rise) in the east.",
            "My cat _______ (sleep) a lot.",
            "They _______ (not, live) in Rome."
        ]

        self.present_simple_entries = []
        for i, question in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=5, padx=15)

            q_text = question
            entry_width = 15

            if i == 4: # Special case for "Do you like"
                parts = question.split("___")
                tk.Label(q_frame, text=f"{i+1}. {parts[0]}", font=('Arial', 12), bg='white', fg='#333').pack(side='left')
                entry1 = tk.Entry(q_frame, font=('Arial', 12), width=5)
                entry1.pack(side='left', padx=5)
                self.present_simple_entries.append(entry1) # This is a placeholder, only the first box is checked
                tk.Label(q_frame, text=f"{parts[1]}", font=('Arial', 12), bg='white', fg='#333').pack(side='left')
            else:
                q_label = tk.Label(q_frame, text=f"{i+1}. {q_text}", 
                               font=('Arial', 12), bg='white', fg='#333')
                q_label.pack(side='left', anchor='w')

            entry = tk.Entry(q_frame, font=('Arial', 12), width=entry_width)
            entry.pack(side='right', padx=(10, 0))
            self.present_simple_entries.append(entry)


        # Check button
        check_btn = tk.Button(exercise_frame, text="Check Answers", 
                              command=lambda: self.check_answers('present_simple'),
                              bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        check_btn.pack(pady=15)

    def show_present_continuous_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)

        title = tk.Label(slide_frame, text="Present Continuous: Actions Happening Now", 
                         font=('Arial', 18, 'bold'), bg='white', fg='#0056b3')
        title.pack(pady=(10, 20))

        rules_content = """The Present Continuous is used for actions happening right now or temporary actions.

Rules:
• Form: verb "to be" (am/is/are) + verb-ing
• Am for I (I am eating)
• Is for he/she/it/singular nouns (He is reading)
• Are for you/we/they/plural nouns (They are playing)
• For negative sentences, add not after "to be" (He is not sleeping)
• For questions, put "to be" before the subject (Are you listening?)

Examples:
• I am reading a book right now.
• She is watching TV.
• They are not playing outside.
• Is he listening to music?"""

        self.create_rule_box(slide_frame, "Grammar Rules", rules_content)

        exercise_frame = tk.Frame(slide_frame, bg='white', relief='ridge', bd=1)
        exercise_frame.pack(fill='x', pady=20, padx=10)

        exercise_title = tk.Label(exercise_frame, text="Exercise: Describe What's Happening", 
                                  font=('Arial', 16, 'bold'), bg='white', fg='#007bff')
        exercise_title.pack(pady=(10, 15))

        questions = [
            "Un ragazzo sta mangiando una mela. ->",
            "Una ragazza sta correndo nel parco. ->",
            "Due amici stanno parlando. ->",
            "Un cane sta dormendo. ->",
            "Una mamma sta cucinando la cena. ->"
        ]

        self.present_continuous_entries = []
        for i, question in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=8, padx=15)
            
            q_label = tk.Label(q_frame, text=f"{i+1}. {question}", 
                               font=('Arial', 12), bg='white', fg='#333')
            q_label.pack(side='left')

            entry = tk.Entry(q_frame, font=('Arial', 12), width=30)
            entry.pack(side='left', padx=(10, 0), expand=True, fill='x')
            self.present_continuous_entries.append(entry)

        check_btn = tk.Button(exercise_frame, text="Check Answers", 
                              command=lambda: self.check_answers('present_continuous'),
                              bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        check_btn.pack(pady=15)
        
    def show_past_simple_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)

        title = tk.Label(slide_frame, text="Past Simple: Completed Actions", 
                         font=('Arial', 18, 'bold'), bg='white', fg='#0056b3')
        title.pack(pady=(10, 20))

        rules_content = """The Past Simple is used for actions that started and finished in the past.

Rules:
• For regular verbs, add -ed (walked, played, finished)
• For irregular verbs, the form changes (go→went, eat→ate, see→saw) - you must learn them!
• For questions, use did before the subject
• For negative sentences, use didn't before the base form of the verb

Examples:
• I walked to school yesterday.
• She ate pizza last night.
• They didn't visit their grandparents.
• Did he go to the party?"""

        self.create_rule_box(slide_frame, "Grammar Rules", rules_content)

        exercise_frame = tk.Frame(slide_frame, bg='white', relief='ridge', bd=1)
        exercise_frame.pack(fill='x', pady=20, padx=10)

        exercise_title = tk.Label(exercise_frame, text="Exercise: Complete the Sentences (Past Simple)", 
                                  font=('Arial', 16, 'bold'), bg='white', fg='#007bff')
        exercise_title.pack(pady=(10, 15))

        questions = [
            "Yesterday, I _______ (visit) my aunt.",
            "Last summer, we _______ (go) to the beach.",
            "She _______ (not, finish) her homework.",
            "My brother _______ (play) football with his friends.",
            "_______ you _______ (see) that movie?",
            "They _______ (buy) a new car last month.",
            "He _______ (not, like) the food.",
            "I _______ (wake up) late this morning."
        ]

        self.past_simple_entries = []
        for i, question in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=5, padx=15)
            
            q_text = question
            entry_width = 15
            
            if i == 4: # Special case for "Did you see"
                parts = question.split("___")
                tk.Label(q_frame, text=f"{i+1}. {parts[0]}", font=('Arial', 12), bg='white', fg='#333').pack(side='left')
                entry1 = tk.Entry(q_frame, font=('Arial', 12), width=5)
                entry1.pack(side='left', padx=5)
                self.past_simple_entries.append(entry1) # This is a placeholder
                tk.Label(q_frame, text=parts[1], font=('Arial', 12), bg='white', fg='#333').pack(side='left')
            else:
                q_label = tk.Label(q_frame, text=f"{i+1}. {q_text}", 
                                   font=('Arial', 12), bg='white', fg='#333')
                q_label.pack(side='left', anchor='w')

            entry = tk.Entry(q_frame, font=('Arial', 12), width=entry_width)
            entry.pack(side='right', padx=(10, 0))
            self.past_simple_entries.append(entry)


        check_btn = tk.Button(exercise_frame, text="Check Answers", 
                              command=lambda: self.check_answers('past_simple'),
                              bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        check_btn.pack(pady=15)

    def show_adjectives_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)

        title = tk.Label(slide_frame, text="Adjectives: Describing Nouns", 
                         font=('Arial', 18, 'bold'), bg='white', fg='#0056b3')
        title.pack(pady=(10, 20))

        rules_content = """Adjectives are words that describe nouns (people, places, things). They tell us more about the noun, like its size, color, feeling, etc.

Rules:
• Adjectives usually come before the noun they describe (a big house, a red car)
• They can also come after the verb "to be" (The house is big, The car is red)
• Adjectives don't change their form for plural nouns (two big houses, not "bigs")

Examples:
• She has long hair.
• The movie was very interesting.
• He is a happy boy."""

        self.create_rule_box(slide_frame, "Grammar Rules", rules_content)

        exercise_frame = tk.Frame(slide_frame, bg='white', relief='ridge', bd=1)
        exercise_frame.pack(fill='x', pady=20, padx=10)

        exercise_title = tk.Label(exercise_frame, text="Exercise: Choose the Best Adjective", 
                                  font=('Arial', 16, 'bold'), bg='white', fg='#007bff')
        exercise_title.pack(pady=(10, 15))

        word_bank = tk.Label(exercise_frame, text="Word Bank: happy, tall, blue, delicious, fast, difficult", 
                             font=('Arial', 12, 'italic'), bg='white', fg='#666')
        word_bank.pack(pady=(0, 10))

        questions = [
            "The sky is _______.",
            "The cake was very _______.",
            "My friend is a very _______ runner.",
            "He is a _______ boy because he got a new toy.",
            "This math problem is very _______.",
            "My brother is very _______; he can reach the top shelf."
        ]

        self.adjectives_entries = []
        for i, question in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=5, padx=15)
            
            q_label = tk.Label(q_frame, text=f"{i+1}. {question}", 
                               font=('Arial', 12), bg='white', fg='#333')
            q_label.pack(side='left', anchor='w')

            entry = tk.Entry(q_frame, font=('Arial', 12), width=15)
            entry.pack(side='right', padx=(10, 0))
            self.adjectives_entries.append(entry)

        check_btn = tk.Button(exercise_frame, text="Check Answers", 
                              command=lambda: self.check_answers('adjectives'),
                              bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        check_btn.pack(pady=15)

    def show_prepositions_slide(self):
        slide_frame = self.create_scrollable_frame(self.content_frame)

        title = tk.Label(slide_frame, text="Prepositions of Place: Where Things Are", 
                         font=('Arial', 18, 'bold'), bg='white', fg='#0056b3')
        title.pack(pady=(10, 20))

        rules_content = """Prepositions of place tell us where something is located.

Common prepositions:
• in: inside something (in the box, in the room)
• on: on a surface (on the table, on the wall)
• under: below something (under the chair)
• next to / beside: right next to something (next to the door)
• between: in the middle of two things (between the sofa and the chair)
• in front of: at the front of something (in front of the house)
• behind: at the back of something (behind the tree)

Examples:
• The book is on the table.
• My keys are in my bag.
• The cat is sleeping under the bed."""

        self.create_rule_box(slide_frame, "Grammar Rules", rules_content)

        exercise_frame = tk.Frame(slide_frame, bg='white', relief='ridge', bd=1)
        exercise_frame.pack(fill='x', pady=20, padx=10)

        exercise_title = tk.Label(exercise_frame, text="Exercise: Complete with Prepositions", 
                                  font=('Arial', 16, 'bold'), bg='white', fg='#007bff')
        exercise_title.pack(pady=(10, 15))

        questions = [
            "The cat is _______ the bed. (It's hiding underneath.)",
            "The picture is _______ the wall. (It's hanging there.)",
            "The toys are _______ the box. (They're inside.)",
            "My pencil is _______ the book. (It's right next to it.)",
            "The apples are _______ the table. (They're on the surface.)",
            "The dog is sleeping _______ the tree. (It's at the base, under the branches.)"
        ]

        self.prepositions_entries = []
        for i, question in enumerate(questions):
            q_frame = tk.Frame(exercise_frame, bg='white')
            q_frame.pack(fill='x', pady=8, padx=15)
            
            q_label = tk.Label(q_frame, text=f"{i+1}. {question}", 
                               font=('Arial', 12), bg='white', fg='#333', wraplength=500, justify='left')
            q_label.pack(side='left')

            entry = tk.Entry(q_frame, font=('Arial', 12), width=15)
            entry.pack(side='right', padx=(10, 0))
            self.prepositions_entries.append(entry)

        check_btn = tk.Button(exercise_frame, text="Check Answers", 
                              command=lambda: self.check_answers('prepositions'),
                              bg='#28a745', fg='white', font=('Arial', 12, 'bold'), pady=5)
        check_btn.pack(pady=15)

    def show_summary_slide(self):
        summary_frame = self.create_scrollable_frame(self.content_frame)

        title = tk.Label(summary_frame, text="🎉 Congratulations! You've Completed the Course!", 
                         font=('Arial', 18, 'bold'), bg='white', fg='#0056b3')
        title.pack(pady=(10, 20))

        summary_text = """Great job! You've learned about:

✅ Present Simple - for habits and routines
✅ Present Continuous - for actions happening now
✅ Past Simple - for completed actions in the past
✅ Adjectives - for describing nouns
✅ Prepositions of Place - for describing locations

Remember: Learning English is a journey, not a destination!"""

        summary_label = tk.Label(summary_frame, text=summary_text, 
                                 font=('Arial', 14), bg='white', fg='#333', justify='left')
        summary_label.pack(pady=20)

        tips_frame = tk.Frame(summary_frame, bg='#fff3cd', relief='solid', bd=1)
        tips_frame.pack(fill='x', pady=20, padx=10)

        tips_title = tk.Label(tips_frame, text="💡 Tips for Continued Learning:", 
                              font=('Arial', 14, 'bold'), bg='#fff3cd', fg='#856404')
        tips_title.pack(pady=(10, 5))

        tips_text = """• Practice regularly - even 15 minutes a day helps!
• Read English books, watch English movies
• Try to think in English sometimes
• Don't be afraid to make mistakes - they're part of learning
• Keep a vocabulary notebook
• Practice speaking with friends or family
• Use English learning apps and websites
• Be patient with yourself - progress takes time!"""

        tips_label = tk.Label(tips_frame, text=tips_text, font=('Arial', 12), 
                              bg='#fff3cd', fg='#856404', justify='left')
        tips_label.pack(pady=(0, 10))

        restart_btn = tk.Button(summary_frame, text="🔄 Restart Course", 
                                command=self.restart_course,
                                bg='#dc3545', fg='white', font=('Arial', 14, 'bold'), 
                                pady=10, padx=20)
        restart_btn.pack(pady=30)
        
    def check_answers(self, exercise_type):
        entries = []
        if exercise_type == 'present_simple':
            entries = self.present_simple_entries
        elif exercise_type == 'present_continuous':
            entries = self.present_continuous_entries
        elif exercise_type == 'past_simple':
            entries = self.past_simple_entries
        elif exercise_type == 'adjectives':
            entries = self.adjectives_entries
        elif exercise_type == 'prepositions':
            entries = self.prepositions_entries

        correct_answers_map = self.answers[exercise_type]
        results = []
        all_correct = True
        
        entry_index = 0
        for i in range(len(correct_answers_map)):
            entry = entries[entry_index]
            user_answer = entry.get().strip().lower()
            correct_answer = correct_answers_map[i].lower()
            
            # Special handling for multiple acceptable answers or split inputs
            is_correct = False
            if exercise_type == 'present_simple' and i == 4:
                # "Do you like pizza?" - expecting "Do"
                is_correct = user_answer == 'do'
                entry_index += 1 # Skip the placeholder entry
            elif exercise_type == 'past_simple' and i == 4:
                # "Did you see that movie?" - expecting "Did"
                is_correct = user_answer == 'did'
                entry_index += 1 # Skip the placeholder entry
            elif exercise_type == 'prepositions' and i == 3:  # next to / beside
                is_correct = user_answer in ['next to', 'beside']
            elif exercise_type == 'present_continuous' and i == 3:  # It is sleeping / The dog is sleeping
                is_correct = user_answer in ['it is sleeping', 'the dog is sleeping', 'it is sleeping.', 'the dog is sleeping.']
            else:
                is_correct = user_answer == correct_answer

            if is_correct:
                entry.config(bg='#e6ffe6', fg='#006600')
                results.append(f"✓ Question {i+1}: Correct!")
            else:
                entry.config(bg='#ffe6e6', fg='#cc0000')
                results.append(f"✗ Question {i+1}: Incorrect. Correct answer: {correct_answers_map[i]}")
                all_correct = False
            
            entry_index +=1

        if all_correct:
            messagebox.showinfo("Great Job!", "🎉 All answers are correct!\nWell done!")
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
        if messagebox.askyesno("Restart Course", "Are you sure you want to restart the course? All progress will be lost."):
            self.current_slide = 0
            self.user_answers = {}
            self.show_slide()
            messagebox.showinfo("Course Restarted", "Welcome back! The course has been restarted.")

def main():
    root = tk.Tk()
    app = EnglishLearningApp(root)

    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()

if __name__ == "__main__":
    main()
