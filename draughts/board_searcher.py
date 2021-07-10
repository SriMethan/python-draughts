# -*- coding: utf-8 -*-
#
# This file is part of the python-draughts library.
# Copyright (C) 2010-2018 ImparaAI https://impara.ai (MIT License)
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

WHITE = 2
BLACK = 1

class BoardSearcher:

    def build(self, board):
        self.board = board
        self.uncaptured_pieces = list(filter(lambda piece: not piece.captured, board.pieces))
        self.open_positions = []
        self.filled_positions = []
        self.player_positions = {}
        self.player_pieces = {}
        self.position_pieces = {}

        self.build_filled_positions()
        self.build_open_positions()
        self.build_player_positions()
        self.build_player_pieces()
        self.build_position_pieces()

    def build_filled_positions(self):
        self.filled_positions = reduce((lambda open_positions, piece: open_positions + [piece.position]), self.uncaptured_pieces, [])

    def build_open_positions(self):
        self.open_positions = [position for position in range(1, self.board.position_count) if not position in self.filled_positions]

    def build_player_positions(self):
        self.player_positions = {
            1: reduce((lambda positions, piece: positions + ([piece.position] if piece.player == BLACK else [])), self.uncaptured_pieces, []),
            2: reduce((lambda positions, piece: positions + ([piece.position] if piece.player == WHITE else [])), self.uncaptured_pieces, [])
        }

    def build_player_pieces(self):
        self.player_pieces = {
            1: reduce((lambda pieces, piece: pieces + ([piece] if piece.player == BLACK else [])), self.uncaptured_pieces, []),
            2: reduce((lambda pieces, piece: pieces + ([piece] if piece.player == WHITE else [])), self.uncaptured_pieces, [])
        }

    def build_position_pieces(self):
        self.position_pieces = {piece.position: piece for piece in self.uncaptured_pieces}

    def get_pieces_by_player(self, player_number):
        return self.player_pieces[player_number]

    def get_positions_by_player(self, player_number):
        return self.player_positions[player_number]

    def get_pieces_in_play(self):
        return self.player_pieces[self.board.player_turn] if not self.board.piece_requiring_further_capture_moves else [self.board.piece_requiring_further_capture_moves]

    def get_piece_by_position(self, position):
        return self.position_pieces.get(position)