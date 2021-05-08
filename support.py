'''
support.py 2021-05-05 - Wed

suggestion import as s
support function are organized alphabetically

'''


# <editor-fold desc="python imports"
from collections import namedtuple
from dataclasses import dataclass
import logging as log
import colors
import os
import signals
import sys
# </editor-fold>

# <editor-fold desc="local imports"
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
# </editor-fold>

# <editor-fold desc="Gui callback cmds"
@dataclass
class GuiCmdType:
    cmd: str = 'cmd'
    entry: str = 'entry'
    color: str = 'color'
    display: str = 'display'
    lift: str = 'lift'
    restore: str = 'restore'
    wait: str = 'wait'


@dataclass
class ColorCmd:
    '''
    Non-valid defaults intentionally!

    No default values causes failure to load!
    Hard discovery that a valid value and cause things to work!  Hopefully the default
    values won't be valid!  If so could intentionally put in-valid values there.
    todo - 2021.05.07 is that this needs tested!
    '''
    name: str = 'color'
    index: int = 9
    color: str = ''
    tsg: str = ''

@dataclass
class EntryCmd:
    '''
    Non-valid defaults intentionally!

    No default values causes failure to load!
    Hard discovery that a valid value and cause things to work!  Hopefully the default
    values won't be valid!  If so could intentionally put in-valid values there.
    todo - 2021.05.07 is that this needs tested!
    '''
    name: str = 'color'
    entry: str = ''

@dataclass
class LiftCmd:
    '''
    Non-valid defaults intentionally!

    No default values causes failure to load!
    Hard discovery that a valid value and cause things to work!  Hopefully the default
    values won't be valid!  If so could intentionally put in-valid values there.
    todo - 2021.05.07 is that this needs tested!
    '''
    name: str = 'lift'
    index: int = 9

@dataclass
class GridCmd:
    '''
    Non-valid defaults intentionally!

    No default values causes failure to load!
    Hard discovery that a valid value and cause things to work!  Hopefully the default
    values won't be valid!  If so could intentionally put in-valid values there.
    todo - 2021.05.07 is that this needs tested!
    '''
    name: str = 'cmd'
    index: int = 9
    square: str = ''
    cell: str = ''

gui_cmd_type = GuiCmdType()
gui_cmd_name = gui_cmd_type.wait

entry_cmd = EntryCmd()
lift_cmd = LiftCmd()
grid_cmd = GridCmd()
color_cmd = ColorCmd()
# </editor-fold>

def convert_bsrc(value):
    try:
        x = int(value[0])
        y = int(value[1])
        a = 1 + (3 * ((x - 1) // 3)) + ((y - 1) // 3)
        b = 1 + (3 * ((x + 2) % 3)) + ((y + 2) % 3)
        return (str(a) + str(b))

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def deconstruct_cmd(cmd):
    G = cmd[0] + cmd[2] + cmd[5]
    X = cmd[1]
    Y = cmd[3]
    O = cmd[4]
    Z = cmd[6]

    cmd_stuff = namedtuple('cmd_stuff', 'grid row, col, op, val')
    return cmd_stuff(grid=G, row=X, col=Y, op=O, val=Z)

def form_cmd(grid, sqr, op, val):
    '''
    Forms basic_cmd string of length=7 with grid, sqr, op, and val

    :param grid:  3-letter grid name
    :param sqr:   square - 2-digit, digits in g.DIGITS
    :param op:    operation = g.SET | g.CLR
    :param val:    1-letter digit or value

    :return:  sudoku command as 7-letter string
    '''
    cmd = grid[0] + sqr[0] + grid[1] + sqr[1] + op + grid[2] + val
    return cmd

def grid_name(cmd):
    return cmd[0] + cmd[2] + cmd[5]

def grid_name_from_cmd(cmd):
    name = cmd[0] + cmd[2] + cmd[5]
    return name

def intersect_to_string(text_list):
    try:
        result = text_list.pop()
        for next in text_list:
            result = set(result).intersection(next)

        result = list(result)
        result.sort()
        result = ''.join(result)
        return result

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def is_grid_set(bool_):
    if bool_:
        signals.is_load = True
        signals.is_grid = True
        colors.remove_row_col = 'orange'
        colors.remove_block_only = 'red'
        colors.remove_rcn_block = 'cyan'
    else:
        signals.is_grid = False
        signals.is_load = False
        colors.remove_row_col = 'red'
        colors.remove_block_only = 'red'
        colors.remove_rcn_block = 'red'

def is_load_set(bool_):
    if bool_:
        signals.is_load = True
        signals.is_grid = False
        colors.remove_row_col = 'orange'
        colors.remove_block_only = 'red'
        colors.remove_rcn_block = 'cyan'
    else:
        signals.is_load = False
        signals.is_grid = False
        colors.remove_row_col = 'red'
        colors.remove_block_only = 'red'
        colors.remove_rcn_block = 'red'

def pause(inp=': '):
    input(inp)
    return inp

def union_to_string(text_list):
    try:
        result = text_list.pop()
        for next in text_list:
            result = set(result).union(next)

        result = list(result)
        result.sort()
        result = ''.join(result)
        return result

    except Exception as e:
        logger_except.exception(e)
        sys.exit()


if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')

else:
    file = __file__
    print(f'importing {file} ')
