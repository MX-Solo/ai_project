from board import Board
import random

def expectimax(board, depth, maximizing_player, player_color):
    if depth == 0 or (not board.get_valid_moves('B') and not board.get_valid_moves('W')):
        return None, evaluate_board(board, player_color)

    valid_moves = board.get_valid_moves(player_color if maximizing_player else ('W' if player_color == 'B' else 'B'))
    if not valid_moves:
        return None, evaluate_board(board, player_color)

    if maximizing_player:
        max_eval = -float('inf')
        best_move = None
        for move in valid_moves:
            new_board = copy_board(board)
            new_board.place_disc(move[0], move[1], player_color)
            _, eval = expectimax(new_board, depth-1, False, player_color)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move, max_eval
    else:
        expected_value = 0
        for move in valid_moves:
            new_board = copy_board(board)
            opponent_color = 'W' if player_color == 'B' else 'B'
            new_board.place_disc(move[0], move[1], opponent_color)
            _, eval = expectimax(new_board, depth-1, True, player_color)
            expected_value += eval
        return None, expected_value / len(valid_moves)

def evaluate_board(board, player_color):
    B_score, W_score = board.get_score()
    opponent_color = 'W' if player_color == 'B' else 'B'
    player_score = B_score if player_color == 'B' else W_score
    opponent_score = W_score if player_color == 'B' else B_score

    score = player_score - opponent_score

    # Calculate corner advantage
    corners = [(0, 0), (0, board.size - 1), (board.size - 1, 0), (board.size - 1, board.size - 1)]
    player_corners = sum(1 for x, y in corners if board.board[x][y] == player_color)
    opponent_corners = sum(1 for x, y in corners if board.board[x][y] == opponent_color)
    score += 25 * (player_corners - opponent_corners)

    # Calculate edge control
    edges = [
        (0, i) for i in range(1, board.size - 1)
    ] + [(board.size - 1, i) for i in range(1, board.size - 1)] + [
        (i, 0) for i in range(1, board.size - 1)
    ] + [(i, board.size - 1) for i in range(1, board.size - 1)]
    player_edges = sum(1 for x, y in edges if board.board[x][y] == player_color)
    opponent_edges = sum(1 for x, y in edges if board.board[x][y] == opponent_color)
    score += 5 * (player_edges - opponent_edges)

    # Calculate mobility
    player_moves = len(board.get_valid_moves(player_color))
    opponent_moves = len(board.get_valid_moves(opponent_color))
    if player_moves + opponent_moves != 0:
        score += 10 * (player_moves - opponent_moves)

    # Calculate stable discs
    player_stable_discs = count_stable_discs(board, player_color)
    opponent_stable_discs = count_stable_discs(board, opponent_color)
    score += 15 * (player_stable_discs - opponent_stable_discs)

    return score

def count_stable_discs(board, color):
    stable_discs = 0
    for x in range(board.size):
        for y in range(board.size):
            if board.board[x][y] == color and is_stable(board, x, y):
                stable_discs += 1
    return stable_discs

def is_stable(board, x, y):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < board.size and 0 <= ny < board.size:
            if board.board[nx][ny] is None:
                return False
            nx += dx
            ny += dy
    return True

def copy_board(board):
    new_board = Board(board.size)
    new_board.board = [row[:] for row in board.board]
    return new_board
