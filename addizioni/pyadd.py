import pygame
import random

# Inizializza pygame
pygame.init()

# Costanti
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
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
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

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
                        draw_text("Corretto!", font, GREEN, screen, 300, 500)
                    else:
                        draw_text(f"Sbagliato! La risposta corretta è {correct_answer}.", font, RED, screen, 200, 500)
                    answered = True
                    break
    
    if current_question_index < 10:
        draw_text(f"Domanda {current_question_index + 1}/10", font, BLACK, screen, 20, 20)
        draw_text(f"{num1} + {num2} = ?", font, BLACK, screen, 20, 80)

        option_rects = []
        for i, option in enumerate(options):
            x = 20 + (i % 2) * 200
            y = 200 + (i // 2) * 100
            draw_text(str(option), font, BLACK, screen, x, y)
            option_rect = pygame.Rect(x, y, 100, 50)
            option_rects.append(option_rect)
            pygame.draw.rect(screen, BLACK, option_rect, 2)

        if answered:
            pygame.time.delay(1000)
            current_question_index += 1
            if current_question_index < 10:
                num1, num2, correct_answer, options = generate_question(level)
                answered = False
            else:
                draw_text(f"Hai risposto correttamente a {score} domande su 10.", font, BLACK, screen, 200, 500)
                if score > 7:
                    level += 1
                    draw_text("Ottimo lavoro! Il prossimo test sarà più difficile.", font, BLACK, screen, 150, 550)
                else:
                    level = 1
    else:
        draw_text(f"Hai risposto correttamente a {score} domande su 10.", font, BLACK, screen, 200, 500)
        draw_text("Clicca per ripetere il test", font, BLACK, screen, 250, 550)
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_question_index = 0
            score = 0
            num1, num2, correct_answer, options = generate_question(level)
            answered = False

    pygame.display.flip()

pygame.quit()
