import sys
import pygame
import pygame.time
import numpy as np

pygame.init()

#Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#Proportions and Sizes
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

#Makes the lines of the board
def draw_lines(color = WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i),  LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

#Draws a circle or cross in the middle of the square
def draw_figures(color = WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

#Claims the square to the user or AI
def mark_square(row, col, player):
    board[row][col] = player

#Checks to see if the square is claimed by the user or the AI
def available_square(row, col):
    return board[row][col] == 0

#Checks to see if all squares are claimed between the user and AI
def is_board_full(check_board = board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

#check if there is 3 of the same symbol in a line
def check_win(player, check_board = board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

#Runs through every possibility and chooses the best or worst route
def minimax(minimax_board, depth, is_maximizing):
    #AI wins
    if check_win(2, minimax_board):
        return float("inf")
    #AI loses
    elif check_win(1, minimax_board):
        return float("-inf")
    #AI ties with player (neutral move)
    elif is_board_full(minimax_board):
        return 0
    
    #AI pretends to be the AI and predicts what the player would do to minimize the player's score
    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score) #if you switch min and max the AI will let you win
        return best_score
    
    #AI pretends to be the player and predicts what the AI would do to minimize the AI's score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score) #if you switch min and max the AI will let you win
        return best_score

#Determines best move for AI
def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score  = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

#Prints to screen how to restart the game
def draw_restart_message():
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press R to restart", True, PURPLE)
    text_rect = text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

#Prints to screen  whats inside the parameter "message"
def draw_end_message(message, vertical_offset = 0):
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, PURPLE)
    text_rect = text.get_rect(center = (WIDTH // 2, HEIGHT // 2 + vertical_offset))
    screen.blit(text, text_rect)


#initalization of the actual game
draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1 #changing the player in a mathematical way

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1 #changing the player in a mathematical way

                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
            draw_end_message("You Won!", -30)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
            draw_end_message("You Lost!", -30)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)
            draw_end_message("It's a Tie!", -30)
        draw_restart_message()

    pygame.display.update()