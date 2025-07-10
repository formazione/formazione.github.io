import pygame
import screen_manager

# Game variables
player_x = 400
player_y = 300
player_speed = 5

def update_game():
    """Update game logic each frame"""
    global player_x, player_y
    
    # Get pressed keys
    keys = pygame.key.get_pressed()
    
    # Move player based on arrow keys
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed
    
    # Keep player on screen
    player_x = max(25, min(775, player_x))
    player_y = max(25, min(575, player_y))

def draw_game(screen):
    """Draw everything to the screen"""
    # Draw player as a white rectangle
    pygame.draw.rect(screen, (255, 255, 255), (player_x - 25, player_y - 25, 50, 50))
    
    # Draw some UI text
    font = pygame.font.Font(None, 36)
    text = font.render("Use WASD or Arrow Keys to Move", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def handle_events(event):
    """Handle specific events"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            screen_manager.stop()
        elif event.key == pygame.K_SPACE:
            print("Space pressed!")

def main():
    # Initialize the screen
    screen_manager.init_screen(800, 600, "My Game", 60)
    
    # Set background color to dark blue
    screen_manager.set_background((0, 0, 50))
    
    # Set up game functions
    screen_manager.set_update(update_game)
    screen_manager.set_draw(draw_game)
    screen_manager.set_events(handle_events)
    
    # Start the game loop
    screen_manager.loop()

if __name__ == "__main__":
    main()