'''
solve_dual_force.py

2021-06-18-1114  archive
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
            cmd = ''
            if df.case == 1:
                cmd = df.cmd_1
            elif df.case == 2:
                cmd = df.cmd_2

            sigs.big_cmd = f'{df.df_cmd} => {cmd}'
            enter_cmd(cb)

            grid_name = df.df_cmd[0:3]
            grid_index = GRID_NAMES.index(grid_name)
            square = df.square
            highlight_square(cb, grid_index, square)

            color_df_pair(cb)


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

def highlight_square(cb, grid_index, sqr):
    s.gui_cmd_name = s.gui_cmd_type.color
    s.color_cmd.index = grid_index
    s.color_cmd.color = colors.highlight
    s.color_cmd.tag = f'SS_{sqr}'
    cb()
    s.color_cmd.tag = f'BS_{sqr}'
    cb()
# </editor-fold>

# <editor-fold desc="dual force coloring"
def color_df_pair(cb):
    try:
        global board_list_1
        global board_list_2
        global board_list_3

        for grid_index in range(NUMBER_OF_GRIDS):
            for square in SQUARES:
                cell = board_list_3[grid_index][square]
                if cell[0] in DIGITS:
                    cell_1 = board_list_1[grid_index][square]
                    cell_2 = board_list_2[grid_index][square]

                    if cell_1 != cell:





                    if cell_2[0] != CELL_SOLVE_MARK and cell_1[0] != CELL_SOLVE_MARK:
                        color_dig2_dig1(cb, cell, cell_2, cell_1)
                    if cell_2[0] != CELL_SOLVE_MARK and cell_1[0] == CELL_SOLVE_MARK:
                        color_dig2_set1(cb, cell, cell_2, cell_1)
                    if cell_2[0] == CELL_SOLVE_MARK and cell_1[0] != CELL_SOLVE_MARK:
                        color_set2_dig1(cb, cell, cell_2, cell_1)
                    if cell_2[0] == CELL_SOLVE_MARK and cell_1[0] == CELL_SOLVE_MARK:
                        color_set2_set1(cb, cell, cell_2, cell_1)

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def color_dig2_dig1(cb, cell, cell_2, cell_1):
    if cell_1 == cell_2:
        pass
    else:
        pass

def color_dig2_set1(cb, cell, cell_2, cell_1):
    if cell_1 == cell_2:
        pass
    else:
        pass

def color_set2_dig1(cb, cell, cell_2, cell_1):
    if cell_1 == cell_2:
        pass
    else:
        pass

def color_set2_set1(cb, cell, cell_2, cell_1):
    if cell_1 == cell_2:
        pass
    else:
        pass
# </editor-fold>

# <editor-fold desc="count & sort"
def count(df_list):
    global min_count
    global max_count

    for df1 in df_list:
        if df1.count_1 > max_count:
            max_count = df1.count_1
        if df1.count_2 > max_count:
            max_count = df1.count_2
        if df1.count_1 < min_count:
            min_count = df1.count_1
        if df1.count_2 < min_count:
            max_count = df1.count_2
    return (min_count, max_count)

def sort():
    try:
        global dual_force_list

        if len(dual_force_list) > 1:
            df_min_count, df_max_count = count(dual_force_list)

        if df_max_count == MAX_CELLS:
            max_list = [df for df in dual_force_list if df.count_1 == MAX_CELLS or
                        df.count_2 == MAX_CELLS]


        df_fails = [df for df in dual_force_list if df.is_Fail]

        if len(max_list) > 0:
            sigs.big_cmd = max_list[0].df_cmd
            square = max_list[0].square
            if max_list.count_1 == MAX_CELLS:
                pass
            elif max_list.ount_2 == MAX_CELLS:
                pass

        if len(df_fails) > 1:
            fail_min_count, fail_max_count = count(df_fails)


        print('max_list')
        print('='*50)
        for df in max_list:
            print(df)
        print()

        print('fails')
        print('='*50)
        for df in df_fails:
            print(df)
        print()

    except Exception as e:
        logger_except.exception(e)
        sys.exit()
# </editor-fold>


if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
