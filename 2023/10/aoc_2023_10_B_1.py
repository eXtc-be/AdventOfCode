# aoc_2023_10_B_1.py - Day 10: Pipe Maze - part 2
# find the number of tiles that are enclosed by the loop
# hoping to solve this by scanning top to bottom, left to right
# remembering whether we're inside or out the loop, after much tweaking,
# I finally gave up on this strategy, because what worked for case A didn't for case B and vice versa
# https://adventofcode.com/2023/day/10


from aoc_2023_10_A_1 import (
    DATA_PATH,
    load_data,
    # test_data_1,
    # test_data_2,
    create_grid,
    find_start,
    find_loop,
    # START,
    PIPES,
)


INSIDE = '●'


def replace_start(grid: list[list[str]], loop: list[tuple[int, int]]) -> None:
    """replaces the start pipe with the correct symbol based on its neighbours' directions"""

    # calculate neighbours' directions
    new_dirs = sorted((
        (loop[1][0] - loop[0][0], loop[1][1] - loop[0][1]),
        (loop[-2][0] - loop[-1][0], loop[-2][1] - loop[-1][1])
    ))

    # find a pipe symbol that has the directions to connect its neighbours
    for pipe, dirs in PIPES.items():
        if sorted(dirs) == new_dirs:
            grid[loop[0][0]][loop[0][1]] = pipe


def find_enclosed(grid: list[list[str]], loop: list[tuple[int]]) -> list[str]:
    enclosed = []
    for r, row in enumerate(grid):  # loop through all rows in the grid top to bottom
        # inside serves 2 purposes:
        #   1. remember what character got us inside the loop, and
        #   2. indicate we're inside the loop if not empty
        inside = ''  # reset inside at the start of every row
        for c, char in enumerate(row):  # loop through all columns in the current row left to right
            if (r, c) in loop:
                if inside:
                    if inside == '|':  # enter
                        if char in '|LF':  # exit
                            inside = ''
                        else:  # '-J7'
                            enclosed.append(char)  # grab inside tube
                            grid[r][c] = INSIDE  # mark cell as inside
                    elif inside == 'L':  # enter
                        if char in 'J7':  # exit
                            inside = ''
                        elif char in '-':  # stay inside
                            continue
                        # elif char in '7':  # stay inside and change inside character
                        #     inside = char
                        else:  # '|LF'
                            continue  # never happens
                    elif inside == 'J':  # enter
                        if char in '|L':  # exit
                            inside = ''
                        elif char in 'F':  # stay inside and change inside character
                            inside = char
                        else:  # '-J7'
                            enclosed.append(char)  # grab inside tube
                            grid[r][c] = INSIDE  # mark cell as inside
                    elif inside == 'F':  # enter
                        if char in '7':  # exit
                            inside = ''
                        elif char in '-':  # stay inside
                            continue
                        elif char in 'J':  # stay inside and change inside character
                            inside = char
                        else:  # '|LF'
                            continue  # never happens
                    elif inside == '7':  # enter
                        if char in '|F':  # exit
                            inside = ''
                        elif char in 'L':  # stay inside and change inside character
                            inside = char
                        else:  # '-J7'
                            enclosed.append(char)  # grab inside tube
                            grid[r][c] = INSIDE  # mark cell as inside
                else:
                    inside = char
            else:
                if inside:
                    enclosed.append(char)  # grab inside tube
                    grid[r][c] = INSIDE  # mark cell as inside
    return enclosed


test_data_1 = """.....
.S-7.
.|.|.
.L-J.
.....
""".splitlines()


test_data_1a = """......
.S--7.
.|..|.
.L--J.
......
""".splitlines()


test_data_1b = """......
.S--7.
.|..|.
.|..|.
.L--J.
......
""".splitlines()


test_data_1c = """........
.S----7.
.|....|.
.|....|.
.|....|.
.|....|.
.L----J.
........
""".splitlines()


test_data_1d = """.S----7.
.|....|.
.|....|.
.|....|.
.|....|.
.L----J.
........
""".splitlines()


test_data_1e = """........
.S----7.
.|....|.
.|....|.
.|....|.
.|....|.
.L----J.
""".splitlines()


test_data_1f = """.......
S----7.
|....|.
|....|.
|....|.
|....|.
L----J.
.......
""".splitlines()


test_data_1g = """.......
.S----7
.|....|
.|....|
.|....|
.|....|
.L----J
.......
""".splitlines()


test_data_1h = """S----7
|....|
|....|
|....|
|....|
L----J
""".splitlines()


test_data_2a = """S--7
|.FJ
L-J.
""".splitlines()


test_data_2b = """S----7
|....|
|.F--J
|.|...
|.|...
L-J...
""".splitlines()


test_data_3 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""".splitlines()


test_data_4 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".splitlines()


test_data_4b = """.........
.F-----7.
.|F--7.|.
.||..|.|.
.||..L-J.
.||......
.||..F-7.
.||..|.|.
.|L--J.|.
.S-----J.
.........
""".splitlines()


test_data_5 = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
""".splitlines()


test_data_5a = """......
.S--7.
.|..|.
.L7FJ.
..LJ..
""".splitlines()


test_data_5b = """......
.S--7.
.|..|.
.L7FJ.
..||..
..LJ..
""".splitlines()


test_data_5c = """.........
.F-----7.
.|F--7.|.
.||..|.|.
.||..L-J.
.||..F-7.
.||..|.|.
.|L--J.|.
.S-----J.
.........
""".splitlines()


test_data_6 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".splitlines()


test_data_7 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".splitlines()


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    # data_lines = test_data_1
    # data_lines = test_data_2
    data_lines = test_data_3
    # data_lines = test_data_4
    # data_lines = test_data_5
    # data_lines = test_data_6
    # print(data_lines)

    grid = create_grid(data_lines)
    for r in grid:
        print(r)
    print()

    start_row, start_col = find_start(grid)
    # print(f'start character "{START}" was found on row {start_row}, column {start_col}')

    # for row, col in (
    #         (3, 0),  # |
    #         (4, 0),  # L
    #         (4, 1),  # J
    #         (3, 1),  # F
    #         (3, 2),  # -
    #         (2, 3),  # L
    # ):
    #     grid = create_grid(test_data_2)
    #
    #     grid[2][0] = 'F'
    #     grid[row][col] = 'S'
    #     start_row, start_col = row, col
    #
    #     for r in grid:
    #         print(r)
    #     print()
    #
    #     loop = find_loop(grid, start_row, start_col)
    #     # print(loop)
    #
    #     replace_start(grid, loop)
    #     for r in grid:
    #         print(r)
    #     print('-' * 100)

    loop = find_loop(grid, start_row, start_col)
    # print(loop)

    replace_start(grid, loop)
    for r in grid:
        print(r)
    print()

    enclosed = find_enclosed(grid, loop)
    print(enclosed)
    print()

    replace_start(grid, loop)
    for r in grid:
        print(r)
    print()

    print(f'End result: {len(enclosed)}')
