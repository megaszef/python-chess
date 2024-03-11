import pygame
from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x, self.y = pos
        self.color = color
        self.has_moved = False

    @abstractmethod
    def get_possible_moves(self, board):
        pass

    def move(self, board, square, force=False):
        for i in board.squares:
            i.highlight = False

        valid_moves = self.get_valid_moves(board)
        if square in valid_moves or force:
            prev_square = board.get_square_from_pos(self.pos)
            self.pos = square.pos
            self.x, self.y = square.pos
            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True

            if self.notation == ' ' and (self.y == 0 or self.y == 7):
                from data.classes.pieces.Queen import Queen
                square.occupying_piece = Queen((self.x, self.y), self.color, board)

            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    self.castle_rook(board, 3, 0)
                elif prev_square.x - self.x == -2:
                    self.castle_rook(board, 5, 7)

            return True
        else:
            board.selected_piece = None
            return False

    def castle_rook(self, board, rook_x, new_rook_x):
        rook = board.get_piece_from_pos((rook_x, self.y))
        rook.move(board, board.get_square_from_pos((new_rook_x, self.y)), force=True)

    def get_moves(self, board):
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output

    def get_valid_moves(self, board):
        valid_moves = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                valid_moves.append(square)
        return valid_moves

    def attacking_squares(self, board):
        return self.get_moves(board)
