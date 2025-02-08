import pygame
import pickle
from game import Game
from player import Minimaxplayer, RandomPlayer, ExpectimaxPlayer, MCTSPlayer

# Define constants
WINDOW_SIZE = 800  # Increased resolution
GRID_SIZE = 8
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
BACKGROUND_COLOR = (0, 128, 0)  # Dark green
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

moves_list = []

def read_test_file(filename):
    with open(f'{filename}.pickle', 'rb') as handle:
        return pickle.load(handle)

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Othello")
        
        # Load test files
        self.random42 = read_test_file("random42")
        self.minimax = read_test_file("minimaxvsminimax")
        
        self.agent_accuracy = 0
        self.correct_moves = 0
        self.move_index = 0
        self.running = True
        self.mode = self.show_menu()
        self.set_players()

        # Initialize game
        self.game = Game(self.player1, self.player2)

        # Manage the frame rate
        self.clock = pygame.time.Clock()

    def show_menu(self):
        font = pygame.font.SysFont(None, 50)
        options = ["1. Minimax vs Minimax", "2. Minimax vs Random42", "3. MCTS vs Expectimax"]
        selected = 0

        while True:
            self.screen.fill(BACKGROUND_COLOR)
            for i, option in enumerate(options):
                color = WHITE if i == selected else BLACK
                text = font.render(option, True, color)
                self.screen.blit(text, (50, 50 + i * 50))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return ["ai vs ai", "ai vs random", "MCST vs expectimax"][selected]

    def set_players(self):
        if self.mode == "ai vs ai":
            self.player1 = Minimaxplayer('W')
            self.player2 = Minimaxplayer('B')
        elif self.mode == "ai vs random":
            self.player1 = Minimaxplayer('W')
            self.player2 = RandomPlayer('B')
        elif self.mode == "MCST vs expectimax":
            self.player1 = MCTSPlayer('W')
            self.player2 = ExpectimaxPlayer('B', depth=3)

    def draw_board(self):
        self.screen.fill(BACKGROUND_COLOR)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                disc = self.game.board.board[row][col]
                if disc == 'B':
                    pygame.draw.circle(self.screen, BLACK, rect.center, CELL_SIZE // 3)
                elif disc == 'W':
                    pygame.draw.circle(self.screen, WHITE, rect.center, CELL_SIZE // 3)

    def display_turn(self):
        font = pygame.font.SysFont(None, 50)
        turn_text = f"{self.game.current_player.color}'s turn"
        text = font.render(turn_text, True, WHITE)
        self.screen.blit(text, (20, 20))

    def play_ai_game(self):
        # Main loop for the game
        while not self.game.is_game_over() and self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # AI makes its move
            current_ai = self.game.current_player
            row, col = current_ai.make_move(self.game.board)

            # Handle AI move validation for testing modes
            if isinstance(current_ai, Minimaxplayer):
                if self.mode == "ai vs random" and (row, col) == self.random42[self.move_index]:
                    self.correct_moves += 1
                elif self.mode == "ai vs ai" and (row, col) == self.minimax[self.move_index]:
                    self.correct_moves += 1
                self.move_index += 1

            # Update board with the move
            moves_list.append((row, col))
            if row is not None and col is not None:
                self.game.board.place_disc(row, col, current_ai.color)

            # Switch turns
            self.game.switch_turns()

            # Redraw the board and update the display
            self.draw_board()
            self.display_turn()
            pygame.display.flip()
            pygame.time.delay(500)
            # Limit the game speed
            self.clock.tick(30)  # Cap the game at 30 FPS

        self.end_game()

    def end_game(self):
        black_score, white_score = self.game.board.get_score()
        font = pygame.font.SysFont(None, 50)
        if black_score > white_score:
            result_text = f"Black wins! Scores: Black={black_score}, White={white_score}"
        elif white_score > black_score:
            result_text = f"White wins! Scores: Black={black_score}, White={white_score}"
        else:
            result_text = f"It's a tie! Scores: Black={black_score}, White={white_score}"

        text = font.render(result_text, True, (255,0,0))
        self.screen.blit(text, (20, WINDOW_SIZE - 60))
        pygame.display.flip()
        pygame.time.delay(3000)  # Wait for 3 seconds before quitting
        self.agent_accuracy = self.correct_moves
        if self.mode == "ai vs ai" or self.mode == "ai vs random":
            print(f"Agent Accuracy: {(self.agent_accuracy/self.move_index) *100} %")
        self.running = False

if __name__ == "__main__":
    game = Othello()
    while game.running:
        game.play_ai_game()
    
    pygame.quit()
