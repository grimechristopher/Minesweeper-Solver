import tkinter as tk
import tkinter.messagebox as messagebox

class Minefield:
    def __init__(self, grid, num_mines, gui=True):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.num_mines = num_mines
        self.flag_mode = False
        self.gui = gui
        self.game_over = False
        self.has_won = False
        self.button_grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

        self.root = tk.Tk()

        # Create a label for the number of mines and a button for the flag mode
        self.mines_label = tk.Label(self.root, text=f"Mines: {self.num_mines}")
        self.mines_label.grid(row=0, column=0, columnspan=self.cols)

        self.flag_button = tk.Button(self.root, text="Click Mode", command=self.toggle_flag_mode)
        self.flag_button.grid(row=1, column=0, columnspan=self.cols)

        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                button = tk.Button(self.root, text=" ", width=2, command=lambda row=i, col=j: self.button_clicked(row, col))
                button.bind('<Button-3>', lambda event, row=i, col=j: self.button_right_clicked(row, col))
                button.grid(row=i + 2, column=j)
                self.buttons[i][j] = button

    def button_clicked(self, row, col):
        if self.flag_mode:
            # In flag mode, place or remove a flag
            current_text = self.buttons[row][col]['text']
            if current_text == "F":
                # If there's already a flag, remove it and enable the button
                self.buttons[row][col].config(text=" ", state=tk.NORMAL)
            else:
                # If there's no flag, place one and disable the button
                self.buttons[row][col].config(text="F", state=tk.NORMAL)
        else:
            # In click mode, ignore clicks on flagged cells
            current_text = self.buttons[row][col]['text']
            if current_text == "F":
                return

            # Uncover the cell
            value = self.grid[row][col]

            if value == "0":
                self.uncover_adjacent_cells(row, col)
            else:
                self.buttons[row][col].config(text=str(value), relief=tk.SUNKEN)

            if value == "*":
                # If the cell is a mine, show a message and end the game
                if (self.gui):
                    messagebox.showinfo("Boom!", "Game over!")
                else:
                    print("Boom! Game over!")
                    self.print_current_board()
                self.game_over = True
                return


        self.print_current_board()
        self.check_for_win()

    def button_right_clicked(self, row, col):
        current_text = self.buttons[row][col]['text']
        if current_text == "F":
            # If there's already a flag, remove it and enable the button
            self.buttons[row][col].config(text=" ", state=tk.NORMAL)
            self.grid[row][col] = " "
        else:
            # If there's no flag, place one and disable the button
            self.buttons[row][col].config(text="F", state=tk.DISABLED)
            self.grid[row][col] = "F"

        self.print_current_board()

    def uncover_adjacent_cells(self, row, col):
        if self.buttons[row][col]['relief'] == tk.SUNKEN or self.buttons[row][col]['text'] == "F":
            return

        value = self.grid[row][col]
        if value == "0":
            self.buttons[row][col].config(text=" ", relief=tk.SUNKEN)
        else :
            self.buttons[row][col].config(text=str(value), relief=tk.SUNKEN)

        if value != "0":
            return

        for i in range(max(0, row - 1), min(row + 2, self.rows)):
            for j in range(max(0, col - 1), min(col + 2, self.cols)):
                self.uncover_adjacent_cells(i, j)

    def toggle_flag_mode(self):
        self.flag_mode = not self.flag_mode
        self.flag_button.config(text="Flag Mode" if self.flag_mode else "Click Mode")

    def check_for_win(self):
        unclicked_count = sum(button['relief'] != tk.SUNKEN for row in self.buttons for button in row)
        if unclicked_count == self.num_mines:
            if (self.gui):
                messagebox.showinfo("Congratulations!", "You have won the game!")
            else:
                print("Congratulations! You have won the game!")
                self.print_current_board()
                self.has_won = True
            self.game_over = True

    def print_current_board(self):
        # Print column indexes
        print("    "+ " ".join(str(i) for i in range(self.cols)))
        # print a line
        print("-" * (self.cols * 2 + 3))

        button_grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            # Print row index
            print(i, end=" | ")

            for j in range(self.cols):
                button = self.buttons[i][j]
                if button['relief'] == tk.SUNKEN:
                    button_grid[i][j] = self.grid[i][j]
                    print(self.grid[i][j], end=" ")
                elif button['text'] == "F":
                    button_grid[i][j] = "F"
                    print("F", end=" ")
                else:
                    button_grid[i][j] = " "
                    print(button['text'], end=" ")
            print()
        print()
        self.button_grid = button_grid

    def run(self):
        if (self.gui):
            self.root.mainloop()
        else:
            if not self.grid:
                print("No grid found")
                return
            self.print_current_board()
            while not self.game_over:
                input_str = input("Enter row, column and mode (f for flag, c for click): ")
                # String needs to be turned into an array with space as the dilimter
                input_str = input_str.split(" ")

                row = int(input_str[0])
                col = int(input_str[1])
                mode = input_str[2] if len(input_str) > 2 else ""
                if mode == "f":
                    self.button_right_clicked(row, col)
                elif mode == "c" or mode == "":
                    self.button_clicked(row, col)
                else:
                    print("Invalid mode. Please enter f for flag or c for click")
