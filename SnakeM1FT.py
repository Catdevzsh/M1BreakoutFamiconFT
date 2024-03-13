import pygame
import random
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE, BLACK, GREEN, RED = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0)

# Game variables
CELL_SIZE = 20
snake = [(100, 100)]
snake_direction = (1, 0)  # Right
food_position = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                 random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
clock = pygame.time.Clock()

# Sound generation function
def generate_square_wave(frequency=440, volume=0.1, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    period = int(sample_rate / frequency)
    amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    waveform = array('h', [int(amplitude if time < period / 2 else -amplitude) for time in range(period)] * int(duration * frequency))
    sound = pygame.mixer.Sound(waveform)
    sound.set_volume(volume)
    return sound

# Generate a beep sound for eating food
eat_food_sound = generate_square_wave(660, 0.1, 0.1)

# Function to move the snake
def move_snake():
    global snake, snake_direction
    head_x, head_y = snake[0]
    new_head = (head_x + snake_direction[0] * CELL_SIZE, head_y + snake_direction[1] * CELL_SIZE)
    snake = [new_head] + snake[:-1]

# Function to handle collision with food
def handle_food_collision():
    global snake, food_position
    if snake[0] == food_position:
        snake.append(snake[-1])
        food_position = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                         random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
        eat_food_sound.play()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)

    # Move snake
    move_snake()

    # Check for collision with food
    handle_food_collision()

    # Drawing
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
