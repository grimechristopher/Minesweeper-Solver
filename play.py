import generate_minefield
import start_menu as sm
import minefield_window as mf


def print_grid(grid):
    # print the row index at the beginning of each row
    print('    ' + ' '.join(str(i) for i in range(len(grid[0]))))
    print('-' * (len(grid[0]) * 2 + 3))
    for i, row in enumerate(grid):
        print(str(i) + ' | ', end='')
        print(' '.join(row))
    print()
    # print the column index at the bottom of the grid

def main(height=None, width=None, difficulty=None, gui=True):
    # Example usage:
    if not height or not width or not difficulty:
        start_menu = sm.StartMenu()
        start_menu.create_window()
        # Get user input and save variables to generate grid
        grid_height = start_menu.height
        grid_width = start_menu.width
        grid_difficulty = start_menu.difficulty
    else:
        grid_height = height
        grid_width = width
        grid_difficulty = difficulty

    # Generate grid
    minefield_grid = generate_minefield.generate_minefield(grid_height, grid_width, grid_difficulty)

    num_mines = sum(row.count('*') for row in minefield_grid)

    minefield = mf.Minefield(minefield_grid, num_mines, gui)
    minefield.run()

if __name__ == "__main__":
    # main()
    # main(10,10,15,True) # With GUI
    main(10,10,15,False)