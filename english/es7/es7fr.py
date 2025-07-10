import pygame
import random
import asyncio
import edge_tts
import os
import threading
import time

# --- CONFIGURATION ---

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
BLUE = (50, 100, 200)
GREEN = (0, 150, 0)
RED = (200, 0, 0)

# Audio configuration
VOICE = "fr-FR-DeniseNeural"
OUTPUT_FILE = "temp_audio_pygame.mp3"

# Sentence list
MASTER_SENTENCE_LIST = [
    "Le soleil est chaud", "Mon chien est grand", "Je peux courir vite", "Elle a une voiture rouge", "Nous aimons jouer",
    "Il est mon ami", "Le chat est petit", "Je vois un oiseau", "Ceci est un livre", "J'ai un stylo",
    "Le ciel est bleu", "J'aime ma maman", "Il peut sauter haut", "La balle est ronde", "Nous mangeons du poisson",
    "Elle chante bien", "L'arbre est grand", "Je bois du lait", "Il a un vélo bleu", "Je m'appelle Tom",
    "Je vais à l'école", "L'herbe est verte", "J'ai deux mains", "Elle aime lire", "Nous jouons à un jeu"
]

# --- PYGAME APPLICATION CLASS ---

class ListeningApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Exercice d'Écoute en Français")
        self.clock = pygame.time.Clock()
        self.running = True

        # --- Fonts ---
        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 32)
        self.feedback_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 30)

        # --- Game State ---
        self.current_sentences = []
        self.current_sentence_index = -1
        self.correct_answers = 0
        self.user_text = ""
        self.feedback_text = ""
        self.feedback_color = BLACK
        self.feedback_timer = 0
        self.game_state = "menu"  # menu, playing, finished

        # --- UI Elements ---
        self.input_box = pygame.Rect(150, 250, 500, 40)
        self.listen_button_rect = pygame.Rect(325, 180, 150, 50)
        self.check_button_rect = pygame.Rect(325, 320, 150, 50)
        self.new_exercise_button_rect = pygame.Rect(300, 400, 200, 50)
        
    async def generate_audio(self, text):
        """Generates audio file using edge-tts."""
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(OUTPUT_FILE)
        except Exception as e:
            print(f"Error generating audio: {e}")
            self.feedback_text = "Erreur audio. Vérifiez la connexion."
            self.feedback_color = RED

    def play_audio(self):
        """Loads and plays the generated audio file."""
        if os.path.exists(OUTPUT_FILE):
            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()
        else:
            print(f"Audio file not found: {OUTPUT_FILE}")

    def speak_sentence_threaded(self, text):
        """Runs audio generation and playback in a separate thread to avoid freezing the GUI."""
        def target():
            asyncio.run(self.generate_audio(text))
            # Wait for mixer to be free
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            self.play_audio()

        thread = threading.Thread(target=target)
        thread.start()

    def start_new_exercise(self):
        self.current_sentences = random.sample(MASTER_SENTENCE_LIST, 5)
        self.current_sentence_index = 0
        self.correct_answers = 0
        self.game_state = "playing"
        self.next_sentence()

    def next_sentence(self):
        if self.current_sentence_index < len(self.current_sentences):
            self.user_text = ""
            self.feedback_text = ""
            self.speak_sentence_threaded(self.current_sentences[self.current_sentence_index])
        else:
            self.game_state = "finished"
            self.feedback_text = f"Score final : {self.correct_answers} / {len(self.current_sentences)}"
            self.feedback_color = BLUE

    def check_answer(self):
        if self.game_state != "playing":
            return
            
        user_answer = self.user_text.strip().lower()
        correct_answer = self.current_sentences[self.current_sentence_index].lower()

        if user_answer == correct_answer:
            self.correct_answers += 1
            self.feedback_text = "✅ Correct ! Excellent."
            self.feedback_color = GREEN
            self.current_sentence_index += 1
            # Use pygame's timer event to delay moving to the next sentence
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500, True)
        else:
            self.feedback_text = "❌ Incorrect. Essayez encore."
            self.feedback_color = RED
            self.feedback_timer = time.time() # Start timer to clear feedback

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.USEREVENT + 1: # Custom event for next sentence
                self.next_sentence()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "playing":
                    if self.listen_button_rect.collidepoint(event.pos):
                        self.speak_sentence_threaded(self.current_sentences[self.current_sentence_index])
                    if self.check_button_rect.collidepoint(event.pos):
                        self.check_answer()
                if self.game_state in ["menu", "finished"]:
                     if self.new_exercise_button_rect.collidepoint(event.pos):
                        self.start_new_exercise()

            if event.type == pygame.KEYDOWN and self.game_state == "playing":
                if event.key == pygame.K_RETURN:
                    self.check_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode

    def draw_text(self, text, font, color, x, y, center=True):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(LIGHT_GRAY)

        if self.game_state == "menu":
            self.draw_text("Exercice d'Écoute", self.title_font, BLACK, WIDTH // 2, 100)
            # Draw "New Exercise" button
            pygame.draw.rect(self.screen, BLUE, self.new_exercise_button_rect, border_radius=10)
            self.draw_text("Nouvel Exercice", self.button_font, WHITE, self.new_exercise_button_rect.centerx, self.new_exercise_button_rect.centery)

        elif self.game_state == "playing":
            # Draw progress
            progress_text = f"Phrase {self.current_sentence_index + 1} sur {len(self.current_sentences)}"
            self.draw_text(progress_text, self.title_font, BLACK, WIDTH // 2, 100)
            
            # Draw Listen button
            pygame.draw.rect(self.screen, BLUE, self.listen_button_rect, border_radius=10)
            self.draw_text("🔊 Écouter", self.button_font, WHITE, self.listen_button_rect.centerx, self.listen_button_rect.centery)

            # Draw input box
            pygame.draw.rect(self.screen, WHITE, self.input_box)
            pygame.draw.rect(self.screen, BLACK, self.input_box, 2, border_radius=5)
            self.draw_text(self.user_text, self.label_font, BLACK, self.input_box.x + 10, self.input_box.centery, center=False)

            # Draw Check button
            pygame.draw.rect(self.screen, GREEN, self.check_button_rect, border_radius=10)
            self.draw_text("Vérifier", self.button_font, WHITE, self.check_button_rect.centerx, self.check_button_rect.centery)

        elif self.game_state == "finished":
            # Draw "New Exercise" button
            pygame.draw.rect(self.screen, BLUE, self.new_exercise_button_rect, border_radius=10)
            self.draw_text("Recommencer", self.button_font, WHITE, self.new_exercise_button_rect.centerx, self.new_exercise_button_rect.centery)

        # Draw feedback text
        if self.feedback_text:
             # Clear incorrect feedback after a few seconds
            if self.feedback_color == RED and time.time() - self.feedback_timer > 2:
                self.feedback_text = ""
            else:
                self.draw_text(self.feedback_text, self.feedback_font, self.feedback_color, WIDTH // 2, 500)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()
        
        # Cleanup
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        pygame.quit()

# --- EXECUTION ---
if __name__ == "__main__":
    app = ListeningApp()
    app.run()
