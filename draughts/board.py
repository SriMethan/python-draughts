# -*- coding: utf-8 -*-
#
# This file is part of the python-draughts library.
# Copyright (C) 2010-2018 ImparaAI https://impara.ai (MIT LICENSE)
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
from copy import deepcopy
from functools import reduce
from .board_searcher import BoardSearcher
from .board_initializer import BoardInitializer
import pickle

WHITE = 2
BLACK = 1

class Board:

    def __init__(self, variant='standard', fen='startpos'):
        if fen != 'startpos':
            self.player_turn = 2 if fen[0].lower() == 'w' else 1
        else:
            self.player_turn = 2
        if variant == 'brazilian' or variant == 'russian':
            self.width = 4
            self.height = 8
        else:
            self.width = 5
            self.height = 10
        self.position_count = self.width * self.height
        if variant == 'frysk!':
            self.rows_per_user_with_pieces = 1
        elif variant == 'brazilian' or variant == 'russian':
            self.rows_per_user_with_pieces = 3
        else:
            self.rows_per_user_with_pieces = 4
        self.position_layout = {}
        self.piece_requiring_further_capture_moves = None
        self.previous_move_was_capture = False
        self.variant = variant
        self.fen = fen
        self.searcher = BoardSearcher()
        BoardInitializer(self, self.fen).initialize()

    def count_movable_player_pieces(self, player_number=1, captures=None):
        if captures is None:
            captures = []
        return reduce((lambda count, piece: count + (1 if piece.is_movable(captures) else 0)), self.searcher.get_pieces_by_player(player_number), 0)

    def get_possible_moves(self, captures):
        capture_moves = self.get_possible_capture_moves(captures)

        return capture_moves if capture_moves else self.get_possible_positional_moves()

    def get_possible_capture_moves(self, captures):
        return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves(captures)), self.searcher.get_pieces_in_play(), [])

    def get_possible_positional_moves(self):
        return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.searcher.get_pieces_in_play(), [])

    def position_is_open(self, position):
        return not self.searcher.get_piece_by_position(position)

    def create_new_board_from_move(self, move, move_number, captures, return_captured=False):
        new_board = pickle.loads(pickle.dumps(self, -1))  # A lot faster that deepcopy
        enemy_position = None

        if move in self.get_possible_capture_moves(captures):
            if return_captured:
                enemy_position = new_board.perform_capture_move(move, move_number, captures, return_captured=return_captured)
            else:
                new_board.perform_capture_move(move, move_number, captures)
        else:
            new_board.perform_positional_move(move, move_number)

        if return_captured:
            return new_board, enemy_position
        else:
            return new_board

    def perform_capture_move(self, move, move_number, captures, return_captured=False):
        self.previous_move_was_capture = True
        piece = self.searcher.get_piece_by_position(move[0])
        originally_was_king = piece.king
        enemy_piece = piece.capture_move_enemies[move[1]]
        enemy_position = enemy_piece.position
        enemy_piece.capture()
        self.move_piece(move, move_number)
        if not originally_was_king and self.variant != 'russian':
            was_king = piece.king
            piece.king = False
            further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves(captures + [enemy_position]) if move[1] == capture_move[0]]
            if not further_capture_moves_for_piece and was_king:
                piece.king = True
        else:
            further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves(captures + [enemy_position]) if move[1] == capture_move[0]]

        if further_capture_moves_for_piece:
            self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
        else:
            self.piece_requiring_further_capture_moves = None
            self.switch_turn()
        if return_captured:
            return enemy_position

    def perform_positional_move(self, move, move_number):
        self.previous_move_was_capture = False
        self.move_piece(move, move_number)
        self.switch_turn()

    def switch_turn(self):
        self.player_turn = BLACK if self.player_turn == WHITE else WHITE

    def move_piece(self, move, move_number):
        self.searcher.get_piece_by_position(move[0]).move(move[1], move_number)
        self.pieces = sorted(self.pieces, key=lambda piece: piece.position if piece.position else 0)

    def is_valid_row_and_column(self, row, column):
        if row < 0 or row >= self.height:
            return False

        if column < 0 or column >= self.width:
            return False

        return True

    def __setattr__(self, name, value):
        super(Board, self).__setattr__(name, value)

        if name == 'pieces':
            [piece.reset_for_new_board() for piece in self.pieces]

            self.searcher.build(self)