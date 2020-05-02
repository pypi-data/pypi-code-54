# grid.py - render multiple entries in a pad
import curses
# from entry import Entry
# from csvutil import CSVData
from nccsv.entry import Entry
from nccsv.csvutil import CSVData


class Grid():
    def __init__(self, stdscr, size_y, size_x, h, w, win_pos_y, win_pos_x,
                 y_offset, x_offset, e_size_y, e_size_x, csv_data):
        self.stdscr = stdscr
        self.size_y = size_y
        self.size_x = size_x
        self.w = w
        self.h = h
        self.win_pos_y = win_pos_y
        self.win_pos_x = win_pos_x
        self.y_offset = y_offset
        self.x_offset = x_offset
        self.e_size_y = e_size_y
        self.e_size_x = e_size_x
        self.csv_data = csv_data

        # Create 2D array for grid
        self.contents = []
        for i in range(self.size_x):
            self.contents.append([])
            for j in range(self.size_y):
                self.contents[i].append([])

        self.pos_y = 0
        self.pos_x = 0

        self.pad = curses.newpad(self.size_y*(self.e_size_y+5),
                                 self.size_x*(self.e_size_x+5))
        self.fill_grid()
    # init

    def fill_grid(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                self.contents[x][y] = Entry(self.pad,
                                            1 + (y*(self.e_size_y+2)),
                                            1 + (x*(self.e_size_x+2)),
                                            1, 10)
    # fill_grid

    def render(self):
        self.pad.clear()
        # self.pad.addstr(2, 0, f"{self.pos_x}{self.pos_y}")
        # self.pad.refresh()

        self.contents[self.pos_x][self.pos_y].highlight()
        self.pad.refresh(self.pos_y, self.pos_x,
                         self.win_pos_y, self.win_pos_x,
                         self.h - self.y_offset-1, self.w - self.x_offset-1)
        for y in range(self.size_y):
            for x in range(self.size_x):
                self.contents[x][y].render2()
    # render

    def add_row(self):
        pass
    # add_row

    def add_col(self):
        pass
    # add_col

    def handle_input(self, key=None):
        if not key:
            self.pad.keypad(True)
            curses.raw(True)
            key = self.pad.getch()
        # TODO: check for min/max
        if key == ord('s') or key == curses.KEY_DOWN:
            self.contents[self.pos_x][self.pos_y].highlight()
            self.pos_y += 1
        elif key == ord('w') or key == curses.KEY_UP:
            self.contents[self.pos_x][self.pos_y].highlight()
            self.pos_y -= 1
        elif key == ord('d') or key == curses.KEY_RIGHT:
            self.contents[self.pos_x][self.pos_y].highlight()
            self.pos_x += 1
        elif key == ord('a') or key == curses.KEY_LEFT:
            self.contents[self.pos_x][self.pos_y].highlight()
            self.pos_x -= 1
        elif key == curses.KEY_PPAGE or key == ord('k'):  # page up
            self.win_pos_y += 1
        elif key == curses.KEY_NPAGE or key == ord('j'):  # page down
            self.win_pos_y -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            self.contents[self.pos_x][self.pos_y].edit_entry()
            txt = self.contents[self.pos_x][self.pos_y].get_text()
            self.csv_data.update_data(self.contents)
        elif key == curses.KEY_DC or key == curses.KEY_DL:
            self.contents[self.pos_x][self.pos_y].clear_text()
        elif key == 19:  # CTRL + S
            self.csv_data.update_data(self.contents)
            self.csv_data.save()
        elif key == ord('q'):
            raise Exception("App closed")

    # handle_input

# Grid


if __name__ == "__main__":
    def main(stdscr):
        h, w = stdscr.getmaxyx()
        # stdscr.addstr(0, 0, "Grid test")
        # stdscr.refresh()

        csv = CSVData("gridtest.csv")

        g = Grid(stdscr, 20, 6, h, w, 1, 0, 0, 0, 1, 10, csv)
        g.render()
        while True:
            # ch = stdscr.getch()
            # if ch == ord('q'):
            #     break
            g.render()
            g.handle_input()

    # main
    curses.wrapper(main)
