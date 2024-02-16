# aoc_2016_18_A_1.py - Day 18: Like a Rogue - part 1
# In a total of 40 rows (including the starting row), how many safe tiles are there?
# https://adventofcode.com/2016/day/18


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2016_18'

TOTAL_ROWS = 40

TRAP_NEXT = ['^^.', '.^^', '^..', '..^', ]


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _validate_group(group: str) -> str:
    return '^' if group in TRAP_NEXT else '.'


def find_next_row(row: str) -> str:
    next_row = ''
    padded_row = '.' + row + '.'
    for group in zip(padded_row, padded_row[1:], padded_row[2:]):
        next_row += _validate_group(''.join(group))

    return next_row


test_data = '''
..^^.
.^^.^.^^^^
'''.strip().splitlines()


@time_it
def main(first_row: str, total_rows: int = TOTAL_ROWS) -> None:
    rows = [first_row]
    row = first_row

    for _ in range(total_rows-1):
        row = find_next_row(row)
        rows.append(row)
    pprint(rows)

    print(f'End result: {sum(row.count(".") for row in rows)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines[0])
    # main(data_lines[0], 3)
    # main(data_lines[1], 10)
    # using test_data '..^^.':
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using test_data '.^^.^.^^^^':
    #   End result: 38
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1926
    #   Finished 'main' in 1 millisecond
