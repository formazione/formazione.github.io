import pygame
import random
import time

# Inizializza pygame
pygame.init()

# Costanti
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (173, 216, 230)
FONT_SIZE = 36

# Impostazioni finestra
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test di Matematica")

# Font
font = pygame.font.Font(None, FONT_SIZE)

# Funzioni
def generate_question(level):
    max_value = level * 10
    num1 = random.randint(1, max_value)
    num2 = random.randint(1, max_value)
    answer = num1 + num2
    options = [answer]
    while len(options) < 4:
        option = random.randint(1, max_value * 2)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return num1, num2, answer, options

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(surface, rect, color, text):
    pygame.draw.rect(surface, color, rect)
    draw_text(text, font, BLACK, surface, rect.centerx, rect.centery)

# Variabili gioco
current_question_index = 0
score = 0
level = 1
num1, num2, correct_answer, options = generate_question(level)
answered = False

# Ciclo principale
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not answered:
            mouse_x, mouse_y = event.pos
            for i, option in enumerate(options):
                if option_rects[i].collidepoint(mouse_x, mouse_y):
                    if option == correct_answer:
                        score += 1
                        draw_button(screen, option_rects[i], GREEN, str(option))
                        draw_text("Corretto!", font, GREEN, screen, WIDTH // 2, HEIGHT - 50)
                    else:
                        draw_button(screen, option_rects[i], RED, str(option))
                        draw_text(f"Sbagliato! La risposta corretta è {correct_answer}.", font, RED, screen, WIDTH // 2, HEIGHT - 50)
                    answered = True
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    break
    
    if current_question_index < 10:
        draw_text(f"Domanda {current_question_index + 1}/10", font, BLACK, screen, WIDTH // 2, 50)
        draw_text(f"{num1} + {num2} = ?", font, BLACK, screen, WIDTH // 2, 150)

        option_rects = []
        for i, option in enumerate(options):
            x = 200 + (i % 2) * 200
            y = 250 + (i // 2) * 100
            rect = pygame.Rect(x, y, 150, 50)
            draw_button(screen, rect, BLUE, str(option))
            option_rects.append(rect)

        if answered:
            current_question_index += 1
            if current_question_index < 10:
                num1, num2, correct_answer, options = generate_question(level)
                answered = False
            else:
                draw_text(f"Hai risposto correttamente a {score} domande su 10.", font, BLACK, screen, WIDTH // 2, HEIGHT - 100)
                if score > 7:
                    level += 1
                    draw_text("Ottimo lavoro! Il prossimo test sarà più difficile.", font, BLACK, screen, WIDTH // 2, HEIGHT - 50)
                else:
                    level = 1
    else:
        draw_text(f"Hai risposto correttamente a {score} domande su 10.", font, BLACK, screen, WIDTH // 2, HEIGHT - 100)
        draw_text("Clicca per ripetere il test", font, BLACK, screen, WIDTH // 2, HEIGHT - 50)
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_question_index = 0
            score = 0
            num1, num2, correct_answer, options = generate_question(level)
            answered = False

    pygame.display.flip()

pygame.quit()
