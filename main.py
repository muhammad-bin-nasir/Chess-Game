# main.py
import pygame
import chess
import os
import time

# --- Constants ---
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (245, 245, 245)
GRAY = (120, 120, 120)
BLUE = (106, 165, 230)
GREEN = (50, 205, 50)
RED = (255, 0, 0)

# Pygame setup
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess - Phase 2")

use_ai = True
BUTTON_RECT = pygame.Rect(10, 10, 140, 40)  # x, y, width, height
FONT = pygame.font.SysFont(None, 24)
# Load piece images
PIECES = {}
def load_pieces():
    types = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    colors = ["w", "b"]
    for color in colors:
        for ptype in types:
            img = pygame.image.load(os.path.join("assets", "pieces", f"{color}_{ptype}.png"))
            PIECES[f"{color}_{ptype}"] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

# UCI coordinate helper
def rc_to_square(row, col):
    files = ['a','b','c','d','e','f','g','h']
    ranks = ['8','7','6','5','4','3','2','1']
    return files[col] + ranks[row]

# Chess symbols → image filenames
SYMBOL_TO_IMAGE = {
    'P': 'w_pawn',
    'R': 'w_rook',
    'N': 'w_knight',
    'B': 'w_bishop',
    'Q': 'w_queen',
    'K': 'w_king',
    'p': 'b_pawn',
    'r': 'b_rook',
    'n': 'b_knight',
    'b': 'b_bishop',
    'q': 'b_queen',
    'k': 'b_king',
}

# Draw board background
def draw_board(win):
    colors = [WHITE, GRAY]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_ai_toggle(win):
    global use_ai
    pygame.draw.rect(win, (180, 180, 180), BUTTON_RECT)
    label = "AI: ON" if use_ai else "AI: OFF"
    text = FONT.render(label, True, (0, 0, 0))
    win.blit(text, (BUTTON_RECT.x + 10, BUTTON_RECT.y + 10))


# Draw pieces from board state
def draw_pieces(win, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = piece.symbol()
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            img = PIECES[SYMBOL_TO_IMAGE[symbol]]
            win.blit(img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Highlight legal moves
def draw_highlights(win, legal_moves, selected_square):
    for move in legal_moves:
        if move.from_square == selected_square:
            to_square = move.to_square
            row = 7 - chess.square_rank(to_square)
            col = chess.square_file(to_square)
            pygame.draw.rect(win, BLUE, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

# Highlight selected square
def draw_selected_square(win, square):
    if square is not None:
        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)
        pygame.draw.rect(win, GREEN, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

def landing_screen():
    selecting = True
    button_font = pygame.font.SysFont(None, 40)
    title_font = pygame.font.SysFont(None, 60)

    # Buttons
    button_hvh = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 50)
    button_hvai = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 50)

    while selecting:
        WIN.fill((30, 30, 30))
        
        # Title
        title_text = title_font.render("Choose Game Mode", True, (255, 255, 255))
        WIN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 150))

        # Buttons
        pygame.draw.rect(WIN, (70, 130, 180), button_hvh, border_radius=10)
        pygame.draw.rect(WIN, (60, 179, 113), button_hvai, border_radius=10)

        text_hvh = button_font.render("Human vs Human", True, (0, 0, 0))
        text_hvai = button_font.render("Human vs AI", True, (0, 0, 0))

        WIN.blit(text_hvh, (button_hvh.x + 50, button_hvh.y + 10))
        WIN.blit(text_hvai, (button_hvai.x + 70, button_hvai.y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_hvh.collidepoint(event.pos):
                    return False  # Human vs Human
                elif button_hvai.collidepoint(event.pos):
                    return True  # Human vs AI


# Main game loop
def main():
    clock = pygame.time.Clock()
    board = chess.Board()
    selected_square = None
    legal_moves = list(board.legal_moves)
    game_over = False

    use_ai = landing_screen()  # 🎬 Launch mode selector first
    run = True
    while run:
        clock.tick(60)
        draw_board(WIN)
        draw_ai_toggle(WIN)
        draw_highlights(WIN, legal_moves, selected_square)
        draw_selected_square(WIN, selected_square)
        draw_pieces(WIN, board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if game_over:
                continue

            # 🧍‍♂️ Human Turn (Always allow human to click)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON_RECT.collidepoint(pygame.mouse.get_pos()):
                    use_ai = not use_ai
                    print("AI Mode Toggled:", "ON" if use_ai else "OFF")
                    continue  # Skip rest of MOUSEBUTTONDOWN logic

                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                clicked_square = chess.square(col, 7 - row)

                if selected_square is None:
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == board.turn:
                        selected_square = clicked_square
                else:
                    move = chess.Move(selected_square, clicked_square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                        legal_moves = list(board.legal_moves)

                        if board.is_game_over():
                            game_over = True
                            print("Game Over:", board.result())
                    else:
                        selected_square = None

        # 🧠 AI Turn (Only when it's Black’s turn and AI is enabled)
        if not game_over and use_ai and not board.turn:
            print("AI (Black) is thinking...")
            score, ai_move = minimax(board, 4, float('-inf'), float('inf'), True)
            if ai_move:
                time.sleep(0.5)
                board.push(ai_move)
                legal_moves = list(board.legal_moves)
                print("AI played:", ai_move)

                if board.is_game_over():
                    game_over = True
                    print("Game Over:", board.result())

    pygame.quit()

def evaluate_board(board):
    """
    Returns a score from White's perspective.
    Positive = advantage White, Negative = advantage Black
    """
    if board.is_checkmate():
        if board.turn:  # If it's White's turn and checkmate, Black won
            return -9999
        else:
            return 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0,
    }

    value = 0
    for piece_type in piece_values:
        value += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        value -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    return value

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval, best_move

    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval, best_move



if __name__ == "__main__":
    load_pieces()
    main()
