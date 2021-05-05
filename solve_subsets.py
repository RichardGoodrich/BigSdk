'''
solve_subsets.py  2021-05-04 Tue

/home/Big/Dropbox/root/private/computer/software
/PyCharm/Big'sSudoku/play/src/solve_subsets.py

'''

# <editor-fold desc="python imports"
from itertools import combinations
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import board
import settings as g
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
BP = 0
# </editor-fold>

LIMITS = {2: 3, 3: 5, 4: 6}


def do():
    '''
    Finds Sudoku N2, N3, N4.


    :return:  True | False   sigs.big_cmd
    '''
    try:
        while True:
            if do_n2():
                return True
            if do_n3():
                return True
            if do_n4():
                return True
            return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()


def do_n2():
    try:
        for grid_index in range(g.NUMBER_OF_GRIDS):
            if do_house(grid_index, 'x', 2):
                return True
            if do_house(grid_index, 'y', 2):
                return True
            return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_n3():
    try:
        for grid_index in range(g.NUMBER_OF_GRIDS):
            if do_house(grid_index, 'x', 3):
                return True
            if do_house(grid_index, 'y', 3):
                return True
            return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_n4():
    try:
        for grid_index in range(g.NUMBER_OF_GRIDS):
            if do_house(x, grid_index, 'x', 4):
                return True
            if do_house(x, grid_index, 'y', 4):
                return True
            return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()



def do_house(grid_index, house_type, size):
    '''
    do_house.


    :return: True | False
    '''
    try:
        global LIMITS
        limit = LIMITS[size]
        house = ''
        squares = []

        grid = board.grid_list[grid_index]
        grid_name = g.GRID_NAMES[grid_index]
        for i, digit in enumerate(g.DIGITS):
            if house_type == 'x':
                house_type = grid_name[0]
                idx = digit + '0'
                if len(grid[idx]) > limit:
                    house = house_type + digit
                    squares = g.ROWS[i]
            elif house_type == 'y':
                house_type = grid_name[1]
                idx = '0' + digit
                if len(grid[idx]) > limit:
                    house = house_type + digit
                    squares = g.COLS[i]

            pencil_marks = [grid[sqr] if grid[sqr][0] in g.DIGITS else '0' for sqr in squares]
            return do_subset(pencil_marks, size, grid_name, house)

    except Exception as e:
        logger_except.exception(e)
        sys.exit()


def do_subset(members, size, grid, house):
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
        limit = LIMITS[size]
        set_index = []

        # set_index = [idx for idx, cell in enumerate(members) if len(cell) > 1 and len(cell) < limit]

        for index, cell in enumerate(members):
            if len(cell) > 1 and len(cell) < limit:
                set_index.append(index)

        if len(set_index) < size:
            return False

        combo = list(combinations(set_index, size))
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

                # retVal = can_do_set(grid, size, house,
                #                          members, indices, values)
                # return retVal
            BP
        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def can_do_set(grid_name, size, house,
               members, indices, values):
    try:
        line = members.copy()
        for index in indices:
            idx = int(index) - 1
            line[idx] = '0'
        removal_set = set(line)
        removal_set.discard('0')
        if len(removal_set) == 0:
            return False
        removal_list = list(removal_set)
        removal_text = Utils.union_to_string([removal_list])

        house_type = house[0]
        last_ltr = grid_name[2]
        mid_ltr = grid_name[0:2].replace(house_type, '')

        for digit in values:
            if digit in removal_text:
                big_cmd = f'{grid_name} N{str(size)} = ' \
                          f'{last_ltr}{values}-{house}-' \
                          f'{mid_ltr}{indices}'

                result = self.big_cmd_expansion(big_cmd, line)
                return result
        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()


if __name__ == '__main__':
    pass
else:
    print('solve_subsets.py is being imported')
