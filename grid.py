'''
grids.py  2021-04-17-1830 Sat

Learning to build Sudoku Grids again!

'''


# <editor-fold desc="python imports"
import logging as log
import pprint
import sys
import tkinter as tk
# </editor-fold>

# <editor-fold desc="local imports"
import colors
import draw
import signals as sigs
import settings as g
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
COLOR_BACKGROUND = colors.COLOR_BACKGROUND
COLOR_NUMBER_ENTERED = colors.COLOR_NUMBER_ENTERED
COLOR_NUMBER_PUZZLE = colors.COLOR_NUMBER_PUZZLE

GRID_NAMES = g.GRID_NAMES_1
GRID_NAMES_1 = g.GRID_NAMES_1
CELL_GIVEN_MARK = g.CELL_GIVEN_MARK

BP = g.BREAK_POINT
NL = g.NEW_LINE
DIGITS = g.DIGITS
MAX_CELLS = g.MAX_CELLS
SQUARES = g.SQUARES


MAX_DIGITS = len(DIGITS)

GRID_LINE_NARROW = 1
GRID_LINE_WIDE = 4

NUMBER_OF_GRID_LINES = 20
NUMBER_OF_BIG_SQUARES = 81
NUMBER_OF_LITTLE_SQUARES = 9 * 81

BIG_SQUARE_DATA = {
    'fill': 'white',
    'outline': 'white',
    'state': 'normal',
    'tags': ('BS', 'BS_xy'),
    'width': 4
}
# </editor-fold>


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)


class Grid(tk.Frame):
    grid_offset = 40
    grid_pad = 20
    size_of_little_squares = 15
    size_of_big_squares = 3 * size_of_little_squares

    grid_locations = []
    label_coordinates = []
    line_coordinates = []

    big_number_coordinates = []
    big_number_tags = [''] * NUMBER_OF_BIG_SQUARES
    big_square_coordinates = []
    big_square_tags = [''] * NUMBER_OF_BIG_SQUARES

    line_grid_width = {
        0: [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        1: [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        2: [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        3: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    }
    little_square_coordinates = []
    little_numbers = []
    little_number_coordinates = []

    little_number_tags = []
    little_square_tags = []

    def __init__(self, master, name):
        # <editor-fold desc="Basics"
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.protocol('WM_DELETE_WINDOW', self.disable_close)
        self.name = name
        self.grid_index = GRID_NAMES.index(self.name)

        self.master.title(name)
        self.master.geometry(Grid.grid_locations[self.grid_index])

        if sigs.is_resizeable:
            self.master.resizable(True, True)
            self.canvas = ResizingCanvas(self.master, width=500, height=500,
                                         bg=COLOR_BACKGROUND, highlightthickness=0)
        else:
            self.master.resizable(False, False)
            self.canvas = tk.Canvas(self.master, width=500, height=500, bg=COLOR_BACKGROUND)

        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.create_text(20, 20, text=self.name, fill='gray', state='normal', font=("arial", 16))
        # </editor-fold>

        self.color_tag_list = []
        self.puzzle_dict = dict(zip(SQUARES, [DIGITS] * 81))

        self.draw_big_squares()
        self.draw_big_numbers()
        self.draw_little_squares()
        self.draw_little_numbers()

        self.draw_lines(self.grid_index)
        self.draw_grid_labels(self.grid_index)

        self.master.update_idletasks()  # necessary to get valid location below
        # location = self.master.winfo_geometry()
        self.canvas.update()

    @classmethod
    def create_grid_stuff(cls):
        try:
            def print_creations():
                def print_grid_locations():
                    print('Grid.grid_locations = [')
                    pp = pprint.PrettyPrinter(indent=1, width=90, compact=True)
                    pp.pprint(Grid.grid_locations)

                def print_line_locations():
                    print('Grid.line.coordinates')
                    pp = pprint.PrettyPrinter(indent=1, width=120, compact=True)
                    pp.pprint(Grid.line_coordinates)

                def print_big_number_coordinates():
                    print('Grid.big_number_coordinates = ')
                    pp = pprint.PrettyPrinter(indent=1, width=120, compact=True)
                    pp.pprint(Grid.big_number_coordinates)

                def print_big_square_coordinates():
                    print('Grid.big_square_coordinates = ')
                    pp = pprint.PrettyPrinter(indent=1, width=120, compact=True)
                    pp.pprint(Grid.big_square_coordinates)

                def print_little_square_coordinates():
                    print('Grid.little_square_coordinates = ')
                    pp = pprint.PrettyPrinter(indent=1, width=120, compact=True)
                    pp.pprint(Grid.little_square_coordinates)

                # print_grid_locations()
                # print_line_locations()
                # print_little_square_coordinates()
                print_big_square_coordinates()
                print_big_number_coordinates()
                print()

            def create_grid_locations():
                if sigs.screen_height > 1000:
                    Grid.size_of_little_squares = 15  # normally 15
                    Grid.size_of_big_squares = 3 * Grid.size_of_little_squares
                    grid_size = 9 * Grid.size_of_big_squares + Grid.grid_offset + Grid.grid_pad
                    rcn_location = f'{grid_size}x{grid_size}+500+20'
                    rnc_location = f'{grid_size}x{grid_size}+1000+20'
                    ncr_location = f'{grid_size}x{grid_size}+500+550'
                    bns_location = f'{grid_size}x{grid_size}+1000+550'
                    Grid.grid_locations = [rcn_location, rnc_location, ncr_location, bns_location]
                else:
                    Grid.size_of_little_squares = 25
                    Grid.size_of_big_squares = 3 * Grid.size_of_little_squares
                    grid_size = 9 * Grid.size_of_big_squares + Grid.grid_offset + Grid.grid_pad
                    location = f'{grid_size}x{grid_size}+500+20'
                    Grid.grid_locations = [location, location, location, location]

            def create_label_coordinates():
                off = Grid.grid_offset
                size = Grid.size_of_big_squares

                base = off - 20
                inc = off + size / 2

                Grid.label_coordinates = [(base, inc + size * i) for i in range(9)]

            def create_line_coords():
                off = Grid.grid_offset
                size = Grid.size_of_big_squares
                length = 9 * size
                nog = len(GRID_NAMES_1)
                nol = NUMBER_OF_GRID_LINES // 2

                col_coords = [(x * size + off, off, x * size + off, off + length) for x in range(nol)]
                row_coords = [(off, x * size + off, off + length, x * size + off) for x in range(nol)]
                Grid.line_coordinates = row_coords + col_coords

                for i in range(nog):
                    widths = Grid.line_grid_width[i]
                    widths = [1 if x == 0 else 4 for x in widths]
                    Grid.line_grid_width[i] = widths

            def create_big_square_coordinates():
                off = Grid.grid_offset
                ns = NUMBER_OF_BIG_SQUARES
                size = Grid.size_of_big_squares

                x1 = [(lambda x: (size * (x % 9)) + off)(x) for x in range(ns)]
                y1 = [(lambda x: (size * (x // 9)) + off)(x) for x in range(ns)]
                x2 = [(lambda x: (size * (x % 9)) + off + size)(x) for x in range(ns)]
                y2 = [(lambda x: (size * (x // 9)) + off + size)(x) for x in range(ns)]

                Grid.big_square_coordinates = [(x1[i], y1[i], x2[i], y2[i]) for i in range(ns)]

            def create_big_number_coordinates():
                off = Grid.grid_offset
                ns = NUMBER_OF_BIG_SQUARES
                size = Grid.size_of_big_squares
                t_off = off + size / 2

                x1 = [(lambda x: (size * (x % 9)) + t_off)(x) for x in range(ns)]
                y1 = [(lambda x: (size * (x // 9)) + t_off)(x) for x in range(ns)]

                Grid.big_number_coordinates = [(x1[i], y1[i]) for i in range(ns)]

            def create_little_square_coordinates():
                off = Grid.grid_offset
                size = Grid.size_of_little_squares
                ns = NUMBER_OF_LITTLE_SQUARES

                x1 = [(lambda x: (size * (x % 27)) + off)(x) for x in range(ns)]
                y1 = [(lambda x: (size * (x // 27)) + off)(x) for x in range(ns)]
                x2 = [(lambda x: (size * (x % 27)) + off + size)(x) for x in range(ns)]
                y2 = [(lambda x: (size * (x // 27)) + off + size)(x) for x in range(ns)]

                Grid.little_square_coordinates = [(x1[i], y1[i], x2[i], y2[i]) for i in range(ns)]

            def create_little_number_coordinates():
                off = Grid.grid_offset
                size = Grid.size_of_little_squares
                ns = NUMBER_OF_LITTLE_SQUARES
                t_off = off + size / 2

                x1 = [(lambda x: (size * (x % 27)) + t_off)(x) for x in range(ns)]
                y1 = [(lambda x: (size * (x // 27)) + t_off)(x) for x in range(ns)]

                Grid.little_number_coordinates = [(x1[i], y1[i]) for i in range(ns)]

            def create_little_numbers():
                num = lambda x: ((x // 27) % 3) * 3 + (x % 3) + 1
                Grid.little_numbers = [num(x) for x in range(9 * 81)]

            def create_tags():
                nun_tags = [''] * NUMBER_OF_LITTLE_SQUARES
                sqr_tags = [''] * NUMBER_OF_LITTLE_SQUARES

                for i in range(9 * 81):
                    row = i // 81 + 1
                    j = i - (i // 81) * 81

                    j_adjust = 27 * (j // 27)
                    col = (j - j_adjust) // 3 + 1

                    digit = j % 3 + (j // 27) * 3 + 1

                    tag_num = ('SN', f'SN_{row}{col}', f'SN_{row}{col}-{digit}')
                    tag_sqr = ('SS', f'SS_{row}{col}', f'SS_{row}{col}-{digit}')
                    nun_tags[i] = tag_num
                    sqr_tags[i] = tag_sqr

                    Grid.little_number_tags = nun_tags
                    Grid.little_square_tags = sqr_tags

                for i in range(81):
                    row = i // 9 + 1
                    col = i % 9 + 1

                    tag_num = ('BN', f'BN_{row}{col}')
                    tag_sqr = ('BS', f'BS_{row}{col}')
                    Grid.big_number_tags[i] = tag_num
                    Grid.big_square_tags[i] = tag_sqr

            create_grid_locations()
            create_label_coordinates()
            create_line_coords()
            create_little_square_coordinates()
            create_little_number_coordinates()
            create_little_numbers()
            create_tags()
            create_big_square_coordinates()
            create_big_number_coordinates()

            if sigs.is_pretty_print:
                print_creations()

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    # <editor-fold desc="Drawing Widgets"
    def draw_big_numbers(self):
        ns = NUMBER_OF_BIG_SQUARES
        coords = Grid.big_number_coordinates
        data = {'fill': 'black', 'state': 'hidden', 'font': ('arial', 24), 'text': 0}
        tags = Grid.big_number_tags

        [self.canvas.create_text(coords[i], data, tags=tags[i]) for i in range(ns)]

    def draw_big_squares(self):
        try:
            ns = NUMBER_OF_BIG_SQUARES
            coords = Grid.big_square_coordinates
            data = {'activefill': 'cyan', 'fill': 'white', 'state': 'hidden', 'width': 0}
            tags = Grid.big_square_tags

            for i in range(ns):
                self.canvas.create_rectangle(coords[i], data, tags=tags[i])

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def draw_grid_labels(self, grid_index):
        try:
            grid_name = GRID_NAMES[grid_index]
            x = grid_name[0]
            y =grid_name[1]

            coords = Grid.label_coordinates
            for i, digit in enumerate(DIGITS):
                self.canvas.create_text(coords[i], text=x + digit, font=('arial', 16))
                self.canvas.create_text(coords[i][1], coords[i][0], text=y + digit, font=('arial', 16))

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def draw_little_squares(self):
        ns = NUMBER_OF_LITTLE_SQUARES
        coords = Grid.little_square_coordinates

        tags = tags = Grid.little_square_tags
        data = {'activefill': 'cyan', 'fill': 'white', 'state': 'normal', 'width': 0}
        [self.canvas.create_rectangle(coords[i], data, tags=tags[i]) for i in range(ns)]

    def draw_little_numbers(self):
        ns = NUMBER_OF_LITTLE_SQUARES

        coords = Grid.little_number_coordinates
        nums = Grid.little_numbers
        tags = tags = Grid.little_number_tags

        data = {'fill': 'black', 'state': 'normal'}

        [self.canvas.create_text(coords[i], data, text=nums[i], tags=tags[i]) for i in range(ns)]

    def draw_lines(self, grid_index):
        coords = Grid.line_coordinates
        widths = Grid.line_grid_width[grid_index]
        color = colors.grid_line_color

        nols = NUMBER_OF_GRID_LINES
        [self.canvas.create_line(coords[i], width=widths[i], fill=color, tags='LINES') for i in range(nols)]
    # </editor-fold>

    # <editor-fold desc="various commands"
    def color_square(self, tag, color):
        try:
            self.canvas.itemconfig(tag, state='normal')
            state = self.canvas.itemcget(tag, 'state')
            fill = self.canvas.itemcget(tag, 'fill')
            self.color_tag_list.append((tag, fill))
            self.canvas.itemconfig(tag, fill=color)
            self.canvas.update()
        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def color_restore(self):
        try:
            for item in self.color_tag_list:
                self.canvas.itemconfig(item[0], fill='white')
            self.canvas.update()
            self.color_tag_list = []
        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def cmd(self, sqr, cell):
        try:
            self.puzzle_dict[sqr] = cell
        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def display_numbers(self):
        try:
            for s in SQUARES:
                digits = self.puzzle_dict[s]
                if digits[0] in DIGITS:
                    for d in DIGITS:
                        small_square = 'SS_' + s + '-' + d
                        small_number = 'SN_' + s + '-' + d
                        if (d in digits):
                            self.canvas.itemconfig(small_square, state='normal')
                            self.canvas.itemconfig(small_number, state='normal')
                        else:
                            self.canvas.itemconfig(small_square, state='hidden')
                            self.canvas.itemconfig(small_number, state='hidden')
                    self.canvas.tag_raise('SS_' + s)
                    self.canvas.tag_raise('SN_' + s)
                else:
                    if digits[0] == CELL_GIVEN_MARK:
                        color_big_number = COLOR_NUMBER_PUZZLE
                    else:
                        color_big_number = COLOR_NUMBER_ENTERED
                    digit = digits[1]
                    self.canvas.itemconfig('BN_' + s,
                                           state='normal',
                                           text=digit,
                                           fill=color_big_number)      # add d to Big Numnber at s
                    self.canvas.itemconfig('SS_' + s, state='hidden')  # hide Small Square at s
                    self.canvas.itemconfig('SN_' + s, state='hidden')  # hide Small Number at s
                    self.canvas.tag_raise('BN_' + s)                   # Big Number at s to the top
            self.canvas.tag_raise('LINES')
            self.canvas.update()

        except Exception as e:
            logger_except.exception(e)
            sys.exit()

    def erase_puzzle(self):
        try:
            self.puzzle_dict = dict(zip(SQUARES, [DIGITS] * 81))
            self.canvas.itemconfig('SS', state='normal')
            self.canvas.itemconfig('BS', state='hidden')
            self.canvas.itemconfig('BN', state='hidden')
            # self.draw_grid(self.name)
            self.display_numbers()
            self.canvas.update()
            return
        except Exception as e:
            logger_except.exception(e)
            sys.exit()


    # </editor-fold>

    def disable_close(self):
        pass


def gui(root):
    root.geometry('200x200+300+10')

    Grid.create_grid_stuff()

    rcn = Grid(tk.Toplevel(), 'rcn')
    rnc = Grid(tk.Toplevel(), 'rnc')
    ncr = Grid(tk.Toplevel(), 'ncr')
    bns = Grid(tk.Toplevel(), 'bns')

    root.resizable(1, 1)

def main():
    sigs.is_pretty_print = True

    root = tk.Tk()

    sigs.screen_width = root.winfo_screenwidth()
    sigs.screen_height = root.winfo_screenheight()
    sigs.screen_depth = root.winfo_screendepth()

    gui(root)
    root.mainloop()

if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
    main()
else:
    file = __file__
    print(f'importing {file} ')



'''
rectangle

https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html

id = C.create_rectangle(x0, y0, x1, y1, option, ...)

x0,y0 is top left corner and start right on that pixedl
x1,y1 is bottom right corner and one pixel outside


active*  when mouse over activefill=
fill = color  default = ''  no color
outline = color  default is black
state = NORMAL | DISABLED | ACTIVE (when mouse over it)
tags = 
width = width of border

https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/canvas-methods.html

canvas.itemconfigure
canvas.itemcget

https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/universal.html

w.winfo_geometry  Warning  see  .update_idletasks()  returns by default '1x1+0+0'

common screen resolutions

                1920 x 1080
                1366 x 768
                1440 x 900
                1536 x



'''