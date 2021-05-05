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

import utility as u
# </editor-fold>

# <editor-fold desc="Global Constants"
IS_DEBUG = False
BP = 0

DIGITS = '123456789'
MAX_DIGITS = len(DIGITS)
LIST_TYPE = []
STRING_TYPE = ''
MAX_CELLS = 81
PERIOD = '.'
ZERO = '0'

BLOCK_LIMITED_PEERS = {
    20: [0, 1, 2, 9, 10, 11, 18, 19],
    23: [3, 4, 5, 12, 13, 14, 21, 22],
    47: [27, 28, 29, 36, 37, 38, 45, 46],
    53: [33, 34, 35, 42, 43, 44, 51, 52],
    77: [57, 58, 59, 66, 67, 68, 75, 76],
    80: [60, 61, 62, 69, 70, 71, 78, 79]
}
PEERS =  {
    0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72],
    1: [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 28, 37, 46, 55, 64, 73],
    2: [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 29, 38, 47, 56, 65, 74],
    3: [0, 1, 2, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 30, 39, 48, 57, 66, 75],
    4: [0, 1, 2, 3, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 31, 40, 49, 58, 67, 76],
    5: [0, 1, 2, 3, 4, 6, 7, 8, 12, 13, 14, 21, 22, 23, 32, 41, 50, 59, 68, 77],
    6: [0, 1, 2, 3, 4, 5, 7, 8, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78],
    7: [0, 1, 2, 3, 4, 5, 6, 8, 15, 16, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79],
    8: [0, 1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 24, 25, 26, 35, 44, 53, 62, 71, 80],
    9: [0, 1, 2, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 36, 45, 54, 63, 72],
    10: [0, 1, 2, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 28, 37, 46, 55, 64, 73],
    11: [0, 1, 2, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29, 38, 47, 56, 65, 74],
    12: [3, 4, 5, 9, 10, 11, 13, 14, 15, 16, 17, 21, 22, 23, 30, 39, 48, 57, 66, 75],
    13: [3, 4, 5, 9, 10, 11, 12, 14, 15, 16, 17, 21, 22, 23, 31, 40, 49, 58, 67, 76],
    14: [3, 4, 5, 9, 10, 11, 12, 13, 15, 16, 17, 21, 22, 23, 32, 41, 50, 59, 68, 77],
    15: [6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78],
    16: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79],
    17: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 24, 25, 26, 35, 44, 53, 62, 71, 80],
    18: [0, 1, 2, 9, 10, 11, 19, 20, 21, 22, 23, 24, 25, 26, 27, 36, 45, 54, 63, 72],
    19: [0, 1, 2, 9, 10, 11, 18, 20, 21, 22, 23, 24, 25, 26, 28, 37, 46, 55, 64, 73],
    20: [0, 1, 2, 9, 10, 11, 18, 19, 21, 22, 23, 24, 25, 26, 29, 38, 47, 56, 65, 74],
    21: [3, 4, 5, 12, 13, 14, 18, 19, 20, 22, 23, 24, 25, 26, 30, 39, 48, 57, 66, 75],
    22: [3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 23, 24, 25, 26, 31, 40, 49, 58, 67, 76],
    23: [3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 24, 25, 26, 32, 41, 50, 59, 68, 77],
    24: [6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 33, 42, 51, 60, 69, 78],
    25: [6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 34, 43, 52, 61, 70, 79],
    26: [6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 35, 44, 53, 62, 71, 80],
    27: [0, 9, 18, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 54, 63, 72],
    28: [1, 10, 19, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 55, 64, 73],
    29: [2, 11, 20, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 56, 65, 74],
    30: [3, 12, 21, 27, 28, 29, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 57, 66, 75],
    31: [4, 13, 22, 27, 28, 29, 30, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 58, 67, 76],
    32: [5, 14, 23, 27, 28, 29, 30, 31, 33, 34, 35, 39, 40, 41, 48, 49, 50, 59, 68, 77],
    33: [6, 15, 24, 27, 28, 29, 30, 31, 32, 34, 35, 42, 43, 44, 51, 52, 53, 60, 69, 78],
    34: [7, 16, 25, 27, 28, 29, 30, 31, 32, 33, 35, 42, 43, 44, 51, 52, 53, 61, 70, 79],
    35: [8, 17, 26, 27, 28, 29, 30, 31, 32, 33, 34, 42, 43, 44, 51, 52, 53, 62, 71, 80],
    36: [0, 9, 18, 27, 28, 29, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 54, 63, 72],
    37: [1, 10, 19, 27, 28, 29, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 55, 64, 73],
    38: [2, 11, 20, 27, 28, 29, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 56, 65, 74],
    39: [3, 12, 21, 30, 31, 32, 36, 37, 38, 40, 41, 42, 43, 44, 48, 49, 50, 57, 66, 75],
    40: [4, 13, 22, 30, 31, 32, 36, 37, 38, 39, 41, 42, 43, 44, 48, 49, 50, 58, 67, 76],
    41: [5, 14, 23, 30, 31, 32, 36, 37, 38, 39, 40, 42, 43, 44, 48, 49, 50, 59, 68, 77],
    42: [6, 15, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 51, 52, 53, 60, 69, 78],
    43: [7, 16, 25, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 51, 52, 53, 61, 70, 79],
    44: [8, 17, 26, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 51, 52, 53, 62, 71, 80],
    45: [0, 9, 18, 27, 28, 29, 36, 37, 38, 46, 47, 48, 49, 50, 51, 52, 53, 54, 63, 72],
    46: [1, 10, 19, 27, 28, 29, 36, 37, 38, 45, 47, 48, 49, 50, 51, 52, 53, 55, 64, 73],
    47: [2, 11, 20, 27, 28, 29, 36, 37, 38, 45, 46, 48, 49, 50, 51, 52, 53, 56, 65, 74],
    48: [3, 12, 21, 30, 31, 32, 39, 40, 41, 45, 46, 47, 49, 50, 51, 52, 53, 57, 66, 75],
    49: [4, 13, 22, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 50, 51, 52, 53, 58, 67, 76],
    50: [5, 14, 23, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 51, 52, 53, 59, 68, 77],
    51: [6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 60, 69, 78],
    52: [7, 16, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 61, 70, 79],
    53: [8, 17, 26, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 62, 71, 80],
    54: [0, 9, 18, 27, 36, 45, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74],
    55: [1, 10, 19, 28, 37, 46, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74],
    56: [2, 11, 20, 29, 38, 47, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74],
    57: [3, 12, 21, 30, 39, 48, 54, 55, 56, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77],
    58: [4, 13, 22, 31, 40, 49, 54, 55, 56, 57, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77],
    59: [5, 14, 23, 32, 41, 50, 54, 55, 56, 57, 58, 60, 61, 62, 66, 67, 68, 75, 76, 77],
    60: [6, 15, 24, 33, 42, 51, 54, 55, 56, 57, 58, 59, 61, 62, 69, 70, 71, 78, 79, 80],
    61: [7, 16, 25, 34, 43, 52, 54, 55, 56, 57, 58, 59, 60, 62, 69, 70, 71, 78, 79, 80],
    62: [8, 17, 26, 35, 44, 53, 54, 55, 56, 57, 58, 59, 60, 61, 69, 70, 71, 78, 79, 80],
    63: [0, 9, 18, 27, 36, 45, 54, 55, 56, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74],
    64: [1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74],
    65: [2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 66, 67, 68, 69, 70, 71, 72, 73, 74],
    66: [3, 12, 21, 30, 39, 48, 57, 58, 59, 63, 64, 65, 67, 68, 69, 70, 71, 75, 76, 77],
    67: [4, 13, 22, 31, 40, 49, 57, 58, 59, 63, 64, 65, 66, 68, 69, 70, 71, 75, 76, 77],
    68: [5, 14, 23, 32, 41, 50, 57, 58, 59, 63, 64, 65, 66, 67, 69, 70, 71, 75, 76, 77],
    69: [6, 15, 24, 33, 42, 51, 60, 61, 62, 63, 64, 65, 66, 67, 68, 70, 71, 78, 79, 80],
    70: [7, 16, 25, 34, 43, 52, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 78, 79, 80],
    71: [8, 17, 26, 35, 44, 53, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 78, 79, 80],
    72: [0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 73, 74, 75, 76, 77, 78, 79, 80],
    73: [1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 72, 74, 75, 76, 77, 78, 79, 80],
    74: [2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 72, 73, 75, 76, 77, 78, 79, 80],
    75: [3, 12, 21, 30, 39, 48, 57, 58, 59, 66, 67, 68, 72, 73, 74, 76, 77, 78, 79, 80],
    76: [4, 13, 22, 31, 40, 49, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 77, 78, 79, 80],
    77: [5, 14, 23, 32, 41, 50, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 78, 79, 80],
    78: [6, 15, 24, 33, 42, 51, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80],
    79: [7, 16, 25, 34, 43, 52, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80],
    80: [8, 17, 26, 35, 44, 53, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]
}
BLOCK_INDEX = [20, 23, 47, 53, 77, 80]
# <editor-fold desc="GRID_MASK"
r1 = '111111000'
r2 = '111111000'
r3 = '11.11.000'
# --------------
r4 = '111000111'
r5 = '111000111'
r6 = '11.00011.'
# --------------
r7 = '000111111'
r8 = '000111111'
r9 = '00011.11.'

band_1 = r1 + r2 + r3
band_2 = r4 + r5 + r6
band_3 = r7 + r8 + r9

GRID_MASK = band_1 + band_2 + band_3
# </editor-fold>
GRID_BASE = [
    0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13,
    14, 18, 19, 21, 22, 27, 28, 29, 33, 34, 35,
    36, 37, 38, 42, 43, 44, 45, 46, 51, 52, 57]
GRID_NEXT = [
    6, 7, 8, 15, 16, 17, 20, 23, 24, 25, 26,
    30, 31, 32, 39, 40, 41, 47, 48, 49, 50, 53,
    54, 55, 56, 63, 64, 65, 72, 73, 74, 77, 80]
GRID_LEFT = [
    58, 59, 60, 61, 62,
    66, 67, 68, 69, 70,
    71, 75, 76, 78, 79]
PAIR_SIZE = len(GRID_BASE)
LEFT_SIZE = len(GRID_LEFT)

CODE_BOOK = [
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
    ['0', 'k', 'm', 'r', 's', 't', 'u', 'w', 'x', 'z']]
DECODE_BOOK = {'.': '00', '0': '00',
    '1': '10', '2': '20', '3': '30', '4': '40', '5': '50',
    '6': '60', '7': '70', '8': '80', '9': '90',
    'A': '11', 'B': '21', 'C': '31', 'D': '41', 'E': '51',
    'F': '61', 'G': '71', 'H': '81', 'I': '91',
    'a': '12', 'b': '22', 'c': '32', 'd': '42', 'e': '52',
    'f': '62', 'g': '72', 'h': '82', 'i': '92',
    'k': '13', 'm': '23', 'r': '33', 's': '43', 't': '53',
    'u': '63', 'w': '73', 'x': '83', 'z': '93'}
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
    print('codec.py is being imported')
    #

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
