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

from __future__ import unicode_literals

import draughts
import unittest

class BoardTestCase(unittest.TestCase):
    def test_default(self):
        board_none = draughts.Board()
        board_fen = draughts.Board(draughts.STARTING_FEN)
        self.assertEqual(board_none, board_fen)
        self.assertEqual(board_none.fen(), draughts.STARTING_FEN)
        self.assertEqual(str(board_none), str(board_fen))
        self.assertEqual(repr(board_none), repr(board_fen))
        self.assertEqual(board_none.turn, draughts.BLACK)

    def test_stalemate(self):
        board = draughts.Board('+R+N+SGKG+S+N+R/+B+N+SG+LG+S+N+B/P+LPP+LPP+LP/1P2P2P1/9/9/9/9/6k2 b - 200')
        self.assertEqual(len(board.pseudo_legal_moves), 0)

    def test_bishop_center(self):
        board = draughts.Board('9/9/9/9/4B4/9/9/9/9 b - 1')
        self.assertTrue(draughts.Move.from_hub('5e4d') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e3c') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e2b') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e1a') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e6f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e7g') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e8h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e9i') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e4f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e3g') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e2h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e1i') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e6d') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e7c') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e8b') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e9a') in board.legal_moves)

        self.assertTrue(draughts.Move.from_hub('5e3c+') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e2b+') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e1a+') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e7c+') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e8b+') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5e9a+') in board.legal_moves)

        self.assertEqual(len(board.legal_moves), 22)

    def test_bishop_9a(self):
        board = draughts.Board('B8/9/9/9/9/9/9/9/9 b - 1')
        self.assertEqual(len(board.legal_moves), 16)

    def test_double_pawn_in_a_row(self):
        board = draughts.Board('k8/9/9/9/9/9/9/9/P8 b P 1')
        self.assertFalse(draughts.Move.from_hub('P*9b') in board.legal_moves)
        self.assertFalse(draughts.Move.from_hub('P*9c') in board.legal_moves)
        self.assertFalse(draughts.Move.from_hub('P*9d') in board.legal_moves)
        self.assertFalse(draughts.Move.from_hub('P*9e') in board.legal_moves)
        self.assertFalse(draughts.Move.from_hub('P*9f') in board.legal_moves)
        self.assertFalse(draughts.Move.from_hub('P*9g') in board.legal_moves)
        self.assertFalse(draughts.Move.from_hub('P*9h') in board.legal_moves)
        self.assertEqual(len(board.legal_moves), 65)

    def test_suicide(self):
        board = dr.Board('1k7/9/1G7/9/9/9/9/9/9 w - 1')
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('8a8b')))
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('8a9b')))
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('8a7b')))
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('8a6b')))
        self.assertEqual(len(board.legal_moves), 2)

    def test_check_by_dropping_pawn(self):
        # check by dropping pawn
        board = draughts.Board('kn7/9/1G7/9/9/9/9/9/9 b P 1')
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('P*9b')))
        self.assertEqual(len(board.legal_moves), 76)
        board = draughts.Board('kn7/9/9/1NN6/9/9/9/9/9 b P 1')
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('P*9b')))
        self.assertEqual(len(board.legal_moves), 73)

        # king can escape
        board = dr.Board('k8/9/9/9/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('P*9b')))
        self.assertEqual(len(board.legal_moves), 72)

        # dropping pawn is not protected and king cannot escape
        board = draughts.Board('kn7/1n7/9/9/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('P*9b')))
        self.assertEqual(len(board.legal_moves), 71)

        # dropping pawn is protected but king can escape
        board = draughts.Board('kn7/9/9/1N7/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('P*9b')))
        self.assertEqual(len(board.legal_moves), 73)
        board = draughts.Board('k8/9/1S7/9/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('P*9b')))
        self.assertEqual(len(board.legal_moves), 81)

        # dropping pawn can be captured other pieces besides king
        board = draughts.Board('kg7/9/1G7/9/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(draughts.Move.from_hub('P*9b')))
        self.assertEqual(len(board.legal_moves), 77)

    def test_lance_move(self):
        board = draughts.Board('9/9/9/9/4L4/9/9/9/9 b - 1')
        self.assertEqual(len(board.legal_moves), 6)

    def test_is_fourfold_repetition(self):
        board = draughts.Board('ln3g2l/1r2g1sk1/1pp1ppn2/p2ps1ppp/1PP6/2GP4P/P1N1PPPP1/1R2S1SK1/L4G1NL w Bb 44')
        for move_str in ['9d9e', '8h6h', '8b6b', '6h8h', '6b8b', '8h6h', '8b6b', '6h8h',
                         '6b8b', '8h6h', '8b6b', '6h8h']:
            board.push(draughts.Move.from_hub(move_str))
        self.assertFalse(board.is_fourfold_repetition())
        board.push(draughts.Move.from_hub('6b8b'))
        self.assertTrue(board.is_fourfold_repetition())

    def test_legal_moves_in(self):
        board = draughts.Board()
        self.assertTrue(draughts.Move.from_hub('9g9f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('8g8f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('7g7f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('6g6f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5g5f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('4g4f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('3g3f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('2g2f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('1g1f') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('9i9h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('1i1h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('7i7h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('7i6h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('3i4h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('3i3h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('6i7h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('6i6h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('6i5h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('4i5h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('4i4h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('4i3h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('2h7h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('2h6h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('2h5h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('2h4h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('2h3h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('2h1h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5i6h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5i5h') in board.legal_moves)
        self.assertTrue(draughts.Move.from_hub('5i4h') in board.legal_moves)

        # opposite turn
        self.assertFalse(draughts.Move.from_hub('9c9d') in board.legal_moves)

    def test_fen_piece_in_hand_order(self):
        # ref: https://github.com/rhalbersma/scan/blob/master/protocol.txt
        # Invalid fen, but acceptable in python-draughts
        board = draughts.Board('4k4/9/9/9/9/9/9/9/4K4 b 9p2l2n2s2gbr9P2L2N2S2GBR 1')
        self.assertEqual(board.fen(), '4k4/9/9/9/9/9/9/9/4K4 b RB2G2S2N2L9Prb2g2s2n2l9p 1')

    def test_issue_6(self):
        # double pawn should be checked for their own pawn
        board = draughts.Board('lr7/3skgg1+B/2n2s1pp/p1p1ppP2/3p1np2/1PPPP4/PS1G1P2P/2GS3R1/LNK4NL w L2pb 58')
        self.assertEqual(len(board.legal_moves), 92)

    def test_issue_7(self):
        # SQUARES_R45 was wrong
        board = draughts.Board('lnsg1g1nl/3k3r1/pppp1s1pp/b3p1p2/2PP1p2B/P3P3P/1P3PPP1/1S3K1R1/LN1G1GSNL w - 1')
        self.assertEqual(len(board.legal_moves), 39)

    def test_issue_9(self):
        self.assertEqual(bool(draughts.Move.null()), False)
        board = draughts.Board()
        board.push(draughts.Move.null())
        self.assertEqual(board.captured_piece_stack[0], 0)

    def test_issue_15(self):
        # Issue: All moves from "9a" are not pseudo legal.
        board = draughts.Board()
        # pass turn to white
        board.push(draughts.Move.from_hub('9h9g'))
        move = draughts.Move.from_hub('9a9b')
        self.assertEqual(board.is_pseudo_legal(move), True)

    def test_issue_17(self):
        board = draughts.Board('ln1g3+Rl/1ks4s1/pp1gppbpp/2p3N2/9/5P1P1/PPPP1S1bP/2K1R1G2/LNSG3NL w 4p 42')
        move = draughts.Move.from_hub('2g5d+')
        self.assertTrue(move in board.legal_moves)

if __name__ == '__main__':
    unittest.main()
