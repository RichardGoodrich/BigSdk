'''
solve_point.py

2021-05-14 Fri
'''

# <editor-fold desc="python imports"
import logging as log
import re
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import board
import cmds
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
BLK_SQR_ROWS = g.BLK_SQR_ROWS
BP = g.BREAK_POINT
CLR = g.OP_CLR
LIMITS = {2: 3, 3: 4, 4: 5}
# </editor-fold>

def do(cb):
    try:
        for box_index in g.DIGITS:
            BP
            for num_index in g.DIGITS:
                squares = board.bns[box_index + num_index]
                bns_squares = f'b{box_index}n{num_index}s{squares}'
                for box_row_squares in BLK_SQR_ROWS:
                    if s.union_to_string([squares, box_row_squares]) == box_row_squares:
                        row_point = do_row_point(bns_squares, box_row_squares)
                        if row_point != '':
                            sigs.big_cmd = row_point
                            cmds.big_cmd(cb)
                            return True

                for box_col_squares in g.BLK_SQR_COLS:
                    if s.union_to_string([squares, box_col_squares]) == box_col_squares:
                        col_point = do_col_point(bns_squares, box_col_squares)
                        if col_point != '':
                            sigs.big_cmd = col_point
                            cmds.big_cmd(cb)
                            return True
        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_col_point(bns_sqrs, box_col_sqrs):
    try:
        num_list = re.findall('[0-9]+', bns_sqrs)

        bs_list = [num_list[0] + sqr for sqr in box_col_sqrs]
        rc_list = [s.convert_bsrc(bs) for bs in bs_list]
        boxcol_rows = ''.join([item[0] for item in rc_list])

        col_index = rc_list[0][1]
        num_index = bns_sqrs[3]
        NC = num_index + col_index
        col_rows = board.ncr[NC]

        col_row_union = s.union_to_string([col_rows, boxcol_rows])
        if len(col_row_union) > len(boxcol_rows):
            extra_col_rows = col_row_union.replace(boxcol_rows, '')

            N = bns_sqrs[3]
            B = bns_sqrs[1]
            C = rc_list[0][1]

            col_point = f'rcn Point = n{N}b{B}c{C}'
            removal = f'c{C}r{extra_col_rows}{CLR}n{N}'

            if len(removal) > g.BASIC_CMD_LENGTH:
                sigs.removal_list = [f'c{C}r{extra}{CLR}n{N}' for extra in extra_col_rows]
            else:
                sigs.removal_list = [removal]

            return col_point
        else:
            return ''

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def do_row_point(bns_sqrs, box_row_sqrs):
    try:
        num_list = re.findall('[0-9]+', bns_sqrs)

        bs_list = [num_list[0] + ssr for ssr in box_row_sqrs]
        rc_list = [s.convert_bsrc(bs) for bs in bs_list]
        boxrow_cols = ''.join([item[1] for item in rc_list])

        row_index = rc_list[0][0]
        num_index = bns_sqrs[3]
        RN = row_index + num_index
        row_cols = board.rnc[RN]

        row_col_union = s.union_to_string([row_cols, boxrow_cols])
        if len(row_col_union) > len(boxrow_cols):
            extra_row_cols = row_col_union.replace(boxrow_cols, '')

            N = bns_sqrs[3]
            B = bns_sqrs[1]
            R = rc_list[0][0]

            row_point = f'rcn Point = n{N}b{B}r{R}'
            removal = f'r{R}c{extra_row_cols}{CLR}n{N}'

            if len(removal) > g.BASIC_CMD_LENGTH:
                sigs.removal_list = [f'r{R}c{extra}{CLR}n{N}' for extra in extra_row_cols]
            else:
                sigs.removal_list = [removal]

            return row_point
        else:
            return ''

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
