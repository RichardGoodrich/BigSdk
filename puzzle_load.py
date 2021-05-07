'''
puzzle_load.py

2021.04.17 Sat
'''

# <editor-fold desc="python imports"
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import cmds
from codec import Codec
import dancing_links
import settings as g
import signals as sigs
import support as s
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
BP = g.BREAK_POINT
SET = g.OP_SET

PUZZLE_DEFAULT =\
'.....627........5....54..311.....5..97.8.2.64..6.....764..29....8........526.....'
# </editor-fold>

codec = Codec()
encoded_puzzle = ''
solved_puzzle = ''

def load(cb, puz=PUZZLE_DEFAULT):
    try:
        global codec
        global encoded_puzzle
        global solved_puzzle

        if sigs.is_grid:
            puzzle_list = puz
            num_list = [item if len(item) == 1 else '.' for item in puzzle_list]
            puzzle_81 = ''.join(num_list)
        else:
            puzzle_81 = puz
            puzzle_list = list(puzzle_81)

        puzzle_81 = puzzle_81.replace('0', '.')

        if filter_puzzle(puzzle_list):
            return False

        solved_puzzle = dancing_links.filter(20, puzzle_81)
        encoded_puzzle = codec.encode(puzzle_81, solved_puzzle)

        if '.' in solved_puzzle:
            return False

        do_puzzle(cb, puzzle_list)

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_puzzle(cb, puz_list):
    try:
        puzValue = get_puz_value(puz_list)
        while True:
            try:
                step = sigs.step

                cmd = next(puzValue)
                cmds.big_cmd_load(cb, cmd)

                if sigs.step != sigs.steps.no_step:
                    s.gui_cmd_name = s.gui_cmd_type.wait
                    cb()

            except Exception as e:
                s.gui_cmd_name = s.gui_cmd_type.display
                cb()

                # sigs.is_load(False)
                return

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def get_puz_value(puz_list):
    try:
        for i, value in enumerate(puz_list):
            square = g.SQUARES[i]
            if value != '.':
                cmd = 'r' + square[0] + 'c' + square[1] + SET + 'n' + value
                yield cmd
    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def filter_puzzle(puz_list):
    '''

    :param puz_list:
    :return: False if passes filter
    '''
    try:
        if len(puz_list) != g.MAX_CELLS:
            return True

        digits = g.DIGITS
        count = 0
        for value in puz_list:
            if len(value) > 1:
                for item in value:
                    if item not in g.DIGITS:
                        return True
            else:
                if value not in g.DIGITS and value != '.':
                    return True
                if value in digits:
                    digits = digits.replace(value, '')
                count += 1

        if count < 17:
            return True

        if len(digits) > 1:
            '''
            There must be at least 8 sudoku digits present
            Refer to Olivier Grégoire\'s suggestion about checking for 8 digits
               http://norvig.com/sudoku.html by Peter Norvig
            '''
            return True

        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()


if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
