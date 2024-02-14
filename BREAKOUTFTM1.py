import pygame
import sys
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")

# Colors
BLACK, WHITE, RED, GREEN, BLUE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)

# Game variables
paddle_width, paddle_height = 100, 20
ball_diameter = 20
ball_radius = ball_diameter // 2
brick_width, brick_height = 75, 30
num_bricks_per_row = SCREEN_WIDTH // (brick_width + 10)
num_rows_of_bricks = 5
paddle = pygame.Rect(SCREEN_WIDTH // 2 - paddle_width // 2, SCREEN_HEIGHT - paddle_height - 10, paddle_width, paddle_height)
ball = pygame.Rect(SCREEN_WIDTH // 2 - ball_radius, SCREEN_HEIGHT // 2 - ball_radius, ball_diameter, ball_diameter)
ball_speed = [5, -5]
bricks = []

# Sound generation function
def generate_square_wave(frequency=440, volume=0.1, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    period = int(sample_rate / frequency)
    amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    waveform = array('h', [int(amplitude if time < period / 2 else -amplitude) for time in range(period)] * int(duration * frequency))
    sound = pygame.mixer.Sound(waveform)
    sound.set_volume(volume)
    return sound

# Predefined sounds
hit_paddle_sound = generate_square_wave(660, 0.1, 0.1)
break_brick_sound = generate_square_wave(440, 0.1, 0.1)
game_over_sound = generate_square_wave(220, 0.1, 0.5)

# Function to reset the game
def reset_game():
    global ball_speed, paddle, ball, bricks
    paddle.left = SCREEN_WIDTH // 2 - paddle_width // 2
    ball.left = SCREEN_WIDTH // 2 - ball_radius
    ball.top = SCREEN_HEIGHT // 2 - ball_radius
    ball_speed = [5, -5]
    bricks = [pygame.Rect(x * (brick_width + 10), y * (brick_height + 5) + 50, brick_width, brick_height) for y in range(num_rows_of_bricks) for x in range(num_bricks_per_row)]

reset_game()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-10, 0)
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.move_ip(10, 0)

    # Ball movement
    ball.move_ip(ball_speed)
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed[0] = -ball_speed[0]
        hit_paddle_sound.play()
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
        hit_paddle_sound.play()
    if ball.bottom >= SCREEN_HEIGHT:
        game_over_sound.play()
        reset_game()

    # Ball and paddle collision
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
        hit_paddle_sound.play()

    # Ball and bricks collision
    brick_collision_index = ball.collidelist(bricks)
    if brick_collision_index >= 0:
        brick = bricks.pop(brick_collision_index)
        ball_speed[1] = -ball_speed[1]
        break_brick_sound.play()

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.circle(screen, RED, ball.center, ball_radius)
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()
