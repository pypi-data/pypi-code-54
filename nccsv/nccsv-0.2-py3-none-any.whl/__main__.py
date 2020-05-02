# __main__.py - run the nccsv package

from nccsv import main
from curses import wrapper

if __name__ == "__main__":
    wrapper(main)
