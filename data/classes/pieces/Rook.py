import pygame
from data.classes.Piece import Piece


class Rook(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        img_path = f'data/imgs/{color[0]}_rook.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'R'

    def get_possible_moves(self, board):
        output = []

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            moves = []
            x, y = self.x + dx, self.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                square = board.get_square_from_pos((x, y))
                moves.append(square)
                if square.occupying_piece:
                    break
                x += dx
                y += dy
            output.append(moves)

        return output
