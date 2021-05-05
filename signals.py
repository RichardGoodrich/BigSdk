'''
2021-04-12-1840 Mon

/home/Big/Dropbox/root/private/computer/software
/PyCharm/Big'sSudoku/play/src/signals.py
'''

from collections import namedtuple
import colors

is_pretty_print = False

is_resizeable = False
screen_width = 0
screen_height = 0
screen_depth = 0

StepMode = namedtuple('StepMode', ['every_step', 'major_step', 'no_step'])
steps = StepMode(every_step="Every Step", major_step="Major Step", no_step="No Step")
step = steps.no_step

GuiCmd = namedtuple('GuiCmd', ['wait', 'color', 'lift', 'grid',
                               'restoreColors',
                               'displayNumbers'
                               ])
gui_cmd = GuiCmd(wait='wait', color='color', lift='lift', grid='grid',
                 restoreColors='restoreColors',
                 displayNumbers='displayNumbers')

big_cmd = ''

class GuiCmd:
    cmd = gui_cmd.wait
    cell = ''
    color = ''
    grid_index = 0
    square = ''
    tag = ''

is_next = False

base_path = '/home/Big/Dropbox/root/private/computer/software/PyCharm/'
sudoku_path = 'Big\'sSudoku/play/'
logs_dir = 'logs/'
exception_file = 'log_exceptions.txt'

except_path = base_path + sudoku_path + logs_dir + exception_file

except_format = '%(asctime)s  :%(levelname)s  :%(funcName)s  :%(lineno)d  :%(message)s'

docs_dir = ''
log_dir = ''
root_dir = ''
src_dir = ''

is_DF = False
is_grid = False
is_load = False
is_solve = False
is_trace = False

def is_grid_set(bool_):
    global is_grid
    global is_load

    if bool_:
        is_load = True
        is_grid = True
        colors.remove_row_col = 'orange'
        colors.remove_block_only = 'red'
        colors.remove_rcn_block = 'cyan'
    else:
        is_grid = False
        is_load = False
        colors.remove_row_col = 'red'
        colors.remove_block_only = 'red'
        colors.remove_rcn_block = 'red'

def is_load_set(bool_):
    global is_grid
    global is_load

    if bool_:
        is_load = True
        is_grid = False
        colors.remove_row_col = 'orange'
        colors.remove_block_only = 'red'
        colors.remove_rcn_block = 'cyan'
    else:
        is_load = False
        is_grid = False
        colors.remove_row_col = 'red'
        colors.remove_block_only = 'red'
        colors.remove_rcn_block = 'red'


# for use by board_to_main()
is_color = False
is_wait = False

# from board.py
board_grid_list = []

fail_msg = ''