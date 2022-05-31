import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        # how many red and white pieces do you have
        self.red_left = self.white_left = 12
        # initial amount of kings at start of game
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)

        # draws the rows and columns
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # incentivize AI to create kings
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    # so that the AI can consider all the moves of all the
    # pieces
    def get_all_pieces(self, color):
        pieces = []
        # accessing the two dimentional array in
        # _init_ function at the beginning of the Board class
        # this access is done through self.board
        for row in self.board:
            # each piece in array is a piece on board
            for piece in row:
                # if there is a piece on a certain space
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces


    # to make pieces move around
    def move(self, piece, row, col):
        # swap places in a list, for the checker pieces
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]

        piece.move(row, col)

        # make the piece a king when it reaches appropriate place
        # since this is in move position, it won't make pieces on those
        # intial rows into becoming kings
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                # if not white king, it must've been a red king
                self.red_kings += 1

    # give row, col, get piece back
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                # since red and black squares are on odd and even columns
                # from row to row
                if col % 2 == ((row +  1) % 2):
                    # for the white pieces
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    # for the red pieces, rows 5,6,7
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            # this removes a piece
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    # remove red piece
                    self.red_left -= 1
                else:
                    # remove white piece
                    self.white_left -= 1
    
    # determines if game has been won
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        # ex. (3,2) =[(1,1)] might be an available move call in the dictionary
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # check if you can move up or down based off piece colors
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))


        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    # look on left diagonal for a piece
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        # what row you start, stop at, and how much you're step
        for r in range(start, stop, step):
            # no longer in range of columns, so break
            if left < 0:
                break
            
            current = self.board[r][left]

            # if empty squared found
            if current == 0:
                # if skipped over something, but no more to skip again, break
                if skipped and not last:
                    break

                elif skipped:
                    moves[(r, left)] = last + skipped

                else:
                    moves[(r, left)] = last

                # check to see if you can skip anymore from that space
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break

            # piece was found, leave loop
            elif current.color == color:
                break

            else:
                last = [current]

            left -= 1
        
        return moves

    # look at the right diagonal for a piece
    # identical structure/variables to _traverse_left with
    # a few exceptions
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves