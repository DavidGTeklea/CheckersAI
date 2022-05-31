import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None

        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        # uses the winner class from the board function
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        # don't have to call move and select
        # just select, and see if u can move it
        if self.selected:
            # let's try to move what you select
            result = self._move(row, col)
            # if move is not valid
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        # not selecting empty piece, and if is your turn
        # valid selection returns true, else False
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # move selected piece to the row, and column
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    # when you click on a piece and those little circles show you where
    # you can move, that is because of this function
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        # this gets rid of blue dots after every move
        self.valid_moves = {}

        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    # to get the board object in the code above
    def get_board(self):
        return self.board

    # this program doesn't "make moves"
    # it just makes a new board object based on
    # the desired moves
    def ai_move(self, board):
        self.board = board
        self.change_turn()