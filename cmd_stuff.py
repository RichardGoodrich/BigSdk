
# <editor-fold desc="python imports"
import logging as log
import sys
# </editor-fold>

# <editor-fold desc="local imports"
import settings as g
import signals as sigs
# </editor-fold>

# <editor-fold desc="globasl"
BP = 0
NL = '\n'
GRID_NAMES_1 = ['rcn', 'rnc', 'ncr', 'bns']
GRID_NAMES_2 = ['crn', 'nrc', 'cnr', 'nbs']
GRID_NAMES = GRID_NAMES_1 + GRID_NAMES_2
MAX_GRID_LENGTH = len(GRID_NAMES_1)

BLOCK_PEERS = {
    '1': '5689',
    '2': '4679',
    '3': '4578',
    '4': '2389',
    '5': '1379',
    '6': '1278',
    '7': '2356',
    '8': '1346',
    '9': '1245',
}
RCN_BLOCK_PEERS = {
    '11': ['b23n.-s123', 'b47n.-s147'],
    '12': ['b23n.-s123', 'b47n.-s258'],
    '13': ['b23n.-s123', 'b47n.-s369'],
    '14': ['b13n.-s123', 'b58n.-s147'],
    '15': ['b13n.-s123', 'b58n.-s258'],
    '16': ['b13n.-s123', 'b58n.-s369'],
    '17': ['b12n.-s123', 'b69n.-s147'],
    '18': ['b12n.-s123', 'b69n.-s258'],
    '19': ['b12n.-s123', 'b69n.-s369'],
    '21': ['b23n.-s456', 'b47n.-s147'],
    '22': ['b23n.-s456', 'b47n.-s258'],
    '23': ['b23n.-s456', 'b47n.-s369'],
    '24': ['b13n.-s456', 'b58n.-s147'],
    '25': ['b13n.-s456', 'b58n.-s258'],
    '26': ['b13n.-s456', 'b58n.-s369'],
    '27': ['b12n.-s456', 'b69n.-s147'],
    '28': ['b12n.-s456', 'b69n.-s258'],
    '29': ['b12n.-s456', 'b69n.-s369'],
    '31': ['b23n.-s789', 'b47n.-s147'],
    '32': ['b23n.-s789', 'b47n.-s258'],
    '33': ['b23n.-s789', 'b47n.-s369'],
    '34': ['b13n.-s789', 'b58n.-s147'],
    '35': ['b13n.-s789', 'b58n.-s258'],
    '36': ['b13n.-s789', 'b58n.-s369'],
    '37': ['b12n.-s789', 'b69n.-s147'],
    '38': ['b12n.-s789', 'b69n.-s258'],
    '39': ['b12n.-s789', 'b69n.-s369'],
    '41': ['b56n.-s123', 'b17n.-s147'],
    '42': ['b56n.-s123', 'b17n.-s258'],
    '43': ['b56n.-s123', 'b17n.-s369'],
    '44': ['b46n.-s123', 'b28n.-s147'],
    '45': ['b46n.-s123', 'b28n.-s258'],
    '46': ['b46n.-s123', 'b28n.-s369'],
    '47': ['b45n.-s123', 'b39n.-s147'],
    '48': ['b45n.-s123', 'b39n.-s258'],
    '49': ['b45n.-s123', 'b39n.-s369'],
    '51': ['b56n.-s456', 'b17n.-s147'],
    '52': ['b56n.-s456', 'b17n.-s258'],
    '53': ['b56n.-s456', 'b17n.-s369'],
    '54': ['b46n.-s456', 'b28n.-s147'],
    '55': ['b46n.-s456', 'b28n.-s258'],
    '56': ['b46n.-s456', 'b28n.-s369'],
    '57': ['b45n.-s456', 'b39n.-s147'],
    '58': ['b45n.-s456', 'b39n.-s258'],
    '59': ['b45n.-s456', 'b39n.-s369'],
    '61': ['b56n.-s789', 'b17n.-s147'],
    '62': ['b56n.-s789', 'b17n.-s258'],
    '63': ['b56n.-s789', 'b17n.-s369'],
    '64': ['b46n.-s789', 'b28n.-s147'],
    '65': ['b46n.-s789', 'b28n.-s258'],
    '66': ['b46n.-s789', 'b28n.-s369'],
    '67': ['b45n.-s789', 'b39n.-s147'],
    '68': ['b45n.-s789', 'b39n.-s258'],
    '69': ['b45n.-s789', 'b39n.-s369'],
    '71': ['b89n.-s123', 'b14n.-s147'],
    '72': ['b89n.-s123', 'b14n.-s258'],
    '73': ['b89n.-s123', 'b14n.-s369'],
    '74': ['b79n.-s123', 'b25n.-s147'],
    '75': ['b79n.-s123', 'b25n.-s258'],
    '76': ['b79n.-s123', 'b58n.-s369'],
    '77': ['b78n.-s123', 'b36n.-s147'],
    '78': ['b78n.-s123', 'b36n.-s258'],
    '79': ['b78n.-s123', 'b36n.-s369'],
    '81': ['b89n.-s456', 'b14n.-s147'],
    '82': ['b89n.-s456', 'b14n.-s258'],
    '83': ['b89n.-s456', 'b14n.-s369'],
    '84': ['b79n.-s456', 'b25n.-s147'],
    '85': ['b79n.-s456', 'b25n.-s258'],
    '86': ['b79n.-s456', 'b25n.-s369'],
    '87': ['b78n.-s456', 'b36n.-s147'],
    '88': ['b78n.-s456', 'b36n.-s258'],
    '89': ['b78n.-s456', 'b36n.-s369'],
    '91': ['b89n.-s789', 'b14n.-s147'],
    '92': ['b89n.-s789', 'b14n.-s258'],
    '93': ['b89n.-s789', 'b14n.-s369'],
    '94': ['b79n.-s789', 'b25n.-s147'],
    '95': ['b79n.-s789', 'b25n.-s258'],
    '96': ['b79n.-s789', 'b25n.-s369'],
    '97': ['b78n.-s789', 'b36n.-s147'],
    '98': ['b78n.-s789', 'b36n.-s258'],
    '99': ['b78n.-s789', 'b36n.-s369'],
}
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


def convert_bsrc(self, value):
    try:
        x = int(value[0])
        y = int(value[1])
        a = 1 + (3 * ((x - 1) // 3)) + ((y - 1) // 3)
        b = 1 + (3 * ((x + 2) % 3)) + ((y + 2) % 3)
        return (str(a) + str(b))

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def intersect_to_string(self, text_list):
    try:
        result = text_list.pop()
        for next in text_list:
            result = set(result).intersection(next)

        result = list(result)
        result.sort()
        result = ''.join(result)
        return result

    except Exception as e:
        logger_except.exception(e)
        sys.exit()

def union_to_string(self, text_list):
    try:
        if g.IS_LOG_METHOD:
            logger_methods.info('')

        result = text_list.pop()
        for next in text_list:
            result = set(result).union(next)

        result = list(result)
        result.sort()
        result = ''.join(result)
        return result

    except Exception as e:
        logger_except.exception(e)
        sys.exit()



class CmdS:
    block_sqr = ''
    block_cmd = ''
    cmd_main = ''
    cmd_alt = ''
    from_cmd = ''
    grid = ''
    grid_index = 0
    numbers = ''
    operation = g.SET
    square = ''
    value = ''

    letters_list = g.GRID_NAMES
    cmds_list = []
    multiple_cmds_list = []
    numbers_list = []
    peer_subs = []
    block_subs = ''

    @classmethod
    def convert_bsrc(cls, value):
        x = int(value[0])
        y = int(value[1])
        a = 1 + (3 * ((x - 1) // 3)) + ((y - 1) // 3)
        b = 1 + (3 * ((x + 2) % 3)) + ((y + 2) % 3)
        return (str(a) + str(b))

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
            logger_1.exception(e)
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
            cls.block_sqr = cls.convert_bsrc(cls.square)
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
                rcn_numbers[0], rcn_numbers[1] = CmdS.convert_bsrc(sqr)
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
                bns_numbers[0], bns_numbers[2] = cls.convert_bsrc(sqr)
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
            if cls.operation == g.SET:
                L = cls.letters_list[cls.grid_index]
                D = cls.numbers_list[cls.grid_index]
                # square = D[0:2]
                peers_row = f'{L[0]}{D[0]}{L[1]}!{D[1]}{g.CLR}{L[2]}{D[2]}'
                peers_col = f'{L[1]}{D[1]}{L[0]}!{D[0]}{g.CLR}{L[2]}{D[2]}'
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
                    peer = peer.replace(g.SET, g.CLR)
                    peer += BLOCK_PEERS[end_digit]
                    cls.block_subs = peer
                return True
            else:
                return False

        except Exception as e:
            logger_except.exception(e)
            sys.exit()


if __name__ == '__main__':
    pass
else:
    print('cmd_stuff.py is being imported')
