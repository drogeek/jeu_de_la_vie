import sys,os
import curses
import numpy as np
from jeuDeLaVie import World
from time import sleep

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    curses.start_color()

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    height, width = stdscr.getmaxyx()
    cases = np.zeros([height,width],dtype=bool)
    # Loop where k is the last character pressed
    while (k != ord('q')):

        if k == ord('\n'):
            for i in range(width):
                for j in range(height):
                    cases[j,i] = stdscr.inch(j,i) & 0xff == ord('0')
            w=World.from_np_array(cases)
            it = iter(w)
            while True:
                stdscr.clear()
                next(it)
                for i in range(width):
                    for j in range(height):
                        if w.cases[j,i]:
                            stdscr.addstr(j,i,'0')
                stdscr.refresh()
                sleep(0.1)

        # Initialization
        # stdscr.clear()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        if k == ord(' '):
            stdscr.addstr(cursor_y,cursor_x,'0')
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
