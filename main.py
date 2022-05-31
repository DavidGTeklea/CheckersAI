import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
import difficulty

# this isn't a checker's constant, it's a rendering constant
FPS = 60

# checkers window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True

    # limits fps
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:

        clock.tick(FPS)

        if game.turn == WHITE:

            # establishes the depth at 3
            value, new_board = minimax(game.get_board(), difficulty.foresight, WHITE, game)
            game.ai_move(new_board)


        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    # quits window
    pygame.quit()

main()