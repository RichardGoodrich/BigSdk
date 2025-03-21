'''
solve.py  2021.05.04 Tue

/home/Big/Dropbox/root/private/computer/software/PyCharm
/Big'sSudoku/play/src/solve.py
'''

# <editor-fold desc="python imports"
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import board
import cmds
import settings as g
import signals as sigs
import solve_claim
import solve_dual_force
import solve_point
import solve_subsets
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
GRID_NAMES = g.GRID_NAMES
COLS = g.COLS
ROWS = g.ROWS
MAX_CELLS = g.MAX_CELLS
# </editor-fold>

def all(cb):
    '''
    All uses all seolution methods.

    :return:
    '''

    try:
        while True:
            if singles(cb):
                if s.is_solved():
                    return
                continue
            if solve_subsets.do(cb):
                if s.is_solved():
                    return
                continue
            if solve_claim.do(cb):
                if s.is_solved():
                    return
                continue
            if solve_point.do(cb):
                if s.is_solved():
                    return
                continue
            if solve_point.do(cb):
                if s.is_solved():
                    return
                continue
            if solve_dual_force.do(cb):
                if s.is_solved():
                    return
                continue

            return

        print('Solved All can do!')

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def singles(cb):
    '''
    Singles are solved by row on all grids.

    :return:
    '''

    try:
        for grid_index in range(4):
            grid = board.board_list[grid_index]
            grid_name = GRID_NAMES[grid_index]
            for row in ROWS:
                for square in row:
                    values = grid[square]
                    if len(values) == 1:
                        cmd = s.form_cmd(grid[0], square, SET, values)
                        sigs.big_cmd = f'{grid_name} NS = {cmd}'
                        cmds.big_cmd(cb)
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
