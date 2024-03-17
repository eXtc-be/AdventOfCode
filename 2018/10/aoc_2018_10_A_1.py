# aoc_2018_10_A_1.py - Day 10: The Stars Align - parts 1 & 2
# Part 1: What message will eventually appear in the sky?
# Part 2: Exactly how many seconds would they have needed to wait for that message to appear?
# https://adventofcode.com/2018/day/10


import sys
sys.path.insert(0, '../..')

from tools import time_it

from dataclasses import dataclass
import re
import curses
from curses import wrapper
import os

from pprint import pprint

DATA_PATH = './input_2018_10'

POINT = re.compile(r'position=<\s*(?P<px>[\d-]+),\s*(?P<py>[\d-]+)>\s*velocity=<\s*(?P<vx>[\d-]+),\s*(?P<vy>[\d-]+)>')

MAX_SIZE = 50


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class Point:
    position: Coord
    velocity: Coord


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_points(data_lines: list[str], factor: int = 1) -> list[Point]:
    points = []
    for line in data_lines:
        match = POINT.match(line)
        if match:
            points.append(
                Point(
                    Coord(
                        int(match.group('px')) * factor,
                        int(match.group('py')) * factor
                    ),
                    Coord(
                        int(match.group('vx')) * factor,
                        int(match.group('vy')) * factor
                    )
                )
            )

    return points


def move_points(points: list[Point], t: int) -> list[Coord]:
    return [
        Coord(
            point.position.x+point.velocity.x*t,
            point.position.y+point.velocity.y*t
        )
        for point in points
    ]


def draw_grid(stdscr, points: list[Point], t: int = 0) -> None:
    coords = move_points(points, t)

    x_min = min(coord.x for coord in coords)
    x_max = max(coord.x for coord in coords)
    y_min = min(coord.y for coord in coords)
    y_max = max(coord.y for coord in coords)

    zoom = max(1, (x_max - x_min) // MAX_SIZE + 1, (y_max - y_min) // MAX_SIZE + 1)

    # Clear screen
    stdscr.clear()

    stdscr.addstr(0, 0, f't=[{t:10,}] x=[{x_min:10,}]-[{x_max:10,}] y=[{y_min:10,}]-[{y_max:10,}] z=[{zoom:5,}]\n')

    for y in range(y_min // zoom, y_max // zoom + 1):
        line = ['.'] * ((x_max - x_min + 1) // zoom + 1)
        for coord in [c for c in coords if c.y in range(y * zoom, (y + 1) * zoom)]:
            line[(coord.x - x_min) // zoom] = '#'
        stdscr.addstr(''.join(line) + '\n')
        # stdscr.addstr(y - y_min, 0, ''.join(line))


test_data = '''
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
'''.strip().splitlines()


# @time_it
def main(stdscr, data_lines: list[str]) -> None:
    # Turn off blinking cursor
    curses.curs_set(False)

    points = get_points(data_lines, 10)
    # pprint(points)

    t = 0

    while True:
        # draw the screen
        draw_grid(stdscr, points, t)
        stdscr.refresh()
        key_pressed = stdscr.getch()
        # print(key_pressed)
        match key_pressed:
            case q if q == ord('q'):
                break
            case curses.KEY_UP:
                t += 1
            case curses.KEY_DOWN:
                t -= 1
            case curses.KEY_PPAGE:
                t += 10
            case curses.KEY_NPAGE:
                t -= 10
            case curses.KEY_HOME:
                t += 100
            case curses.KEY_END:
                t -= 100
            case curses.KEY_IC:
                t += 1000
            case curses.KEY_DC:
                t -= 1000
            case _:
                pass

    # print(f'End result: {0}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    wrapper(main, data_lines)

    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: NBHEZHCJ
    #   Finished 'main' in 10558 'seconds'
