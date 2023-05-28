import pygame
import random
import csv

# Maze parameters
MAZE_WIDTH = 11
MAZE_HEIGHT = 11
CELL_SIZE = 40
WALL_THICKNESS = 4

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the display
window_width = MAZE_WIDTH * CELL_SIZE
window_height = MAZE_HEIGHT * CELL_SIZE
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Maze Game")

# Generate the maze
# Initialize with all walls
maze = [[1] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]


def generate_maze(x, y):
    maze[y][x] = 0  # Mark current cell as a path

    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 1:
            maze[y + dy // 2][x + dx // 2] = 0
            maze[ny][nx] = 0
            generate_maze(nx, ny)

            # Add random extra paths
            if random.random() < 0.2:
                random_direction = random.choice(directions)
                extra_nx, extra_ny = nx + \
                    random_direction[0], ny + random_direction[1]
                if 0 <= extra_nx < MAZE_WIDTH and 0 <= extra_ny < MAZE_HEIGHT and maze[extra_ny][extra_nx] == 1:
                    maze[ny][nx] = 0
                    maze[extra_ny][extra_nx] = 0
                    generate_maze(extra_nx, extra_ny)


generate_maze(1, 1)

# Randomly block certain routes to ensure only one path to the destination
for i in range(2, MAZE_HEIGHT - 1, 2):
    for j in range(2, MAZE_WIDTH - 1, 2):
        if maze[i][j] == 0 and random.random() < 0.3:
            neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
            random.shuffle(neighbors)
            blocked = False
            for nx, ny in neighbors:
                if maze[ny][nx] == 1:
                    maze[ny][nx] = 1
                    blocked = True
                    break
            if not blocked:
                maze[i][j] = 1

# Player starting position
player_x = 1
player_y = 1

# Destination position
destination_x = MAZE_WIDTH - 2
destination_y = MAZE_HEIGHT - 2

# Load questions, choices, and answers from CSV file
questions = []
choices = []
answers = []

with open("QA.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        question = row["Question"]
        choice1 = row["Choice 1"]
        choice2 = row["Choice 2"]
        choice3 = row["Choice 3"]
        answer = row["Answer"]

        choices.append([choice1, choice2, choice3])
        questions.append(question)
        answers.append(answer)

# Game states
GAME_STATE_MAZE = 0
GAME_STATE_QUESTION = 1

# Set initial game state
game_state = GAME_STATE_MAZE

# Initialize the result
result = ""
score = 0
score_per_question = 5

# Initialize font for displaying Chinese characters
font = pygame.font.Font("msjhbd.ttc", 24)

# Initialize mouse button states
left_button_down = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            left_button_down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            left_button_down = False
            if game_state == GAME_STATE_QUESTION:
                # Get the mouse position
                mouse_x, mouse_y = event.pos

                # Check if the mouse click is within the answer choices area
                if 20 <= mouse_x <= window_width - 20 and 60 <= mouse_y <= window_height - 50:
                    # Calculate the index of the clicked choice
                    choice_index = (mouse_y - 60) // 30

                    # Check if the choice index is within the available choices
                    if 0 <= choice_index < len(choices[0]):
                        # Process user answer based on the choice index
                        if choices[0][choice_index] == answers[0]:
                            result = "Correct!"
                            score += score_per_question
                        else:
                            result = "Wrong!"

                        # Remove the answered question
                        questions.pop(0)
                        choices.pop(0)
                        answers.pop(0)

                        # Transition back to the maze state if there are more questions
                        if len(questions) > 0:
                            game_state = GAME_STATE_MAZE
        elif event.type == pygame.KEYDOWN:
            if game_state == GAME_STATE_MAZE:
                if event.key == pygame.K_UP and maze[player_y - 1][player_x] == 0:
                    player_y -= 1
                elif event.key == pygame.K_DOWN and maze[player_y + 1][player_x] == 0:
                    player_y += 1
                elif event.key == pygame.K_LEFT and maze[player_y][player_x - 1] == 0:
                    player_x -= 1
                elif event.key == pygame.K_RIGHT and maze[player_y][player_x + 1] == 0:
                    player_x += 1
            else:
                continue
    window.fill(BLACK)

    if game_state == GAME_STATE_MAZE:
        # Draw the maze
        for i in range(MAZE_HEIGHT):
            for j in range(MAZE_WIDTH):
                if maze[i][j] == 1:
                    pygame.draw.rect(
                        window, WHITE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the player
        pygame.draw.rect(window, GREEN, (player_x * CELL_SIZE,
                         player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the destination
        pygame.draw.rect(window, RED, (destination_x * CELL_SIZE,
                         destination_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Check if the player has reached the destination
        if player_x == destination_x and player_y == destination_y:
            game_state = GAME_STATE_QUESTION

    elif game_state == GAME_STATE_QUESTION:
        if len(questions) > 0:
            # Render question and choices
            question_text = font.render(questions[0], True, WHITE)
            window.blit(question_text, (20, 20))

            choice_texts = []
            for i, choice in enumerate(choices[0]):
                choice_text = font.render(f"{i+1}. {choice}", True, WHITE)
                choice_texts.append(choice_text)
                window.blit(choice_text, (20, 60 + i * 30))

            # Render result
            if result == "Correct!":
                result_text_color = GREEN
            else:
                result_text_color = RED

            score_result = f"score={score}"
            result_text = font.render(result, True, result_text_color)
            result_text_2 = font.render(score_result, True, WHITE)
            window.blit(result_text, (20, window_height - 100))
            window.blit(result_text_2, (20, window_height - 50))
        else:
            # If no more questions, display game over message
            game_over_text = font.render(
                f"Game Over!\nScore={score}", True, WHITE)
            window.blit(game_over_text, (20, 20))

            # Render final result
            final_result_text = font.render(
                "Congratulations, you completed the game!", True, WHITE)
            window.blit(final_result_text, (20, 60))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
