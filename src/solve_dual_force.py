'''
solve_dual_force.py

/home/Big/Dropbox/root/private/computer/software/PyCharm
/Big'sSudoku/play/src/solve_dual_force.py
'''

# <editor-fold desc="python imports"
import copy
from dataclasses import dataclass
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import board
import cmds
import colors
import settings as g
import signals as sigs
import solve
import solve_claim
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
DIGITS = g.DIGITS
ROWS = g.ROWS
SQUARES = g.SQUARES
MAX_CELLS = g.MAX_CELLS
NUMBER_OF_GRIDS = g.NUMBER_OF_GRIDS
CELL_SOLVE_MARK = g.CELL_SOLVE_MARK
SET = g.OP_SET
# </editor-fold>

board_list_1 = copy.deepcopy(board.board_list)
board_list_2 = copy.deepcopy(board.board_list)
board_list_3 = copy.deepcopy(board.board_list)
dual_force_list = []
grid_save_list =[]

min_count = 90
max_count = 0
original_count = 0

@dataclass
class DualForceType:
    is_Fail: bool = False
    case: int = 0
    df_cmd: str = 'DF'
    square: str = '00'
    cmd_1: str = 'r0c0=n0'
    cmd_2: str = 'r1c1=n0'
    count_1: int = 0
    count_2: int = 0


def do(cb):
    try:
        global board_list_1
        global board_list_2
        global board_list_3
        global dual_force_list
        global max_count
        global min_count

        board_list_1 = copy.deepcopy(board.board_list)
        board_list_2 = copy.deepcopy(board.board_list)
        board_list_3 = copy.deepcopy(board.board_list)
        grids_save(cb)

        if do_grids(cb):
            df = dual_force_list[-1]
            color_solve_all(cb, df)
            cmd = ''
            if df.case == 1:
                cmd = df.cmd_1
            elif df.case == 2:
                cmd = df.cmd_2

            sigs.big_cmd = f'{df.df_cmd} => {cmd}'
            enter_cmd(cb)

            grid_name = df.df_cmd[0:3]
            grid_index = s.grid_index_from_name(grid_name)
            square = df.square
            highlight_square(cb, grid_index, square)

            if cmds.basic_cmd(cb, cmd):
                return True
            return False

        else:
            df_fails = [df for df in dual_force_list if df.is_Fail]
            if len(df_fails) > 0:
                min_count, max_count = count(df_fails)
            BP

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

# <editor-fold desc="major support"
def do_grids(cb):
    global original_count

    sigs.is_DF = True
    for grid_index in range(NUMBER_OF_GRIDS):
        brd = board.board_list[grid_index]
        highlight_grid(cb, grid_index)
        original_count = brd[1]
        if do_squares(cb, grid_index):
            return True
    return False

def do_squares(cb, grid_index):
    global dual_force_list

    x, y, z = GRID_NAMES[grid_index]
    for sqr in g.SQUARES:
        brd = board.board_list[grid_index]
        cell = brd[sqr]
        if cell[0] in g.DIGITS and len(cell) == 2:
            highlight_square(cb, grid_index, sqr)

            dual_force_list.append(DualForceType())
            long_cmd = f'{z}{cell}-{x}{sqr[0]}-{y}{sqr[1]}'
            sigs.big_cmd = f'{x + y + z} DF = {long_cmd}'
            dual_force_list[-1].df_cmd = sigs.big_cmd
            dual_force_list[-1].square = sqr

            enter_cmd(cb)
            if do_cases(cb, grid_index, sqr):
                return True
    return False

def do_cases(cb, grid_index, sqr):
    global board_list_1
    global board_list_2
    global board_list_3
    global dual_force_list

    brd = board.board_list[grid_index]
    cell = brd[sqr]
    x, y, z = GRID_NAMES[grid_index]
    cmd_base = x + sqr[0] + y + sqr[1] + SET + z
    cmd_list = [cmd_base + val for val in cell]
    for case, cmd in enumerate(cmd_list, start=1):
        sigs.df_case = case
        dual_force_list[-1].case = case
        if cmds.basic_cmd(cb, cmd):
            other_solves(cb)
            display_cmd(cb)

            if sigs.is_DF_Fail:
                dual_force_list[-1].is_Fail = True
                sigs.is_DF_Fail = False
            if case == 1:
                dual_force_list[-1].cmd_1 = cmd
                dual_force_list[-1].count_1 = brd[1]
                board_list_1 = copy.deepcopy(board.board_list)
            elif case == 2:
                dual_force_list[-1].cmd_2 = cmd
                dual_force_list[-1].count_2 = brd[1]
                board_list_2 = copy.deepcopy(board.board_list)

            board.board_list = copy.deepcopy(board_list_3)
            brd = board.board_list[grid_index]

            grids_restore(cb)
            display_cmd(cb)

            if dual_force_list[-1].count_1 == MAX_CELLS:
                return True
            elif dual_force_list[-1].count_2 == MAX_CELLS:
                return True

    return False

def other_solves(cb):
    '''
    All uses all seolution methods.

    :return:
    '''

    try:
        while True:
            if solve.singles(cb):
                if sigs.is_DF_Fail:
                    return
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
            return

        print('Solved All can do!')

    except Exception as e:
        logger_except.exception(e)
        sys.exit()
# </editor-fold>

# <editor-fold desc="dual force coloring"
def color_solve_all(cb, df):
    try:
        global board_list_1
        global board_list_2
        global board_list_3

        grid_name = df.df_cmd[0:3]
        grid_index = GRID_NAMES.index(grid_name)
        square = df.square
        highlight_square(cb, grid_index, square)

        brd_list = board_list_1
        if df.case == 1:
            cmd = df.cmd_1
        elif df.case == 2:
            brd_list = board_list_2
            cmd = df.cmd_2

        for i in range(NUMBER_OF_GRIDS):
            for sqr in SQUARES:
                cell_solve = brd_list[i][sqr]
                cell_orig = board_list_3[i][sqr]
                if cell_solve != cell_orig:
                    color_digit(cb, i, sqr, cell_solve[1], colors.assert_small_square)
        return

    except Exception as e:
        logger_except.exception(e)
        sys.exit()
# </editor-fold>

# <editor-fold desc="gui callback"
def display_cmd(cb):
    s.gui_cmd_name = s.gui_cmd_type.display
    cb()

def enter_cmd(cb):
    s.gui_cmd_name = s.gui_cmd_type.entry
    s.entry_cmd.entry = sigs.big_cmd
    cb()

def grids_restore(cb):
    s.gui_cmd_name = s.gui_cmd_type.grids_restore
    cb()

def grids_save(cb):
    s.gui_cmd_name = s.gui_cmd_type.grids_save
    cb()

def highlight_grid(cb, grid_index):
    s.gui_cmd_name = s.gui_cmd_type.lift
    s.lift_cmd.index = grid_index
    cb()


def color_digit(cb, grid_index, sqr, value, color):
    s.gui_cmd_name = s.gui_cmd_type.color
    s.color_cmd.index = grid_index
    s.color_cmd.color = color
    s.color_cmd.tag =  f'SS_{sqr}-{value}'
    cb()


def highlight_square(cb, grid_index, sqr):
    s.gui_cmd_name = s.gui_cmd_type.color
    s.color_cmd.index = grid_index
    s.color_cmd.color = colors.highlight
    s.color_cmd.tag = f'SS_{sqr}'
    cb()
    s.color_cmd.tag = f'BS_{sqr}'
    cb()
# </editor-fold>






if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
