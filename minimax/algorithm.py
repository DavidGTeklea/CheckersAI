from copy import deepcopy
# deep copy allows you to make copies of board object
# without saving that copy to the original board address
# of the board instances
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

# position really stands for board
# depth stands for how long to go through "tree of decisiosn"
# max_player is True, means to maximize advantage. False means vice versa
# position is only evaluated at end of decision tree
def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        # negative infinity is the best of a position before you see it
        maxEval = float('-inf')
        # stores best move you can make
        best_move = None

        for move in get_all_moves(position, WHITE, game):
            # the [0] on the end of evaluation is just to get
            # rid of the paht, because you only need the number,
            # and you can get the path later when you return best_move
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):

            # the parameter is True here in order to recursively go back
            # to evaluating the other side's candidates for moves

            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

# to get all the possible moves in a position
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():


            # you don't wanna modify the same board,
            # making a copy of each board will make moving
            # pieces easier, and to display that movement
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)

            # taking first three parameters, and applying it to a deepcopoy
            # of a new board
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves



