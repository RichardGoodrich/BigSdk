'''
colors.py  2021-05-05 Wed

refactored
'''

COLOR_TRANSPARENT = ''        # keep for info purposes
COLOR_BACKGROUND = 'white'

COLOR_NUMBER_ENTERED = 'blue'
COLOR_NUMBER_PUZZLE  = 'black'

MENU_BAR_NORMAL = 'cyan'
MENU_BAR_ACTIVE = 'green'
NEXT_BUTTON_INACTIVE = 'yellow'

# these are to be set ONLY by signals.is_load_set(bool_) or signals.is_grid_set(bool_)
remove_block_only = 'red'
remove_row_col = 'orange'
remove_rcn_block = 'cyan'

# color_clr loaded from one above
remove_small_square = 'red'
assert_small_square = 'green'
highlight = 'yellow'

grid_line_color = 'blue'

if __name__ == '__main__':
    file = __file__
    print(f'running {file} ')
else:
    file = __file__
    print(f'importing {file} ')
