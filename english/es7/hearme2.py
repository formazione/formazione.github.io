# Interactive Listening Exercise
#
# This Python script is a desktop application that helps users practice their listening
# and spelling skills. It's a conversion of the provided HTML/JavaScript version.
#
# Required libraries:
# - tkinter: For the graphical user interface (usually included with Python).
# - edge_tts: For generating high-quality text-to-speech audio.
# - pygame: For playing the generated audio.
#
# You can install the necessary packages using pip:
# pip install tkinter edge-tts pygame

import tkinter as tk
from tkinter import messagebox, font
import asyncio
import edge_tts
import pygame
from io import BytesIO
import random
import threading

# --- Configuration ---
VOICE = "en-US-JennyNeural"
APP_BG_COLOR = "#f4f4f4"
EXERCISE_BG_COLOR = "#ffffff"
BORDER_COLOR = "#dddddd"
BUTTON_COLOR = "#007bff"
BUTTON_HOVER_COLOR = "#0056b3"
TEXT_COLOR = "#333333"
TITLE_COLOR = "#0056b3"
CORRECT_BG_COLOR = "#d4edda"
INCORRECT_BORDER_COLOR = "#e57373"
DEFAULT_BORDER_COLOR = "#cccccc"

# --- Main Application Class ---

class ListeningExerciseApp:
    """
    The main class for the listening exercise application.
    It handles the GUI, sentence logic, text-to-speech, and audio playback.
    """

    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Interactive Listening Exercise")
        self.root.configure(bg=APP_BG_COLOR)
        self.root.geometry("850x450")

        # --- Data ---
        self.master_sentence_list = [
            "The sun is hot", "My dog is big", "I can run fast", "She has a red car", "We like to play",
            "He is my friend", "The cat is small", "I see a bird", "This is a book", "I have a pen",
            "The sky is blue", "I love my mom", "He can jump high", "The ball is round", "We eat fish",
            "She can sing well", "The tree is tall", "I drink milk", "He has a blue bike", "My name is Tom",
            "I go to school", "The grass is green", "I have two hands", "She likes to read", "We play a game",
            "The pig is pink", "I can see the moon", "He kicks the ball", "The duck can swim", "I sit on a chair"
        ]
        self.current_sentences = []
        self.current_sentence_index = 0
        self.letter_boxes = [] # To hold the Entry widgets

        # --- Initialize Pygame Mixer for Audio ---
        try:
            pygame.mixer.init()
        except pygame.error as e:
            messagebox.showerror("Audio Error", f"Could not initialize the audio player: {e}\nPlease ensure you have a working audio device.")
            self.root.destroy()
            return

        # --- Build the GUI ---
        self.create_widgets()

    def create_widgets(self):
        """Create and layout all the GUI widgets."""
        # Define fonts
        self.title_font = font.Font(family="Arial", size=20, weight="bold")
        self.body_font = font.Font(family="Arial", size=11)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")
        self.progress_font = font.Font(family="Arial", size=14, weight="normal")
        self.letter_font = font.Font(family="Arial", size=16, weight="bold")

        # Main container frame
        main_frame = tk.Frame(self.root, bg=APP_BG_COLOR, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title and Instructions
        tk.Label(main_frame, text="Interactive Listening Exercise", font=self.title_font, bg=APP_BG_COLOR, fg=TITLE_COLOR).pack(pady=(0, 5))
        tk.Label(main_frame, text="Listen to the sentence, then type each letter. Press Enter to listen again.", font=self.body_font, bg=APP_BG_COLOR, fg=TEXT_COLOR).pack(pady=(0, 20))

        # Exercise Frame
        exercise_frame = tk.Frame(main_frame, bg=EXERCISE_BG_COLOR, relief="solid", bd=1, padx=20, pady=20)
        exercise_frame.pack(expand=True, fill="both")

        # Top controls (Start button)
        controls_frame = tk.Frame(exercise_frame, bg=EXERCISE_BG_COLOR)
        controls_frame.pack(fill="x", pady=(0, 15))
        self.start_button = tk.Button(controls_frame, text="✨ Start / Generate Exercise", font=self.button_font, bg=BUTTON_COLOR, fg="white", relief="flat", command=self.start_new_exercise)
        self.start_button.pack()

        # Progress Indicator
        self.progress_indicator = tk.Label(exercise_frame, text="", font=self.progress_font, bg=EXERCISE_BG_COLOR, fg=TEXT_COLOR)
        self.progress_indicator.pack(pady=10)

        # Sentence Display Area (where letter boxes will go)
        self.sentence_display_area = tk.Frame(exercise_frame, bg=EXERCISE_BG_COLOR, pady=20)
        self.sentence_display_area.pack(expand=True)

    def start_new_exercise(self):
        """Resets and starts a new set of 5 sentences."""
        self.current_sentence_index = 0
        shuffled = random.sample(self.master_sentence_list, 5)
        self.current_sentences = shuffled
        self.display_sentence()

    def display_sentence(self):
        """Clears the old sentence and displays the new one."""
        # Clear previous sentence widgets
        for widget in self.sentence_display_area.winfo_children():
            widget.destroy()
        self.letter_boxes = []

        if self.current_sentence_index >= len(self.current_sentences):
            messagebox.showinfo("Exercise Complete!", "Fantastic! You've completed the exercise.")
            self.progress_indicator.config(text="Exercise Complete!")
            return

        # Update progress label
        self.progress_indicator.config(text=f"Sentence {self.current_sentence_index + 1} of {len(self.current_sentences)}")
        sentence = self.current_sentences[self.current_sentence_index]

        # Container for the speaker button and words
        sentence_container = tk.Frame(self.sentence_display_area, bg=EXERCISE_BG_COLOR)
        sentence_container.pack()

        # Speak Button
        speak_btn = tk.Button(sentence_container, text='🔊', font=self.letter_font, bg=EXERCISE_BG_COLOR, fg=BUTTON_COLOR, relief="flat", command=lambda: self.speak_in_thread(sentence))
        speak_btn.pack(side="left", padx=(0, 10))

        # Words Wrapper
        words_wrapper = tk.Frame(sentence_container, bg=EXERCISE_BG_COLOR)
        words_wrapper.pack(side="left")

        # Create letter boxes for each character in the sentence
        words = sentence.split(' ')
        for word in words:
            word_frame = tk.Frame(words_wrapper, bg=EXERCISE_BG_COLOR)
            word_frame.pack(side="left", padx=10)
            for i, char in enumerate(word):
                entry = tk.Entry(word_frame, width=2, font=self.letter_font, justify='center', relief="solid", bd=2, highlightthickness=2, highlightbackground=DEFAULT_BORDER_COLOR, highlightcolor=BUTTON_COLOR)
                entry.pack(side="left", padx=2)
                self.letter_boxes.append(entry)
                
                # Bind events
                entry.bind("<KeyRelease>", lambda e, idx=len(self.letter_boxes)-1: self.on_key_release(e, idx))
                entry.bind("<Return>", lambda e: self.speak_in_thread(sentence))
                entry.bind("<BackSpace>", lambda e, idx=len(self.letter_boxes)-1: self.on_backspace(e, idx))

        # Focus on the first letter box
        if self.letter_boxes:
            self.letter_boxes[0].focus_set()

        # Automatically speak the sentence after a short delay
        self.root.after(200, lambda: self.speak_in_thread(sentence))

    def on_key_release(self, event, index):
        """Handle character input and focus movement."""
        entry = self.letter_boxes[index]
        # Move to next box if a character is entered
        if event.char.isalnum() and len(entry.get()) > 0:
            if index < len(self.letter_boxes) - 1:
                self.letter_boxes[index + 1].focus_set()
            else:
                # If it's the last box, check the sentence
                self.check_sentence()

    def on_backspace(self, event, index):
        """Handle backspace for focus movement."""
        entry = self.letter_boxes[index]
        if len(entry.get()) == 0 and index > 0:
            self.letter_boxes[index - 1].focus_set()

    def check_sentence(self):
        """Check if the entered letters match the correct sentence."""
        correct_sentence = self.current_sentences[self.current_sentence_index].replace(" ", "").lower()
        user_answer = "".join([box.get() for box in self.letter_boxes]).lower()

        if user_answer == correct_sentence:
            self.handle_correct_answer()
        else:
            self.handle_incorrect_answer()

    def handle_correct_answer(self):
        """Visual feedback for a correct answer and move to the next sentence."""
        for box in self.letter_boxes:
            box.config(state="disabled", disabledbackground=CORRECT_BG_COLOR, relief="flat")
        self.current_sentence_index += 1
        # Wait a moment before showing the next sentence
        self.root.after(1200, self.display_sentence)

    def handle_incorrect_answer(self):
        """Visual feedback for an incorrect answer."""
        for box in self.letter_boxes:
            box.config(highlightbackground=INCORRECT_BORDER_COLOR, highlightcolor=INCORRECT_BORDER_COLOR)
        # Revert the color after a short time
        self.root.after(500, lambda: [box.config(highlightbackground=DEFAULT_BORDER_COLOR, highlightcolor=BUTTON_COLOR) for box in self.letter_boxes])

    def speak_in_thread(self, sentence):
        """Run the TTS and audio playback in a separate thread to avoid freezing the GUI."""
        thread = threading.Thread(target=self.run_async_speak, args=(sentence,))
        thread.daemon = True
        thread.start()

    def run_async_speak(self, sentence):
        """Set up and run the asyncio event loop for edge-tts."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.speak_sentence(sentence))
        loop.close()

    async def speak_sentence(self, sentence):
        """Generate speech using edge-tts and play it with pygame."""
        if pygame.mixer.music.get_busy():
            return # Don't interrupt if already speaking

        try:
            communicate = edge_tts.Communicate(sentence, VOICE)
            audio_buffer = BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])
            
            # Play the audio from the in-memory buffer
            audio_buffer.seek(0)
            pygame.mixer.music.load(audio_buffer)
            pygame.mixer.music.play()
        except Exception as e:
            # Run messagebox in the main thread
            self.root.after(0, lambda: messagebox.showerror("TTS Error", f"Failed to generate or play audio: {e}"))


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ListeningExerciseApp(root)
    # Ensure pygame mixer quits properly when the window is closed
    def on_closing():
        pygame.mixer.quit()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
