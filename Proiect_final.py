import random

# Constants
MAZE_WIDTH = 40
MAZE_HEIGHT = 30
PLAYER_SYMBOL = '@'
WALL_SYMBOL = '#'
PATH_SYMBOL = ' '
GOAL_SYMBOL = '$'
KEY_SYMBOL = '*'
DOOR_SYMBOL = '+'
LOCK_SYMBOL = '!'

# Game state
player_x = 1
player_y = 1
keys_collected = 0
goal_reached = False
doors_unlocked = 0

# Create the maze
maze = [[WALL_SYMBOL for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]

# Carve out the maze using recursive backtracking
def carve_maze(x, y):
    maze[y][x] = PATH_SYMBOL
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x, new_y = x + dx * 2, y + dy * 2
        if 0 < new_x < MAZE_WIDTH - 1 and 0 < new_y < MAZE_HEIGHT - 1 and maze[new_y][new_x] == WALL_SYMBOL:
            maze[y + dy][x + dx] = PATH_SYMBOL
            carve_maze(new_x, new_y)

carve_maze(1, 1)

# Place the goal and key
goal_x, goal_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
while maze[goal_y][goal_x] != PATH_SYMBOL:
    goal_x, goal_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
maze[goal_y][goal_x] = GOAL_SYMBOL

key_x, key_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
while maze[key_y][key_x] != PATH_SYMBOL or (key_x, key_y) == (goal_x, goal_y):
    key_x, key_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
maze[key_y][key_x] = KEY_SYMBOL

# Place doors and locks
door_x, door_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
while maze[door_y][door_x] != PATH_SYMBOL:
    door_x, door_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
maze[door_y][door_x] = DOOR_SYMBOL

lock_x, lock_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
while maze[lock_y][lock_x] != PATH_SYMBOL or (lock_x, lock_y) == (door_x, door_y):
    lock_x, lock_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
maze[lock_y][lock_x] = LOCK_SYMBOL

# Game loop
while True:
    # Clear the screen
    print("\033[H\033[J", end="")

    # Draw the maze
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if x == player_x and y == player_y:
                print(PLAYER_SYMBOL, end="")
            elif maze[y][x] == DOOR_SYMBOL and keys_collected >= doors_unlocked:
                print(LOCK_SYMBOL, end="")
            elif maze[y][x] == DOOR_SYMBOL and keys_collected < doors_unlocked:
                print(DOOR_SYMBOL, end="")
            elif maze[y][x] == LOCK_SYMBOL:
                print(LOCK_SYMBOL, end="")
            else:
                print(maze[y][x], end="")
        print()

    # Check for win condition
    if player_x == goal_x and player_y == goal_y:
        if keys_collected > 0:
            print("You win!")
            break
        else:
            print("You need to find the key first.")

    # Get user input
    move = input("Enter your move (w/a/s/d): ")

    # Initialize new_x and new_y
    new_x, new_y = player_x, player_y

    # Update new_x and new_y based on the move
    if move == "w":
        new_y -= 1
    elif move == "s":
        new_y += 1
    elif move == "a":
        new_x -= 1
    elif move == "d":
        new_x += 1
    else:
        continue

    # Check if the new position is valid
    if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != WALL_SYMBOL:
        player_x, player_y = new_x, new_y
        if maze[new_y][new_x] == KEY_SYMBOL:
            keys_collected += 1
            maze[new_y][new_x] = PATH_SYMBOL
            print("You collected a key!")
        elif maze[new_y][new_x] == DOOR_SYMBOL:
            if keys_collected > 0:
                keys_collected -= 1
                doors_unlocked += 1
                maze[new_y][new_x] = PATH_SYMBOL
                print("You unlocked a door!")
            else:
                print("You need a key to unlock this door.")
    else:
        print("You cannot move there.")
