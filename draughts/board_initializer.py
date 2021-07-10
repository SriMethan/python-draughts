# -*- coding: utf-8 -*-
#
# This file is part of the python-draughts library.
# Copyright (c) 2010-2018 ImparaAI https://impara.ai (MIT License)
# Copyright (C) 2021- TheYoBots (Yohaan Seth Nathan)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from math import ceil
from functools import reduce
import pickle
from .piece import Piece

WHITE = 2
BLACK = 1

class BoardInitializer:

    def __init__(self, board, fen='startpos'):
        self.board = board
        self.fen = fen

    def initialize(self):
        self.build_position_layout()
        self.set_starting_pieces()

    def build_position_layout(self):
        self.board.position_layout = {}
        position = 1

        for row in range(self.board.height):
            self.board.position_layout[row] = {}

            for column in range(self.board.width):
                self.board.position_layout[row][column] = position
                position += 1

    def set_starting_pieces(self):
        pieces = []
        if self.fen != 'startpos':
            starting = self.fen[0]
            board = self.fen[1:]
            for index, postion in enumerate(board):
                piece = None
                if postion.lower() == 'w':
                    # Index + 1 because enumerate returns 0-49 while the board takes 1-50.
                    piece = self.create_piece(2, index + 1)
                elif postion.lower() == 'b':
                    piece = self.create_piece(1, index + 1)
                if postion == 'W' or postion == 'B':
                    piece.king = True
                if piece:
                    pieces.append(piece)
        else:
            starting_piece_count = self.board.width * self.board.rows_per_user_with_pieces
            player_starting_positions = {
                1: list(range(1, starting_piece_count + 1)),
                2: list(range(self.board.position_count - starting_piece_count + 1, self.board.position_count + 1))
            }

            for key, row in self.board.position_layout.items():
                for key, position in row.items():
                    player_number = 1 if position in player_starting_positions[1] else 2 if position in player_starting_positions[2] else None

                    if player_number:
                        pieces.append(self.create_piece(player_number, position))

        self.board.pieces = pieces

    def create_piece(self, player_number, position):
        piece = Piece(variant=self.board.variant)
        piece.player = player_number
        piece.position = position
        piece.board = self.board

        return piece