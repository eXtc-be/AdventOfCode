# aoc_2023_10_A_1.py - Day 10: Pipe Maze - part 1
# follow pipes in a grid to find a loop
# https://adventofcode.com/2023/day/10


# imports


DATA_PATH = './input_2023_10'

START = 'S'

DIRECTIONS: dict[str, tuple[int, int]] = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

PIPES: dict[str, list[tuple[int, int]]] = {
    'S': [DIRECTIONS['U'], DIRECTIONS['D'], DIRECTIONS['L'], DIRECTIONS['R'], ],
    '|': [DIRECTIONS['U'], DIRECTIONS['D'], ],
    '-': [DIRECTIONS['L'], DIRECTIONS['R'], ],
    'L': [DIRECTIONS['U'], DIRECTIONS['R'], ],
    'J': [DIRECTIONS['U'], DIRECTIONS['L'], ],
    'F': [DIRECTIONS['D'], DIRECTIONS['R'], ],
    '7': [DIRECTIONS['D'], DIRECTIONS['L'], ],
    '.': [],
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def create_grid(data_lines: list[str]) -> list[list[str]]:
    return [[char for char in row] for row in data_lines]


def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == START:
                return r, c


def _find_neighbour(grid: list[list[str]],
                    pipe: str,
                    row: int,
                    col: int,
                    excluded_direction: tuple[int, ...] = (0, 0)
                    ) -> tuple[int, int]:
    for direction in PIPES[pipe]:
        if direction == excluded_direction:
            continue  # skip excluded direction to avoid going back to where we came from (incomplete loop)
        if 0 <= row + direction[0] < len(grid):  # check vertical bounds
            if 0 <= col + direction[1] < len(grid[row + direction[0]]):  # check horizontal bounds
                neighbour = grid[row + direction[0]][col + direction[1]]
                for i, axis in enumerate(direction):
                    if axis != 0:
                        for n_dir in PIPES[neighbour]:
                            if n_dir[i] == -axis:
                                return row + direction[0], col + direction[1]


def find_loop(
        grid: list[list[str]],
        start_row: int,
        start_col: int
) -> list[tuple[int, int]]:
    loop = [(start_row, start_col)]
    current_pipe = START
    current_row, current_col = start_row, start_col
    excluded_direction = (0, 0)

    while True:
        # print(current_pipe)
        next_pipe = _find_neighbour(grid, current_pipe, current_row, current_col, excluded_direction)
        loop.append(next_pipe)
        excluded_direction = current_row - next_pipe[0], current_col - next_pipe[1]
        current_row, current_col = next_pipe
        current_pipe = grid[current_row][current_col]
        if current_pipe == START:
            # print(current_pipe)
            return loop


test_data_1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF
""".splitlines()


test_data_2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""".splitlines()


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data_1
    # data_lines = test_data_2
    # print(data_lines)

    grid = create_grid(data_lines)
    # print(grid)

    start_row, start_col = find_start(grid)
    print(f'start character "{START}" was found on row {start_row}, column {start_col}')

    loop = find_loop(grid, start_row, start_col)
    print(loop)

    print(f'End result: {(len(loop) - 1) // 2}')
