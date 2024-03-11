import pygame
from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        return [Square(x, y, self.tile_width, self.tile_height) for y in range(8) for x in range(8)]

    def get_square_from_pos(self, pos):
        return next((square for square in self.squares if (square.x, square.y) == pos), None)

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece:
                    square = self.get_square_from_pos((x, y))
                    color = 'white' if piece[0] == 'w' else 'black'
                    piece_type = {'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King, 'P': Pawn}[piece[1]]
                    square.occupying_piece = piece_type((x, y), color, self)

    def handle_click(self, mx, my):
        if (self.width <= mx <= self.width + self.tile_width and
                self.height // 2 <= my <= self.height // 2 + self.tile_height):
            return

        x, y = mx // self.tile_width, my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))

        if clicked_square is not None:
            if self.selected_piece is None:
                if clicked_square.occupying_piece is not None and clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece

            else:
                target_square = self.get_square_from_pos((x, y))
                if self.selected_piece.move(self, target_square):
                    self.turn = 'white' if self.turn == 'black' else 'black'
                    self.selected_piece = None

                elif target_square.occupying_piece is not None and target_square.occupying_piece.color == self.turn:
                    self.selected_piece = target_square.occupying_piece

    def is_in_check(self, color, board_change=None):
        output = False
        king_pos = None
        changing_piece = old_square = new_square = new_square_old_piece = None

        if board_change:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [i.occupying_piece for i in self.squares if i.occupying_piece]

        if changing_piece and changing_piece.notation == 'K':
            king_pos = new_square.pos
        if king_pos is None:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                    king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True

        if board_change:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece

        return output

    def is_in_checkmate(self, color):
        king = next((piece.occupying_piece for piece in self.squares if piece.occupying_piece and
                     piece.occupying_piece.notation == 'K' and piece.occupying_piece.color == color), None)
        if king and not king.get_valid_moves(self) and self.is_in_check(color):
            return True
        return False

    def draw(self, display):
        if self.selected_piece:
            selected_square = self.get_square_from_pos(self.selected_piece.pos)
            selected_square.highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display)
