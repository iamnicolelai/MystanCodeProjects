"""
File: babygraphics.py
Name: Nicole Lai
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    num_years = len(YEARS)
    spacing = (width - 2*GRAPH_MARGIN_SIZE) / num_years
    x_coordinate = GRAPH_MARGIN_SIZE + year_index * spacing
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    # create vertical lines according to the years (x-coordinate)
    for i in range(len(YEARS)):
        new_x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(new_x, 0, new_x, CANVAS_HEIGHT)
        canvas.create_text(new_x+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=YEARS[i], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #
    color_index = 0
    for name in lookup_names:
        if name in name_data:
            data = name_data[name]
            prev_x = None
            prev_y = None
            # line_color to ensure the color will loop within the lists
            line_color = COLORS[color_index % len(COLORS)]
            for year in YEARS:
                rank = data[str(year)] if str(year) in data else "*"
                x_coord = get_x_coordinate(CANVAS_WIDTH, YEARS.index(year))
                if rank != "*":
                    y_coord = GRAPH_MARGIN_SIZE + (int(rank) * (CANVAS_HEIGHT - 2*GRAPH_MARGIN_SIZE)/MAX_RANK)
                    canvas.create_text(x_coord + TEXT_DX, y_coord, text=name+' '+rank, anchor=tkinter.SW,
                                       fill=line_color)
                    if prev_x is None and prev_y is None:
                        prev_x = x_coord
                        prev_y = y_coord
                    else:
                        canvas.create_line(prev_x, prev_y, x_coord, y_coord, width=LINE_WIDTH, fill=line_color)
                        prev_x = x_coord
                        prev_y = y_coord
                else:
                    y_coord = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                    canvas.create_text(x_coord + TEXT_DX, y_coord, text=name+' *', anchor=tkinter.SW, fill=line_color)
                    if prev_x is None and prev_y is None:
                        prev_x = x_coord
                        prev_y = y_coord
                    else:
                        canvas.create_line(prev_x, prev_y, x_coord, y_coord, width=LINE_WIDTH, fill=line_color)
                        prev_x = x_coord
                        prev_y = y_coord
        color_index += 1


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
