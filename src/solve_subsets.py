'''
solve_subsets.py  2021-05-04 Tue

'''

# <editor-fold desc="python imports"
from itertools import combinations
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import cmds
import board
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
CLR = g.OP_CLR
LIMITS = {2: 3, 3: 4, 4: 5}
# </editor-fold>

# <editor-fold desc="global variables"
'''
grid_name     set by:  do_n*()             used by:  can_do_set()
house         set by:  *_pencil_marks,     used by:  can_do_set()
pencil_marks  set by:  *_pencil_marks      used by:  can_do_set(),  do_subsets()
size          set by:  do_n*()             used by:  can_do_set(),  do_subsets()
'''
grid_name = ''
house = ''
pencil_marks = []
size = 2
# </editor-fold>

def do(cb):
    '''
    Finds Sudoku N2, N3, N4.

    :return:  True | False   sigs.big_cmd
    '''
    try:
        # sigs.step = sigs.steps.major_step  # todo hack
        while True:
            if do_n2(cb):
                cmds.big_cmd(cb)
                return True
            if do_n3(cb):
                cmds.big_cmd(cb)
                return True
            if do_n4(cb):
                cmds.big_cmd(cb)
            return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_n2(cb):
    try:
        global LIMITS
        global grid_name
        global size
        size = 2

        limit = LIMITS[size]
        for grid_index in range(g.NUMBER_OF_GRIDS):
            grid = board.board_list[grid_index]
            grid_name = g.GRID_NAMES[grid_index]
            row_ltr = grid_name[0]
            col_ltr = grid_name[1]

            if get_row_pencil_marks(cb, grid, row_ltr, limit):
                return True

            if get_col_pencil_marks(cb, grid, col_ltr, limit):
                return True

        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_n3(cb):
    try:
        global LIMITS
        global grid_name
        global size
        size = 3

        limit = LIMITS[size]
        for grid_index in range(g.NUMBER_OF_GRIDS):
            grid = board.board_list[grid_index]
            grid_name = g.GRID_NAMES[grid_index]
            row_ltr = grid_name[0]
            col_ltr = grid_name[1]

            if get_row_pencil_marks(cb, grid, row_ltr, limit):
                return True

            if get_col_pencil_marks(cb, grid, col_ltr, limit):
                return True

        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_n4(cb):
    try:
        global LIMITS
        global grid_name
        global size
        size = 4

        limit = LIMITS[size]
        for grid_index in range(g.NUMBER_OF_GRIDS):
            grid = board.board_list[grid_index]
            grid_name = g.GRID_NAMES[grid_index]
            row_ltr = grid_name[0]
            col_ltr = grid_name[1]

            if get_row_pencil_marks(cb, grid, row_ltr, limit):
                return True

            if get_col_pencil_marks(cb, grid, col_ltr, limit):
                return True

        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def get_row_pencil_marks(cb, grid, row_ltr, limit):
    try:
        global house
        global pencil_marks

        for i, digit in enumerate(g.DIGITS):
            house =  row_ltr + digit
            row_index = digit + '0'
            cell = grid[row_index]
            length = len(cell)
            if length > limit:
                squares = g.ROWS[i]
                pencil_marks = [grid[sqr] if grid[sqr][0]
                    in g.DIGITS else '0' for sqr in squares]

                if do_subset(cb):
                    return True
        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def get_col_pencil_marks(cb, grid, col_ltr, limit):
    try:
        global house
        global pencil_marks

        for i, digit in enumerate(g.DIGITS):
            house = col_ltr + digit
            col_index = '0' + digit
            cell = grid[col_index]
            length = len(cell)
            if length > limit:
                squares = g.ROWS[i]
                pencil_marks = [grid[sqr] if grid[sqr][0]
                    in g.DIGITS else '0' for sqr in squares]

                if do_subset(cb):
                    return True

        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_subset(cb):
    '''
    Finds N digits in N cells exactly.

    :param members: list of string digits of len 9
    :param size: 2 | 3 | 4
    :param grid:  'bns' | 'cnr' | 'rcn' | 'rnc'
    :param house: # = 1|2|3|4|5|6|7|8|9
        for 'bns': 'b#'
        for 'cnr': 'c#' | 'n#'
        for 'rcn': 'r#' | 'c#'
        for 'rnc': 'r#' | 'n#'
    :return: if found: a 'quad' string of length 12
             else: am empty string
    '''
    try:
        global LIMITS
        global pencil_marks
        global size

        limit = LIMITS[size]
        members = pencil_marks

        pm_indices = [index for index, cell in enumerate(members)
                     if len(cell) > 1 and len(cell) < limit]

        if len(pm_indices) < size:
            return False

        combo = list(combinations(pm_indices, size))
        for indices in combo:
            values = set()
            for i in list(indices):
                values = set(members[i]) | values
                if len(values) > size:
                    break

            if len(values) == size:
                indices = list(indices)
                for j, index in enumerate(indices):
                    indices[j] = str(indices[j] + 1)
                values = list(values)
                values.sort()
                values = ''.join(values)
                indices = ''.join(indices)

                retVal = can_do_set(cb, indices, values)
                return retVal
            BP
        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def can_do_set(cb, indices, values):
    try:
        global LIMITS
        global house
        global pencil_marks
        global size

        members = pencil_marks

        line = members.copy()
        for index in indices:
            idx = int(index) - 1
            line[idx] = '0'
        removal_set = set(line)
        removal_set.discard('0')
        if len(removal_set) == 0:
            return False

        removal_list = list(removal_set)
        removal_text = s.union_to_string(removal_list)

        house_type = house[0]
        last_ltr = grid_name[2]
        mid_ltr = grid_name[0:2].replace(house_type, '')

        for digit in values:
            if digit in removal_text:
                big_cmd = f'{grid_name} N{str(size)} = ' \
                          f'{last_ltr}{values}-{house}-' \
                          f'{mid_ltr}{indices}'

                result = big_cmd_expansion(cb, big_cmd, line)
                return result
        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def big_cmd_expansion(cb, big_cmd, members):
    try:
        value_list = big_cmd.split(' ')
        last = value_list[-1]
        part_list = last.split('-')
        ltr_list = [part_list[0][0], part_list[1][0], part_list[2][0]]
        num_list = [part_list[0][1:], part_list[1][1:], part_list[2][1:]]
        cmd_base = f'{ltr_list[1]}{num_list[1]}{ltr_list[2]}'
        sigs.removal_list = []
        retVal = False
        for i, digits in enumerate(members):
            idx = str(i + 1)
            if digits != '0':
                for num in num_list[0]:
                    if num in digits:
                        sub = f'{cmd_base}{idx}{CLR}{ltr_list[0]}{num}'
                        if cmds.can_do_cmd(cb, sub):
                            sigs.removal_list.append(sub)
                            sigs.big_cmd = big_cmd
                            retVal = True
        sigs.big_cmd = big_cmd
        return retVal

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
