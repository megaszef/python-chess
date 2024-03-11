import pygame
from data.classes.Piece import Piece


class Bishop(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        img_path = f'data/imgs/{color[0]}_bishop.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'B'

    def get_possible_moves(self, board):
        output = []

        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            possible_moves = []
            x, y = self.x + dx, self.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                possible_moves.append(board.get_square_from_pos((x, y)))
                x += dx
                y += dy
            output.append(possible_moves)

        return output
