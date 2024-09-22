import random

def create_grid(height, width):
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    return grid

def place_mines(grid, num_mines):
    height = len(grid)
    width = len(grid[0])
    mines_placed = 0

    while mines_placed < num_mines:
        row = random.randint(0, height - 1)
        col = random.randint(0, width - 1)

        if grid[row][col] != '*':
            grid[row][col] = '*'
            mines_placed += 1

    return grid

def count_nearby_mines(grid, row, col):
    height = len(grid)
    width = len(grid[0])
    count = 0

    for i in range(max(0, row - 1), min(row + 2, height)):
        for j in range(max(0, col - 1), min(col + 2, width)):
            if grid[i][j] == '*':
                count += 1

    return count

def populate_numbers(grid):
    height = len(grid)
    width = len(grid[0])

    for i in range(height):
        for j in range(width):
            if grid[i][j] != '*':
                count = count_nearby_mines(grid, i, j)
                grid[i][j] = str(count)

    return grid

def determine_num_mines(height, width, difficulty):
    total_boxes = height * width
    num_mines = int(total_boxes * difficulty / 100)
    return num_mines

def generate_minefield(height, width, difficulty):
    num_mines = determine_num_mines(height, width, difficulty)
    grid = create_grid(height, width)
    grid = place_mines(grid, int(num_mines) )
    grid = populate_numbers(grid)
    return grid
