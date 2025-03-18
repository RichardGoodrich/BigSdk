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
is_DF_Fail = False
is_display = True
is_grid = False
is_load = False
is_resizeable = True
is_pretty_print = False

is_grid_choose = False
is_string81_choose = False

is_lifted_index = 0

df_case = 0

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




