import sys,os
import curses
import numpy as np
from jeuDeLaVie import World
from time import sleep

SHOWN_CHARACTER = 'o'
def draw_menu(stdscr):
    k = 0
    height, width = stdscr.getmaxyx()
    cursor_x = width//2 - 1
    cursor_y = height//2 - 1
    curses.start_color()

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    cases = np.zeros([height,width],dtype=bool)
    # Loop where k is the last character pressed
    while (k != ord('q')):

        if k == ord('\n'):
            curses.curs_set(0)
            for i in range(width):
                for j in range(height):
                    cases[j,i] = stdscr.inch(j,i) & 0xff == ord(SHOWN_CHARACTER)
            w=World.from_np_array(cases)
            it = iter(w)
            k2 = -1 
            stdscr.nodelay(True)
            delay = 0.1
            while k2 != ord(' '):
                stdscr.clear()
                next(it)
                for i in range(width):
                    for j in range(height):
                        if w.cases[j,i]:
                            stdscr.addstr(j,i,SHOWN_CHARACTER)
                options = [
                        'espace : stoper la simulation',
                        'flèche droite/gauche : accélerer/ralentir'
                        ]
                for i, desc in enumerate(options):
                    stdscr.addstr(height-i-1, 0, desc)

                k2 = stdscr.getch()
                if k2 == curses.KEY_RIGHT:
                    delay/=2
                elif k2 == curses.KEY_LEFT:
                    delay*=2
                stdscr.refresh()
                sleep(delay)
            stdscr.nodelay(False)

        curses.curs_set(2)

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
            if stdscr.inch(cursor_y, cursor_x) & 0xff == ord(SHOWN_CHARACTER):
                stdscr.addstr(cursor_y,cursor_x,' ')
            else:
                stdscr.addstr(cursor_y,cursor_x,SHOWN_CHARACTER)

        elif k == curses.KEY_BACKSPACE:
            stdscr.clear()


        # Refresh the screen
        stdscr.refresh()
        options = [
                'q : quitter', 
                'espace : ajouter/enlever une cellule', 
                'retour arrière : effacer l\'écran',
                'entrée : lancer la simulation',
                ]
        for i, desc in enumerate(options):
            stdscr.addstr(height-i-1, 0, desc)
        stdscr.move(cursor_y, cursor_x)

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
