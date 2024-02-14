# Python code to create a simple Pygame application similar to the provided image with sound integration

import pygame
import sys
from array import array

# Initialize Pygame
pygame.init()

# Setup constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
PADDLE_WIDTH, PADDLE_HEIGHT = 75, 15
BALL_SIZE = 12
BLOCK_WIDTH, BLOCK_HEIGHT = 64, 20
BLOCK_ROWS, BLOCK_COLUMNS = 5, 10
FREQUENCY, SIZE, CHANNELS, BUFFER = 22050, -16, 2, 4096

# Colors
BLACK, WHITE, RED, GREEN, BLUE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)
COLORS = [RED, GREEN, BLUE]

# Initialize Pygame mixer
pygame.mixer.init(frequency=FREQUENCY, size=SIZE, channels=CHANNELS, buffer=BUFFER)

# Function to generate square wave sounds
def generate_square_wave(frequency=440, volume=0.1):
    period = int(round(FREQUENCY / frequency))
    amplitude = 2 ** (abs(SIZE) - 1) - 1
    samples = array('h', [amplitude if time < period / 2 else -amplitude for time in range(period)] * int(FREQUENCY / period))
    return pygame.mixer.Sound(buffer=samples)

# Sound effects
beep_sound = generate_square_wave(880, 0.1)
boop_sound = generate_square_wave(440, 0.1)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game with Sound")

# Paddle setup
paddle = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 35), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Ball setup
ball = pygame.Rect((SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2), (BALL_SIZE, BALL_SIZE))
ball_speed = [5, -5]

# Blocks setup
blocks = []
for row in range(BLOCK_ROWS):
    block_color = COLORS[row % len(COLORS)]
    for column in range(BLOCK_COLUMNS):
        block_x = column * (BLOCK_WIDTH + 5) + 20
        block_y = row * (BLOCK_HEIGHT + 5) + 50
        block = pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT)
        blocks.append((block, block_color))

# Game loop
running = True
game_over = False
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    if not game_over:
        # Ball movement
        ball.left += ball_speed[0]
        ball.top += ball_speed[1]

        # Wall collision
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speed[0] = -ball_speed[0]
            beep_sound.play()
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
            beep_sound.play()
        if ball.bottom >= SCREEN_HEIGHT:
            game_over = True

        # Paddle collision
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]
            boop_sound.play()

        # Block collision
        for block, color in blocks[:]:
            if ball.colliderect(block):
                blocks.remove((block, color))
                ball_speed[1] = -ball_speed[1]
                beep_sound.play()
                break

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= 6
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.right += 6

    # Drawing
    screen.fill(BLACK)
    for block, color in blocks:
        pygame.draw.rect(screen, color, block)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, RED, ball)

    # Game over screen
    if game_over:
        font = pygame.font.SysFont(None, 74)
        text = font.render('GAME OVER', True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(30)

# Clean up
pygame.quit()
sys.exit()

