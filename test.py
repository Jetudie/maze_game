import pygame
import random

# Maze parameters
MAZE_WIDTH = 25
MAZE_HEIGHT = 25
CELL_SIZE = 20
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
