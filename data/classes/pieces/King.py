import pygame
from data.classes.Piece import Piece


class King(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_filename = f"data/imgs/{color[0]}_king.png"
        self.img = pygame.transform.scale(pygame.image.load(img_filename), (board.tile_width - 20, board.tile_height - 20))
        self.notation = 'K'

    def get_possible_moves(self, board):
        output = []
        directions = [
            (0, -1),  # north
            (1, -1),  # ne
            (1, 0),   # east
            (1, 1),   # se
            (0, 1),   # south
            (-1, 1),  # sw
            (-1, 0),  # west
            (-1, -1), # nw
        ]

        for dx, dy in directions:
            new_pos = (self.x + dx, self.y + dy)
            if 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8:
                output.append([board.get_square_from_pos(new_pos)])

        return output

    def can_castle(self, board):
        if not self.has_moved:
            rook_positions = {
                'white': [(0, 7), (7, 7)],
                'black': [(0, 0), (7, 0)]
            }
            for pos in rook_positions[self.color]:
                rook = board.get_piece_from_pos(pos)
                if rook and not rook.has_moved:
                    if pos[0] == 0:
                        if [board.get_piece_from_pos((i, pos[1])) for i in range(1, 4)] == [None] * 3:
                            return 'queenside'
                    elif pos[0] == 7:
                        if [board.get_piece_from_pos((i, pos[1])) for i in range(5, 7)] == [None] * 2:
                            return 'kingside'
        return None

    def get_valid_moves(self, board):
        output = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                output.append(square)

        castling = self.can_castle(board)
        if castling:
            if castling == 'queenside':
                output.append(board.get_square_from_pos((self.x - 2, self.y)))
            elif castling == 'kingside':
                output.append(board.get_square_from_pos((self.x + 2, self.y)))

        return output
