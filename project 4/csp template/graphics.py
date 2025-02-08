import tkinter as tk
import Solver
from Solver import Solver
import time


class SkyscraperPuzzleGUI:
    def __init__(self, root, grid_size, solver: Solver):
        self.root = root
        self.grid_size = grid_size
        self.cells = {}
        self.counter = 0
        self.clues = []
        self.create_widgets()
        self.solver = solver


    def create_widgets(self):
        """Sets up the main window with the grid and the solve button."""

        # Create a frame for the counter at the top
        self.counter_frame_top = tk.Frame(self.root)
        self.counter_frame_top.pack(pady=10)

        # Create and pack the counter label at the top
        self.counter_label_top = tk.Label(self.counter_frame_top, text=f"Number of Assignments : {self.counter}",
                                          font=("Arial", 20, "bold"))
        self.counter_label_top.pack()

        # Timer label
        self.timer_label = tk.Label(self.counter_frame_top, text="Elapsed Time: 0s", font=("Arial", 20, "bold"))
        self.timer_label.pack()

        # Create a frame to center the puzzle grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=20)

        # Create the grid and the clues
        self.create_grid()

        # Add a "Solve" button centered below the grid
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_puzzle, font=("Arial", 14))
        solve_button.pack(pady=20)

    def create_grid(self):
        """Creates the grid with white cells and black borders."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Create each cell as a label widget inside a frame to have the black border
                frame = tk.Frame(self.grid_frame, highlightbackground="black", highlightthickness=1)
                frame.grid(row=row + 1, column=col + 1, sticky='nsew')

                # Create the label for the cell, store its reference
                cell = tk.Label(frame, text="", font=("Arial", 16), width=4, height=2, bg="white")
                cell.pack(expand=True)
                self.cells[(row, col)] = cell

    def add_clue(self, row, col, number, direction):
        """Add a clue dynamically around the grid."""
        # Create a frame for the clue and triangle to ensure proper layout
        clue_frame = tk.Frame(self.grid_frame)
        clue_frame.grid(row=row, column=col, sticky="nsew")

        canvas = tk.Canvas(clue_frame, width=40, height=40, bg=self.grid_frame.cget("bg"), highlightthickness=0)
        canvas.pack()

        # Add the clue number, and place it based on the direction

        # Add triangle below or above the clue number
        if direction == "down":
            clue_label = tk.Label(canvas, text=str(number), font=("Arial", 16), bg=self.grid_frame.cget("bg"))
            canvas.create_window(20, 10, window=clue_label)

            canvas.create_polygon(20, 25, 30, 35, 10, 35, fill="black")  # Down-pointing triangle
        elif direction == "up":
            clue_label = tk.Label(canvas, text=str(number), font=("Arial", 16), bg=self.grid_frame.cget("bg"))
            canvas.create_window(20, 30, window=clue_label)

            canvas.create_polygon(20, 15, 30, 5, 10, 5, fill="black")  # Up-pointing triangle

            # Add triangle left or right of the clue number
        elif direction == "right":
            clue_label = tk.Label(canvas, text=str(number), font=("Arial", 16), bg=self.grid_frame.cget("bg"))
            canvas.create_window(10, 20, window=clue_label)
            canvas.create_polygon(25, 20, 35, 30, 35, 10, fill="black")  # Right-pointing triangle
        elif direction == "left":
            clue_label = tk.Label(canvas, text=str(number), font=("Arial", 16), bg=self.grid_frame.cget("bg"))
            canvas.create_window(25, 20, window=clue_label)
            canvas.create_polygon(15, 20, 5, 30, 5, 10, fill="black")  # Left-pointing triangle

    def set_number(self, row, col, number):
        """Set the number for a specific cell based on table coordinates."""
        if (row, col) in self.cells:
            self.cells[(row, col)].config(text=str(number), bg='lightgreen')
            # self.update_counter_label()

    def clear_number(self, row, col):
        """Clear the number in a specific cell."""
        if (row, col) in self.cells:
            self.cells[(row, col)].config(text="", bg="white")

    def update_counter_label(self, number):
        """Update the counter labels with the current counter value."""
        self.counter_label_top.config(text=f"Number of Assignments : {number}")


    def solve_puzzle(self):
        """Solve the puzzle using the CSP solver and display the solution."""
        self.start_time = time.time()
        solution = dict(self.solver.backtrack_solver())
        elapsed_time = int(time.time() - self.start_time)
        self.update_counter_label(self.solver.csp.assignments_number)
        self.timer_label.config(text=f"Elapsed Time: {elapsed_time}s")
        if solution:
            # Update each cell in the grid with the values from the solution
            for (i, j), value in solution.items():
                self.set_number(i - 1, j - 1, value)
        else:
            print("No solution found!")

