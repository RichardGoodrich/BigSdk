

# <editor-fold desc="python imports"
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import board
from cmd_stuff import CmdS
import colors
import settings as g
import signals as sigs
# </editor-fold>

# <editor-fold desc="globasl"
L2 = g.SP * 3
L3 = g.SP * 6
L4 = g.SP * 9

BP = 0
NL = '\n'
GRID_NAMES_1 = ['rcn', 'rnc', 'ncr', 'bns']
GRID_NAMES_2 = ['crn', 'nrc', 'cnr', 'nbs']
GRID_NAMES = GRID_NAMES_1 + GRID_NAMES_2
MAX_GRID_LENGTH = len(GRID_NAMES_1)

BLOCK_PEERS = {
    '1': '5689',
    '2': '4679',
    '3': '4578',
    '4': '2389',
    '5': '1379',
    '6': '1278',
    '7': '2356',
    '8': '1346',
    '9': '1245',
}

RCN_BLOCK_PEERS = {
    '11': ['b23n.-s123', 'b47n.-s147'],
    '12': ['b23n.-s123', 'b47n.-s258'],
    '13': ['b23n.-s123', 'b47n.-s369'],
    '14': ['b13n.-s123', 'b58n.-s147'],
    '15': ['b13n.-s123', 'b58n.-s258'],
    '16': ['b13n.-s123', 'b58n.-s369'],
    '17': ['b12n.-s123', 'b69n.-s147'],
    '18': ['b12n.-s123', 'b69n.-s258'],
    '19': ['b12n.-s123', 'b69n.-s369'],
    '21': ['b23n.-s456', 'b47n.-s147'],
    '22': ['b23n.-s456', 'b47n.-s258'],
    '23': ['b23n.-s456', 'b47n.-s369'],
    '24': ['b13n.-s456', 'b58n.-s147'],
    '25': ['b13n.-s456', 'b58n.-s258'],
    '26': ['b13n.-s456', 'b58n.-s369'],
    '27': ['b12n.-s456', 'b69n.-s147'],
    '28': ['b12n.-s456', 'b69n.-s258'],
    '29': ['b12n.-s456', 'b69n.-s369'],
    '31': ['b23n.-s789', 'b47n.-s147'],
    '32': ['b23n.-s789', 'b47n.-s258'],
    '33': ['b23n.-s789', 'b47n.-s369'],
    '34': ['b13n.-s789', 'b58n.-s147'],
    '35': ['b13n.-s789', 'b58n.-s258'],
    '36': ['b13n.-s789', 'b58n.-s369'],
    '37': ['b12n.-s789', 'b69n.-s147'],
    '38': ['b12n.-s789', 'b69n.-s258'],
    '39': ['b12n.-s789', 'b69n.-s369'],
    '41': ['b56n.-s123', 'b17n.-s147'],
    '42': ['b56n.-s123', 'b17n.-s258'],
    '43': ['b56n.-s123', 'b17n.-s369'],
    '44': ['b46n.-s123', 'b28n.-s147'],
    '45': ['b46n.-s123', 'b28n.-s258'],
    '46': ['b46n.-s123', 'b28n.-s369'],
    '47': ['b45n.-s123', 'b39n.-s147'],
    '48': ['b45n.-s123', 'b39n.-s258'],
    '49': ['b45n.-s123', 'b39n.-s369'],
    '51': ['b56n.-s456', 'b17n.-s147'],
    '52': ['b56n.-s456', 'b17n.-s258'],
    '53': ['b56n.-s456', 'b17n.-s369'],
    '54': ['b46n.-s456', 'b28n.-s147'],
    '55': ['b46n.-s456', 'b28n.-s258'],
    '56': ['b46n.-s456', 'b28n.-s369'],
    '57': ['b45n.-s456', 'b39n.-s147'],
    '58': ['b45n.-s456', 'b39n.-s258'],
    '59': ['b45n.-s456', 'b39n.-s369'],
    '61': ['b56n.-s789', 'b17n.-s147'],
    '62': ['b56n.-s789', 'b17n.-s258'],
    '63': ['b56n.-s789', 'b17n.-s369'],
    '64': ['b46n.-s789', 'b28n.-s147'],
    '65': ['b46n.-s789', 'b28n.-s258'],
    '66': ['b46n.-s789', 'b28n.-s369'],
    '67': ['b45n.-s789', 'b39n.-s147'],
    '68': ['b45n.-s789', 'b39n.-s258'],
    '69': ['b45n.-s789', 'b39n.-s369'],
    '71': ['b89n.-s123', 'b14n.-s147'],
    '72': ['b89n.-s123', 'b14n.-s258'],
    '73': ['b89n.-s123', 'b14n.-s369'],
    '74': ['b79n.-s123', 'b25n.-s147'],
    '75': ['b79n.-s123', 'b25n.-s258'],
    '76': ['b79n.-s123', 'b58n.-s369'],
    '77': ['b78n.-s123', 'b36n.-s147'],
    '78': ['b78n.-s123', 'b36n.-s258'],
    '79': ['b78n.-s123', 'b36n.-s369'],
    '81': ['b89n.-s456', 'b14n.-s147'],
    '82': ['b89n.-s456', 'b14n.-s258'],
    '83': ['b89n.-s456', 'b14n.-s369'],
    '84': ['b79n.-s456', 'b25n.-s147'],
    '85': ['b79n.-s456', 'b25n.-s258'],
    '86': ['b79n.-s456', 'b25n.-s369'],
    '87': ['b78n.-s456', 'b36n.-s147'],
    '88': ['b78n.-s456', 'b36n.-s258'],
    '89': ['b78n.-s456', 'b36n.-s369'],
    '91': ['b89n.-s789', 'b14n.-s147'],
    '92': ['b89n.-s789', 'b14n.-s258'],
    '93': ['b89n.-s789', 'b14n.-s369'],
    '94': ['b79n.-s789', 'b25n.-s147'],
    '95': ['b79n.-s789', 'b25n.-s258'],
    '96': ['b79n.-s789', 'b25n.-s369'],
    '97': ['b78n.-s789', 'b36n.-s147'],
    '98': ['b78n.-s789', 'b36n.-s258'],
    '99': ['b78n.-s789', 'b36n.-s369'],
}
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
    def base_cmd(cls, x, basic_cmd):
        '''
        The single point of contact for writing a new grid value

        It there is not an exception simply returns

        :param cmd: is basic_cmd  e.g. xXyYOn  O = operation , ADD | CLR | SET
        :return:
        '''
        try:
            cls.cmd = basic_cmd
            CmdS.set(cls.cmd)
            cls.op = CmdS.operation
            cls.sqr = CmdS.square
            cls.val = CmdS.value
            cls.grid_index = CmdS.grid_index
            cls.cell = board.grid_list[cls.grid_index][cls.sqr]

            cls.dual_force_handler()

            if cls.cell == '':
                raise Exception(f'cmd = {cls.cmd}, cell = {cls.cell}')

            if cls.val not in cls.cell and not sigs.is_grid:
                raise Exception(f'cmd = {cls.cmd}, '
                                f'val = {cls.val} not in cell = {cls.cell}')

            if cls.op == g.CLR:
                cls.clr_cmd()
            elif cls.op == g.SET:
                cls.set_cmd()
            elif cls.op == g.ADD:
                cls.add_cmd()

            if sigs.step != sigs.steps.no_step:
                cls.color_cmd(x)

            board.cmd(cls.grid_index, cls.sqr, cls.cell)
            cls.dual_force_handler()

            sigs.GuiCmd.cmd = sigs.gui_cmd.grid
            sigs.GuiCmd.grid_index = cls.grid_index
            sigs.GuiCmd.square = cls.sqr
            sigs.GuiCmd.cell = cls.cell
            x()

            if sigs.step == sigs.steps.every_step:
                sigs.GuiCmd.cmd = sigs.gui_cmd.wait
                x()

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
            if CellCmd.op == g.SET:
                CellCmd.df_string = f'{L2}cmd = {CellCmd.cmd} sqr = {CellCmd.sqr}' \
                                 f'  cell = {CellCmd.cell} ->'
            elif CellCmd.op == g.CLR:
                CellCmd.df_string = f'{L2}cmd = {CellCmd.cmd} sqr = {CellCmd.sqr}' \
                                 f'  cell = {CellCmd.cell} ->'
            else:
                CellCmd.df_count[CellCmd.df_case] += 1
                count = CellCmd.df_count[CellCmd.df_case]
                CellCmd.df_string += f'{CellCmd.cell} for case {CellCmd.df_case}, ' \
                                  f'count = {count} '

    def color_cmd(x):
        sigs.GuiCmd.cmd = sigs.gui_cmd.color
        sigs.GuiCmd.grid_index = CellCmd.grid_index
        if CellCmd.op == g.SET:
            sigs.GuiCmd.tag = f'SS_{CellCmd.sqr}'
            sigs.GuiCmd.color = colors.highlight
            x()

            sigs.GuiCmd.tag = f'BS_{CellCmd.sqr}'
            sigs.GuiCmd.color = colors.highlight
            x()

            sigs.GuiCmd.tag = f'SS_{CellCmd.sqr}-{CellCmd.val}'
            sigs.GuiCmd.color = colors.assert_small_square
            x()
        elif CellCmd.op == g.CLR:
            sigs.GuiCmd.tag = f'SS_{CellCmd.sqr}-{CellCmd.val}'
            sigs.GuiCmd.color = colors.remove_small_square
            x()

if __name__ == '__main__':
    pass
else:
    print('cell_cmd.py is being imported')
