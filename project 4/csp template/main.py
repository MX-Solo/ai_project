import tkinter as tk
import argparse
from collections import deque

from map_reader import map_reader
from graphics import SkyscraperPuzzleGUI
from CSP import CSP
from Solver import Solver


def longest_increasing_sequence(arr):
    """Find the length of the longest increasing sequence starting from the beginning."""
    length = 1
    max = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max:
            length += 1
            max = arr[i]
    return length


# Main part of the code to run the GUI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skyscraper Puzzle Solver")

    parser.add_argument(
        "-m",
        "--map",
        type=int,
        choices=[i for i in range(3, 100)],
        help="Map must be less than 100 and greater than 2",
    )
    parser.add_argument(
        "-lcv",
        "--lcv",
        action="store_true",
        help="Enable least constraint value (LCV) as a order-type optimizer"
    )
    parser.add_argument(
        "-mrv",
        "--mrv",
        action="store_true",
        help="Enable minimum remaining values (MRV) as a order-type optimizer"
    )
    parser.add_argument(
        "-MAC",
        "--maintaining_arc_consistency",
        action="store_true",
        help="Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution"
    )

    args = parser.parse_args()
    clues = map_reader(args.map)  # clues= [top, bottom, left, right]
    grid_size = len(clues[0])


    """ You should implement your model building here """


    # Initialize the CSP
    csp = CSP()

    # Define variables
    for i in range(1, grid_size + 1):
        for j in range(1, grid_size + 1):
            variable_name = f"{i},{j}"
            domain = list(range(1, grid_size + 1))
            csp.add_variable(variable_name, domain)

    # Define constraints
    # Row constraints: all unique values in each row
    for i in range(1, grid_size + 1):
        row_vars = [f"{i},{j}" for j in range(1, grid_size + 1)]
        csp.add_constraint(lambda *args: None not in args and len(set(args)) == len(args), row_vars)

    # Column constraints: all unique values in each column
    for j in range(1, grid_size + 1):
        col_vars = [f"{i},{j}" for i in range(1, grid_size + 1)]
        csp.add_constraint(lambda *args: None not in args and len(set(args)) == len(args), col_vars)

    # Helper function to fix lambda scope issue
    def create_clue_constraint(clue_value):
        return lambda *args: None not in args and longest_increasing_sequence(args) == clue_value

    # Clue constraints: check visibility clues
    for i, direction in enumerate(["top", "bottom", "left", "right"]):
        clue = clues[i]
        for index, clue_value in enumerate(clue):
            if clue_value == 0:  # Ignore clues with value 0 (no constraint)
                continue

            if direction == "top":
                vars_in_clue = [f"{j + 1},{index + 1}" for j in range(grid_size)]
            elif direction == "bottom":
                vars_in_clue = [f"{grid_size - j},{index + 1}" for j in range(grid_size)]
            elif direction == "left":
                vars_in_clue = [f"{index + 1},{j + 1}" for j in range(grid_size)]
            elif direction == "right":
                vars_in_clue = [f"{index + 1},{grid_size - j}" for j in range(grid_size)]


            # Add clue constraint using helper function
            csp.add_constraint(create_clue_constraint(clue_value), vars_in_clue)

    root = tk.Tk()
    root.title("Skyscraper Puzzle")

    # Center the window
    window_width, window_height = 600, 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    solver = Solver(csp, args.lcv, args.mrv, args.maintaining_arc_consistency)

    puzzle = SkyscraperPuzzleGUI(root, grid_size, solver)

    # Adding clues to the GUI
    for j in range(1, grid_size + 1):
        puzzle.add_clue(0, j, clues[0][j - 1], "down")  # Top clue pointing down
        puzzle.add_clue(grid_size + 1, j, clues[1][j - 1], "up")  # Bottom clue pointing up
    for i in range(1, grid_size + 1):
        puzzle.add_clue(i, 0, clues[2][i - 1], "right")  # Left clue pointing right
        puzzle.add_clue(i, grid_size + 1, clues[3][i - 1], "left")  # Right clue pointing left

    root.mainloop()