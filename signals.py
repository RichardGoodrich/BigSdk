'''
settings.py  2021-05-05 Wed  Refactored

see alphabetical listing in block comments at end
'''

from collections import namedtuple
import colors

big_cmd = ''
fail_msg = ''

# <editor-fold desc="boolean signals (is_)"
is_DF = False
is_grid = False
is_load = False
is_resizeable = False
is_pretty_print = False
# </editor-fold>

# <editor-fold desc="paths"
base_path = '/home/Big/Dropbox/root/private/computer/software/PyCharm/'
sudoku_path = 'BigSdk/'
logs_dir = 'logs/'
exception_file = 'log_exceptions.txt'
except_path = base_path + sudoku_path + logs_dir + exception_file
except_format = '%(asctime)s  :%(levelname)s  :%(funcName)s  :%(lineno)d  :%(message)s'

docs_dir = ''
log_dir = ''
root_dir = ''
src_dir = ''
# </editor-fold>

# <editor-fold desc="screen config"
screen_width = 0
screen_height = 0
screen_depth = 0
# </editor-fold>

# <editor-fold desc="StepMode signals"
StepMode = namedtuple('StepMode', ['every_step', 'major_step', 'no_step'])
steps = StepMode(every_step="Every Step", major_step="Major Step", no_step="No Step")
step = steps.no_step
# </editor-fold>

# <editor-fold desc="Call Back signaling to GUI (passing cb)"
GuiCmd = namedtuple('GuiCmd', ['wait', 'color', 'lift', 'grid',
                               'restoreColors',
                               'displayNumbers'
                               ])
gui_cmd = GuiCmd(wait='wait', color='color', lift='lift', grid='grid',
                 restoreColors='restoreColors',
                 displayNumbers='displayNumbers')

class GuiCmd:
    cmd = gui_cmd.wait
    cell = ''
    color = ''
    grid_index = 0
    square = ''
    tag = ''
# </editor-fold>


# <editor-fold desc="Alphabetical Listing"
'''
aphabetical listing

base_path 
big_cmd 
class GuiCmd:
docs_dir 

except_format 
except_path 
exception_file

fail_msg

gui_cmd = GuiCmd(...)
GuiCmd = namedtuple ...

is_DF = False
is_grid = False
is_load = False
is_next = False
is_resizeable = False
is_pretty_print = False
is_solve = False
is_trace = False

log_dir 
logs_dir 

root_dir

screen_width = 0
screen_height = 0
screen_depth = 0

src_dir 

step = steps.no_step
steps = StepMode(...}
StepMode = namedtuple ...

sudoku_path
'''
# </editor-fold>


