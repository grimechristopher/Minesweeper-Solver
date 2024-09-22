import generate_minefield
import minefield_window as mf

import random

class AI:
    def __init__(self, row_length, col_length, mine_pct):
        minefield_button_grid = generate_minefield.generate_minefield(row_length, col_length, mine_pct)
        num_mines = sum(row.count('*') for row in minefield_button_grid)
        self.minefield = mf.Minefield(minefield_button_grid, num_mines, False)

    def make_move(self):
        # Apply deterministic rules
        for row in range(self.minefield.rows):
            for col in range(self.minefield.cols):
                if self.minefield.button_grid[row][col] in '12345678': # if theres mines next to the cell
                    action, cell = self.deterministic(row, col)
                    if action:
                        print("Deterministic")
                        # for i, j in cells:
                        if action == 'f':
                            self.minefield.button_right_clicked(cell[0], cell[1])
                        elif action == 'c':
                            self.minefield.button_clicked(cell[0], cell[1])
                        return

        # If no deterministic rule can be applied, use probabilistic reasoning
        # best_cell = self.probabilistic()
        best_cell = self.apply_random()
        print("Probabilistic", best_cell)
        self.minefield.button_clicked(best_cell[0], best_cell[1])

    def deterministic(self, row, col):
        # Initialize variables
        num_mines = 0
        neighbors = []
        unrevealed_neighbors = []
        flagged_neighbors = []

        # Check if row and col are within bounds of game
        if not (0 <= row < self.minefield.rows and 0 <= col < self.minefield.cols):
            return (None, [])

        cell = self.minefield.button_grid[row][col]

        # If the cell is a number
        if cell.isdigit():
            num_mines = int(cell)
            # Generate neighbor coordinates
            for i in range(max(0, row - 1), min(row + 2, self.minefield.rows)):
                for j in range(max(0, col - 1), min(col + 2, self.minefield.cols)):
                    if (i, j) != (row, col):
                        neighbors.append((i, j))

            # Filter neighbors based on state
            for i, j in neighbors:
                neighbor_state = self.minefield.button_grid[i][j]
                if neighbor_state == ' ':
                    unrevealed_neighbors.append((i, j))
                elif neighbor_state == 'F':
                    flagged_neighbors.append((i, j))

        # If the number of mines is equal to the number of unrevealed neighbors + flagged neighbors, all those neighbors are mines
        if num_mines == len(unrevealed_neighbors) + len(flagged_neighbors):
            if unrevealed_neighbors:
                return ('f', unrevealed_neighbors[0])
            else:
                return (None, [])

        # If the number on the cell is equal to the number of flagged neighbors, all the remaining unrevealed neighbors are safe
        if num_mines == len(flagged_neighbors):
            if unrevealed_neighbors:
                return ('c', unrevealed_neighbors[0])
            else:
                return (None, [])

        return (None, [])

    def probabilistic(self):
        # If the cell at (0, 0) is unrevealed, choose it as the first move
        if self.minefield.button_grid[0][0] == ' ':
            return (0, 0)

        unrevealed_cells = []
        cell_scores = {}
        unrevealed_cells_next_to_number = []

        # Iterate over each cell in the button_grid
        for row in range(self.minefield.rows):
            for col in range(self.minefield.cols):
                # If the cell is unrevealed and not flagged, add it to the list
                if self.minefield.button_grid[row][col] == ' ':
                    unrevealed_cells.append((row, col))

                    # Calculate the score for the cell
                    neighbors = [(i, j) for i in range(max(0, row - 1), min(row + 2, self.minefield.rows))
                                for j in range(max(0, col - 1), min(col + 2, self.minefield.cols))] # Get all neighbors of the cell
                    unrevealed_neighbors = [(i, j) for i, j in neighbors if self.minefield.button_grid[i][j] == ' '] # Get all unrevealed cells ' '
                    numbered_neighbors = [(i, j) for i, j in neighbors if self.minefield.button_grid[i][j].isdigit()] # Get all numbered cells
                    flagged_neighbors = [(i, j) for i, j in neighbors if self.minefield.button_grid[i][j] == 'F'] # Get all flagged cells

                    cell_scores[(row, col)] = (sum(int(self.minefield.button_grid[i][j]) for i, j in numbered_neighbors) - len(flagged_neighbors)) / len(unrevealed_neighbors) if unrevealed_neighbors else 0

                    # If the cell is next to a number, add it to the list
                    if numbered_neighbors:
                        unrevealed_cells_next_to_number.append((row, col))

        # If there are any unrevealed cells next to a number, choose the one with the lowest score
        if unrevealed_cells_next_to_number:
            min_score = min(cell_scores.values())
            min_cells = [cell for cell, score in cell_scores.items() if score == min_score]
            return random.choice(min_cells)

        # If there are no unrevealed cells next to a number, choose the one with the lowest score
        elif unrevealed_cells:
            min_score = min(cell_scores.values())
            min_cells = [cell for cell, score in cell_scores.items() if score == min_score]
            return random.choice(min_cells)

        # If there are no unrevealed cells, return None
        return None

    def apply_random(self):
        unrevealed_cells = []
        for row in range(self.minefield.rows):
            for col in range(self.minefield.cols):
                if self.minefield.button_grid[row][col] == ' ':
                    unrevealed_cells.append((row, col))
        return random.choice(unrevealed_cells)

if __name__ == "__main__":
    games = 0
    wins = 0
    while games < 1000:
        ai = AI(10, 10, 15)
        while not ai.minefield.game_over:
            ai.make_move()
        if ai.minefield.has_won:
            wins += 1
        unrevealed_count = sum(row.count(' ') for row in ai.minefield.button_grid)
        if unrevealed_count < ai.minefield.cols * ai.minefield.rows - 1:
            games += 1
    print(wins)