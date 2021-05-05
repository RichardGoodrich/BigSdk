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

class CellCmd:
    cell = ''
    cmd = ''
    df_case = 0
    df_string = ''
    df_count = [[], []]
    grid_index = 0
    op = ''
    sqr = ''
    val = ''

    @classmethod
    def base_cmd(cls, cb, basic_cmd):
        '''
        The single point of contact for writing a new grid value

        It there is not an exception simply returns

        :param cmd: is basic_cmd  e.g. xXyYOn  O = operation , ADD | CLR | SET
        :return:
        '''
        try:
            cls.cmd = basic_cmd
            c.set(cls.cmd)
            cls.op = c.operation
            cls.sqr = c.square
            cls.val = c.value
            cls.grid_index = c.grid_index
            cls.cell = board.grid_list[cls.grid_index][cls.sqr]

            cls.dual_force_handler()

            if cls.cell == '':
                raise Exception(f'cmd = {cls.cmd}, cell = {cls.cell}')

            if cls.val not in cls.cell and not sigs.is_grid:
                raise Exception(f'cmd = {cls.cmd}, '
                                f'val = {cls.val} not in cell = {cls.cell}')

            if cls.op == CLR:
                cls.clr_cmd()
            elif cls.op == SET:
                cls.set_cmd()
            elif cls.op == ADD:
                cls.add_cmd()

            if sigs.step != sigs.steps.no_step:
                cls.color_cmd(cb)

            board.cmd(cls.grid_index, cls.sqr, cls.cell)
            cls.dual_force_handler()

            sigs.GuiCmd.cmd = sigs.gui_cmd.grid
            sigs.GuiCmd.grid_index = cls.grid_index
            sigs.GuiCmd.square = cls.sqr
            sigs.GuiCmd.cell = cls.cell
            cb()

            if sigs.step == sigs.steps.every_step:
                sigs.GuiCmd.cmd = sigs.gui_cmd.wait
                cb()

            return

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def add_cmd():
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
        try:
            if CellCmd.cell == g.DIGITS:
                CellCmd.cell = CellCmd.val
            else:
                CellCmd.cell += CellCmd.val

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def clr_cmd():
        try:
            if CellCmd.cell[0] == g.CELL_GIVEN_MARK:
                msg_given = f'cmd = {CellCmd.cmd} can NOT erase cell = ' \
                            f'{CellCmd.cell}. It is a given!'
                raise Exception(msg_given)

            elif CellCmd.cell[0] == g.CELL_SOLVE_MARK:
                msg_solved = f'cmd = {CellCmd.cmd} can NOT erase cell = ' \
                             f'{CellCmd.cell}. It is solved!'
                raise Exception(msg_solved)

            else:
                CellCmd.cell = board.grid_list[CellCmd.grid_index][CellCmd.sqr]
                CellCmd.cell = CellCmd.cell.replace(CellCmd.val, '')

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def set_cmd():
        try:
            if sigs.is_load:
                CellCmd.cell = g.CELL_GIVEN_MARK + CellCmd.val
            else:
                CellCmd.cell = g.CELL_SOLVE_MARK + CellCmd.val

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def dual_force_handler():
        if sigs.is_DF:
            if CellCmd.op == SET:
                CellCmd.df_string = f'{L2}cmd = {CellCmd.cmd} sqr = {CellCmd.sqr}' \
                                 f'  cell = {CellCmd.cell} ->'
            elif CellCmd.op == CLR:
                CellCmd.df_string = f'{L2}cmd = {CellCmd.cmd} sqr = {CellCmd.sqr}' \
                                 f'  cell = {CellCmd.cell} ->'
            else:
                CellCmd.df_count[CellCmd.df_case] += 1
                count = CellCmd.df_count[CellCmd.df_case]
                CellCmd.df_string += f'{CellCmd.cell} for case {CellCmd.df_case}, ' \
                                  f'count = {count} '

    def color_cmd(cb):
        sigs.GuiCmd.cmd = sigs.gui_cmd.color
        sigs.GuiCmd.grid_index = CellCmd.grid_index
        if CellCmd.op == SET:
            sigs.GuiCmd.tag = f'SS_{CellCmd.sqr}'
            sigs.GuiCmd.color = colors.highlight
            cb()

            sigs.GuiCmd.tag = f'BS_{CellCmd.sqr}'
            sigs.GuiCmd.color = colors.highlight
            cb()

            sigs.GuiCmd.tag = f'SS_{CellCmd.sqr}-{CellCmd.val}'
            sigs.GuiCmd.color = colors.assert_small_square
            cb()
        elif CellCmd.op == CLR:
            sigs.GuiCmd.tag = f'SS_{CellCmd.sqr}-{CellCmd.val}'
            sigs.GuiCmd.color = colors.remove_small_square
            cb()


if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
