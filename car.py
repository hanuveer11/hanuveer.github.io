import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 1000
CAR_WIDTH = 40
CAR_HEIGHT = 80
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 60
FPS = 60  
SPACE_REDUCTION_DURATION = 2000  # Duration in milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLOCK_COLOR = (50, 50, 50)
TRANSPARENT_GRAY = (50, 50, 50, 180)  # RGBA for semi-transparent gray

# Load images
PLAYER_CAR = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
PLAYER_CAR.fill(GREEN)
BACKGROUND_IMAGE = pygame.image.load('background.jpg')  # Load your background image
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit the screen

# Obstacle class
class Obstacle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        self.y = -OBSTACLE_HEIGHT

    def update(self, speed):
        self.y += speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

def reset_game():
    return {
        "player_x": SCREEN_WIDTH // 2 - CAR_WIDTH // 2,
        "player_y": SCREEN_HEIGHT - CAR_HEIGHT - 10,
        "obstacles": [],
        "score": 0,
        "high_score": 0,
        "game_over": False,
        "car_speed": 5,  # Initial speed of the car
        "speed_reduction_time": 0,  # Timer for speed reduction
        "countdown_start": False,  # Track countdown state
        "countdown_time": 0,  # Timer for countdown
        "game_over_time": 0  # Timer for game over
    }

def draw_road(screen):
    screen.fill(BLACK)
    lane_width = SCREEN_WIDTH // 2
    for i in range(1, 4):
        pygame.draw.rect(screen, WHITE, (i * lane_width - 5, 0, 10, SCREEN_HEIGHT))

def draw_score(screen, score, high_score):
    font = pygame.font.SysFont(None, 36)
    score_bg = pygame.Rect(10, 10, 180, 40)
    high_score_bg = pygame.Rect(10, 60, 180, 40)
    pygame.draw.rect(screen, BLOCK_COLOR, score_bg)
    pygame.draw.rect(screen, BLOCK_COLOR, high_score_bg)
    screen.blit(font.render(f'Score: {score}', True, WHITE), (20, 15))
    screen.blit(font.render(f'High Score: {high_score}', True, WHITE), (20, 65))

def check_collision(player_rect, obstacles):
    return any(player_rect.colliderect(pygame.Rect(obstacle.x, obstacle.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)) for obstacle in obstacles)

def draw_start_screen(screen):
    screen.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the background image

    # Create a transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(TRANSPARENT_GRAY)  # Fill overlay with semi-transparent gray
    screen.blit(overlay, (0, 0))  # Draw the overlay on the screen

    font = pygame.font.SysFont(None, 74)
    title_text = font.render('CAR GAME', True, WHITE)
    instructions_text = font.render('Press Start to Begin', True, WHITE)

    # Define start button with a border
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
    border_rect = button_rect.inflate(10, 10)  # Create a slightly larger rectangle for the border

    # Draw border and button
    pygame.draw.rect(screen, WHITE, border_rect)  # White border around the button
    pygame.draw.rect(screen, GREEN, button_rect)  # Button background
    button_text = font.render('Start', True, BLACK)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))

    # Draw the title and instructions on the overlay
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    pygame.display.flip()
    return button_rect

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game_state = reset_game()
    game_started = False  # Track if the game has started

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Check for mouse click on start button
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                mouse_pos = event.pos
                button_rect = draw_start_screen(screen)  # Draw the start screen and get button rect
                if button_rect.collidepoint(mouse_pos):  # If the start button is clicked
                    game_started = True  # Set game started to true
                    game_state["countdown_start"] = True  # Begin countdown
                    game_state["countdown_time"] = 3000  # 3 seconds countdown

        if not game_started:
            draw_start_screen(screen)  # Show start screen until the game starts
            continue

        if game_state["countdown_start"]:
            # Countdown logic
            if game_state["countdown_time"] > 0:
                screen.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the background image
                font = pygame.font.SysFont(None, 74)
                countdown_text = font.render(str(game_state["countdown_time"] // 1000), True, WHITE)
                screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                game_state["countdown_time"] -= clock.get_time()  # Reduce the countdown time
                clock.tick(FPS)
                continue  # Skip to the next iteration to avoid drawing the game screen

            # Countdown finished, reset game state
            game_state["countdown_start"] = False
            game_state = reset_game()  # Reset game state after countdown

        if not game_state["game_over"]:
            keys = pygame.key.get_pressed()
            # Control car movement
            if keys[pygame.K_LEFT] and game_state["player_x"] > 0:
                game_state["player_x"] -= game_state["car_speed"]
            if keys[pygame.K_RIGHT] and game_state["player_x"] < SCREEN_WIDTH - CAR_WIDTH:
                game_state["player_x"] += game_state["car_speed"]
            # Control car speed with up and down arrows
            if keys[pygame.K_UP]:
                game_state["car_speed"] = min(15, game_state["car_speed"] + 0.75)  # Increase speed
            if keys[pygame.K_DOWN]:
                game_state["car_speed"] = max(1, game_state["car_speed"] - 0.75)  # Decrease speed

            # Brake with space bar (temporary reduction)
            if keys[pygame.K_SPACE] and game_state["speed_reduction_time"] == 0:
                original_speed = game_state["car_speed"]
                game_state["car_speed"] = max(1, original_speed - 2)  # Apply brake
                game_state["speed_reduction_time"] = pygame.time.get_ticks()  # Start timer

            # Restore speed after duration
            if game_state["speed_reduction_time"] != 0:
                if pygame.time.get_ticks() - game_state["speed_reduction_time"] >= SPACE_REDUCTION_DURATION:
                    game_state["car_speed"] = original_speed  # Restore original speed
                    game_state["speed_reduction_time"] = 0  # Reset timer

            # Add and update obstacles
            if random.randint(1, 30) == 1:
                game_state["obstacles"].append(Obstacle())
            for obstacle in game_state["obstacles"]:
                obstacle.update(game_state["car_speed"])
            game_state["obstacles"] = [obstacle for obstacle in game_state["obstacles"] if obstacle.y < SCREEN_HEIGHT]

            # Check for collisions
            player_rect = pygame.Rect(game_state["player_x"], game_state["player_y"], CAR_WIDTH, CAR_HEIGHT)
            if check_collision(player_rect, game_state["obstacles"]):
                game_state["game_over"] = True
                game_state["game_over_time"] = pygame.time.get_ticks()  # Record the time when game over occurs

            # Increment score and update high score
            game_state["score"] += 1
            game_state["high_score"] = max(game_state["high_score"], game_state["score"])

        draw_road(screen)
        screen.blit(PLAYER_CAR, (game_state["player_x"], game_state["player_y"]))
        for obstacle in game_state["obstacles"]:
            obstacle.draw(screen)
        draw_score(screen, game_state["score"], game_state["high_score"])

        if game_state["game_over"]:
            font = pygame.font.SysFont(None, 74)
            small_font = pygame.font.SysFont(None, 36)
            
            # Blink logic for 'GAME OVER'
            current_time = pygame.time.get_ticks()
            if (current_time // 500) % 2 == 0:  # Blink every 500 ms
                game_over_text = font.render('GAME OVER', True, (255, 0, 0))  # Red color
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

            # Check if 1 second has passed since game over
            if current_time - game_state["game_over_time"] > 1000:  # 1000 ms = 1 second
                # Display 'Press R to play again'
                press_r_text = small_font.render('Press R to play again', True, WHITE)
                screen.blit(press_r_text, (SCREEN_WIDTH // 2 - press_r_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:  # Restart game if 'R' is pressed
                game_state = reset_game()  # Reset the game state
                game_state["game_over"] = False  # Reset game over state
                continue  # Skip to the next iteration

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
 
