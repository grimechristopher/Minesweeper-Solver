import tkinter as tk
from tkinter import messagebox

class StartMenu:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.difficulty = 0

    def create_window(self):
        window = tk.Tk()
        window.title("Start Menu")

        height_label = tk.Label(window, text="Height:")
        height_label.pack()
        height_entry = tk.Entry(window)
        height_entry.pack()

        width_label = tk.Label(window, text="Width:")
        width_label.pack()
        width_entry = tk.Entry(window)
        width_entry.pack()

        difficulty_label = tk.Label(window, text="Difficulty:")
        difficulty_label.pack()
        difficulty_slider = tk.Scale(window, from_=10, to=35, orient=tk.HORIZONTAL)
        difficulty_slider.set(15)
        difficulty_slider.pack()

        submit_button = tk.Button(window, text="Submit", command=lambda: self.submit(window, height_entry.get(), width_entry.get(), difficulty_slider.get()))
        submit_button.pack()

        window.mainloop()

    def submit(self, window, height, width, difficulty):
        try:
            self.height = int(height)
            self.width = int(width)
            self.difficulty = int(difficulty)
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter integers.")

