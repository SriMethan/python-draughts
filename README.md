# python-draughts: A draughts library written purely in python.

## Introduction

This is the module for draughts written in Pure Python. It's based on [python-shogi](https://github.com/gunyarakun/python-shogi), which is based on [python-chess](https://github.com/niklasf/python-chess/commit/6203406259504cddf6f271e6a7b1e04ba0c96165).

## Features

- Supports Python 2.7 and Python 3.3+.

- Supports standard draughts (10x10)

- Legal move generator and move validation.

```python
>>> draughts.Move.from_hub("5i5a") in board.legal_moves
False
```

- Make and unmake moves.

```python
>>> last_move = board.pop() # Unmake last move
>>> last_move
Move.from_hub('2b3a')

>>> board.push(last_move) # Restore
```

- Show a simple ASCII board.

```python
>>> print(board)
l  n  s  g  .  k +B  n  l
.  r  .  .  g  B  .  .  .
p  p  p  p  p  p  .  p  p
.  .  .  .  .  .  p  .  .
.  .  .  .  .  .  .  .  .
.  .  P  .  .  .  .  .  .
P  P  .  P  P  P  P  P  P
.  .  .  .  .  .  .  R  .
L  N  S  G  K  G  S  N  L
<BLANKLINE>
S*1
```

- Show a PDN style board.

```python
>>> print(board.pdn_str())
後手の持駒：
  ９ ８ ７ ６ ５ ４ ３ ２ １
+---------------------------+
|v香v桂v銀v金 ・v玉 馬v桂v香|一
| ・v飛 ・ ・v金 角 ・ ・ ・|二
|v歩v歩v歩v歩v歩v歩 ・v歩v歩|三
| ・ ・ ・ ・ ・ ・v歩 ・ ・|四
| ・ ・ ・ ・ ・ ・ ・ ・ ・|五
| ・ ・ 歩 ・ ・ ・ ・ ・ ・|六
| 歩 歩 ・ 歩 歩 歩 歩 歩 歩|七
| ・ ・ ・ ・ ・ ・ ・ 飛 ・|八
| 香 桂 銀 金 玉 金 銀 桂 香|九
+---------------------------+
先手の持駒：　銀
```

- Detects checkmates, stalemates.

```python
>>> board.is_stalemate()
False
>>> board.is_game_over()
True
```

- Detects repetitions. Has a half move clock.

```python
>>> board.is_fourfold_repetition()
False
>>> board.move_number
8
```

- Detects checks and attacks.

```python
>>> board.is_check()
True
>>> board.is_attacked_by(draughts.BLACK, draughts.A4)
True
>>> attackers = board.attackers(draughts.BLACK, draughts.H5)
>>> attackers
SquareSet(0b111000010000000000000000000000000000000000000000000000000000000000000000000000)
>>> draughts.H2 in attackers
True
>>> print(attackers)
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . 1 .
. . . 1 1 1 . . .
```

- Parses and creates HUB representation of moves.

```python
>>> board = draughts.Board()
>>> draughts.Move(draughts.E2, draughts.E4).hub()
'2e4e'
```

- Parses and creates FENs

```python
>>> board.fen()
'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1'
>>> board.piece_at(draughts.I5)
Piece.from_symbol('K')
```

- Read PDNs.

```python
>>> import draughts.PDN

>>> pdn = draughts.PDN.Parser.parse_file('data/games/habu-fujii-2006.pdn')[0]

>>> pdn['names'][draughts.BLACK]
'羽生善治'
>>> pdn['names'][draughts.WHITE]
'藤井猛'
>>> pdn['moves'] # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
['7g7f',
 '3c3d',
    ...,
 '9a9b',
 '7a7b+']
>>> pdn['win']
'b'
```

- Communicate with a CSA protocol. <br/> <br/>
Please see [random_csa_tcp_match](https://github.com/TheYoBots/python-draughts/blob/master/scripts/random_csa_tcp_match).

- Parse professional draughts players' name

```python
>>> import draughts.Person

>>> draughts.Person.Name.is_professional('羽生　善治 名人・棋聖・王位・王座')
True
```

## Performance

python-draughts is not intended to be used by serious draughts engines where
performance is critical. The goal is rather to create a simple and relatively
highlevel library.

You can install the `gmpy2` or `gmpy` (https://code.google.com/p/gmpy/) modules
in order to get a slight performance boost on basic operations like bit scans
and population counts.

python-draughts will only ever import very basic general (non-draughts-related)
operations from native libraries. All logic is pure Python. There will always
be pure Python fallbacks.

## Installing

- With pip:

```python
sudo pip install python-draughts
```

- From current source code:

```python
python setup.py sdist
sudo python setup.py install
```

## How to test

```python
> nosetests
or
> python setup.py test # requires python setup.py install
```

If you want to print lines from the standard output, execute nosetests like following.

```python
> nosetests -s
```

If you want to test among different Python versions, execute tox.

```python
> pip install tox
> tox
```

## How to release

```python
rm -rf dist
python setup.py sdist
twine upload dist/*
```

## Acknowledgements

- [python-chess](https://pypi.python.org/pypi/python-shogi)
- [python-shogi](https://pypi.python.org/pypi/chess)
- [draughtsnet](https://github.com/RoepStoep/draughtsnet)