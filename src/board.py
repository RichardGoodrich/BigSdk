'''
board.py  2021.04.17 Sat

/home/Big/Dropbox/root/private/computer/software
/PyCharm/Big'sSudoku/play/src/board.py

'''

# <editor-fold desc="python imports"
import copy
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import settings as g
import signals as sigs
# </editor-fold>

# <editor-fold desc="logging setup"
logger_except = log.getLogger(__name__)
logger_except.setLevel(log.INFO)
formatter_except = log.Formatter(sigs.except_format)

file_handler_except = log.FileHandler(sigs.except_path)
file_handler_except.setLevel(log.ERROR)
file_handler_except.setFormatter(formatter_except)
logger_except.addHandler(file_handler_except)
# </editor-fold>

# <editor-fold desc="globals"
BP = 0

# <editor-fold desc="GRID_DICT Docs"
''' 
index = 0   3-letter grid name
index = 1   int count of solved cells
index = 01 to 09   digits not solved in that col
index = 10 to 90   digits not solved in that row
'''
# </editor-fold>

GRID_DICT = g.BOARD_GRID_DICT

# </editor-fold>

rcn = None
rnc = None
ncr = None
bns = None
board_list = []

def cmd(index, square, value):
    try:
        grid = board_list[index]
        grid[square] = value
        if value == '' and sigs.is_DF:
            return
        if value[0] not in g.DIGITS:
            digit = value[1]
            grid[1] += 1
            col_index = '0' + square[1]
            row_index = square[0] + '0'
            grid[col_index] = grid[col_index].replace(digit, '')
            grid[row_index] = grid[row_index].replace(digit, '')
    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def erase():
    try:
        global board_list
        global rcn
        global rnc
        global ncr
        global bns

        board_list = [copy.deepcopy(GRID_DICT) for _ in range(4)]

        for i in range(4):
            board_list[i][0] = g.GRID_NAMES[i]

        rcn = board_list[0]
        rnc = board_list[1]
        ncr = board_list[2]
        bns = board_list[3]

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def print_grid(grid_index):
    '''
    Peter Norvig's Print Sudoku Grid

    link: https://norvig.com/sudoku.html

    :param grid_index:
    :return:
    '''
    try:
        grid = board_list[grid_index]
        width = 1 + max(len(grid[s]) for s in g.SQUARES)
        line = '+'.join(['-' * (width * 3)] * 3)
        print(g.NL + g.GRID_NAMES[grid_index])
        print(line)

        for r in g.DIGITS:
            print(''.join(grid[r + c].center(width)
                          + ('|' if c in '36' else '')
                          for c in g.DIGITS))
            if r in '36': print(line)
        print()

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

erase()


def main():
    # digits = '123456789'
    # squares = [i + j for i in digits for j in digits]
    # grid = {sqr: '12345' for sqr in squares}
    print_grid(0)

if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
    main()
else:
    file = __file__
    print(f'importing {file} ')
