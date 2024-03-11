import pygame
from data.classes.Piece import Piece


class Knight(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        img_path = f'data/imgs/{color[0]}_knight.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'N'

    def get_possible_moves(self, board):
        output = []
        moves = [
            (1, -2), (2, -1), (2, 1), (1, 2),
            (-1, 2), (-2, 1), (-2, -1), (-1, -2)
        ]

        for dx, dy in moves:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                output.append([board.get_square_from_pos((new_x, new_y))])

        return output
