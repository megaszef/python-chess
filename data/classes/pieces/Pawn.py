import pygame
from data.classes.Piece import Piece


class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        img_path = f'data/imgs/{color[0]}_pawn.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))

        self.notation = ' '

    def get_possible_moves(self, board):
        output = []
        forward_moves = [(0, -1)] if self.color == 'white' else [(0, 1)]
        if not self.has_moved:
            forward_moves.append((0, -2)) if self.color == 'white' else forward_moves.append((0, 2))

        for dx, dy in forward_moves:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                square = board.get_square_from_pos((new_x, new_y))
                if square and not square.occupying_piece:
                    output.append(square)

        return output

    def get_moves(self, board):
        output = []
        forward_moves = [(0, -1)] if self.color == 'white' else [(0, 1)]
        if not self.has_moved:
            forward_moves.append((0, -2)) if self.color == 'white' else forward_moves.append((0, 2))

        for dx, dy in forward_moves:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                square = board.get_square_from_pos((new_x, new_y))
                if square and not square.occupying_piece:
                    output.append(square)

        attack_directions = [(1, -1), (-1, -1)] if self.color == 'white' else [(1, 1), (-1, 1)]

        for dx, dy in attack_directions:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                square = board.get_square_from_pos((new_x, new_y))
                if square and square.occupying_piece and square.occupying_piece.color != self.color:
                    output.append(square)

        return output

    def attacking_squares(self, board):
        return self.get_moves(board)
