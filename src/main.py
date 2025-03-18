'''
main.py is the GUI

ref: ../notes/root.txt  for paths
'''

# <editor-fold desc="python imports"
import copy
import logging as log
import re
import sys
import tkinter as tk
# </editor-fold>

# <editor-fold desc="local imports"
import board
import colors
from grid import Grid
import puzzle_load as pz
import settings as g
import signals as sigs
import support as s
import solve
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
GRID_NAMES = g.GRID_NAMES
NUMBER_OF_GRIDS = g.NUMBER_OF_GRIDS
# </editor-fold>



def main():
    root = tk.Tk()
    gui_ref = gui(root)
    root.mainloop()

def gui(root):
    # <editor-fold desc="Basic Setup"
    sigs.screen_width = root.winfo_screenwidth()
    sigs.screen_height = root.winfo_screenheight()
    sigs.screen_depth = root.winfo_screendepth()
    Grid.create_grid_stuff()

    root.title("Big's Sudoku")
    root.geometry('250x250+200+20')
    root.resizable(1, 1)

    menuBar = tk.Menu(root)
    menuBar['bg'] = colors.MENU_BAR_NORMAL
    root['menu'] = menuBar
    subMenu = tk.Menu(menuBar)
    # </editor-fold>

    # <editor-fold desc="Grid Menu"
    def toggle_all():
        for index, location in reversed(list(enumerate(Grid.grid_locations))):
            grid_list[index].master.geometry(location)
        toggle_rcn()

    def toggle_bns():
        toggle_color_normal()
        toggle_color_active('bns')

    def toggle_ncr():
        toggle_color_normal()
        toggle_color_active('ncr')

    def toggle_rcn():
        toggle_color_normal()
        toggle_color_active('rcn')

    def toggle_rnc():
        toggle_color_normal()
        toggle_color_active('rnc')

    def toggle_spk():
        print('todo main.toggle_spk')

    def toggle_color_active(grid_name):
        sigs.is_lifted_index = GRID_NAMES.index(grid_name)
        grid_list[sigs.is_lifted_index].canvas["bg"] = colors.lift_color_active
        grid_list[sigs.is_lifted_index].canvas.update()
        grid_list[sigs.is_lifted_index].master.lift()

    def toggle_color_normal():
        grid_index = sigs.is_lifted_index
        grid_list[grid_index].canvas["bg"] = colors.lift_color_normal
        grid_list[grid_index].canvas.update()


    grid_menu = tk.Menu(subMenu)
    grid_menu.add_command(label='rcn', command=toggle_rcn)
    grid_menu.add_command(label='rnc', command=toggle_rnc)
    grid_menu.add_command(label='ncr', command=toggle_ncr)
    grid_menu.add_command(label='bns', command=toggle_bns)
    grid_menu.add_command(label='speak', command=toggle_spk)
    grid_menu.add_command(label='ALL', command=toggle_all)
    menuBar.add_cascade(label='Grids', menu=grid_menu)
    # </editor-fold>

    # <editor-fold desc="Puzzle Menu"
    def clear_puzzle():
        try:
            board.erase()
            for grid in grid_list:
                grid.erase_puzzle()
        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def load_puzzle():
        try:
            s.is_load_set(True)

            if sigs.step == sigs.steps.no_step:
                menuBar['bg'] = colors.MENU_BAR_NORMAL
            else:
                menuBar['bg'] = colors.MENU_BAR_ACTIVE

            pz.load(cb)
            s.is_load_set(False)
        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def load_grids():
        s.is_grid_set(True)
        sigs.is_grid_choose = True
        while sigs.is_grid_choose:
            for grid_ in pz.grid_choice:
                entry_var.set(grid_)
                root.wait_variable(next_button_var)
                next_button_var.set(False)

    def load_81_char_strings():
        s.is_load_set(True)
        sigs.is_string81_choose = True
        # pz.string_81(cb)
        while sigs.is_string81_choose:
            for value in pz.string81_choice:
                entry_var.set(value)
                root.wait_variable(next_button_var)
                next_button_var.set(False)

    puz_menu = tk.Menu(subMenu)
    puz_menu.add_command(label='Clear', command=clear_puzzle)
    puz_menu.add_command(label='Default', command=load_puzzle)
    puz_menu.add_command(label='Grids', command=load_grids)
    puz_menu.add_command(label='81 char string', command=load_81_char_strings)
    menuBar.add_cascade(label='Puzzles', menu=puz_menu)
    # </editor-fold>

    # <editor-fold desc="Solve Menu"
    def solve_all():
        try:
            solve.all(cb)
        except Exception as e:
            print(e)
            sys.exit()

    solve_menu = tk.Menu(subMenu)
    solve_menu.add_command(label='Solve All', command=solve_all)
    menuBar.add_cascade(label='Solving', menu=solve_menu)
    # </editor-fold>

    # <editor-fold desc="Next Button setup"
    def next_button_cmd():
        menuBar['bg'] = colors.MENU_BAR_NORMAL
        next_button_var.set(True)
        return ('Next Button Pressed')

    next_button_var = tk.BooleanVar()
    next_button_var.set(False)
    next_button = tk.Button(root, text='Next', height=1, width=10,
                            bg=colors.NEXT_BUTTON_INACTIVE,
                            command=next_button_cmd).pack()
    # </editor-fold>

    # <editor-fold desc="step_mode Radio ButtonS"
    def step_mode_cmd():
        sigs.step = step_mode_var.get()

    step_mode_var = tk.StringVar()
    step_mode_var.set(sigs.steps.no_step)

    for step in sigs.steps:
        tk.Radiobutton(root,
                       text=step,
                       variable=step_mode_var,
                       value=step,
                       command=step_mode_cmd,
                       ).pack(anchor=tk.W)
    # </editor-fold>

    # <editor-fold desc="Entry Widget Setup"
    def entry_cmd():
        '''
        Rev-4 line 679 main.entry_cmd()

        :return:
        '''
        puzzle = entry_var.get()
        if puzzle == 'doc':
            print('todo - doc stub')
            return

        if puzzle == 'EXIT':
            print('todo EXIT stub')
        elif sigs.is_grid_choose:
            puz = pz.grid_choice_dict[puzzle]
            grid_list = re.findall('[0-9]+', puz)
            pz.load(cb, grid_list)
            sigs.is_grid_choose = False
        elif sigs.is_string81_choose:
            puz = pz.string81_choice_dict[puzzle]
            pz.load(cb, puz)
            sigs.is_string81_choose = False
        else:
            grid_list = re.findall('[0-9]+', puzzle)
            sigs.is_grid = True
            sigs.is_grid_choose = True
            pz.load(cb, grid_list)
            # sigs.is_grid_choose = False

    entry_var = tk.StringVar()

    entry = tk.Entry(root, width=50,
                     textvariable=entry_var).pack()

    entry_button = tk.Button(root,
                             text='Enter Puzzle',
                             height=1,
                             width=10,
                             command=entry_cmd).pack()
    # </editor-fold>

    # <editor-fold desc="The Grids"
    bns = Grid(tk.Toplevel(), 'bns')
    ncr = Grid(tk.Toplevel(), 'ncr')
    rnc = Grid(tk.Toplevel(), 'rnc')
    rcn = Grid(tk.Toplevel(), 'rcn')
    grid_list = [rcn, rnc, ncr, bns]

    toggle_rcn()
    # </editor-fold>

    def cmd_to_gui():
        '''
        The only way for business logic to send commands to gui

        :param kwargs:
        :return:
        '''
        try:
            name = s.gui_cmd_name
            cmd_types = s.GuiCmdType()

            if name == cmd_types.cmd:
                index = s.grid_cmd.index
                square = s.grid_cmd.square
                cell = s.grid_cmd.cell

                grid = grid_list[index]
                grid.cmd(square, cell)
                return

            elif name == cmd_types.color:
                index = s.color_cmd.index
                color = s.color_cmd.color
                tag = s.color_cmd.tag

                grid = grid_list[index]
                grid.color_square(tag, color)
                return

            elif name == cmd_types.entry:
                value = s.entry_cmd.entry
                entry_var.set(value)
                root.update()
                return

            elif name == cmd_types.display:
                for grid in grid_list:
                    grid.display_numbers()
                return

            elif name == cmd_types.grids_restore:
                for grid in grid_list:
                    grid.puzzle_dict = copy.deepcopy(grid.puzzle_save)
                return

            elif name == cmd_types.grids_save:
                for grid in grid_list:
                    grid.puzzle_save = copy.deepcopy(grid.puzzle_dict)
                return

            elif name == cmd_types.lift:
                toggle_color_normal()
                sigs.is_lifted_index = s.lift_cmd.index
                grid_list[sigs.is_lifted_index].canvas["bg"] = colors.lift_color_active
                grid_list[sigs.is_lifted_index].canvas.update()
                grid_list[sigs.is_lifted_index].master.lift()
                return

            elif name == cmd_types.restore:
                for grid in grid_list:
                    grid.color_restore()
                return

            elif name == cmd_types.wait:
                root.wait_variable(next_button_var)
                next_button_var.set(False)
                menuBar['bg'] = colors.MENU_BAR_ACTIVE
                return

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    cb = cmd_to_gui   # cb for call back

def test_support():
    print(f'{NL}Testing support.py{NL}')

    print(s.gui_cmd_type)

    print(f'{NL}support Gui Cmd Type defaults:')
    print(s.grid_cmd)
    print(s.color_cmd)

if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')

    # test_support()
    main()


