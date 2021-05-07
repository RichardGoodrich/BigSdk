'''
settings.py  2021-05-05 Wed  Refactored

see alphabetical listing in block comments at end
'''

# <editor-fold desc="python imports"
import os
from collections import namedtuple
# </editor-fold>

big_cmd = ''
fail_msg = ''
removal_list = []

# <editor-fold desc="paths"
root_path = os.getcwd()
docs_dir = os.path.join(root_path, 'docs/')
logs_dir = os.path.join(root_path, 'logs/')
notes_dir = os.path.join(root_path, 'notes/')
src_dir = os.path.join(root_path, 'src/')
except_path = os.path.join(logs_dir, 'log_exceptions.txt')

except_format = '%(asctime)s  :%(levelname)s  :%(funcName)s  :%(lineno)d  :%(message)s'
# </editor-fold>

# <editor-fold desc="boolean signals (is_)"
is_DF = False
is_grid = False
is_load = False
is_resizeable = False
is_pretty_print = False
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


