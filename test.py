import pygame
import random

# Maze parameters
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
CELL_SIZE = 30
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
maze = []
for i in range(MAZE_HEIGHT):
    row = []
    for j in range(MAZE_WIDTH):
        if i == 0 or i == MAZE_HEIGHT - 1 or j == 0 or j == MAZE_WIDTH - 1:
            row.append(1)  # Boundary walls
        elif i % 2 == 0 and j % 2 == 0:
            row.append(1)  # Inner walls
        else:
            row.append(0)  # Path
    maze.append(row)

# Recursive backtracking algorithm to generate the maze


def generate_maze(x, y):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 1:
            maze[y + dy // 2][x + dx // 2] = 0
            maze[ny][nx] = 0
            generate_maze(nx, ny)


generate_maze(1, 1)

# Randomly block certain routes to ensure only one path to the destination
for i in range(2, MAZE_HEIGHT - 1, 2):
    for j in range(2, MAZE_WIDTH - 1, 2):
        if random.random() < 0.3:
            if maze[i][j - 1] == 0 and maze[i][j + 1] == 0:
                maze[i][j] = 1
            elif maze[i - 1][j] == 0 and maze[i + 1][j] == 0:
                maze[i][j] = 1

# Player starting position
player_x = 1
player_y = 1

# Destination position
destination_x = MAZE_WIDTH - 2
destination_y = MAZE_HEIGHT - 2

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and maze[player_y - 1][player_x] == 0:
                player_y -= 1
            elif event.key == pygame.K_DOWN and maze[player_y + 1][player_x] == 0:
                player_y += 1
            elif event.key == pygame.K_LEFT and maze[player_y][player_x - 1] == 0:
                player_x -= 1
            elif event.key == pygame.K_RIGHT and maze[player_y][player_x + 1] == 0:
                player_x += 1

    window.fill(BLACK)

    # Draw the maze
    for i in range(MAZE_HEIGHT):
        for j in range(MAZE_WIDTH):
            if maze[i][j] == 1:
                pygame.draw.rect(window, WHITE, (j * CELL_SIZE,
                                 i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the player
    pygame.draw.rect(window, GREEN, (player_x * CELL_SIZE,
                     player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the destination
    pygame.draw.rect(window, RED, (destination_x * CELL_SIZE,
                     destination_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Check if the player has reached the destination
    if player_x == destination_x and player_y == destination_y:
        font = pygame.font.Font(None, 36)
        text = font.render("You Win!", True, WHITE)
        text_rect = text.get_rect(
            center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)
        running = False

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
