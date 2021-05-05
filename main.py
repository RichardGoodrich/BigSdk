#!/usr/bin/python3

'''
main.py 2021-05-05 Wed

ref: ../notes/root.txt  for paths
'''

# <editor-fold desc="python imports"
from collections import namedtuple
import logging as log
import os
import sys
import tkinter as tk
# </editor-fold>

# <editor-fold desc="local imports"
import board
import colors
from grid import Grid
import puzzle_load
import signals as sigs
import solve
# </editor-fold>

# <editor-fold desc="globals"
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

def main():
    root = tk.Tk()
    gui_ref = gui(root)
    print('gui loop')
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
        pass

    def toggle_bns():
        pass

    def toggle_ncr():
        pass

    def toggle_rcn():
        pass

    def toggle_rnc():
        pass

    def toggle_spk():
        pass

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
            sigs.is_load_set(True)

            if sigs.step == sigs.steps.no_step:
                menuBar['bg'] = colors.MENU_BAR_NORMAL
            else:
                menuBar['bg'] = colors.MENU_BAR_ACTIVE

            puzzle_load.load(x)
            sigs.is_load_set(False)
        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def load_grids():
        sigs.is_grid_set(True)
        print('todo - main.load_grids need routine')
        sigs.is_grid_set(False)

    def load_81_char_strings():
        sigs.is_load_set(True)
        print('todo - main.load_81_char_strings need routine')
        sigs.is_load_set(False)

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
            solve.all(x)
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
        pass

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
    # </editor-fold>

    def cmd_to_gui(**kwargs):
        '''
        The only way for business logic to send commands to gui

        :param kwargs:
        :return:
        '''
        try:
            cmd = sigs.GuiCmd.cmd

            if cmd == sigs.gui_cmd.wait:
                root.wait_variable(next_button_var)
                next_button_var.set(False)
                menuBar['bg'] = colors.MENU_BAR_ACTIVE
                return

            elif cmd == sigs.gui_cmd.color:
                index = sigs.GuiCmd.grid_index
                grid = grid_list[index]
                color = sigs.GuiCmd.color
                tag = sigs.GuiCmd.tag
                grid.color_square(tag, color)
                return

            elif cmd == sigs.gui_cmd.restoreColors:
                for grid in grid_list:
                    grid.color_restore()
                return

            elif cmd == sigs.gui_cmd.displayNumbers:
                for grid in grid_list:
                    grid.display_numbers()
                return

            elif cmd == sigs.gui_cmd.grid:
                index = sigs.GuiCmd.grid_index
                grid = grid_list[index]
                square = sigs.GuiCmd.square
                cell = sigs.GuiCmd.cell
                grid.cmd(square, cell)
                return

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    x = cmd_to_gui   # callback reference is this 'x' to keep typing to minimum!


def set_folders():
    try:
        sigs.src_dir = os.getcwd()
        sigs.root_dir = sigs.src_dir.replace('/src', '')
        sigs.lo = os.path.join(sigs.root_dir, '/logs')

    except Exception as e:
        logger_except.exception(e)
        sys.exit()


if __name__ == '__main__':
    main()

''''
Corey Schafer Sep 12, 2019
Python Threading Tutorial: Run Code Concurrently 
  Using the Threading Module

15:25  importing concurrent futures  

CS 16-mins in

'''