'''
cell_cmd.py

2021-05-05 Wed
'''

# <editor-fold desc="python imports"
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import board
from cmd_support import CmdS as c
import colors
import settings as g
import signals as sigs
import support as s
# </editor-fold>

# <editor-fold desc="globasl"
L2 = ' ' * 3
L3 = ' ' * 6
L4 = ' ' * 9

ADD = g.OP_ADD
CLR = g.OP_CLR
SET = g.OP_SET


BP = g.BREAK_POINT
NL = g.NEW_LINE
GRID_NAMES_1 = g.GRID_NAMES_1
GRID_NAMES_2 = g.GRID_NAMES_2
GRID_NAMES = g.GRID_NAMES

MAX_GRID_LENGTH = g.NUMBER_OF_GRIDS

BLOCK_PEERS = g.BLOCK_PEERS
RCN_BLOCK_PEERS = g.RCN_BLOCK_PEERS
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

df_case = 0
df_count= [[], []]
df_string = ''

def base_cmd(cb, basic_cmd):
    '''
    The single point of contact for writing a new grid value

    It there is not an exception simply returns

    :param cmd: is basic_cmd  e.g. xXyYOn  O = operation , ADD | CLR | SET
    :return:
    '''
    try:
        cmd = basic_cmd
        c.set(cmd)
        op = c.operation
        sqr = c.square
        val = c.value
        grid_index = c.grid_index
        cell = board.grid_list[grid_index][sqr]

        dual_force_handler(cell=cell, cmd=cmd, op=op, sqr=sqr)

        if cell == '':
            raise Exception(f'cmd = {cmd}, cell = {cell}')

        if val not in cell and not sigs.is_grid:
            raise Exception(f'cmd = {cmd}, '
                            f'val = {val} not in cell = {cell}')

        if op == CLR:
            cell = clr_cmd(cell=cell, cmd=cmd,
                           gridIndex=grid_index, sqr=sqr, val=val)
        elif op == SET:
            cell = set_cmd(cell, val)
        elif op == ADD:
            cell = add_cmd(cell, val)

        if sigs.step != sigs.steps.no_step:
            color_cmd(cb=cb, gridIndex=grid_index,
                      op=op, sqr=sqr, val=val)

        board.cmd(grid_index, sqr, cell)
        dual_force_handler(cell=cell, cmd=cmd, op=op, sqr=sqr)

        s.grid_cmd.index = grid_index
        s.grid_cmd.square = sqr
        s.grid_cmd.cell = cell
        s.gui_cmd_name = s.gui_cmd_type.cmd
        cb()

        if sigs.step == sigs.steps.every_step:
            s.gui_cmd_name = s.gui_cmd_type.wait
            cb()

        return

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def add_cmd(cell, val):
    '''
    Adds multiple digits to a cell iff a grid is being loaded.

    (but loaded one at a time with the ADD operation)
    and ONLY then when more than one digit is being loaded into a cell.
    In case of a single digit the normal SET basic_cmd is used.

    Prior to this method being invoked all the grids are loaded with
    all the DIGITS

     assumes CellCmd.is_grid = True
    :param cell:
    :param val:
    :return:
    '''

    if cell == g.DIGITS:
        cell = val
    else:
        cell += val

    return cell

def clr_cmd(**kwargs):
    try:
        cell = kwargs['cell']
        cmd = kwargs['cmd']
        grid_index = kwargs['gridIndex']
        sqr = kwargs['sqr']
        val = kwargs['val']

        if cell[0] == g.CELL_GIVEN_MARK:
            msg_given = f'cmd = {cmd} can NOT erase cell = ' \
                        f'{cell}. It is a given!'
            raise Exception(msg_given)

        elif cell[0] == g.CELL_SOLVE_MARK:
            msg_solved = f'cmd = {cmd} can NOT erase cell = ' \
                         f'{cell}. It is solved!'
            raise Exception(msg_solved)

        else:
            cell = board.grid_list[grid_index][sqr]
            cell = cell.replace(val, '')

        return cell

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def set_cmd(cell, val):
    if sigs.is_load:
        cell = g.CELL_GIVEN_MARK + val
    else:
        cell = g.CELL_SOLVE_MARK + val

    return cell

def dual_force_handler(**kwargs):
    global df_case
    global df_count
    global df_string

    cell = kwargs['cell']
    cmd = kwargs['cmd']
    op = kwargs['op']
    sqr = kwargs['sqr']

    if sigs.is_DF:
        if op == SET:
            df_string = f'{L2}cmd = {cmd} sqr = {sqr}' \
                             f'  cell = {cell} ->'
        elif op == CLR:
            df_string = f'{L2}cmd = {cmd} sqr = {sqr}' \
                             f'  cell = {cell} ->'
        else:
            df_count[df_case] += 1
            count = df_count[df_case]
            df_string += f'{cell} for case {df_case}, ' \
                              f'count = {count} '

def color_cmd(**kwargs):
    cb = kwargs['cb']
    grid_index = kwargs['gridIndex']
    op = kwargs['op']
    sqr = kwargs['sqr']
    val = kwargs['val']

    s.gui_cmd_name = s.gui_cmd_type.color
    s.color_cmd.index = grid_index

    if op == SET:
        s.color_cmd.color = colors.highlight
        s.color_cmd.tag = f'SS_{sqr}'
        cb()

        s.color_cmd.tag = f'BS_{sqr}'
        cb()

        s.color_cmd.color = colors.assert_small_square
        s.color_cmd.tag = f'SS_{sqr}-{val}'
        cb()

    elif op == CLR:
        s.color_cmd.color = colors.remove_small_square
        s.color_cmd.tag = f'SS_{sqr}-{val}'
        cb()


if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
