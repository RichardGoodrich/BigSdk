'''
cmds.py

2021-05-05 Wed
'''

# <editor-fold desc="python imports"
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import board
import cell_cmd as cc
from cmd_support import CmdS as c
import colors
import settings as g
import signals as sigs
import support as s
# </editor-fold>

# <editor-fold desc="globasl"
BP = g.BREAK_POINT
NL = g.NEW_LINE
ADD = g.OP_ADD
CLR = g.OP_CLR
SET = g.OP_SET

GRID_NAMES = g.GRID_NAMES

BLK_SQR_ROWS = g.BLK_SQR_ROWS
BLK_SQR_COLS = g.BLK_SQR_ROWS

BLK_TO_COLS = g.BLK_TO_COLS
BLK_TO_ROWS= g.BLK_TO_ROWS
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

# <editor-fold desc="big_cmd() and support"
def big_cmd(cb):
    try:
        token_list = sigs.big_cmd.split(' ')
        grid_name = token_list[0]
        type = token_list[1]
        cmd = token_list[3]
        grid_index = g.GRID_NAMES.index(grid_name)

        if grid_index != sigs.is_lifted_index and sigs.step != sigs.steps.no_step:
            s.gui_cmd_name = s.gui_cmd_type.lift
            s.lift_cmd.index = grid_index
            cb()

        if type == 'DF':
            cmd = token_list[3:]
            dual_force(cb, cmd)

        if type == 'NS':
            if not basic_cmd(cb, cmd):
                s.gui_cmd_name = s.gui_cmd_type.restore
                cb()

                s.gui_cmd_name = s.gui_cmd_type.display
                cb()

                print(sigs.fail_msg)
                return

        elif type == 'N2' or type == 'N3' or type == 'N4':
            subset(cb, cmd, grid_index, grid_name)
        elif type == 'Claim':
            claim(cb, cmd, grid_name)
        elif type == 'Point':
            point(cb, cmd, grid_name)

        for removal in sigs.removal_list:
            basic_cmd(cb, removal)

        if sigs.step == sigs.steps.major_step:
            s.entry_cmd.entry = sigs.big_cmd
            s.gui_cmd_name = s.gui_cmd_type.entry
            cb()

            s.gui_cmd_name = s.gui_cmd_type.wait
            cb()

        s.gui_cmd_name = s.gui_cmd_type.restore
        cb()

        s.gui_cmd_name = s.gui_cmd_type.display
        cb()
        BP

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def big_cmd_load(cb, cmd):
    try:
        if sigs.is_grid_choose:
            basic_cmd_grid(cb, cmd)
        else:
            basic_cmd(cb, cmd)

        if sigs.step == sigs.steps.major_step:
            s.gui_cmd_name = s.gui_cmd_type.wait
            cb()

        s.gui_cmd_name = s.gui_cmd_type.restore
        cb()

        s.gui_cmd_name = s.gui_cmd_type.display
        cb()

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def subset(cb, cmd, grid_index, grid_name):
    '''
    N2, N3, N$

    :param cb:
    :param cmd:
    :param grid_index:
    :param grid_name:
    :return:
    '''
    try:
        ltr_list = [val for val in cmd if val.isalpha()]
        part_list = cmd.split('-')

        z_vals = part_list[0][1:]
        if ltr_list[1] == grid_name[0]:
            x_vals = part_list[1][1:]
            y_vals = part_list[2][1:]
        else:
            x_vals = part_list[2][1:]
            y_vals = part_list[1][1:]

        if len(x_vals) == 1:
            squares = [(x_vals + y) for y in y_vals]
        elif len(y_vals == 1):
            squares = [(x + y_vals) for x in x_vals]

        tags_BS = [f'BS_{sqr}' for sqr in squares]
        tags_SS = [f'SS_{sqr}' for sqr in squares]
        tags_SV = [f'SS_{sqr}-{val}' for sqr in squares for val in z_vals]
        tags = tags_BS + tags_SS

        s.gui_cmd_name = s.gui_cmd_type.color
        s.color_cmd.index = grid_index
        s.color_cmd.color = colors.highlight

        for tag in tags:
            s.color_cmd.tag = tag
            cb()

        s.color_cmd.color = colors.assert_small_square
        for tag in tags_SV:
            s.color_cmd.tag = tag
            cb()
        BP

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def claim(cb, cmd, grid_name):
    try:
        grid_index = GRID_NAMES.index(grid_name)
        ltr_list = [val for val in cmd if val.isalpha()]
        num_list = [num for num in cmd if num.isdigit()]
        val_num = num_list[0]
        blk_num = num_list[1]
        if ltr_list[2] == 'c':
            # Claim = num-block-col  e.g. n4b5c4
            col_num = num_list[2]
            rows = g.BLK_TO_ROWS[col_num]
            squares = [(row + col_num)  for row in rows if val_num in board.rcn[row + col_num]]
        else:
            # Claim = num-block-row  e.g. n4b5r6
            row = num_list[2]
            cols = g.BLK_TO_COLS[blk_num]
            squares = [(row + col)  for col in cols if val_num in board.rcn[row + col]]

        tags_BS = [f'BS_{sqr}' for sqr in squares]
        tags_SS = [f'SS_{sqr}' for sqr in squares]
        tags_SV = [f'SS_{sqr}-{val_num}' for sqr in squares]
        tags_HI = tags_BS + tags_SS

        s.gui_cmd_name = s.gui_cmd_type.color
        s.color_cmd.index = grid_index
        s.color_cmd.color = colors.highlight

        for tag in tags_HI:
            s.color_cmd.tag = tag
            cb()

        s.color_cmd.color = colors.assert_small_square
        for tag in tags_SV:
            s.color_cmd.tag = tag
            cb()

        BP

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def point(cb, cmd, grid_name):
    '''
    Color point.

    :param cb:
    :param cmd: e.g. 'n9b5r6'
    :param grid_name: 'rcn'
    :return:
    '''
    try:
        ltr_list = [val for val in cmd if val.isalpha()]
        num_list = [num for num in cmd if num.isdigit()]
        house_letter = ltr_list[2]
        num_digit = num_list[0]
        blk_digit = num_list[1]

        if house_letter == 'r':
            row_digit = num_list[2]
            cols = BLK_TO_COLS[blk_digit]
            square_list = [(row_digit + col) for col in cols
                           if num_digit in board.rcn[row_digit + col]]

        elif house_letter == 'c':
            col_digit = num_list[2]
            rows = BLK_TO_ROWS[blk_digit]
            square_list = [(row + num_digit) for row in rows
                           if num_digit in board.rcn[row + num_digit]]

        size = len(square_list)
        color_BS = [colors.highlight] * size
        color_SS = [colors.highlight] * size
        color_SD = [colors.assert_small_square] * size
        color_list = color_BS + color_SS + color_SD

        s.gui_cmd_name = s.gui_cmd_type.color
        s.color_cmd.index = 0

        tags_BS = [f'BS_{sqr}' for sqr in square_list]
        tags_SS = [f'SS_{sqr}' for sqr in square_list]
        tags_SD = [f'SS_{sqr}-{num_digit}' for sqr in square_list]
        tags = tags_BS + tags_SS + tags_SD

        for color, tag  in zip(color_list, tags):
            s.color_cmd.color = color
            s.color_cmd.tag = tag
            cb()

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def dual_force(cb, cmd_list):
    try:
        long_cmd = sigs.big_cmd
        short_cmd = ''.join(cmd_list)
        token_list = short_cmd.split('-')
        cmd = token_list[-2] + token_list[-1]
        if not basic_cmd(cb, cmd):
            print('todo DF FAIl!')
        BP


    except Exception as e:
        logger_except.exception(e)
        sys.exit()
# </editor-fold>

# <editor-fold desc="basic_cmd() and support"
def basic_cmd(cb, from_cmd):
    '''
    Basic Cmd.

    todo-2021-04.30-0723 - removal to be verified.
    of bramch to basc_cmd_grid()

    if sigs.is_grid == True self.is_Load  is also True
    main.gui needs to insure if self.is_grid == True
      that the basic_cmd_grid(from_cmd) is called directly

    '''
    try:
        c.set(from_cmd)
        operation = c.operation
        c.do_lists()
        cmd_list = c.cmds_list

        for cmd in cmd_list:
            retVal = can_do_cmd(cb, cmd)
            '''
            retVal can be True | False | None.

            retVal can only be None for operation == g.CLR (removal)
            if retVal is False for operation = g.SET
               it can't assert the value in all grids
            elif retVal is False for operation = g.CLR
                 means trying to remove last value in a cell   
            '''
            if retVal is False:
                sigs.fail_msg = f'basic_cmd = {cmd} failed'
                return False   # -------------------------------> early fail!
            sigs.fail_msg = ''

        for cmd in cmd_list:
            retVal = can_do_cmd(cb, cmd)
            '''
            retVal can be True | False | None.

            retVal is True for operation == g.SET
            retVal is conditionally True for operation = g.CLR (removal(
            '''
            if retVal is True:
                cc.base_cmd(cb, cmd)

        if operation == SET:
            if not basic_cmd_removals(cb, cmd_list):
                return False # --------------------------------> early fail!


        return True

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def basic_cmd_grid(cb, from_cmd):
    try:
        # todo - Add Traces.py hooks
        if sigs.is_grid:  # Only True if "self.is_Load_"  is also True
            if c.multiple_cmds_from_last_digits(from_cmd):
                multiple_cmd_list = c.multiple_cmds_list
                for rcn_cmd in multiple_cmd_list:
                    rcn_cmd = rcn_cmd.replace(SET, ADD)
                    c.set(rcn_cmd)
                    c.do_lists()
                    add_list = c.cmds_list
                    for cmd in add_list:
                        cc.base_cmd(cb, cmd)
            else:
                c.set(from_cmd)
                c.do_lists()
                set_list = c.cmds_list
                for cmd in set_list:
                    cc.base_cmd(cb, cmd)
            return

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def basic_cmd_removals(cb, cmd_list):
    try:
        colors.remove_small_square = colors.remove_row_col

        for cmd in cmd_list:
            c.set(cmd)
            c.do_peers()
            peer_list = c.peer_subs

            if not cmd_expansion(cb, peer_list):
                return False # ------------------------------> Fail!

        if not block_only_removals(cb):
            return False     # ------------------------------> Fail!

        return True

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def cmd_expansion(cb, peer_removals):
    try:
        if len(peer_removals) == 4:
            row_block_peers = peer_removals[0:2]
            col_block_peers = peer_removals[2:]
            if not rcn_row_expansion(cb, row_block_peers):
                return False   # -------------------------------------> Fail!
            if not rcn_col_expansion(cb, col_block_peers):
                return False   # -------------------------------------> Fail!
        else:
            for peer_sub in peer_removals:
                colors.remove_small_square = colors.remove_row_col

                digits = g.DIGITS
                i = peer_sub.index('!') + 1
                digits = digits.replace(peer_sub[i], '')
                peers = []
                for digit in digits:
                    peer = peer_sub.replace(peer_sub[i-1: i+1], digit)
                    peers.append(peer)
                for cmd in peers:
                    c.set(cmd)
                    cmdx = c.cmd_main
                    retVal = can_do_cmd(cb, cmdx)
                    if retVal is False:
                        sigs.fail_msg = cmdx
                        return False # ------------------------------> Fail!
                    elif retVal is True:
                        cc.base_cmd(cb, cmdx)

        return True

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def rcn_row_expansion(cb, row_block):
    row_peer = row_block[0]
    blk_peer = row_block[1]
    blk_nums = blk_peer[1:3]

    digits = g.DIGITS
    i = row_peer.index('!') + 1
    digits = digits.replace(row_peer[i], '')
    row_peers = [row_peer.replace(row_peer[i - 1: i + 1], digit) for digit in digits]

    total_peers = []
    for row_peer in row_peers:
        c.set(row_peer)
        block_cmd = c.block_cmd
        total_peers.append(row_peer)
        if block_cmd[1] in blk_nums:
            total_peers.append(block_cmd)

    for removal in total_peers:
        c.set(removal)
        cmdx = c.cmd_main

        if cmdx[0] == 'b':
            colors.remove_small_square = colors.remove_rcn_block
        else:
            colors.remove_small_square = colors.remove_row_col

        retVal = can_do_cmd(cb, cmdx)
        if retVal is False:
            return False          # -------------------------> Fail!
        elif retVal is True:
            cc.base_cmd(cb, cmdx)
    return True

def rcn_col_expansion(cb, col_block):
    col_peer = col_block[0]
    blk_peer = col_block[1]
    blk_nums = blk_peer[1:3]

    digits = g.DIGITS
    i = col_peer.index('!') + 1
    digits = digits.replace(col_peer[i], '')
    col_peers = [col_peer.replace(col_peer[i - 1: i + 1], digit) for digit in digits]

    total_peers = []
    for col_peer in col_peers:
        c.set(col_peer)
        block_cmd = c.block_cmd
        total_peers.append(col_peer)
        if block_cmd[1] in blk_nums:
            total_peers.append(block_cmd)

    for removal in total_peers:
        c.set(removal)
        cmdx = c.cmd_main

        if cmdx[0] == 'b':
            colors.remove_small_square = colors.remove_rcn_block
        else:
            colors.remove_small_square = colors.remove_row_col

        retVal = can_do_cmd(cb, cmdx)
        if retVal is False:
            sigs.fail_msg = cmdx
            return False  # -------------------------> Fail!
        elif retVal is True:
            cc.base_cmd(cb, cmdx)
    return True

def block_only_removals(cb):
    '''
    Block only peer removals in rcn-grid generate removals in rnc & ncr grids.

    subs: set-up in c.block_subs      e.g.  'b2n6-s4578'
    B = base of block removals           e.g   'b2n6-s'
    blk_subs:                            e.g.  ['b2n6-s4', 'b2n6-s5', 'b2n6-s7', 'b2n6-s8']

    in this example
    for b2n6-s4:       sub_list = ['r2c4-n6', 'r2n6-c4', 'n6c4-r2', 'b2n6-s4']
    will pop off last entry to:   ['r2c4-n6', 'r2n6-c4', 'n6c4-r2']
    will iterate through this list of length three doing removals if able

    :param x:  Call back to GUI in main.py
    :return:  True/False   False:  could not remove last digit in cell: Fail!
    '''
    try:
        subs = c.block_subs
        B = subs[:-4]
        blk_subs = [B + subs[-4], B + subs[-3], B + subs[-2], B + subs[-1]]
        colors.remove_small_square = colors.remove_block_only

        for blk_sub in blk_subs:
            c.set(blk_sub)
            c.do_lists()
            sub_list = c.cmds_list
            sub_list.pop()

            for sub in sub_list:
                retVal = can_do_cmd(cb, sub)
                if retVal is False:
                    return False  # --------------------------->  Fail!
                if retVal is True:
                    cc.base_cmd(cb, sub)

        return True

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def can_do_cmd(cb, basic_cmd):
    '''
    Checks legality of command.

    :param basic_cmd = srring of length = 7
    :return: True | False | None
    '''
    try:
        c.set(basic_cmd)
        grid_index = c.grid_index
        square = c.square
        operation = c.operation
        value = c.value
        grid = board.board_list[grid_index]
        cell = grid[square]

        if operation == SET:
            if cell[0] in g.DIGITS and value in cell:
                return True
            else:
                raise Exception(f'cmds.can_do_cmd(), cant set all grids')  # -----> Fail!

        elif operation == CLR:
            if cell[0] in g.DIGITS and value in cell:
                if len(cell) > 1:
                    return True
                else:
                    if sigs.is_DF:
                        cc.base_cmd(cb, basic_cmd)
                        sigs.fail_msg = "can't delete last digit in cell"
                        sigs.is_DF_Fail = True
                    return False
            else:
                return None

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
