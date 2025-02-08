from board import Board
from utils import *

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """

    def __init__(self, color='W'):
        self.color = color

    # def getAction(self, state):
    #     """
    #     The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
    #     must return an action from Directions.{North, South, East, West, Stop}
    #     """

    #     raiseNotDefined()

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.current_player = player1

    def start(self):
        # Main game loop
        counter = 0
        while not self.is_game_over():
            self.board.display()
            print(f"{self.current_player.color}'s turn")

            valid_moves = self.board.get_valid_moves(self.current_player.color)
            if valid_moves:
                row, col = self.current_player.make_move(self.board)
                self.board.place_disc(row, col, self.current_player.color)
            else:
                print(f"No valid moves for {self.current_player.color}. Skipping turn.")

            self.switch_turns()
            counter+=1
        self.declare_winner()
        print(counter)
    def switch_turns(self):
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def is_game_over(self):
        # Game is over if no valid moves exist for both players or the board is full
        return self.board.is_full() or not any(self.board.get_valid_moves(player.color) for player in self.players)

    def declare_winner(self):
        black_score, white_score = self.board.get_score()
        if black_score > white_score:
            print("Black wins!")
        elif white_score > black_score:
            print("White wins!")
        else:
            print("It's a tie!")
