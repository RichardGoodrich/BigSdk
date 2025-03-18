#!/usr/bin/python3

# <editor-fold desc="Python and Tk version"
"""
  Python 3.8.5
  Tkinter 8.6
  >conda deactivate-(default) => '>' | >conda activate => '(base) >'
"""
# </editor-fold>

# <editor-fold desc="Imports"
import sys
# </editor-fold>

# <editor-fold desc="Imports"
import codec_support as s
import settings as g
# </editor-fold>

# <editor-fold desc="Global Constants"
IS_DEBUG = False
LIST_TYPE = []
PERIOD = '.'
STRING_TYPE = ''
ZERO = '0'

BP = g.BREAK_POINT
DIGITS = g.DIGITS
MAX_CELLS = g.MAX_CELLS
MAX_DIGITS = g.MAX_DIGITS

BLOCK_INDEX = s.BLOCK_INDEX
BLOCK_LIMITED_PEERS = s.BLOCK_LIMITED_PEERS

CODE_BOOK = s.CODE_BOOK
DECODE_BOOK = s.DECODE_BOOK

GRID_BASE = s.GRID_BASE
GRID_MASK = s.GRID_MASK
GRID_LEFT = s.GRID_LEFT
GRID_NEXT = s.GRID_NEXT

LEFT_SIZE = s.LEFT_SIZE
PAIR_SIZE = s.PAIR_SIZE
PEERS = s.PEERS
# </editor-fold>

class Codec():
    def __init__(self):
        BP
    def decode(self, encoded):
        '''
        :param encodes: 48 char string
                encoded with g.CODE_BOOK
                (strings are converted to list)
                members of value in g.VALID_GRID_ENTRIES
        :return: Sudoku 81-char string
        '''
        try:
            decode_grid = ['0'] * MAX_CELLS
            given_grid = ['0'] * MAX_CELLS
            solved_grid = ['0'] * MAX_CELLS
            j = 0
            for i, x in enumerate(GRID_MASK):
                if x == '1':
                    value = encoded[j]
                    result = DECODE_BOOK[value]
                    j += 1
                else:
                    result = '00'
                decode_grid[i] = result
            BP
            for i, (digit, code_index) in enumerate(decode_grid):
                solved_grid[i] = digit
            BP
            if IS_DEBUG:
                u.print_grid(decode_grid, 'decode_grid')
                u.print_grid(solved_grid, 'solved_grid')
            BP

            # <editor-fold desc="Solve solved_grid for full house in its blocks"
            for index in BLOCK_INDEX:
                peers = BLOCK_LIMITED_PEERS[index]
                digits = DIGITS
                for digit_index in peers:
                    digit = solved_grid[digit_index]
                    if digit in digits:
                         digits = digits.replace(digit, '')
                    if len(digits) == 1:
                         solved_grid[index] = digits
                         break
            if IS_DEBUG:
                u.print_grid(solved_grid, 'solved_grid')
            BP
            # </editor-fold>

            # <editor-fold desc="Solves remainder of solved_grid"
            for i, digit in enumerate(solved_grid):
                if digit == '0':
                    peers = PEERS[i]
                    digits = DIGITS
                    for digit_index in peers:
                        digit = solved_grid[digit_index]
                        if digit in digits:
                             digits = digits.replace(digit, '')
                        if len(digits) == 1:
                             solved_grid[i] = digits
                             break
            if IS_DEBUG:
                u.print_grid(solved_grid, 'solved_grid')
            BP
            # </editor-fold>

            # <editor-fold desc="Solves given_grid"
            given_grid = solved_grid.copy()
            write_base = {'0': False, '1': False, '2': True, '3': True}
            write_next = {'0': False, '1': True, '2': False, '3': True}
            for i in range(PAIR_SIZE):
                base_index = GRID_BASE[i]
                next_index = GRID_NEXT[i]
                (digit, code_index) = decode_grid[base_index]
                if write_base[code_index]:
                    given_grid[base_index] = PERIOD
                if write_next[code_index]:
                    given_grid[next_index] = PERIOD
            BP
            for i in range(LEFT_SIZE):
                base_index = GRID_LEFT[i]
                (digit, code_index) = decode_grid[base_index]
                if code_index == '1':
                    given_grid[base_index] = PERIOD
            if IS_DEBUG:
                u.print_grid(given_grid, 'given_grid')
            BP
            # </editor-fold>

            given = ''.join(given_grid)
            solved = ''.join((solved_grid))
            return (given, solved)
        except Exception as e:
            print(e)
            print('in codec.encode_puz')
            sys.exit()
            #
    def encode(self, given, solved):
        try:
            assert len(given) == MAX_CELLS
            assert len(solved) == MAX_CELLS
            assert type(given) == type(STRING_TYPE)
            assert type(solved) == type(STRING_TYPE)
            # todo assert members are in g.VALID_GRID_ENTRIES

            encoded = ''
            given_mask = [ZERO] * MAX_CELLS
            given = given.replace(PERIOD, ZERO)
            given_grid = list(given)
            solved_grid = list(solved)
            for i in range(len(given_grid)):
                if given_grid[i] > ZERO:
                    given_mask[i] = '1'

            cd = {'00': 3, '01': 2, '10': 1, '11': 0}
            for i in range(PAIR_SIZE):
                base_index = GRID_BASE[i]
                next_index = GRID_NEXT[i]
                dig_idx = int(solved_grid[base_index])
                c1 = given_mask[base_index]
                c2 = given_mask[next_index]
                code = CODE_BOOK[cd[c1 + c2]][dig_idx]
                encoded += code
            BP
            for i in range(LEFT_SIZE):
                index = GRID_LEFT[i]
                dig_idx = int(solved_grid[index])
                c2 = given_mask[index]
                code = CODE_BOOK[cd['1' + c2]][dig_idx]
                encoded += code
                BP
            return encoded
        except Exception as e:
            print(e)
            print('in codec.encode_puz')
            sys.exit()
            #

if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')

    # <editor-fold desc="Given Grid"
    r1 = '.8..749.5'
    r2 = '..9.382.4'
    r3 = '4...9268.'
    # --------------
    r4 = '..74.58..'
    r5 = '84.917.6.'
    r6 = '..18.34..'
    # --------------
    r7 = '..83417.6'
    r8 = '736259148'
    r9 = '1.4786.9.'

    band_1 = r1 + r2 + r3
    band_2 = r4 + r5 + r6
    band_3 = r7 + r8 + r9

    original_given = band_1 + band_2 + band_3
    # </editor-fold>
    # <editor-fold desc="Solved Grid"
    r1 = '682174935'
    r2 = '519638274'
    r3 = '473592681'
    # --------------
    r4 = '367425819'
    r5 = '845917362'
    r6 = '291863457'
    # --------------
    r7 = '958341726'
    r8 = '736259148'
    r9 = '124786593'

    band_1 = r1 + r2 + r3
    band_2 = r4 + r5 + r6
    band_3 = r7 + r8 + r9

    original_solved = band_1 + band_2 + band_3
    # </editor-fold>

    sdk = Codec()
    sudoku_encoded = sdk.encode(original_given, original_solved)
    sudoku_decoded = sdk.decode(sudoku_encoded)
    decoded_given = sudoku_decoded[0]
    decoded_solved = sudoku_decoded[1]
    BP

else:
    file = __file__
    print(f'importing {file} ')


# <editor-fold desc="How the cell pairing works"
'''
The following applies to the decode_grid list whose members are two digits
in string format.

1. Digit One = cell value (in range 0,1,2,3,4,5,6,7,8,9)  0 = not solved
2. Digit Two = index to the code/decode alphabet (in range 0, 1, 2, 3)

There are 33 cells which are removed in the 'encoded' sudoku string, leaving
48 'base' cells.  The first 33 of these 'base' cells are paired with one
of the 33 'next' (removed cells) to describe their paired status. This
is described by CODE_BOOK with four possible encryption alphabets.

These paired cells are indexed in the following two list of length 33:

Codec.Grid_base  = index of base cell of a pair
Codec.Grid_next  = index of next cell of a pair

If a cell is not indexed in the Code.Grid_base list than it is one of the 48
cells not paired with one of the 33 'next' cells.  Therefore the "Digit Two"
previously described, is indexed in the list "CLUE_TYPE" as either a 1 or 2.
The 1 meaning a GIVEN cell or a SOLVED cell.

However, if the index of those first 33 'base' cells to be in the 'encoded' string
is found in Codec.Grid_base then is has an index to its corresponding 'next' cell
which is found in Codec.Grid_next at the same index value in both lists.
The afore mentioned "Digit Two" now has four possible encrypted alphabets shown
in the PAIR_TYPE list below.

     Cell Pairs
     Visible-Invisible  or base-next
     -----------------
0 = G-G  Given-Given
1 = G-S  Given-Solve
2 = S-G  Solve-Given
3 = S-S  Solve-Solve
'''
# </editor-fold>
