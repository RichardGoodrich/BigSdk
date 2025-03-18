'''
solve_claim.py  2021-05-10 Mon

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

def do(cb):
    try:
        rnc = board.board_list[1]
        ncr = board.board_list[2]

        for num_index, num in enumerate(g.DIGITS):
            row_squares = g.COLS[num_index]
            col_squares = g.ROWS[num_index]

            rows = [squares[0] for squares in row_squares if rnc[squares][0] in g.DIGITS]
            cols = [squares[1] for squares in col_squares if ncr[squares][0] in g.DIGITS]

            if is_claim(num, rows, cols):
                cmds.big_cmd(cb)
                return True

        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def is_claim(num, rows, cols):
    try:
        row_col_list = [row + col for row in rows for col in cols]
        for row, col in row_col_list:
            row_blks = g.ROW_TO_BLKS[row]
            row_sqrs = g.ROW_TO_SQRS[row]
            col_blks = g.COL_TO_BLKS[col]
            col_sqrs = g.COL_TO_SQRS[col]
            blk = s.intersect_to_string([row_blks, col_blks])
            if len(blk) == 1:
                blk_cols = g.BLK_TO_COLS[blk]
                blk_rows = g.BLK_TO_ROWS[blk]
                blk_sqrs = board.bns[blk + num]
                row_cols = board.rnc[row + num]  # cols in this row that have this number
                col_rows = board.ncr[num + col]  # rows in this col that have this number
                row_cols_union = s.union_to_string([blk_cols, row_cols])
                col_rows_union = s.union_to_string([blk_rows, col_rows])
                if row_cols_union == blk_cols:
                    # cols in this row confined to block
                    row_meet = s.intersect_to_string([blk_sqrs, row_sqrs])
                    if blk_sqrs != row_meet:
                        # num-blk-row claim
                        rc_list = [s.convert_bsrc(blk + sqr) for sqr in blk_sqrs if sqr not in row_meet]
                        sigs.removal_list = [f'r{rc[0]}c{rc[1]}{CLR}n{num}' for rc in rc_list]
                        sigs.big_cmd = f'rcn Claim = n{num}b{blk}r{row}'
                        return True
                if col_rows_union == blk_rows:
                    # rows in this col confined to block
                    col_meet = s.intersect_to_string([blk_sqrs, col_sqrs])
                    if blk_sqrs != col_meet:
                        # num-blk-col claim
                        rc_list = [s.convert_bsrc(blk + sqr) for sqr in blk_sqrs if sqr not in col_meet]
                        sigs.removal_list = [f'r{rc[0]}c{rc[1]}{CLR}n{num}' for rc in rc_list]
                        sigs.big_cmd = f'rcn Claim = n{num}b{blk}c{col}'
                        return True
        return False

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
