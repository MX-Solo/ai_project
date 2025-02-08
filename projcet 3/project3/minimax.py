from board import Board

def minimax(state, lvl, is_maximizing, color, pruning_enabled=False, alpha_val=-float('inf'), beta_val=float('inf')):
    if lvl == 0 or state.is_terminal():
        return None, evaluate_board(state, color)

    moves = state.get_valid_moves(color)
    if not moves:
        return None, evaluate_board(state, color)

    optimal_move = None

    if is_maximizing:
        best_score = -float('inf')
        for m in moves:
            simulated_board = state.copy()
            simulated_board.place_disc(m[0], m[1], color)
            _, score = minimax(simulated_board, lvl - 1, False, color, pruning_enabled, alpha_val, beta_val)
            if score > best_score:
                best_score = score
                optimal_move = m
            if pruning_enabled:
                alpha_val = max(alpha_val, score)
                if beta_val <= alpha_val:
                    break
        return optimal_move, best_score
    else:
        worst_score = float('inf')
        opponent = 'W' if color == 'B' else 'B'
        for m in moves:
            simulated_board = state.copy()
            simulated_board.place_disc(m[0], m[1], opponent)
            _, score = minimax(simulated_board, lvl - 1, True, color, pruning_enabled, alpha_val, beta_val)
            if score < worst_score:
                worst_score = score
                optimal_move = m
            if pruning_enabled:
                beta_val = min(beta_val, score)
                if beta_val <= alpha_val:
                    break
        return optimal_move, worst_score

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
