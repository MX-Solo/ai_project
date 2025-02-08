import numpy as np
import random
import argparse


def longest_increasing_sequence(arr):
    """Find the length of the longest increasing sequence starting from the beginning."""
    length = 1
    max_value = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_value:
            length += 1
            max_value = arr[i]
    return length


def is_latin_square(square):
    n = len(square)

    # Check that all rows contain unique elements
    for row in square:
        if len(set(row)) != n:
            return False

    # Check that all columns contain unique elements
    for col in square.T:  # Transpose the matrix to access columns as rows
        if len(set(col)) != n:
            return False

    # Check that the elements are between 1 and n (or the valid symbol set)
    valid_symbols = set(range(1, n + 1))
    for row in square:
        if not set(row).issubset(valid_symbols):
            return False

    return True

    # def analyze_matrix(matrix):
    """Analyze the matrix rows (or columns) to find the increasing sequences."""
    sequence_rows = []
    sequence_cols = []
    for i in range(len(matrix)):
        row = matrix[i]
        col = matrix[:, i]

        # Find longest increasing sequence
        start_seq_length_row = longest_increasing_sequence(row)
        end_seq_length_row = longest_increasing_sequence(np.flip(row))
        sequence_rows.append((start_seq_length_row, end_seq_length_row))

        start_seq_length_col = longest_increasing_sequence(col)
        end_seq_length_col = longest_increasing_sequence(np.flip(col))
        sequence_cols.append((start_seq_length_col, end_seq_length_col))

    if not is_latin_square(matrix):
        print("Warning: The matrix is not a valid Latin square.")
        return
    print("####### ", is_latin_square(matrix), " #######")
    print('   ', end='')
    for tup in sequence_cols:
        print(f"{tup[0]}  ", end='')
    print()

    for j, tup in enumerate(sequence_rows):
        row = matrix[j]
        print(f"{tup[0]} {list(row)} {tup[1]}")

    print('   ', end='')
    for tup in sequence_cols:
        print(f"{tup[1]}  ", end='')

    print("\n-----------------------------------------------------")


def analyze_matrix(matrix):
    """Analyze the matrix rows (or columns) to find the increasing sequences and return the analysis as a formatted string."""
    sequence_rows = []
    sequence_cols = []
    output = []

    # Calculate increasing sequences for each row and column
    for i in range(len(matrix)):
        row = matrix[i]
        col = matrix[:, i]

        # Find longest increasing sequence
        start_seq_length_row = longest_increasing_sequence(row)
        end_seq_length_row = longest_increasing_sequence(np.flip(row))
        sequence_rows.append((start_seq_length_row, end_seq_length_row))

        start_seq_length_col = longest_increasing_sequence(col)
        end_seq_length_col = longest_increasing_sequence(np.flip(col))
        sequence_cols.append((start_seq_length_col, end_seq_length_col))

    # Check if the matrix is a valid Latin square
    if not is_latin_square(matrix):
        print("Warning: The matrix is not a valid Latin square.\n")
    else:
        print("####### True #######\n")

    # Format the column sequence analysis
    output.append('   ' + '  '.join(f"{tup[0]}" for tup in sequence_cols) + '\n')

    # Format the row sequence analysis
    for j, tup in enumerate(sequence_rows):
        row = matrix[j]
        output.append(f"{tup[0]} {list(row)} {tup[1]}\n")

    # Format the bottom row of column sequence analysis
    output.append('   ' + '  '.join(f"{tup[1]}" for tup in sequence_cols) + '\n')
    # print(output)
    # Return the joined output as a single string
    return ''.join(output)


def generate_latin_square_backtracking(square):
    return permute_latin_square(square)


def generate_multiple_latin_squares_backtracking(n, num_examples=3):
    """Generate 'num_examples' Latin squares using backtracking with randomization"""
    examples = []
    square = generate_latin_square(n)
    for _ in range(num_examples):
        latin_square = generate_latin_square_backtracking(square)
        examples.append(latin_square)
    return examples


# Example n x n Latin square generator
def generate_latin_square(n):
    # Generate a basic n x n Latin square using cyclic method
    base = np.arange(1, n + 1)
    latin_square = np.array([np.roll(base, i) for i in range(n)])
    return latin_square


def permute_latin_square(square):
    # Permute rows and then columns
    square_permuted_rows = square[np.random.permutation(len(square))]
    square_permuted = square_permuted_rows[:, np.random.permutation(len(square_permuted_rows))]
    return square_permuted


def main():
    parser = argparse.ArgumentParser(description="Generate and analyze Latin squares.")
    parser.add_argument("-grid_size", type=int, required=True, help="The grid size for the Latin square.")
    parser.add_argument("-map", type=int, required=True, help="The map number for the output file name.")

    args = parser.parse_args()

    # Generate a Latin square of the specified grid size
    base_square = generate_latin_square(args.grid_size)
    latin_square = generate_latin_square_backtracking(base_square)

    # Analyze the matrix and get formatted string output
    analysis = analyze_matrix(latin_square)

    # Write the Latin square and its analysis to a file
    output_file = f"map{args.map}.txt"
    with open(output_file, "w") as f:
        f.write(analysis)

    print(f"Latin square of size {args.grid_size} written to {output_file}")


if __name__ == "__main__":
    main()

