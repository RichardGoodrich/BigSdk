'''
puzzle_load.py

2021.04.17 Sat
'''

# <editor-fold desc="python imports"
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import cmds
from codec import Codec
import dancing_links
import puzzles
import settings as g
import signals as sigs
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
NL = g.NEW_LINE
SET = g.OP_SET

PUZZLE_DEFAULT =\
'.....627........5....54..311.....5..97.8.2.64..6.....764..29....8........526.....'
# </editor-fold>

codec = Codec()
encoded_puzzle = ''
solved_puzzle = ''

grid_choice = []
grid_choice_dict = {}
grid_choice_msg = []

string81_choice = []
string81_choice_dict = {}
string81_choice_msg = []


# <editor-fold desc="puzzle entry load"
def load(cb, puz=PUZZLE_DEFAULT):
    try:
        global codec
        global encoded_puzzle
        global solved_puzzle

        if sigs.is_grid:
            puzzle_list = puz
            num_list = [item if len(item) == 1 else '.' for item in puzzle_list]
            puzzle_81 = ''.join(num_list)
        else:
            puzzle_81 = puz
            puzzle_list = list(puzzle_81)

        puzzle_81 = puzzle_81.replace('0', '.')

        if filter_puzzle(puzzle_list):
            return False

        solved_puzzle = dancing_links.filter(20, puzzle_81)
        encoded_puzzle = codec.encode(puzzle_81, solved_puzzle)

        if '.' in solved_puzzle:
            return False

        do_puzzle(cb, puzzle_list)

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_puzzle(cb, puz_list):
    try:
        puzValue = get_puz_value(puz_list)
        while True:
            try:
                step = sigs.step

                cmd = next(puzValue)
                cmds.big_cmd_load(cb, cmd)

                if sigs.step != sigs.steps.no_step:
                    s.gui_cmd_name = s.gui_cmd_type.wait
                    cb()

            except Exception as e:
                s.gui_cmd_name = s.gui_cmd_type.display
                cb()

                # sigs.is_load(False)
                return

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def get_puz_value(puz_list):
    try:
        for i, value in enumerate(puz_list):
            square = g.SQUARES[i]
            if value != '.':
                cmd = 'r' + square[0] + 'c' + square[1] + SET + 'n' + value
                yield cmd
    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def filter_puzzle(puz_list):
    '''

    :param puz_list:
    :return: False if passes filter
    '''
    try:
        if len(puz_list) != g.MAX_CELLS:
            return True

        digits = g.DIGITS
        count = 0
        for value in puz_list:
            if len(value) > 1:
                for item in value:
                    if item not in g.DIGITS:
                        return True
            else:
                if value not in g.DIGITS and value != '.':
                    return True
                if value in digits:
                    digits = digits.replace(value, '')
                count += 1

        if count < 17:
            return True

        if len(digits) > 1:
            '''
            There must be at least 8 sudoku digits present
            Refer to Olivier Grégoire\'s suggestion about checking for 8 digits
               http://norvig.com/sudoku.html by Peter Norvig
            '''
            return True

        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()
# </editor-fold>

# <editor-fold desc="puzzle menu loads"
def get_puzzle_grid():
    try:
        global grid_choice
        global grid_choice_dict
        global grid_choice_msg

        msg = puzzles.GRID_CHOICES
        msg_list = msg.split(NL)
        # remove double quotes from each end of list
        msg_list.pop(0)
        msg_list.pop()

        grid_choice = [val for val in msg_list if "GRID" in val]
        grid_choice.append('EXIT')

        value = ''
        message_list  = []
        for item in msg_list:
            if 'GRID' in item:
                if value == '':
                    value = item + NL
                else:
                    message_list.append(value)
                    value = item + NL
            else:
                value += item + NL

        message_list.append(value)

        for i, choice in enumerate(grid_choice):
            if choice == 'GRID_Claim_B5':
                value = puzzles.GRID_Claim_B5
                grid_choice_dict[choice] = value
                message_list[i] = message_list[i] + value
            elif choice == 'GRID_JellyFish':
                value = puzzles.GRID_JellyFish
                grid_choice_dict[choice] = value
                message_list[i] = message_list[i] + value
            elif choice == 'GRID_Point_in_Col':
                value = puzzles.GRID_Point_in_Col
                grid_choice_dict[choice] = value
                message_list[i] = message_list[i] + value
            elif choice == 'GRID_X_Wing_in_Row':
                value = puzzles.GRID_X_Wing_in_Row
                grid_choice_dict[choice] = value
                message_list[i] = message_list[i] + value

        grid_choice_msg = message_list
        BP

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def get_puzzle_string():
    try:
        global string81_choice
        global string81_choice_dict
        global string81_choice_msg

        msg = puzzles.PUZZLE_CHOICES
        msg_list = msg.split(NL)
        msg_list.pop(0)
        msg_list.pop()

        string81_choice = [val for val in msg_list if val[0] != ' ']
        string81_choice.append('EXIT')

        value = ''
        message_list  = []
        for item in msg_list:
            if item[0] != ' ':
                if value == '':
                    value = item + NL
                else:
                    message_list.append(value)
                    value = item + NL
            else:
                value += item + NL

        message_list.append(value)

        for i, choice in enumerate(string81_choice):
            if choice == 'ARTO_INKALA':
                value = puzzles.ARTO_INKALA
                string81_choice_dict[choice] = value
                message_list[i] = message_list[i] + value + NL
            elif choice == 'HIDDEN_TRIPLE':
                value = puzzles.HIDDEN_TRIPLE
                string81_choice_dict[choice] = value
                message_list[i] = message_list[i] + value + NL
            elif choice == 'QUADS':
                value = puzzles.QUADS
                string81_choice_dict[choice] = value
                message_list[i] = message_list[i] + value + NL
            elif choice == 'PAIRS':
                value = puzzles.PAIRS
                string81_choice_dict[choice] = value
                message_list[i] = message_list[i] + value + NL
            elif choice == 'SOMETHING':
                value = puzzles.SOMETHING
                string81_choice_dict[choice] = value
                message_list[i] = message_list[i] + value + NL
            elif choice == 'SINGLES':
                value = puzzles.SINGLES
                string81_choice_dict[choice] = value
                message_list[i] = message_list[i] + value + NL
            elif choice == 'SOLUTIONS_8':
                value = puzzles.SOLUTIONS_8
                string81_choice_dict[choice] = value
                message_list[i] = message_list[i] + value + NL

        string81_choice_msg = message_list
        BP

    except Exception as e:
        logger_except.exception(e)
        sys.exit()
# </editor-fold>

get_puzzle_grid()
get_puzzle_string()


if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
