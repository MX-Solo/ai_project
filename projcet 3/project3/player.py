from minimax import minimax
from expectimax import expectimax
from board import Board
from game import Agent
import random 
from collections import defaultdict
class RandomPlayer(Agent):
    def __init__(self, color):
        super().__init__(color)
        random.seed(42)
    
    def make_move(self, board):
        valid_moves = board.get_valid_moves(self.color)
        if not valid_moves:
            print(f"{self.color} has no valid moves.")
            return (None, None)
        return random.choice(valid_moves)
    



class MCTSPlayer(Agent):
    def __init__(self, color, simulations=100):
        super().__init__(color)
        random.seed(42)
        self.simulations = simulations
    
    def simulate_random_game(self, board, color):
        current_color = color
        while not board.is_full() and board.get_valid_moves(current_color):
            valid_moves = board.get_valid_moves(current_color)
            if valid_moves:
                move = random.choice(valid_moves)
                board.place_disc(move[0], move[1], current_color)
            current_color = 'B' if current_color == 'W' else 'W'
        return board.get_score()

    def mcts(self, board, simulations):
        # Monte Carlo Tree Search main function
        win_counts = defaultdict(int)
        play_counts = defaultdict(int)

        for _ in range(simulations):
            # Choose a random valid move and simulate the result
            temp_board = board.copy()
            valid_moves = board.get_valid_moves(self.color)
            if not valid_moves:
                return None, None

            move = random.choice(valid_moves)
            temp_board.place_disc(move[0], move[1], self.color)

            score_B, score_W = self.simulate_random_game(temp_board, 'B' if self.color == 'W' else 'W')
            winner = 'B' if score_B > score_W else 'W'

            play_counts[move] += 1
            if winner == self.color:
                win_counts[move] += 1

        # Choose the move with the highest win rate
        best_move = max(valid_moves, key=lambda x: win_counts[x] / play_counts[x])
        return best_move

    def make_move(self, board):
        # Use MCTS to make a move
        return self.mcts(board, self.simulations)

class IntelligentPlayer(Agent):
    def __init__(self, color):
        super().__init__(color)
    
    def evaluate_board(self, board):
        """Enhanced board evaluation function with more complex heuristics."""
        black_score, white_score = board.get_score()
        score = black_score if self.color == 'B' else white_score
        
        # Corner heuristic: prioritize control of corners
        corners = [(0, 0), (0, board.size - 1), (board.size - 1, 0), (board.size - 1, board.size - 1)]
        corner_value = 25
        for row, col in corners:
            if board.board[row][col] == self.color:
                score += corner_value
            elif board.board[row][col] == ('W' if self.color == 'B' else 'B'):
                score -= corner_value
        
        # Mobility heuristic: maximize our valid moves, minimize opponent's
        opponent_color = 'W' if self.color == 'B' else 'B'
        my_moves = len(board.get_valid_moves(self.color))
        opponent_moves = len(board.get_valid_moves(opponent_color))
        mobility_value = 5
        score += mobility_value * (my_moves - opponent_moves)
        
        return score

    def get_move_score(self, board, move):
        """Evaluate the board score after making the move."""
        if move is None:
            return float('-inf')  # No move, very bad score
        temp_board = board.copy()
        temp_board.place_disc(move[0], move[1], self.color)
        return self.evaluate_board(temp_board)

    def make_move(self, board):
        valid_moves = board.get_valid_moves(self.color)
        if not valid_moves:
            print(f"{self.color} has no valid moves.")
            return (None, None)

        best_move = None
        best_score = float('-inf')

        # Evaluate each valid move and choose the best one
        for move in valid_moves:
            score = self.get_move_score(board, move)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move


class FirstValidMovePlayer(Agent):
    def __init__(self, color):
        super().__init__(color)
    
    def make_move(self, board):
        valid_moves = board.get_valid_moves(self.color)
        if not valid_moves:
            print(f"{self.color} has no valid moves.")
            return None
        return valid_moves[0]    
    
class EvaluativePlayer(Agent):
    def __init__(self, color):
        super().__init__(color)
    
    def make_move(self, board):
        valid_moves = board.get_valid_moves(self.color)
        if not valid_moves:
            print(f"{self.color} has no valid moves.")
            return None
        print("valid moves: ",valid_moves)
        # Simple evaluation: Choose the move that flips the most discs
        best_move = None
        max_flips = 0
        
        for move in valid_moves:
            row, col = move
            # Copy the board and simulate the move
            board_copy = self.copy_board(board)
            board_copy.place_disc(row, col, self.color)
            flips = self.count_flips(board_copy, row, col, self.color)
            if flips > max_flips:
                max_flips = flips
                best_move = move
        
        return best_move

    def copy_board(self, board):
        # Create a deep copy of the board to simulate moves
        new_board = Board(board.size)
        new_board.board = [row[:] for row in board.board]
        return new_board
    
    def count_flips(self, board, row, col, color):
        # Count how many discs would be flipped by placing a disc at (row, col)
        flips = 0
        opponent_color = 'W' if color == 'B' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < board.size and 0 <= c < board.size and board.board[r][c] == opponent_color:
                r += dr
                c += dc
                if 0 <= r < board.size and 0 <= c < board.size and board.board[r][c] == color:
                    flips += len([(i, j) for i in range(row + dr, r + dr, dr) for j in range(col + dc, c + dc, dc)])
                    break
        
        return flips


class Minimaxplayer(Agent):
    def __init__(self, color, depth=3):
        super().__init__(color)
        self.depth = depth

    def make_move(self, board):
        # Use minimax to determine the best move
        move, _ = minimax(board, self.depth, True, self.color)

        print(f"AI ({self.color}) plays: {move}")
        if move is None:
            return (None,None)
        
        return move


class ExpectimaxPlayer:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth

    def make_move(self, board):
        move, _ = expectimax(board, self.depth, True, self.color)
        print(f"AI ({self.color}) plays: {move}")
        if move is None:
            return (None,None)
        return move


class EvaluativePlayer(Agent):
    def __init__(self, color):
        super().__init__(color)
    
    def make_move(self, board):
        print(self.color)
        valid_moves = board.get_valid_moves(self.color)
        print(valid_moves)
        if not valid_moves:
            print(f"{self.color} has no valid moves.")
            return None
        
        # Simple evaluation: Choose the move that flips the most discs
        best_move = None
        max_flips = 0
        
        for move in valid_moves:
            row, col = move
            print(move)
            # Copy the board and simulate the move
            board_copy = self.copy_board(board)
            board_copy.place_disc(row, col, self.color)
            flips = self.count_flips(board_copy, row, col, self.color)
            if flips > max_flips:
                max_flips = flips
                best_move = move
        print(best_move)
        return best_move

    def copy_board(self, board):
        # Create a deep copy of the board to simulate moves
        new_board = Board(board.size)
        new_board.board = [row[:] for row in board.board]
        return new_board
    
    def count_flips(self, board, row, col, color):
        # Count how many discs would be flipped by placing a disc at (row, col)
        flips = 0
        opponent_color = 'W' if color == 'B' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < board.size and 0 <= c < board.size and board.board[r][c] == opponent_color:
                r += dr
                c += dc
                if 0 <= r < board.size and 0 <= c < board.size and board.board[r][c] == color:
                    flips += len([(i, j) for i in range(row + dr, r + dr, dr) for j in range(col + dc, c + dc, dc)])
                    break
        
        return flips