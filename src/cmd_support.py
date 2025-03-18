'''
cmd_support.py  2021-05-05  Wed

renamed from cmd_stuff.py
'''


# <editor-fold desc="python imports"
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import settings as g
import signals as sigs
import support as s
# </editor-fold>

# <editor-fold desc="globals"
CLR = g.OP_CLR
SET = g.OP_SET
BP = g.BREAK_POINT
NL = g.NEW_LINE

GRID_NAMES_1 = g.GRID_NAMES_1
GRID_NAMES_2 = g.GRID_NAMES_2
GRID_NAMES = g.GRID_NAMES
MAX_GRID_LENGTH = g.NUMBER_OF_GRIDS
BLOCK_PEERS = g.BLOCK_PEERS
RCN_BLOCK_PEERS = g.RCN_BLOCK_PEERS
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

class CmdS:
    block_sqr = ''
    block_cmd = ''
    cmd_main = ''
    cmd_alt = ''
    from_cmd = ''
    grid = ''
    grid_index = 0
    numbers = ''
    operation = SET
    square = ''
    value = ''

    letters_list = g.GRID_NAMES
    cmds_list = []
    multiple_cmds_list = []
    numbers_list = []
    peer_subs = []
    block_subs = ''


    @classmethod
    def multiple_cmds_from_last_digits(cls, big):
        try:
            length = len('r1c2=n3')
            if len(big) > length:
                base_cmd = big[:6]
                last_digits = big[6:]
                cls.multiple_cmds_list = [base_cmd + digit for digit in last_digits]
                return True
            else:
                cls.multiple_cmds_list = []
                return False

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    @classmethod
    def set(cls, cmd):
        '''
        A basic_cmd (7-types) string of length = 7 is parsed ... ref the following.

        The following class attributes are generated
        --------------------------------------------------------------------------
        block_sqr   = string of length= 2  BN where B & N is digit in '123456789'
                      B is the row index of the bns grid
                      N is the col index of the bns grid
                      unless bns basic_cmd is param, then it is the 'RC' square
                      (maybe should call alt_sqr ?)
        block_cmd   = a basic_cmd of lentth = 7 for the bns grid see cmd param:
        cmd_main    = basic_cmd string: see 1st choice of :param cmd below
        cmd_alt     = basic_cmd string: see 2nd choice of :param cmd below
        from_cmd    = basic_cmd string passed in
        grid_index  =  int:  0 | 1 | 2 | 3
        numbers     = string of length 3 for the X,Y,Z described in :param cmd
        operation   = string of length 1 = g.CLR(-) | g.SET(+)
        square      = string of length 2 = usual Sudoku grid indexing e.g '11' to '99'
                         of the basic_cmd passed int
        value       = string of length 1, the last digit in the basic_cmd


        :param cmd:  e.g. x{X} + y{Y} + {OP} + z(Z}     length = 7
               where xyz = rcn | crn   grid_index = 0
                         = rnc | ncr   grid_index = 1
                         = ncr | cnr   grid_index = 2
                         = bns         grid_index = 3
               where X, Y, Z  =  digit in '123456789'
               where OP = g.SET(=)
                          g.CLR(-)

        :return: None
        '''
        try:
            cls.from_cmd = cmd
            cls.grid = f'{cmd[0]}{cmd[2]}{cmd[5]}'

            cls.grid_index = GRID_NAMES.index(cls.grid)
            if cls.grid_index >= MAX_GRID_LENGTH:
                cls.grid_index -= MAX_GRID_LENGTH
                cls.cmd_alt = cmd
                cls.cmd_main = f'{cmd[2]}{cmd[3]}{cmd[0]}{cmd[1]}{cmd[4:7]}'
            else:
                cls.cmd_main = cmd
                cls.cmd_alt = f'{cmd[2]}{cmd[3]}{cmd[0]}{cmd[1]}{cmd[4:7]}'

            cls.grid = f'{cls.cmd_main[0]}{cls.cmd_main[2]}{cls.cmd_main[5]}'
            cls.grid_index = GRID_NAMES.index(cls.grid)
            cls.numbers = f'{cls.cmd_main[1]}{cls.cmd_main[3]}{cls.cmd_main[6]}'
            cls.operation = cls.cmd_main[4]
            cls.square = f'{cls.cmd_main[1]}{cls.cmd_main[3]}'
            cls.value = f'{cls.cmd_main[6]}'
            cls.block_sqr = s.convert_bsrc(cls.square)
            cls.block_cmd = f'b{cls.block_sqr[0]}n{cls.value}{cls.operation}s{cls.block_sqr[1]}'
        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    @classmethod
    def do_lists(cls):
        try:
            cls.cmds_list = []
            cls.numbers_list = []
            rcn_numbers = [0, 0, 0]
            rnc_numbers = [0, 0, 0]
            ncr_numbers = [0, 0, 0]
            bns_numbers = [0, 0, 0]

            if cls.grid == 'rcn':
                cls.grid_index = 0
                rcn_numbers = list(cls.numbers)
            elif cls.grid == 'bns':
                cls.grid_index = 3
                bns_numbers = list(cls.numbers)
                rcn_numbers[2] = bns_numbers[1]
                sqr = bns_numbers[0] + bns_numbers[2]
                rcn_numbers[0], rcn_numbers[1] = s.convert_bsrc(sqr)
            elif cls.grid == 'rnc':
                cls.grid_index = 1
                rnc_numbers = list(cls.numbers)
                rcn_numbers[0] = rnc_numbers[0]
                rcn_numbers[1] = rnc_numbers[2]
                rcn_numbers[2] = rnc_numbers[1]
            elif cls.grid == 'ncr':
                cls.grid_index = 3
                ncr_numbers = list(cls.numbers)
                rcn_numbers[0] = ncr_numbers[2]
                rcn_numbers[1] = ncr_numbers[1]
                rcn_numbers[2] = ncr_numbers[0]

            if bns_numbers == [0, 0, 0]:
                bns_numbers[1] = rcn_numbers[2]
                sqr = rcn_numbers[0] + rcn_numbers[1]
                bns_numbers[0], bns_numbers[2] = s.convert_bsrc(sqr)
            if ncr_numbers == [0, 0, 0]:
                ncr_numbers[0] = rcn_numbers[2]
                ncr_numbers[1] = rcn_numbers[1]
                ncr_numbers[2] = rcn_numbers[0]
            if rnc_numbers == [0, 0, 0]:
                rnc_numbers[0] = rcn_numbers[0]
                rnc_numbers[1] = rcn_numbers[2]
                rnc_numbers[2] = rcn_numbers[1]

            # convert lists to string
            cmds_numbers = []
            cmds_numbers.append(''.join(rcn_numbers))
            cmds_numbers.append(''.join(rnc_numbers))
            cmds_numbers.append(''.join(ncr_numbers))
            cmds_numbers.append(''.join(bns_numbers))

            letters_list = cls.letters_list.copy()
            cls.numbers_list = cmds_numbers
            for letters, digits in zip(letters_list, cls.numbers_list):
                interleave = ''.join(let + num for let, num in zip(letters, digits))
                cmd = interleave[0:4] + cls.operation + interleave[4:7]
                cls.cmds_list.append(cmd)
            BP
        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    @classmethod
    def do_peers(cls):
        try:
            if cls.operation == SET:
                L = cls.letters_list[cls.grid_index]
                D = cls.numbers_list[cls.grid_index]
                # square = D[0:2]
                peers_row = f'{L[0]}{D[0]}{L[1]}!{D[1]}{CLR}{L[2]}{D[2]}'
                peers_col = f'{L[1]}{D[1]}{L[0]}!{D[0]}{CLR}{L[2]}{D[2]}'
                if cls.grid_index == 3:
                    cls.peer_subs = [peers_row]
                elif cls.grid_index == 1 or cls.grid_index == 2:
                    cls.peer_subs = [peers_row, peers_col]

                if cls.grid_index == 0:
                    block_peers = RCN_BLOCK_PEERS[cls.square]
                    num_value = D[2]
                    row_block_peers = block_peers[0].replace('.', num_value)
                    col_block_peers = block_peers[1].replace('.', num_value)
                    cls.peer_subs = [peers_row, row_block_peers, peers_col, col_block_peers]

                    # generate block only peers
                    end_digit = cls.block_cmd[-1]
                    peer = cls.block_cmd[:-1]
                    peer = peer.replace(SET, CLR)
                    peer += BLOCK_PEERS[end_digit]
                    cls.block_subs = peer
                return True
            else:
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
