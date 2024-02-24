import pygame
import random
import sys
# Load word list from a file
from words import word_list

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman Game")

# Set up fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

word = ""
guessed_letters = set()
MAX_TRIES = 9
tries = 0

# Load background images
background_start = pygame.image.load("./sky.png")
background_start = pygame.transform.scale(background_start, (width, height))

background_game = pygame.image.load("./background.jpg")
background_game = pygame.transform.scale(background_game, (width, height))

def reset_game():
    global word, guessed_letters, tries
    word = random.choice(word_list).upper()
    guessed_letters = set()
    tries = 0

def draw_word():
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = font.render(display_word, True, WHITE)
    win.blit(text, (50, 50))

def draw_hangman(tries):
    head_radius = 25
    parts = [
        (100, 400, 300, 400),  # Base
        (200, 400, 200, 100),  # Pole
        (200, 100, 400, 100),  # Top beam
        (400, 100, 400, 150),  # Rope
        (400, 150, 400, 250),  # Body
        (400, 200, 350, 250),  # Left arm
        (400, 200, 450, 250),  # Right arm
        (400, 250, 350, 300),  # Left leg
        (400, 250, 450, 300),  # Right leg
    ]

    for i in range(tries):
        x1, y1, x2, y2 = parts[i]
        pygame.draw.line(win, WHITE, (x1, y1), (x2, y2), 5)

    if tries >= 5:  # Draw head only if tries are greater than or equal to 5
        pygame.draw.circle(win, WHITE, (400, 175), head_radius)

def display_message(message, font_size, position, color):
    text = pygame.font.Font(None, font_size).render(message, True, color)
    rect = text.get_rect(center=position)
    win.blit(text, rect.topleft)

def game_over_message(message, color):
    display_message(message, 48, (width // 2, height // 2 - 50), color)
    display_message(f"The correct word was: {word}", 36, (width // 2, height // 2 + 50), color)
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the message for 3 seconds
    reset_game()

reset_game()
start_screen = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Quit the game if 'Q' key is pressed
                if not start_screen and 'Q' in word:
                    guessed_letters.add('Q')
                else:
                    pygame.quit()
                    sys.exit()
            elif start_screen:
                start_screen = False
                reset_game()
            elif event.key >= 97 and event.key <= 122:  # Check if it's a lowercase letter
                letter = chr(event.key).upper()
                if letter not in guessed_letters:
                    guessed_letters.add(letter)
                    if letter not in word:
                        tries += 1

    # Draw background image
    if start_screen:
        win.blit(background_start, (0, 0))
        display_message("Welcome to HangMan Game", 68, (width // 2, height // 2 - 50), RED)
        display_message("Press any key to start", 48, (width // 2, height // 2 + 50), RED)
    else:
        win.blit(background_game, (0, 0))
        display_message("Press Q to quit", 28, (width - 80, height - 18), RED)
        draw_word()
        draw_hangman(tries)

        if set(word) <= guessed_letters:
            game_over_message("Congratulations! You guessed the word.", GREEN)
            reset_game()
            start_screen = True
        elif tries >= MAX_TRIES:
            game_over_message("Game over! Press any key to restart", BLUE)
            start_screen = True

    pygame.display.flip()
    pygame.time.Clock().tick(60)