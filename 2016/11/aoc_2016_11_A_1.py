# aoc_2016_11_A_1.py - Day 11: Radioisotope Thermoelectric Generators - part 1
# In your situation, what is the minimum number of steps required to bring all the objects to the fourth floor?
# https://adventofcode.com/2016/day/11


import curses
from curses import wrapper

from pprint import pprint

FLOORS = 4

REAL_LAYOUT = {
    'PoG': 1,
    'PoM': 2,
    'TmG': 1,
    'TmM': 1,
    'PmG': 1,
    'PmM': 2,
    'RuG': 1,
    'RuM': 1,
    'CoG': 1,
    'CoM': 1,
}

TEST_LAYOUT = {
    'HG': 2,
    'HM': 1,
    'LG': 3,
    'LM': 1,
}


def main(stdscr, layout: dict[str, int]) -> None:
    # Turn off blinking cursor
    curses.curs_set(False)

    # Clear screen
    stdscr.clear()

    # Set color pairs
    # color pair 0 is used for normal status and cannot be altered
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # microchip's EM shield activated
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # fried

    elevator = 1
    pos = 0
    steps = []

    objects = {elem: layout[elem] for elem in layout}
    object_list = list(objects.keys())

    elem_width = len(object_list[0])
    field_width = 4 + elem_width * len(object_list) + 1

    selected = []

    while True:
        # draw the screen
        stdscr.addstr(0, 0, f'Step: {len(steps):03}')  # status

        # draw all floors
        for floor in range(1, FLOORS+1):
            stdscr.addstr(FLOORS-floor+1, 0, f'{floor} {"E" if elevator == floor else "."} ')  # floor number, elevator position
            for i, elem in enumerate(objects):
                # determine the element's attributes
                attr = curses.A_NORMAL
                if elevator == floor:
                    if i == pos:  # cursor
                        attr |= curses.A_UNDERLINE
                    if i in selected:
                        attr |= curses.A_REVERSE  # selected
                if objects[elem] == floor:
                    if elem[-1] == 'M':  # microchip
                        if objects[elem[:-1]+'G'] == objects[elem]:  # compatible generator on same floor
                            attr |= curses.color_pair(1)  # shielded
                        elif any(objects[e] == floor for e in objects if e[-1] == 'G'):  # check if other generators on same floor
                            attr |= curses.color_pair(2)  # fried
                    elif elem[-1] == 'G':  # generator
                        if objects[elem[:-1] + 'M'] == objects[elem]:  # compatible generator on same floor
                            attr |= curses.color_pair(1)  # shielded
                # draw the object with its attributes
                stdscr.addstr(f'{elem if objects[elem] == floor else "." * elem_width}', attr)

        # footer
        stdscr.addstr(0, field_width, '| < > to move cursor left or right')
        stdscr.addstr(1, field_width, '| Enter to select/deselect objects')
        stdscr.addstr(2, field_width, '| ^ v to move selected objects up or down')
        stdscr.addstr(3, field_width, '| u to undo a step')
        stdscr.addstr(4, field_width, '| q to quit')

        stdscr.refresh()
        key_pressed = stdscr.getch()

        # stdscr.addstr(0, 20, f'{key_pressed=}  ')
        # stdscr.refresh()

        match key_pressed:
            case curses.KEY_LEFT:
                pos = (pos - 1) % len(objects)
            case curses.KEY_RIGHT:
                pos = (pos + 1) % len(objects)
            case curses.KEY_UP:
                if selected:  # at least 1 object needs to be selected to activate the elevator
                    if elevator < FLOORS:
                        # add previous state to undo buffer
                        steps.append(({elem: objects[elem] for elem in objects}, elevator, pos))
                        elevator += 1  # move the elevator
                        while selected:  # move all selected objects to the new floor
                            objects[object_list[selected.pop()]] = elevator
            case curses.KEY_DOWN:
                if selected:  # at least 1 object needs to be selected to activate the elevator
                    if elevator > 1:
                        # add previous state to undo buffer
                        steps.append(({elem: objects[elem] for elem in objects}, elevator, pos))
                        elevator -= 1  # move the elevator
                        while selected:  # move all selected objects to the new floor
                            objects[object_list[selected.pop()]] = elevator
            case curses.KEY_ENTER | 10 | 459:  # select/deselect object under cursor
                if objects[object_list[pos]] == elevator:  # check whether the object under the cursor is on this floor
                    if pos in selected:  # object was already selected
                        selected.remove(pos)
                    elif len(selected) < 2:  # can move 2 objects max
                        selected.append(pos)
            case u if u == ord('u'):
                if steps:
                    objects, elevator, pos = steps.pop()
            case q if q == ord('q'):
                break

        # stdscr.addstr(1, 20, f'{selected=}   ')
        # stdscr.refresh()


if __name__ == "__main__":
    layout = REAL_LAYOUT
    # layout = TEST_LAYOUT
    # print(layout)

    wrapper(main, layout)
    # using input data:
    #   End result: 47
